import base64
from datetime import datetime, timedelta
import json
import urllib

from trimble.id._constants import PACKAGE_NAME
from .http_client import HttpClient
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION

class ClientCredentialTokenProvider:
    """
    A token provider based on the OAuth Client Credential grant type
    """
    def __init__(self, endpoint_provider, client_id, client_secret, product_name=None):
        """
        Initialize ClientCredentialTokenProvider class

        :param endpoint_provider: An endpoint provider that provides the URL for the Trimble Identity token endpoint
        :param client_id: The consumer key for the calling application
        :param client_secret: The consumer secret of the calling application
        :param product_name: Product name of consuming application (optional)
        """
        self._endpointProvider = endpoint_provider
        self._consumerKey = client_id
        self._consumerSecret = client_secret
        self._scopes = None
        self._tokenExpiry = datetime.min
        self._accessToken = None
        self._version = VERSION
        self._productName = product_name

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version,
            application_id=self._consumerKey)

    def with_scopes(self, scopes):
        """
        A method for adding scopes

        :params scopes: The requested scopes of calling application
        """
        self._scopes = scopes
        return self

    async def retrieve_token(self):
        """
        Retrieves an access token for the application

        :return: access token for the given application
        """

        AnalyticsHttpClient.send_method_event(
              name="retrieve_token_method", 
              client_name=PACKAGE_NAME, 
              client_version=self._version, 
              application_id=self._consumerKey)
       
        if self._tokenExpiry < datetime.utcnow():
            await self._refresh_token()
        return self._accessToken

    async def _refresh_token(self):
        tokenEndpoint = await self._endpointProvider.retrieve_token_endpoint()
        client = HttpClient('', {})
        basicAuthorizationValue = base64.b64encode(f'{self._consumerKey}:{self._consumerSecret}'.encode('ascii')).decode('ascii')
        parameters = {
            'grant_type': 'client_credentials'
        }
        if self._scopes is not None:
            parameters['scope'] = ' '.join(self._scopes)
        result = await client.post(
            tokenEndpoint,
            urllib.parse.urlencode(parameters),
            {
                'authorization': f'Basic {basicAuthorizationValue}',
                'content-type': 'application/x-www-form-urlencoded',
                'accept': 'application/json',
                'user-agent': f"{PACKAGE_NAME}/{self._version} python-sdk {self._productName}"
            }
        )
        jsonResult = json.loads(result)
        self._tokenExpiry = datetime.utcnow() + timedelta(0, jsonResult['expires_in'])
        self._accessToken = jsonResult['access_token']
