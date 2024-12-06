from trimble.id._constants import PACKAGE_NAME
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION

class FixedEndpointProvider:
    """
    An endpoint provider that returns fixed OAuth endpoints
    """
    def __init__(
            self, 
            authorization_endpoint, 
            token_endpoint, 
            userinfo_endpoint, 
            token_revocation_endpoint = None, 
            jwks_endpoint = None, 
            product_name = None):
        """
        Initialize FixedEndpointProvider class

        :param authorization_endpoint: Set Authorization Endpoint
        :param token_endpoint: Set Token Endpoint
        :param userinfo_endpoint: Set UserInfo Endpoint
        :param token_revocation_endpoint: Set Token revocation Endpoint
        :param jwks_endpoint: Set JSON Web key set Endpoint
        :param product_name: Product name of the consuming application (optional)
        """
        self._authorizationEndpoint = authorization_endpoint
        self._tokenEndpoint = token_endpoint
        self._userInfoEndpoint = userinfo_endpoint
        self._tokenRevocationEndpoint = token_revocation_endpoint
        self._jwksEndpoint = jwks_endpoint
        self._version = VERSION

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_authorization_endpoint(self):
        """
        Retrieves a fixed Authorization endpoint
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_authorization_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._authorizationEndpoint

    async def retrieve_token_endpoint(self):
        """
        Retrieves a fixed Token endpoint
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_token_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._tokenEndpoint

    async def retrieve_json_web_keyset_endpoint(self):
        """
        Retrieves a fixed JSON Web key set endpoint
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_json_web_keyset_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._jwksEndpoint