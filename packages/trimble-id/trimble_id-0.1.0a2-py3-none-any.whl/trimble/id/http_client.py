import aiohttp
import json
from urllib.parse import urljoin

from .http_exception import HttpException


class HttpClient:
    def __init__(self, base_address, default_headers):
        self._baseAddress = base_address
        self._defaultHeaders = default_headers

    async def post(self, url, value=None, headers={}):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers),
                data=value
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())

                return await response.text()

    async def get(self, url, headers={}):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers)
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())

                return await response.text()

    async def put(self, url, value=None, headers={}):
        async with aiohttp.ClientSession() as session:
            async with session.put(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers),
                data=value
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())

                return await response.text()

    async def patch(self, url, value=None, headers={}):
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers),
                data=value
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())

                return await response.text()

    async def delete(self, url, headers={}):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers)
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())

                return await response.text()

    async def post_json(self, url, value=None, headers={}):
        result = await self.post(
            url,
            None if value is None else json.dumps(value),
            self._combine_headers(
                {"accept": "application/json", "content-type": "application/json"},
                headers
            )
        )
        return json.loads(result)

    async def get_json(self, url, headers={}):
        result = await self.get(
            url, self._combine_headers({"accept": "application/json"}, headers)
        )
        return json.loads(result)

    async def put_json(self, url, value=None, headers={}):
        result = await self.put(
            url,
            None if value is None else json.dumps(value),
            self._combine_headers(
                {"accept": "application/json", "content-type": "application/json"},
                headers
            )
        )
        return json.loads(result)

    async def patch_json(self, url, value=None, headers={}):
        result = await self.patch(
            url,
            None if value is None else json.dumps(value),
            self._combine_headers(
                {"accept": "application/json", "content-type": "application/json"},
                headers
            )
        )
        return json.loads(result)
    
    async def post_full_response(self, url, value=None, headers={}):
        async with aiohttp.ClientSession() as session:
            if value is not None:
                value = json.dumps(value)
                headers = self._combine_headers(
                    {"accept": "application/json", "content-type": "application/json"},
                    headers
                )
            async with session.post(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers),
                data=value
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())
                
                response_text = await response.text()
                return (json.loads(response_text), response)
            
    async def delete_full_response(self, url, headers={}):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                self._combine_url(self._baseAddress, url),
                headers=self._combine_headers(self._defaultHeaders, headers)
            ) as response:
                if response.status >= 400:
                    raise HttpException(response.status, await response.text())
                
                return response

    def _combine_url(self, baseAddress, url):
        return urljoin(baseAddress, url)

    def _combine_headers(self, baseHeaders, headers):
        return {**baseHeaders, **headers}
