from importlib.metadata import version
from os import getenv
from time import time
from typing import Any, Dict, List, Optional

import jwt
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.execution import async_run

from galileo_observe.constants.routes import Routes
from galileo_observe.schema.transaction import TransactionRecordBatch
from galileo_observe.utils.request import HttpHeaders, make_request


class ApiClient:
    def __init__(self, project_name: str):
        self.project_id = None
        self.api_url = self.get_api_url()
        if self.healthcheck():
            self.token = self.get_token()
            try:
                project = self.get_project_by_name(project_name)
                if project["type"] not in ["llm_monitor", "galileo_observe"]:
                    raise Exception(
                        f"Project {project_name} is not a Galileo Observe project"
                    )
                self.project_id = project["id"]
            except Exception as e:
                if "not found" in str(e):
                    self.project_id = self.create_project(project_name)["id"]
                    print(f"🚀 Creating new project... project {project_name} created!")
                else:
                    raise e

    def get_api_url(self) -> str:
        console_url = getenv("GALILEO_CONSOLE_URL")
        if console_url is None:
            raise Exception("GALILEO_CONSOLE_URL must be set")
        if any(map(console_url.__contains__, ["localhost", "127.0.0.1"])):
            api_url = "http://localhost:8088"
        else:
            api_url = console_url.replace("console", "api")
        return api_url

    def get_token(self) -> str:
        api_key = getenv("GALILEO_API_KEY")
        if api_key:
            return self.api_key_login(api_key).get("access_token", "")

        username = getenv("GALILEO_USERNAME")
        password = getenv("GALILEO_PASSWORD")
        if username and password:
            return self.username_login(username, password).get("access_token", "")

        raise Exception(
            "GALILEO_API_KEY or GALILEO_USERNAME and GALILEO_PASSWORD must be set"
        )

    def healthcheck(self) -> bool:
        async_run(
            make_request(
                RequestMethod.GET, base_url=self.base_url, endpoint=Routes.healthcheck
            )
        )
        return True

    def username_login(self, username: str, password: str) -> Dict[str, str]:
        return async_run(
            make_request(
                RequestMethod.POST,
                base_url=self.base_url,
                endpoint=Routes.login,
                data={
                    "username": username,
                    "password": password,
                    "auth_method": "email",
                },
            )
        )

    def api_key_login(self, api_key: str) -> Dict[str, str]:
        return async_run(
            make_request(
                RequestMethod.POST,
                base_url=self.base_url,
                endpoint=Routes.api_key_login,
                json={"api_key": api_key},
            )
        )

    @property
    def base_url(self) -> str:
        return self.api_url

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _make_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        json_request_only: bool = False,
    ) -> Any:
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint not in [Routes.login, Routes.api_key_login] and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        return async_run(
            make_request(
                request_method=request_method,
                base_url=self.base_url,
                endpoint=endpoint,
                json=json,
                data=data,
                files=files,
                params=params,
                headers=headers,
            )
        )

    async def _make_async_request(
        self,
        request_method: RequestMethod,
        endpoint: str,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        json_request_only: bool = False,
    ) -> Any:
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint not in [Routes.login, Routes.api_key_login] and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        await make_request(
            request_method=request_method,
            base_url=self.base_url,
            endpoint=endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )

    async def ingest_batch(
        self, transaction_batch: TransactionRecordBatch
    ) -> Dict[str, str]:
        transaction_batch.client_version = version("galileo_observe")
        return await self._make_async_request(
            RequestMethod.POST,
            endpoint=Routes.ingest.format(project_id=self.project_id),
            json=transaction_batch.model_dump(),
        )

    def get_project_by_name(self, project_name: str) -> Any:
        projects = self._make_request(
            RequestMethod.GET,
            endpoint=Routes.projects,
            params={"project_name": project_name},
        )
        if len(projects) < 1:
            raise Exception(f"Galileo project {project_name} not found")
        return projects[0]

    def create_project(self, project_name: str) -> Dict[str, str]:
        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.projects,
            json={"name": project_name, "type": "llm_monitor"},
        )

    def get_logged_data(
        self,
        start_time: Optional[str],
        end_time: Optional[str],
        chain_id: Optional[str],
        limit: Optional[int],
        offset: Optional[int],
        include_chains: Optional[bool],
        sort_spec: Optional[List[Any]],
        filters: Optional[List[Any]],
        columns: Optional[List[str]],
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if chain_id is not None:
            params["chain_id"] = chain_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if include_chains is not None:
            params["include_chains"] = include_chains

        body: Dict[str, Any] = {}
        if filters is not None:
            body["filters"] = filters
        if sort_spec is not None:
            body["sort_spec"] = sort_spec
        if columns is not None:
            body["columns"] = columns

        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.rows.format(project_id=self.project_id),
            params=params,
            json=body,
        )

    def delete_logged_data(self, filters: List[Dict]) -> Dict[str, Any]:
        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.delete.format(project_id=self.project_id),
            json=dict(filters=filters),
        )

    def get_metrics(
        self,
        start_time: str,
        end_time: str,
        interval: Optional[int],
        group_by: Optional[str],
        filters: Optional[List[Any]],
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "start_time": start_time,
            "end_time": end_time,
        }
        if interval is not None:
            params["interval"] = interval
        if group_by is not None:
            params["group_by"] = group_by

        body: Dict[str, Any] = {}
        if filters is not None:
            body["filters"] = filters

        return self._make_request(
            RequestMethod.POST,
            endpoint=Routes.metrics.format(project_id=self.project_id),
            params=params,
            json=body,
        )
