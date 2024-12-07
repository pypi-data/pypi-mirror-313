import asyncio
import aiohttp
from aiohttp import ClientTimeout

from scan.response import Response
from scan.common import logger


class Downloader:
    def __init__(self):
        self.session = None

    @staticmethod
    async def gen_headers():
        return {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }

    @staticmethod
    async def log_response(response):
        request = response.request_info
        if response.status not in [200, 301, 302]:
            logger.warning(f'{response.status}  {request.url}')
        else:
            logger.debug(f'{response.status}  {request.url}')

    async def request(self, url, params=None, headers=None, cookies=None, auth=None, proxies=None, allow_redirects=True,
                      verify=True, http2=False, content=None, data=None, files=None, json=None, stream=False,
                      timeout=30, cycle=3, tls=False, session=True):
        if not self.session:
            async with asyncio.Lock():
                self.session = aiohttp.ClientSession(timeout=ClientTimeout(timeout))
        if data or json or content:
            method = 'POST'
        else:
            method = 'GET'
        if not headers:
            headers = await self.gen_headers()
        if proxies and isinstance(proxies, dict):
            proxies = list(proxies.values())[0]
        response = Response()
        response.request_url = url
        for _ in range(cycle):
            try:
                resp = await self.session.request(method=method, url=url, data=data, json=json, params=params,
                                                  headers=headers, cookies=cookies, proxy=proxies, auth=auth,
                                                  allow_redirects=allow_redirects)
                await self.log_response(resp)
                content = await resp.read()
                resp.__setattr__('status_code', resp.status)
                resp.__setattr__('content', content)
                response.response = resp
                return response
            except Exception as e:
                response.message = e
                logger.error(f'Failed to request {url}  {e}')
        return response
