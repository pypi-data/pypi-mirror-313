from trimble.id._constants import PACKAGE_NAME
from .http_client import HttpClient
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION

class BearerTokenHttpClientProvider:
    """
    A HttpClient provider for APIs using Bearer token authorization
    """
    def __init__(self, token_provider, base_address, default_headers = {}, product_name=None):
        """
        Initialize Bearer token http client provider

        :param token_provider: A token provider that provides the access token for the authenticated application or user
        :param base_address: The base address for the API that will be called
        :param default_headers: If any default address to be applied in Http request call. (Optional)
        :param product_name: Specify product name of consuming application (optional)
        """
        self._tokenProvider = token_provider
        self._baseAddress = base_address
        self._defaultHeaders = default_headers
        self._version = VERSION
        self._consumerKey = self.retrieve_consumer_key()

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version,
            application_id=self._consumerKey)

    async def retrieve_client(self):
        """
        Retrieves a preconfigured HttpClient to access a given API

        :return: A preconfigured HttpClient to access any given API
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_client", 
            client_name=PACKAGE_NAME, 
            client_version=self._version,
            application_id=self._consumerKey)
        
        token = await self._tokenProvider.retrieve_token()
        
        if 'trimblepaas.com' in self._baseAddress:
            url = self._baseAddress + 'api/'
        else:
            url = self._baseAddress

        url = self._add_trailing_slash(url)

        return HttpClient(url, { **self._defaultHeaders, **{ 'authorization': 'Bearer ' + token } })

    def _add_trailing_slash(self, url):
        if url.endswith('/'):
            return url
        return url + '/'
    
    def retrieve_consumer_key(self):
        if (self._tokenProvider != None) : 
            return self._tokenProvider._consumerKey
        return None
    
