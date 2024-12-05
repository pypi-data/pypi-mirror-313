import logging
import time

import requests

from ml3_platform_sdk.core.enums import HTTPMethod

logger = logging.getLogger("ML3_PLATFORM_SDK")
logging.basicConfig(level=logging.INFO)


class Connection:
    """
    This class
    """

    initialized: bool = False

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self._headers = {"X-Api-Key": self.api_key}
        self.initialized = len(url) > 0 and len(api_key) > 0

    def _get_url(self, path):
        """
        Private method to build the url
        of the API request
        """
        return "/sdk/v1".join([self.url, path])

    def send_api_request(
        self,
        method: HTTPMethod,
        path: str,
        timeout: int,
        max_retries: int = 5,
        retry_delay: float = 10.0,
        **kwargs,
    ) -> requests.Response:
        """
        Helper method to send an API request

        parameters:
        ----------
        method:         The HTTP method to use
        path:           The path of the API request
        timeout:        The timeout of the request
        max_retries:    The maximum number of retries in case of requests.exceptions.ConnectionError or requests.exceptions.Timeout
        retry_delay:    The delay between retries in case of requests.exceptions.ConnectionError or requests.exceptions.Timeout

        returns:
        --------
        requests.Response: The response of the HTTP request

        raises:
        -------
        requests.exceptions.ConnectionError: In case of connection error
        requests.exceptions.Timeout: In case of timeout
        """
        if max_retries < 1:
            raise ValueError(
                f"max_retries must be greater or equal to 1. Got {max_retries}"
            )
        response = requests.Response()
        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method=str(method.value),
                    url=self._get_url(path),
                    headers=self._headers,
                    timeout=timeout,
                    **kwargs,
                )
                return response
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as e:
                if attempt == max_retries - 1:
                    logger.info(
                        f"Failed to send request after {max_retries} attempts"
                    )
                    logger.info(e)
                    raise e
                else:
                    logger.info(
                        f"Failed to send request. Retrying attempt {attempt+1}/{max_retries} in {retry_delay} seconds"
                    )
                    logger.info(e)
                    time.sleep(retry_delay)
        return response

    @staticmethod
    def send_data(presigned_url: dict, data_path: str):
        """
        Send file using a presigned URL
        """

        with open(data_path, "rb") as file:
            files = {"file": file}

            # FIXME consider timeouts
            response = requests.post(  # pylint: disable=W3101
                presigned_url["url"], data=presigned_url["fields"], files=files
            )

            return response
