from enum import Enum


class Routes(str, Enum):
    healthcheck = "healthcheck"
    login = "login"
    api_key_login = "login/api_key"
    get_token = "get-token"
    current_user = "current_user"
    projects = "projects"
    all_projects = "projects/all"
    templates = "projects/{project_id}/templates"
    versions = "projects/{project_id}/templates/{template_id}/versions"
    version = "projects/{project_id}/templates/{template_id}/versions/{version}"
    dataset = "projects/{project_id}/upload_prompt_dataset"
    runs = "projects/{project_id}/runs"
    jobs = "jobs"
    set_metric = "projects/{project_id}/runs/{run_id}/metrics"
    integrations = "integrations/{integration_name}"
    ingest = "projects/{project_id}/observe/ingest"
    rows = "projects/{project_id}/observe/rows"
    delete = "projects/{project_id}/observe/delete"
    metrics = "projects/{project_id}/observe/metrics"
