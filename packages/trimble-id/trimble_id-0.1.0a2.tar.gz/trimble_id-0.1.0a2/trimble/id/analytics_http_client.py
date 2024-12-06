from urllib.parse import urljoin
from enum import Enum
import requests
import uuid

class EventType(Enum):
    INIT = 1
    METHOD_USAGE = 2
    EXCEPTION = 3

class AnalyticsHttpClient:
    """
    A Http client for sending event hits to GA
    """

    _baseAddress = "https://www.google-analytics.com"
    _measurementID = "G-9DHNE789XG"
    _apiKey = "7wd60wEeSnufb8FK6naHOQ"
    _clientID = str(uuid.uuid4())

    @staticmethod
    def send_init_event(name, client_name = None, client_version = None, application_id = None, cid = None):
        """
        Send initialization events

        :param name: Name of an event
        :param client_name: Name of the client SDK
        :param client_version: Version of the client SDK
        :param cid: Client ID (optional)
        """
        params = { 
            "language": "python-sdk", 
            "client_name": client_name,
            "client_version": client_version,
            "event_type": EventType.INIT.name,
            "application_id": application_id
        }
        AnalyticsHttpClient.send_event(name+"_init", params, cid)

    @staticmethod
    def send_method_event(name, client_name = None, client_version = None, application_id = None, cid = None):
        """
        Send method events

        :param name: Name of an event
        :param client_name: Name of the client SDK
        :param client_version: Version of the client SDK
        :param cid: Client ID (optional)
        """
        params = { 
            "language": "python-sdk", 
            "client_name": client_name,
            "client_version": client_version,
            "event_type": EventType.METHOD_USAGE.name,
            "application_id": application_id
        }
        AnalyticsHttpClient.send_event(name+"_method", params, cid)
 
    @staticmethod
    def send_event(name, params, cid=None):
        """
        The method to send other type of events

        :param name: Name of an event
        :param params: Additional parameters of an event
        :param cid: Client ID (optional)
        """
        try:
            if cid == None:
                cid = AnalyticsHttpClient._clientID
            url = AnalyticsHttpClient._combineUrl(
                AnalyticsHttpClient._baseAddress, 
                f"/mp/collect?measurement_id={AnalyticsHttpClient._measurementID}&api_secret={AnalyticsHttpClient._apiKey}")
            headers = {
                'User-Agent':'TrimbleCloud.AnalyticsHttpClient/1.1.0',
                'Content-Type':'application/json'
                }
            data = {
                "client_id": cid,
                "events": [
                    {
                        "name": name,
                        "params": params
                    }
                ]
            }
            requests.post(url,headers=headers, json=data)
        except:
            pass

    def _combineUrl(baseAddress, url):
        return urljoin(baseAddress, url)

    def _combineHeaders(baseHeaders, headers):
        return {**baseHeaders, **headers}
