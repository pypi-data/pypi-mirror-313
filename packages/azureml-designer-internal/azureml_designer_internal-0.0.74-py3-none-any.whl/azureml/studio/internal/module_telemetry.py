import platform
import os
import requests
import traceback
import time
from azureml.core.run import Run
from azureml.telemetry.contracts import (RequiredFields, StandardFields, ExtensionFields)
from azureml.studio.core.logger import logger
from azureml.studio.core.utils.strutils import to_camel_case

MAX_POST_TIMES = 3
SLEEP_DURATION = 3  # seconds
COMPONENT_NAME = "designer-module-execution"


class ModuleEvent:
    """
    Event to record required, standard and extension fields.

    See reference https://msdata.visualstudio.com/Vienna/_wiki/wikis/Vienna.wiki/4672/Common-Schema
    """

    def __init__(self, designer_event_name, **kwargs):
        run = Run.get_context()
        ws = run.experiment.workspace
        self._designer_event_name = designer_event_name
        self._required_fields = RequiredFields(
            workspace_id=ws._workspace_id,
            subscription_id=ws.subscription_id,
            component_name=COMPONENT_NAME,
        )

        # This try-except is for bug 1167635. When trying to get the parent of one run, the client will send async
        # request to create non-existed data types, which may trigger ErrorResponseException occasionally.
        try:
            parent_run_id = run.parent.id if run.parent else None
        except BaseException as err:
            logger.debug(f"Get parent run failed due to {err}")
            parent_run_id = None

        self._standard_fields = StandardFields(
            workspace_region=run.experiment.workspace.location,
            client_os=platform.system(),
            run_id=run.id,
            parent_run_id=parent_run_id
        )
        self.extension_fields = {**kwargs, 'designer_event_name': self._designer_event_name}

    @property
    def required_fields(self):
        return self._required_fields

    @property
    def standard_fields(self):
        return self._standard_fields

    @property
    def extension_fields(self):
        return self._extension_fields

    @extension_fields.setter
    def extension_fields(self, dct: dict):
        # Make the key string to camel format to be consistent with other fields.
        dct = {to_camel_case(k) if isinstance(k, str) else k: v for k, v in dct.items()}

        self._extension_fields = ExtensionFields(**dct)

    def to_dict(self):
        return {
            "RequiredFields": self.required_fields,
            "StandardFields": self.standard_fields,
            "ExtensionFields": self.extension_fields,
        }


class TelemetryLogger:
    """To log event using Geneva cold path."""
    service_endpoint = os.environ.get("AZUREML_SERVICE_ENDPOINT", "")
    experiment_scope = os.environ.get("AZUREML_EXPERIMENT_SCOPE", "")
    run_token = os.environ.get("AZUREML_RUN_TOKEN", "")

    def __init__(self):
        run = Run.get_context()
        self._telemetry_url = (
                self.service_endpoint + "/execution/v2.0" + self.experiment_scope + "/runs/" + run.id + "/telemetryV2")
        self._headers = self._get_headers()

    def log_event(self, event: ModuleEvent):
        # The size limit of event is between 70 KB and 134 KB. For event above size limit, event can be sent
        # successfully yet cannot be queried in kusto.
        # For kusto to display and parse, the event size limit is 32.768 KB.
        return try_request(
            url=self._telemetry_url,
            json_payload=event.to_dict(),
            headers=self._headers
        )

    def _get_headers(self):
        headers = {
            "Authorization": f"Bearer {self.run_token}",
            "Content-Type": "application/json"
        }
        return headers


class ModuleTelemetryHandler:
    """Handler to log event for telemetry usage."""

    def __init__(self):
        self._logger = TelemetryLogger()

    def log_telemetry(self, designer_event_name: str = None, **kwargs):
        event = ModuleEvent(designer_event_name, **kwargs)
        return self._logger.log_event(event)


def try_request(url, json_payload, headers):
    """Try to send request.

    It will sallow exceptions to avoid breaking callers.
    """
    for _ in range(MAX_POST_TIMES):
        resp = None
        try:
            resp = requests.post(url, json=json_payload, headers=headers)
            resp.raise_for_status()
            return
        except requests.exceptions.HTTPError as http_err:
            if resp:
                logger.warning(
                    f"Failed to send log with error {str(http_err)} response Code: {resp.status_code}, "
                    f"Content: {resp.content}. Detail: {traceback.format_exc()}"
                )
                if resp.status_code >= 500:
                    time.sleep(SLEEP_DURATION)
                    logger.debug("Retrying...")
                else:
                    return
            else:
                logger.warning(
                    f"Failed to send log with error {str(http_err)}"
                )

        except BaseException as exc:  # pylint: disable=broad-except
            logger.warning(f"Failed to send log: {json_payload} with error {exc}. Detail: {traceback.format_exc()}.")
            return
