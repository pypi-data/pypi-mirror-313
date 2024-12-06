import time
import traceback
from collections import defaultdict
from datetime import datetime
from http import HTTPStatus
from json import dumps, loads
from typing import Any, DefaultDict, Dict, List, Optional, Sequence, Union
from uuid import UUID

import pytz
import tiktoken
from galileo_core.helpers.execution import async_run
from galileo_core.schemas.shared.workflows.node_type import NodeType
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.documents import Document
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    message_to_dict,
)
from langchain_core.outputs import (
    ChatGeneration,
    ChatGenerationChunk,
    GenerationChunk,
    LLMResult,
)
from langchain_core.prompt_values import ChatPromptValue
from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1

from galileo_observe.schema.transaction import (
    TransactionLoggingMethod,
    TransactionRecord,
    TransactionRecordBatch,
)
from galileo_observe.utils.api_client import ApiClient

Stringable = (str, int, float)


class GalileoObserveAsyncCallback(AsyncCallbackHandler):
    timers: Dict[str, Dict[str, float]] = {}
    records: Dict[str, TransactionRecord] = {}
    parent_child_mapping: DefaultDict[str, List[str]] = defaultdict(list)
    version: Optional[str]
    client: ApiClient

    def __init__(
        self,
        project_name: str,
        version: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """LangChain callback async handler for Galileo Observe

        Parameters
        ----------
        project_name : str
            Name of the project to log to
        version : Optional[str]
            A version identifier for this system so logs can be attributed
            to a specific configuration
        """
        self.version = version
        self.client = ApiClient(project_name=project_name)
        super().__init__(*args, **kwargs)

    async def _start_new_node(
        self,
        run_id: UUID,
        parent_run_id: Optional[UUID],
        node_name: str,
        serialized: Optional[Dict[str, Any]] = None,
    ) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
        node_id = str(run_id)
        chain_id = str(parent_run_id) if parent_run_id else None
        if chain_id:
            if self.records.get(chain_id):
                self.records[chain_id].has_children = True
                chain_root_id = self.records[chain_id].chain_root_id
                self.parent_child_mapping[chain_id].append(node_id)
            else:
                chain_root_id = node_id
        else:
            chain_root_id = node_id
        # Parse and set the name of the node.
        node_class_reference = None
        if serialized is not None and isinstance(serialized, dict):
            node_name = serialized.get("name") or node_name
            node_class_reference = serialized.get("id")
        if node_class_reference and isinstance(node_class_reference, list):
            node_name = node_class_reference[-1]

        self.timers[node_id] = {}
        self.timers[node_id]["start"] = time.perf_counter()

        return node_id, chain_root_id, chain_id, node_name

    async def _end_node(self, run_id: UUID) -> tuple[str, int]:
        node_id = str(run_id)

        self.timers[node_id]["stop"] = time.perf_counter()
        latency_ms = round((self.timers[node_id]["stop"] - self.timers[node_id]["start"]) * 1000)
        del self.timers[node_id]

        return node_id, latency_ms

    async def _finalize_node(self, record: TransactionRecord) -> None:
        self.records[record.node_id] = record
        batch_records: List[TransactionRecord] = list()
        # If this record is closing out a root chain,
        # then add all records with that chain_root_id to the batch.
        if record.node_id == record.chain_root_id:
            for node_id, batch_record in self.records.copy().items():
                if batch_record.chain_root_id == record.chain_root_id:
                    # If the node is a non-chain node,
                    # or is a parent node with any children, include it.
                    if batch_record.node_type != NodeType.chain or node_id in self.parent_child_mapping.keys():
                        batch_records.append(batch_record)
                    del self.records[node_id]

            transaction_batch = TransactionRecordBatch(
                records=batch_records,
                logging_method=TransactionLoggingMethod.py_langchain_async,
            )
            async_run(self.client.ingest_batch(transaction_batch))

    async def on_llm_start(
        self,
        serialized: Optional[Dict[str, Any]],
        prompts: List[str],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM starts running."""
        node_id, chain_root_id, chain_id, node_name = await self._start_new_node(
            run_id, parent_run_id, NodeType.llm, serialized
        )
        input_text = prompts[0]
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model_name")
        temperature = invocation_params.get("temperature")
        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            node_name=node_name,
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            temperature=temperature,
            tags=tags,
            user_metadata=metadata,
            node_type=NodeType.llm.value,
            version=self.version,
        )

    async def on_chat_model_start(
        self,
        serialized: Optional[Dict[str, Any]],
        messages: List[List[BaseMessage]],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when Chat Model starts running."""
        node_id, chain_root_id, chain_id, node_name = await self._start_new_node(
            run_id, parent_run_id, NodeType.chat, serialized
        )
        chat_messages = ChatPromptValue(messages=messages[0])
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")
        invocation_params = kwargs.get("invocation_params", {})
        model = invocation_params.get("model", invocation_params.get("_type", "undefined-type"))
        temperature = invocation_params.get("temperature")
        tools = invocation_params.get("tools", None)
        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            node_name=node_name,
            input_text=chat_messages.to_string(),
            tools=dumps(tools) if tools else None,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            temperature=temperature,
            tags=tags,
            user_metadata=metadata,
            node_type=NodeType.chat.value,
            version=self.version,
        )

    async def on_llm_new_token(
        self,
        token: str,
        run_id: UUID,
        chunk: Union[GenerationChunk, ChatGenerationChunk, None] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM generates a new token."""
        node_id = str(run_id)
        model_dict = self.records[node_id].model_dump()
        if model_dict["time_to_first_token_ms"] is None:
            root_node_id = model_dict["chain_root_id"]
            start_time_root = self.timers[root_node_id]["start"]
            # Calculate time to generate the first token and convert to milliseconds
            time_to_first_token_ms = round(
                (time.perf_counter() - start_time_root) * 1000
            )
            model_dict.update(time_to_first_token_ms=time_to_first_token_ms)
            self.records[node_id] = TransactionRecord(**model_dict)

    async def on_llm_end(self, response: LLMResult, run_id: UUID, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        node_id, latency_ms = await self._end_node(run_id)

        generation = response.flatten()[0].generations[0][0]
        tool_calls = None
        # Only chat generations have messages which contain the invocation params
        if isinstance(generation, (ChatGeneration, ChatGenerationChunk)):
            message = generation.message
            if isinstance(message, (AIMessageChunk, AIMessage)):
                tool_calls = message.tool_calls
        output_text = generation.text

        if not output_text and tool_calls:
            output_text = dumps(tool_calls)

        if response.llm_output:
            usage = response.llm_output.get("token_usage", response.llm_output.get("usage", {}))
            num_input_tokens = usage.get("prompt_tokens", usage.get("input_tokens", None))
            num_output_tokens = usage.get("completion_tokens", usage.get("output_tokens", None))
            num_total_tokens = usage.get("total_tokens", None)
        else:
            try:
                encoding = tiktoken.encoding_for_model(self.records[node_id].model or "")
                num_input_tokens = len(encoding.encode(self.records[node_id].input_text))
                num_output_tokens = len(encoding.encode(output_text))
                num_total_tokens = num_input_tokens + num_output_tokens
            except KeyError:
                num_input_tokens = 0
                num_output_tokens = 0
                num_total_tokens = 0

        finish_reason = ""
        if generation.generation_info:
            finish_reason = generation.generation_info.get("finish_reason", finish_reason)

        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=output_text,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            num_total_tokens=num_total_tokens,
            finish_reason=finish_reason,
            latency_ms=latency_ms,
            status_code=HTTPStatus.OK,
        )

        await self._finalize_node(TransactionRecord(**model_dict))

    async def on_llm_error(self, error: BaseException, run_id: UUID, **kwargs: Any) -> Any:
        """Run when LLM errors."""
        node_id, latency_ms = await self._end_node(run_id)

        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error}",
            num_input_tokens=0,
            num_output_tokens=0,
            num_total_tokens=0,
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
        )

        await self._finalize_node(TransactionRecord(**model_dict))

    async def on_chain_start(
        self,
        serialized: Optional[Dict[str, Any]],
        inputs: Dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain starts running."""
        node_id, chain_root_id, chain_id, node_name = await self._start_new_node(
            run_id, parent_run_id, NodeType.chain, serialized
        )
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")

        if isinstance(inputs, Stringable):
            node_input = {"input": inputs}
        elif isinstance(inputs, BaseMessage):
            node_input = message_to_dict(inputs)
        elif isinstance(inputs, dict):
            node_input = dict()
            for key, value in inputs.items():
                if isinstance(value, Stringable):
                    node_input[key] = value
                elif isinstance(value, BaseMessage):
                    node_input[key] = str(message_to_dict(value))
                elif isinstance(value, Sequence):
                    node_input[key] = ". ".join(repr(v) for v in value)
        elif isinstance(inputs, list) and all(isinstance(v, Document) for v in inputs):
            node_input = {str(index): value.page_content for index, value in enumerate(inputs)}
        else:
            node_input = dict()

        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            node_name=node_name,
            input_text=dumps(
                node_input,
                default=GalileoObserveAsyncCallback.json_serializer,
            ),
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            tags=tags,
            user_metadata=metadata,
            node_type=NodeType.chain.value,
            version=self.version,
        )

    async def on_chain_end(
        self,
        outputs: Union[str, Dict[str, Any]],
        run_id: UUID,
        **kwargs: Any,
    ) -> Any:
        """Run when chain ends running."""
        node_id, latency_ms = await self._end_node(run_id)

        if isinstance(outputs, str):
            node_output = {"output": outputs}
        elif isinstance(outputs, dict):
            node_output = outputs
        elif isinstance(outputs, (AgentFinish, AgentAction)):
            node_output = outputs.dict()
        elif isinstance(outputs, BaseMessage):
            node_output = message_to_dict(outputs)
        elif isinstance(outputs, Sequence):
            node_output = [
                message_to_dict(output) if isinstance(output, BaseMessage) else repr(output) for output in outputs
            ]
        else:
            node_output = dict()

        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=dumps(
                node_output,
                default=GalileoObserveAsyncCallback.json_serializer,
            ),
            finish_reason="chain_end",
            latency_ms=latency_ms,
            status_code=HTTPStatus.OK,
        )

        await self._finalize_node(TransactionRecord(**model_dict))

    async def on_chain_error(self, error: BaseException, run_id: UUID, **kwargs: Any) -> Any:
        """Run when chain errors."""
        node_id, latency_ms = await self._end_node(run_id)

        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error}",
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
        )

        await self._finalize_node(TransactionRecord(**model_dict))

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> Any:
        """Run on agent end."""
        node_id = str(run_id)
        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            node_type=NodeType.agent.value,
        )

        self.records[node_id] = TransactionRecord(**model_dict)

    async def on_tool_start(
        self,
        serialized: Optional[Dict[str, Any]],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool starts running."""
        node_id, chain_root_id, chain_id, node_name = await self._start_new_node(
            run_id, parent_run_id, NodeType.tool, serialized
        )
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")

        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            node_name=node_name,
            input_text=input_str,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            tags=tags,
            user_metadata=metadata,
            node_type=NodeType.tool.value,
            version=self.version,
        )

    async def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when the tool ends running.

        Args:
            output (Any): The output of the tool.
            run_id (UUID): The run ID. This is the ID of the current run.
            parent_run_id (UUID): The parent run ID. This is the ID of the parent run.
            tags (Optional[List[str]]): The tags.
            kwargs (Any): Additional keyword arguments.
        """
        node_id, latency_ms = await self._end_node(run_id)

        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=dumps(output, default=GalileoObserveAsyncCallback.json_serializer),
            latency_ms=latency_ms,
            status_code=HTTPStatus.OK,
        )

        await self._finalize_node(TransactionRecord(**model_dict))

    async def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> Any:
        """Run when tool errors."""
        node_id, latency_ms = await self._end_node(run_id)

        error_text = repr(error)
        if isinstance(error, BaseException):
            error_text += "\n" + "".join(traceback.format_exception(type(error), error, error.__traceback__))

        model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error_text}",
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
        )

        record = TransactionRecord(**model_dict)
        await self._finalize_node(record)

    async def on_retriever_start(
        self,
        serialized: Optional[Dict[str, Any]],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever start."""
        node_id, chain_root_id, chain_id, node_name = await self._start_new_node(
            run_id, parent_run_id, NodeType.retriever, serialized
        )

        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            node_name=node_name,
            input_text=str(query),
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            tags=tags,
            user_metadata=metadata,
            node_type=NodeType.retriever.value,
            version=self.version,
        )

    async def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        """Run on retriever end."""
        node_id, latency_ms = await self._end_node(run_id)

        model_dict = self.records[node_id].model_dump()

        docs = dumps([{"page_content": document.page_content, "metadata": document.metadata} for document in documents])

        model_dict.update(
            output_text=str(docs),
            finish_reason="retriever_end",
            latency_ms=latency_ms,
            status_code=HTTPStatus.OK,
        )

        record = TransactionRecord(**model_dict)
        await self._finalize_node(record)

    async def on_retriever_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        """Run on retriever error."""
        node_id, latency_ms = await self._end_node(run_id)

        model_dict = self.records[node_id].model_dump()

        model_dict.update(
            output_text=f"ERROR: {str(error)}",
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", HTTPStatus.INTERNAL_SERVER_ERROR),
        )

    @staticmethod
    def json_serializer(obj: Any) -> Union[str, Dict[Any, Any]]:
        """
        For serializing objects that cannot be serialized by default with json.dumps.

        Checks for certain methods to convert object to dict.
        """
        if isinstance(obj, BaseModel):
            return obj.model_dump(mode="json")
        if isinstance(obj, BaseModelV1):
            return loads(obj.json())
        return str(type(obj))
