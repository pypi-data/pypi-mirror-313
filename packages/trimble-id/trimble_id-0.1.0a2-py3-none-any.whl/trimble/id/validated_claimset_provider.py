import jwt
from trimble.id._constants import PACKAGE_NAME
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION

class ValidatedClaimsetProvider:
    """
    A claimset provider that returns a validated claimset
    """
    def __init__(self, jwk_provider, product_name = None):
        """
        Initialize ValidatedClaimsetProvider class

        :param jwk_provider: A provider for the keyset used to validate the JWT claimeset
        :param product_name: The product name of the consuming application
        """
        self._jwksProvider = jwk_provider
        self._keys = None
        self._version = VERSION

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_claimset(self, token):
        """
        Retrieves a validate claimset from a given JSON web token
        """

        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_claimset", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

        if self._keys == None:
            self._keys = await self._jwksProvider.retrieve_keys()        
        kid = jwt.get_unverified_header(token)['kid']
        if not kid in self._keys:
            self._keys = await self._jwksProvider.retrieve_keys()
            if not kid in self._keys:
                raise Exception('No matching key in JWKS')
        
        # It is important that you hardcode the algorithm and not use the value supplied in the JWT header
        # Don't validate the audience claim. Need to relook this necessity
        return jwt.decode(token, key=self._keys[kid], algorithms=['RS256'], options={'verify_aud': False}) 
