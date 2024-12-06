from trimble.id._constants import PACKAGE_NAME
from .analytics_http_client import AnalyticsHttpClient
from ._version import VERSION

class FixedKeySetProvider:
    """
    A keyset provider that returns a fixed keyset
    """
    def __init__(self, keyset, product_name = None):      
        """
        Initialize FixedKeySetProvider class

        :param keyset: A dictionary of named keys
        :param product_name: Product name of consuming application
        """  
        self._keyset = keyset

        self._version = VERSION

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_keyset(self):
        """
        Retrieves a dictionary of named keys

        :return: Fixed Keyset
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_keyset", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._keyset