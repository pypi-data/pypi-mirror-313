import asyncio
import logging

from trimble.id._constants import PACKAGE_NAME
from .http_client import HttpClient
from .http_client import HttpException
from .bearer_token_http_client_provider import BearerTokenHttpClientProvider
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION
import asyncio

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())

class RobustHttpClientProvider:
    """
    A HttpClient provider to make HTTP connections with protection against transient failures.
    """
    def __init__(self, http_client_provider, retries, backoff, product_name = None):
        """
        Initialize RobustHttpClientProvider class

        :param http_client_provider: A HttpClient provider for APIs using Bearer token authorization
        :param retries: The number of retries to attempt a failed request
        :param backoff: The amount of time to back off before a request retry
        :param product_name: The produce name of the consuming application
        """
        self._httpClientProvider = http_client_provider
        self._retries = retries
        self._backoff = backoff
        self._client = None
        self._version = VERSION

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_client(self):
        """
        Retrieves robust http client that helps to protect against transient failures.
        """

        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_client", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

        if not self._client:
            self._client = self._RobustHttpClient(
                self._httpClientProvider,
                self._retries,
                self._backoff,
            )

        return self._client

    class _RobustHttpClient:

        # retry for the following status codes
        # 408 Request timeout
        # 409 Conflict
        # 418 I'm a teapot
        # 429 Too many requests
        # 500 Internal server error
        # 502 Bad gateway
        # 503 Service unavailable
        # 504 Gateway timeout
        SUPPORTED_EXCEPTIONS = [408, 409, 418, 429, 500, 502, 503, 504]

        def __init__(self, httpClientProvider: BearerTokenHttpClientProvider, retries=3, backoff=5):
            self._httpClientProvider = httpClientProvider
            self._retries = retries
            self._backoff = backoff

        async def post(self, url, value=None, headers=None):
            """ Http post request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.post(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "POST %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "POST %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    _logger.warning(
                        "POST try %d of %d to %s failed with retryable exception",
                        retries,
                        self._retries,
                        url,
                        exc_info=ex,
                    )
                    await asyncio.sleep(self._backoff)

            _logger.error(
                "POST %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def get(self, url, headers=None):
            """ Http get request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.get(url, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "GET %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "GET %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "GET %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def put(self, url, value=None, headers=None):
            """ Http put request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.put(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "PUT %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "PUT %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "PUT %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def patch(self, url, value=None, headers=None):
            """ Http patch request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.patch(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "PATCH %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "PATCH %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "PATCH %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def delete(self, url, headers=None):
            """ delete Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.delete(url, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "DELETE %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "DELETE %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "DELETE %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def post_json(self, url, value=None, headers=None):
            """ postJSON Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.post_json(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "POST json %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "POST json %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "POST json %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def get_json(self, url, headers=None):
            """ getJSON Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.get_json(url, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "GET json %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "GET json %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "GET json %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def put_json(self, url, value=None, headers=None):
            """ put_json Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.put_json(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "PUT json %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "PUT json %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "PUT json %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException

        async def patch_json(self, url, value=None, headers=None):
            """ patch_json Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.patch_json(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "PATCH json %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "PATCH json %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "PATCH json %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException
        
        async def post_full_response(self, url, value=None, headers=None):
            """ post full response Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.post_full_response(url, value, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "POST full response %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "POST full response %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "POST full response %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException
        
        async def delete_full_response(self, url, headers=None):
            """ delete full response Http request """
            headers = headers if headers is not None else {}
            intitialException = None
            retries = -1
            for retries in range(self._retries):
                try:
                    _httpClient = await self._httpClientProvider.retrieve_client()
                    return await _httpClient.delete_full_response(url, headers)
                except HttpException as ex:
                    if ex.status not in self.SUPPORTED_EXCEPTIONS:
                        _logger.error(
                            "DELETE full response %s try %d raised an unsupported exception: %s",
                            url,
                            retries,
                            str(ex),
                            exc_info=ex,
                        )
                        raise
                    else:
                        _logger.info(
                            "DELETE full response %s try %d raised a supported exception %s",
                            url,
                            retries,
                            str(ex),
                        )

                    if not intitialException:
                        intitialException = ex

                    await asyncio.sleep(self._backoff)

            _logger.error(
                "DELETE full response %s giving up after try %d. Initial exception was %s",
                url,
                retries,
                str(intitialException),
            )
            raise intitialException