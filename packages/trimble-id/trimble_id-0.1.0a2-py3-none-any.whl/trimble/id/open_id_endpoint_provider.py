from trimble.id._constants import PACKAGE_NAME
from .http_client import HttpClient
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION 

class OpenIdEndpointProvider:
    """
    An endpoint provider that returns values from a OpenID well known configuration
    """
    def __init__(self, configuration_url, product_name = None):
        """
        Initialize OpenIdEndpointProvider class

        :param configurationUrl: The URL for the Trimble Identity OpenID well know configuration endpoint
        :param productName: Product name of consuming application
        """
        self._configurationUrl = configuration_url
        self._configuration = None

        self._version = VERSION

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
    
    async def retrieve_authorization_endpoint(self):
        """
        Retrieves authorization endpoint from a OpenID well known configuration
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_authorization_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

        if self._configuration is None:
            await self._load_configuration()
        return self._configuration['authorization_endpoint']

    async def retrieve_token_endpoint(self):
        """
        Retrieves token endpoint from a OpenID well known configuration
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_token_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

        if self._configuration is None:
            await self._load_configuration()
        return self._configuration['token_endpoint']

    async def retrieve_jwks_endpoint(self):
        """
        Retrieves JWKS endpoint from a OpenID well known configuration
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_jwks_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

        if self._configuration is None:
            await self._load_configuration()
        return self._configuration['jwks_uri']

    async def _load_configuration(self):
        client = HttpClient('', {})
        self._configuration = await client.get_json(self._configurationUrl, {})