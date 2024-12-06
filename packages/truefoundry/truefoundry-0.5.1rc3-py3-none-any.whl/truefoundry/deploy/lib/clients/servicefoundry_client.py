from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
import socketio
from dateutil.tz import tzlocal
from rich.status import Status
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from truefoundry.common.constants import VERSION_PREFIX
from truefoundry.common.request_utils import request_handling
from truefoundry.common.servicefoundry_client import (
    ServiceFoundryServiceClient as BaseServiceFoundryServiceClient,
)
from truefoundry.common.servicefoundry_client import (
    check_min_cli_version,
    session_with_retries,
)
from truefoundry.deploy.auto_gen import models as auto_gen_models
from truefoundry.deploy.io.output_callback import OutputCallBack
from truefoundry.deploy.lib.auth.servicefoundry_session import ServiceFoundrySession
from truefoundry.deploy.lib.model.entity import (
    Application,
    CreateDockerRepositoryResponse,
    Deployment,
    DockerRegistryCredentials,
    JobRun,
    TriggerJobResult,
    Workspace,
    WorkspaceResources,
)
from truefoundry.deploy.lib.win32 import allow_interrupt
from truefoundry.deploy.v2.lib.models import (
    AppDeploymentStatusResponse,
    ApplicationFqnResponse,
    BuildResponse,
    DeploymentFqnResponse,
)
from truefoundry.logger import logger
from truefoundry.pydantic_v1 import parse_obj_as

DEPLOYMENT_LOGS_SUBSCRIBE_MESSAGE = "DEPLOYMENT_LOGS"
BUILD_LOGS_SUBSCRIBE_MESSAGE = "BUILD_LOGS"
MAX_RETRIES_WORKFLOW_TRIGGER = 3

if TYPE_CHECKING:
    from truefoundry.deploy.auto_gen.models import Application


def _upload_packaged_code(metadata, package_file):
    file_size = os.stat(package_file).st_size
    with open(package_file, "rb") as file_to_upload:
        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="Uploading package",
        ) as progress_bar:
            wrapped_file = CallbackIOWrapper(
                progress_bar.update, file_to_upload, "read"
            )
            headers = metadata.get("headers", {})
            http_response = requests.put(
                metadata["url"], data=wrapped_file, headers=headers
            )

            if http_response.status_code not in [204, 201, 200]:
                raise RuntimeError(f"Failed to upload code {http_response.content}")


class ServiceFoundryServiceClient(BaseServiceFoundryServiceClient):
    # TODO (chiragjn): Rename base_url to tfy_host
    def __init__(self, init_session: bool = True, base_url: Optional[str] = None):
        self._session: Optional[ServiceFoundrySession] = None
        if init_session:
            if base_url:
                logger.warning("Passed base url %r will be ignored", base_url)
            self._session = ServiceFoundrySession()
            base_url = self._session.base_url
        elif not base_url:
            raise Exception("Neither session, not base_url provided")
        super().__init__(base_url=base_url)

    def _get_header(self):
        if not self._session:
            return {}
        return {"Authorization": f"Bearer {self._session.access_token}"}

    @check_min_cli_version
    def get_id_from_fqn(self, fqn_type: str, fqn: str):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/fqn/{fqn_type}"
        response = session_with_retries().get(
            url, headers=self._get_header(), params={"fqn": fqn}
        )
        return request_handling(response)

    @check_min_cli_version
    def list_workspace(self):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace"
        response = session_with_retries().get(url, headers=self._get_header())
        return request_handling(response)

    @check_min_cli_version
    def list_workspaces(
        self,
        cluster_id: Optional[str] = None,
        workspace_name: Optional[str] = None,
        workspace_fqn: Optional[str] = None,
    ) -> List[Workspace]:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace"
        params = {}
        if cluster_id:
            params["clusterId"] = cluster_id
        if workspace_name:
            params["workspaceName"] = workspace_name
        if workspace_fqn:
            params["workspaceFqn"] = workspace_fqn
        response = session_with_retries().get(
            url, params=params, headers=self._get_header()
        )
        response = request_handling(response)
        return parse_obj_as(List[Workspace], response)

    @check_min_cli_version
    def create_workspace(
        self,
        workspace_name: str,
        cluster_name: str,
        resources: WorkspaceResources,
    ) -> Workspace:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace"
        response = session_with_retries().post(
            url,
            json={
                "manifest": {
                    "cluster": cluster_name,
                    "name": workspace_name,
                    "resources": resources.dict(exclude_none=True),
                }
            },
            headers=self._get_header(),
        )
        response_data = request_handling(response)
        return Workspace.parse_obj(response_data)

    @check_min_cli_version
    def remove_workspace(self, workspace_id, force=False) -> Workspace:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace/{workspace_id}"
        force = json.dumps(
            force
        )  # this dumb conversion is required because `params` just casts as str
        response = session_with_retries().delete(
            url, headers=self._get_header(), params={"force": force}
        )
        response = request_handling(response)
        return Workspace.parse_obj(response["workspace"])

    @check_min_cli_version
    def get_workspace_by_name(self, workspace_name, cluster_id):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace"
        response = session_with_retries().get(
            url,
            headers=self._get_header(),
            params={"name": workspace_name, "clusterId": cluster_id},
        )
        return request_handling(response)

    @check_min_cli_version
    def get_workspace(self, workspace_id):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace/{workspace_id}"
        response = session_with_retries().get(url, headers=self._get_header())
        return request_handling(response)

    @check_min_cli_version
    def get_workspace_by_fqn(self, workspace_fqn: str) -> List[Workspace]:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workspace"
        response = session_with_retries().get(
            url,
            headers=self._get_header(),
            params={"fqn": workspace_fqn},
        )
        response = request_handling(response)
        return parse_obj_as(List[Workspace], response)

    @check_min_cli_version
    def list_deployments(self, workspace_id: str = None):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/deployment"
        params = {}
        if workspace_id:
            params["workspaceId"] = workspace_id
        response = session_with_retries().get(
            url=url, params=params, headers=self._get_header()
        )
        return request_handling(response)

    @check_min_cli_version
    def list_cluster(self):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/cluster"
        response = session_with_retries().get(url, headers=self._get_header())
        return request_handling(response)

    @check_min_cli_version
    def get_cluster(self, cluster_id):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/cluster/{cluster_id}"
        response = session_with_retries().get(url, headers=self._get_header())
        return request_handling(response)

    @check_min_cli_version
    def get_presigned_url(self, space_name, service_name, env):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/deployment/code-upload-url"
        response = session_with_retries().post(
            url,
            json={
                "workspaceFqn": space_name,
                "serviceName": service_name,
                "stage": env,
            },
            headers=self._get_header(),
        )
        return request_handling(response)

    @check_min_cli_version
    def upload_code_package(
        self, workspace_fqn: str, component_name: str, package_local_path: str
    ) -> str:
        http_response = self.get_presigned_url(
            space_name=workspace_fqn, service_name=component_name, env="default"
        )
        _upload_packaged_code(metadata=http_response, package_file=package_local_path)

        return http_response["uri"]

    @check_min_cli_version
    def deploy_application(
        self, workspace_id: str, application: auto_gen_models.Workflow
    ) -> Deployment:
        data = {
            "workspaceId": workspace_id,
            "name": application.name,
            "manifest": application.dict(exclude_none=True),
        }
        logger.debug(json.dumps(data))
        url = f"{self._api_server_url}/{VERSION_PREFIX}/deployment"
        deploy_response = session_with_retries().post(
            url, json=data, headers=self._get_header()
        )
        response = request_handling(deploy_response)
        return Deployment.parse_obj(response["deployment"])

    def _get_log_print_line(self, log: dict):
        timestamp = int(log["time"]) / 1e6

        time_obj = datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)
        time_obj.replace(tzinfo=timezone.utc)
        local_time = time_obj.astimezone(tzlocal())
        local_time_str = local_time.isoformat()
        return f'[{local_time_str}] {log["log"].strip()}'

    def _tail_logs(
        self,
        tail_logs_url: str,
        query_dict: dict,
        # NOTE: Rather making this printer callback an argument,
        # we should have global printer callback
        # which will be initialized based on the running env (cli, lib, notebook)
        subscribe_message: str,
        socketio_path: str = "socket.io",
        callback=None,
        wait=True,
    ):
        callback = callback or OutputCallBack()
        sio = socketio.Client(request_timeout=60)
        callback.print_line("Waiting for the task to start...")

        @sio.on(subscribe_message)
        def logs(data):
            try:
                _log = json.loads(data)
                callback.print_line(self._get_log_print_line(_log["body"]))
            except Exception:
                logger.exception(f"Error while parsing log line, {data!r}")

        def sio_disconnect_no_exception():
            try:
                sio.disconnect()
            except Exception:
                logger.exception("Error while disconnecting from socket connection")

        with allow_interrupt(sio_disconnect_no_exception):
            sio.connect(
                tail_logs_url,
                transports="websocket",
                headers=self._get_header(),
                socketio_path=socketio_path,
            )
            # TODO: We should have have a timeout here. `emit` does
            #   not support timeout. Explore `sio.call`.
            sio.emit(
                subscribe_message,
                json.dumps(query_dict),
            )
            if wait:
                sio.wait()

    @check_min_cli_version
    def get_deployment(self, application_id: str, deployment_id: str) -> Deployment:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/app/{application_id}/deployments/{deployment_id}"
        response = session_with_retries().get(url, headers=self._get_header())
        response_data = request_handling(response)
        return Deployment.parse_obj(response_data)

    @check_min_cli_version
    def get_deployment_statuses(
        self, application_id: str, deployment_id: str
    ) -> List[AppDeploymentStatusResponse]:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/app/{application_id}/deployments/{deployment_id}/statuses"
        response = session_with_retries().get(url, headers=self._get_header())
        response_data = request_handling(response)
        return parse_obj_as(List[AppDeploymentStatusResponse], response_data)

    @check_min_cli_version
    def get_deployment_build_response(
        self, application_id: str, deployment_id: str
    ) -> List[BuildResponse]:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/app/{application_id}/deployments/{deployment_id}/builds"
        response = session_with_retries().get(url, headers=self._get_header())
        response_data = request_handling(response)
        return parse_obj_as(List[BuildResponse], response_data)

    def _get_deployment_logs(
        self,
        workspace_id: str,
        application_id: str,
        deployment_id: str,
        job_run_name: Optional[str] = None,
        start_ts_nano: Optional[int] = None,
        end_ts_nano: Optional[int] = None,
        limit: Optional[int] = None,
        num_logs_to_ignore: Optional[int] = None,
    ) -> List:
        get_logs_query = {"applicationId": application_id}
        if deployment_id:
            get_logs_query["deploymentId"] = deployment_id
        data = {"getLogsQuery": json.dumps(get_logs_query)}
        if start_ts_nano:
            data["startTs"] = str(start_ts_nano)
        if end_ts_nano:
            data["endTs"] = str(end_ts_nano)
        if limit:
            data["limit"] = str(limit)
        if num_logs_to_ignore:
            data["numLogsToIgnore"] = int(num_logs_to_ignore)
        if job_run_name:
            data["jobRunName"] = job_run_name

        url = f"{self._api_server_url}/{VERSION_PREFIX}/logs/{workspace_id}"
        response = session_with_retries().get(
            url=url, params=data, headers=self._get_header()
        )
        response_data = request_handling(response)
        return list(response_data["logs"])

    @check_min_cli_version
    def tail_build_logs(
        self,
        build_response: BuildResponse,
        callback=None,
        wait: bool = True,
    ):
        callback = callback or OutputCallBack()
        tail_logs_obj = json.loads(build_response.tailLogsUrl)
        self._tail_logs(
            tail_logs_url=urljoin(
                tail_logs_obj["uri"], f"/?type={BUILD_LOGS_SUBSCRIBE_MESSAGE}"
            ),
            socketio_path=tail_logs_obj["path"],
            query_dict={
                "pipelineRunName": build_response.name,
                "startTs": build_response.logsStartTs,
            },
            callback=callback,
            wait=wait,
            subscribe_message=BUILD_LOGS_SUBSCRIBE_MESSAGE,
        )

    @check_min_cli_version
    def tail_logs_for_deployment(
        self,
        workspace_id: str,
        application_id: str,
        deployment_id: str,
        start_ts: int,
        limit: int,
        callback=None,
        wait: bool = True,
    ):
        callback = callback or OutputCallBack()
        self._tail_logs(
            tail_logs_url=urljoin(
                self._api_server_url, f"/?type={DEPLOYMENT_LOGS_SUBSCRIBE_MESSAGE}"
            ),
            query_dict={
                "workspaceId": workspace_id,
                "startTs": str(int(start_ts * 1e6)),
                "limit": limit,
                "getLogsQuery": {
                    "applicationId": application_id,
                    "deploymentId": deployment_id,
                },
            },
            callback=callback,
            wait=wait,
            subscribe_message=DEPLOYMENT_LOGS_SUBSCRIBE_MESSAGE,
        )

    @check_min_cli_version
    def poll_logs_for_deployment(
        self,
        workspace_id: str,
        application_id: str,
        deployment_id: str,
        job_run_name: Optional[str],
        start_ts: int,
        limit: int,
        poll_interval_seconds: int,
        callback=None,
    ):
        callback = callback or OutputCallBack()
        start_ts_nano = int(start_ts * 1e6)

        with Status(status="Polling for logs") as spinner:
            num_logs_to_ignore = 0

            while True:
                logs_list = self._get_deployment_logs(
                    workspace_id=workspace_id,
                    application_id=application_id,
                    deployment_id=deployment_id,
                    job_run_name=job_run_name,
                    start_ts_nano=start_ts_nano,
                    limit=limit,
                    num_logs_to_ignore=num_logs_to_ignore,
                )

                if len(logs_list) == 0:
                    logger.warning("Did not receive any logs")
                    time.sleep(poll_interval_seconds)
                    continue

                for log in logs_list:
                    callback.print_line(self._get_log_print_line(log))

                last_log_time = logs_list[-1]["time"]
                num_logs_to_ignore = 0
                for log in reversed(logs_list):
                    if log["time"] != last_log_time:
                        break
                    num_logs_to_ignore += 1

                start_ts_nano = int(last_log_time)
                spinner.update(status=f"Waiting for {poll_interval_seconds} secs.")
                time.sleep(poll_interval_seconds)

    @check_min_cli_version
    def fetch_deployment_logs(
        self,
        workspace_id: str,
        application_id: str,
        deployment_id: str,
        job_run_name: Optional[str],
        start_ts: Optional[int],
        end_ts: Optional[int],
        limit: Optional[int],
        callback=None,
    ):
        callback = callback or OutputCallBack()
        logs_list = self._get_deployment_logs(
            workspace_id=workspace_id,
            application_id=application_id,
            deployment_id=deployment_id,
            job_run_name=job_run_name,
            start_ts_nano=int(start_ts * 1e6),
            end_ts_nano=int(end_ts * 1e6),
            limit=limit,
        )
        for log in logs_list:
            callback.print_line(self._get_log_print_line(log))

    @check_min_cli_version
    def fetch_build_logs(
        self,
        build_response: BuildResponse,
        callback=None,
    ) -> None:
        callback = callback or OutputCallBack()
        url = build_response.getLogsUrl
        response = session_with_retries().get(url=url, headers=self._get_header())
        logs_list = request_handling(response)
        for log in logs_list["logs"]:
            # TODO: Have to establish a log line format that includes timestamp, level, message
            callback.print_line(self._get_log_print_line(log))

    @check_min_cli_version
    def get_deployment_info_by_fqn(self, deployment_fqn: str) -> DeploymentFqnResponse:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/fqn/deployment"
        response = session_with_retries().get(
            url, headers=self._get_header(), params={"fqn": deployment_fqn}
        )
        response_data = request_handling(response)
        return DeploymentFqnResponse.parse_obj(response_data)

    @check_min_cli_version
    def get_application_info_by_fqn(
        self, application_fqn: str
    ) -> ApplicationFqnResponse:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/fqn/app"
        response = session_with_retries().get(
            url, headers=self._get_header(), params={"fqn": application_fqn}
        )
        response_data = request_handling(response)
        return ApplicationFqnResponse.parse_obj(response_data)

    @check_min_cli_version
    def remove_application(self, application_id: str):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/app/{application_id}"
        response = session_with_retries().delete(url, headers=self._get_header())
        response = request_handling(response)
        # TODO: Add pydantic here.
        return response

    @check_min_cli_version
    def get_application_info(self, application_id: str) -> Application:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/app/{application_id}"
        response = session_with_retries().get(url, headers=self._get_header())
        response = request_handling(response)
        return Application.parse_obj(response)

    def list_job_runs(
        self,
        application_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search_prefix: Optional[str] = None,
    ) -> List[JobRun]:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/jobs/{application_id}/runs"
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if search_prefix:
            params["searchPrefix"] = search_prefix
        response = session_with_retries().get(
            url, headers=self._get_header(), params=params
        )
        response_data = request_handling(response)
        return parse_obj_as(List[JobRun], response_data["data"])

    def get_job_run(
        self,
        application_id: str,
        job_run_name: str,
    ):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/jobs/{application_id}/runs/{job_run_name}"
        response = session_with_retries().get(url, headers=self._get_header())
        response_data = request_handling(response)
        return parse_obj_as(JobRun, response_data)

    def trigger_job(
        self,
        deployment_id: str,
        command: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> TriggerJobResult:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/jobs/trigger"
        body = {
            "deploymentId": deployment_id,
            "input": {},
        }
        if command:
            body["input"]["command"] = command
        if params:
            body["input"]["params"] = params
        response = session_with_retries().post(
            url, json=body, headers=self._get_header()
        )
        response = request_handling(response)
        return TriggerJobResult.parse_obj(response)

    def trigger_workflow(self, application_id: str, inputs: Dict[str, Any]):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/workflow/{application_id}/executions"
        body = {"inputs": inputs}
        response = session_with_retries(retries=MAX_RETRIES_WORKFLOW_TRIGGER).post(
            url, json=body, headers=self._get_header()
        )
        response = request_handling(response)
        return response

    @check_min_cli_version
    def get_docker_registry_creds(
        self, docker_registry_fqn: str, cluster_id: str
    ) -> DockerRegistryCredentials:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/docker-registry/creds"
        response = session_with_retries().get(
            url,
            headers=self._get_header(),
            params={
                "fqn": docker_registry_fqn,
                "clusterId": cluster_id,
            },
        )
        response = request_handling(response)
        return DockerRegistryCredentials.parse_obj(response)

    @check_min_cli_version
    def create_repo_in_registry(
        self, docker_registry_fqn: str, workspace_fqn: str, application_name: str
    ) -> CreateDockerRepositoryResponse:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/docker-registry/create-repo"
        response = session_with_retries().post(
            url,
            headers=self._get_header(),
            data={
                "fqn": docker_registry_fqn,
                "workspaceFqn": workspace_fqn,
                "applicationName": application_name,
            },
        )
        response = request_handling(response)
        return CreateDockerRepositoryResponse.parse_obj(response)

    @check_min_cli_version
    def list_applications(
        self,
        application_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        application_name: Optional[str] = None,
    ) -> List[Application]:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/app"
        params = {}
        if application_id:
            params["applicationId"] = application_id
        if workspace_id:
            params["workspaceId"] = workspace_id
        if application_name:
            params["applicationName"] = application_name
        response = session_with_retries().get(
            url, params=params, headers=self._get_header()
        )
        response = request_handling(response)
        return parse_obj_as(List[Application], response)

    @check_min_cli_version
    def list_versions(
        self,
        application_id: str,
        deployment_version: Optional[int] = None,
        deployment_id: Optional[str] = None,
    ) -> List[Deployment]:
        url = (
            f"{self._api_server_url}/{VERSION_PREFIX}/app/{application_id}/deployments"
        )
        params = {}
        if deployment_version:
            params["version"] = deployment_version
        if deployment_id:
            params["deploymentId"] = deployment_id
        response = session_with_retries().get(
            url, params=params, headers=self._get_header()
        )
        response = request_handling(response)
        return parse_obj_as(List[Deployment], response)

    @check_min_cli_version
    def apply(self, manifest: Dict[str, Any]):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/apply"
        body = {"manifest": manifest}
        response = session_with_retries().put(
            url, headers=self._get_header(), json=body
        )
        response_data = request_handling(response)
        return response_data

    def terminate_job_run(
        self,
        deployment_id: str,
        job_run_name: str,
    ):
        url = f"{self._api_server_url}/{VERSION_PREFIX}/jobs/terminate"
        body = {
            "deploymentId": deployment_id,
            "jobRunName": job_run_name,
        }
        response = session_with_retries().post(
            url,
            # TODO (chiragjn): Check if this is supposed to be params or json
            params=body,
            json=body,
            headers=self._get_header(),
        )
        response_data = request_handling(response)
        return response_data
