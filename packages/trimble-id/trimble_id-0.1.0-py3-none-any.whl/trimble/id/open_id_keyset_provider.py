import json
import jwt
from .analytics_http_client import AnalyticsHttpClient

from trimble.id._constants import PACKAGE_NAME
from .http_client import HttpClient
from ._version import VERSION

class OpenIdKeySetProvider:
    """
    A keyset provider based on the OAuth well known configuration
    """
    def __init__(self, endpoint_provider, product_name = None):
        """
        Initialize OpenIdKeySetProvider class

        :param endpoint_provider: An endpoint provider that provides the URL for the Trimble Identity JSON web keyset endpoint
        :param product_name: Product name of the consuming application
        """
        self._endpointProvider = endpoint_provider

        self._version = VERSION

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_keys(self):
        """
        Retrieves an dictionary of named keys
        """

        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_keys", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

        client = HttpClient('', {})
        result = await client.get_json(await self._endpointProvider.retrieve_jwks_endpoint(), {})
        self._keys = {}
        for jwk in result['keys']:
            kid = jwk['kid']
            self._keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        return self._keys