import requests
import json
import time
import logging
import pkg_resources


from typing import Dict, Any

from requests import Response
from http import HTTPStatus

GUARDIAN_CLIENT_SDK_VERSION = pkg_resources.get_distribution("guardian-client").version

from guardian_client.python.credentials import GuardianClientCredentialContext


class GuardianAPIClient:
    """
    Client for Guardian API
    """

    def __init__(
        self,
        base_url: str,
        scan_endpoint: str = "scans",
        api_version: str = "v1",
        log_level: str = "INFO",
    ) -> None:
        """
        Initializes the Guardian API client.
        Args:
            base_url (str): The base URL of the Guardian API.
            scan_endpoint (str, optional): The endpoint for scanning. Defaults to "scans".
            api_version (str, optional): The API version. Defaults to "v1".
            log_level (str, optional): The log level. Defaults to "INFO".
        Raises:
            ValueError: If the log level is not one of "DEBUG", "INFO", "ERROR", or "CRITICAL".
        """
        self.endpoint = f"{base_url.rstrip('/')}/{api_version}/{scan_endpoint}"
        log_string_to_level = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        log_level_enum = log_string_to_level.get(log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level_enum,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # client credential context is tied to a client instance.
        # In it's current state, a new client instance is created on each new call
        # to the guardian scanner, so a new context (and consequently a token)
        # is created for each scan request.
        self._access_token_context = GuardianClientCredentialContext(
            guardian_endpoint=base_url
        )

    def scan(self, model_uri: str, poll_interval_secs: int = 5) -> Dict[str, Any]:
        """
        Submits a scan request for the given URI and polls for the scan status until it is completed.

        Args:
            uri (str): The URI to be scanned.
            poll_interval_secs (int, optional): The interval in seconds to poll for the scan status.
                If <= 0, the function returns immediately after submitting the scan. Defaults to 5.

        Returns:
            dict: A dictionary containing the HTTP status code and the scan status JSON.
                  If an error occurs during the scan submission or polling, the dictionary
                  will also contain the error details.
        """
        if not model_uri:
            logging.error("Model URI is required")
            return {
                "http_status_code": None,
                "error": "Model URI is required",
            }

        logging.info(f"Submitting scan for {model_uri}")

        headers = {
            "Authorization": f"Bearer {self._access_token_context.access_token}",
            "User-Agent": f"guardian-sdk/{GUARDIAN_CLIENT_SDK_VERSION}",
        }
        response = requests.post(
            self.endpoint,
            json={"model_uri": model_uri},
            headers=headers,
        )
        if response.status_code != HTTPStatus.ACCEPTED:
            return {
                "http_status_code": response.status_code,
                "error": self._decode_error(response),
            }

        logging.info(
            f"Scan submitted successfully for {model_uri} with status_code: {response.status_code}"
        )

        if poll_interval_secs <= 0:
            return {
                "http_status_code": response.status_code,
                "scan_status_json": response.json(),
            }

        response_json = response.json()
        id = response_json["uuid"]

        # Polling
        scan_status_json = None
        status_response = None

        logging.info(f"Polling for scan outcome for {id} for {model_uri}")
        while True:
            # reload header to check if token is still valid during this processing.
            headers = {
                "Authorization": f"Bearer {self._access_token_context.access_token}",
                "User-Agent": f"guardian-sdk/{GUARDIAN_CLIENT_SDK_VERSION}",
            }

            status_response = requests.get(
                url=f"{self.endpoint}/{id}",
                headers=headers,
            )
            if status_response.status_code == HTTPStatus.OK:
                scan_status_json = status_response.json()
                if scan_status_json["aggregate_eval_outcome"] != "PENDING":
                    break
            else:
                return {
                    "http_status_code": status_response.status_code,
                    "error": self._decode_error(status_response),
                }

            logging.debug(
                f"Scan outcome for {id} is {scan_status_json['aggregate_eval_outcome']}. Sleeping for 5 seconds before next check"
            )
            time.sleep(poll_interval_secs)  # Wait for 5 seconds before next check

        logging.info(f"Scan complete for {id} for {model_uri}")

        return {
            "http_status_code": (
                status_response.status_code if status_response else None
            ),
            "scan_status_json": scan_status_json,
        }

    def get_scan(self, scan_uuid: str) -> Dict[str, Any]:
        """
        Retrieves the scan results for a given past scan.

        Args:
            scan_uuid (str): The ID of the scan to retrieve.

        Returns:
            dict: A dictionary containing the HTTP status code and the scan status JSON.
                  If an error occurred during the scan, the dictionary
                  will contain the error details instead of the scan status.
        """
        if not scan_uuid:
            logging.error("Scan UUID is required")
            return {
                "http_status_code": None,
                "error": "Scan UUID is required",
            }

        logging.info(f"Retrieving scan ID {scan_uuid}")

        # reload header to check if token is still valid during this processing.
        headers = {
            "Authorization": f"Bearer {self._access_token_context.access_token}",
            "User-Agent": f"guardian-sdk/{GUARDIAN_CLIENT_SDK_VERSION}",
        }

        status_response = requests.get(
            url=f"{self.endpoint}/{scan_uuid}",
            headers=headers,
        )
        if status_response.status_code == HTTPStatus.OK:
            scan_status_json = status_response.json()
            return {
                "http_status_code": (
                    status_response.status_code if status_response else None
                ),
                "scan_status_json": scan_status_json,
            }
        else:
            return {
                "http_status_code": status_response.status_code,
                "error": self._decode_error(status_response),
            }

    def _decode_error(self, response: Response) -> str:
        try:
            response_json = response.json()
            if "detail" in response_json and response_json["detail"]:
                if isinstance(response_json["detail"], list):
                    concat_msg = ""
                    for item_ in response_json["detail"]:
                        concat_msg += f"- {item_['msg']}\n"
                    return concat_msg
                elif isinstance(response_json["detail"], str):
                    return response_json["detail"]

            return "Unknown error"
        except json.JSONDecodeError:
            return "Response is not in JSON format"
