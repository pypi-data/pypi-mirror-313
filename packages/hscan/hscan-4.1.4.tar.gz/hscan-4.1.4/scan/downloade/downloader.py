import random
import httpx
import asyncio
import ssl
from httpx import ConnectError, ConnectTimeout, ProxyError, ReadTimeout, ReadError, UnsupportedProtocol
from curl_cffi import requests
from scan.response import Response
from scan.common import logger


class SSLFactory:
    ORIGIN_CIPHERS =['ECDHE+AESGCM', 'ECDHE+CHACHA20', 'DHE+AESGCM', 'DHE+CHACHA20', 'ECDH+AESGCM', 'DH+AESGCM',
                     'ECDH+AES', 'DH+AES', 'RSA+AESGCM', 'RSA+AES']

    def __init__(self):
        self.ciphers = self.ORIGIN_CIPHERS

    def __call__(self) -> ssl.SSLContext:
        random.shuffle(self.ciphers)
        ciphers = ":".join(self.ciphers)
        ciphers = ciphers + ":!aNULL:!eNULL:!MD5:!DSS"
        context = ssl.create_default_context()
        context.set_ciphers(ciphers)
        return context


class Downloader:
    def __init__(self):
        self.ssl_context = None
        self.client_dict = {}
        self.ssl_gen = SSLFactory()

    async def _session_client(self, verify, http2, proxies):
        if isinstance(proxies, dict):
            proxy = proxies.get('https://')
            if not proxy:
                proxy = proxies.get('http://')
            proxy = str(proxy)
        else:
            proxy = str(proxies)
        if proxy in self.client_dict:
            return self.client_dict[proxy]
        else:
            async with asyncio.Lock():
                client = httpx.AsyncClient(proxies=proxies, verify=verify, http2=http2,
                                           event_hooks={'response': [self.log_response]})
                self.client_dict[proxy] = client
                logger.debug(f'新建请求客户端,当前有{len(self.client_dict)}个客户端')
                return client

    @staticmethod
    async def generate_headers():
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

    async def close_session_client(self, proxies):
        if isinstance(proxies, dict):
            proxy = proxies.get('https://')
            if not proxy:
                proxy = proxies.get('http://')
            proxy = str(proxy)
        else:
            proxy = str(proxies)
        if proxy in self.client_dict:
            client = self.client_dict[proxy]
            await client.aclose()
            del self.client_dict[proxy]

    async def close_all(self):
        try:
            for proxy, client in self.client_dict.items():
                await client.aclose()
            self.client_dict.clear()
        except:
            pass

    @staticmethod
    async def log_request(request):
        pass

    @staticmethod
    async def log_response(response):
        """
        日志钩子
        """
        request = response.request
        if response.status_code not in [200, 301, 302]:
            logger.warning(f'{response.status_code}  {request.url}')
        else:
            logger.debug(f'{response.status_code}  {request.url}')

    async def tls_request(self, method, url, data=None, json=None, proxies=None):
        response = Response()
        try:
            if proxies:
                proxy = {'https': proxies.get('https://'), 'http': proxies.get('http://')}
            else:
                proxy = None
            resp = requests.request(method=method, url=url, data=data, json=json, impersonate="chrome101",
                                    proxies=proxy)
            await self.log_response(resp)
            response.response = resp
            response.ok = True
        except Exception as e:
            logger.error(f'tls request error: {e}')
        return response

    async def request(self, url, params=None, headers=None, cookies=None, auth=None, proxies=None, allow_redirects=True,
                      verify=True, http2=False, content=None, data=None, files=None, json=None, stream=False,
                      timeout=30, cycle=3, tls=False, session=True):
        if verify is True:
            verify = self.ssl_gen()
        if data or json or content:
            method = 'POST'
        else:
            method = 'GET'
        if not headers:
            headers = await self.generate_headers()
        if tls:
            return await self.tls_request(method=method, url=url, data=data, json=json, proxies=proxies)
        response = Response()
        response.request_url = url
        for _ in range(cycle):
            try:
                if session:
                    client = await self._session_client(verify, http2, proxies)
                    resp = await client.request(method=method, url=url, content=content, data=data, files=files,
                                                json=json, params=params, headers=headers, cookies=cookies,
                                                auth=auth, follow_redirects=allow_redirects, timeout=timeout)
                    response.response = resp
                    response.ok = True
                elif stream:
                    client = httpx.AsyncClient(proxies=proxies, event_hooks={'response': [self.log_response]},
                                               verify=verify, http2=http2, follow_redirects=allow_redirects)
                    request = client.build_request(method=method, url=url, headers=headers, cookies=cookies,
                                                   content=content, data=data, files=files, json=json, timeout=timeout)
                    resp = await client.send(request, stream=True)
                    response.response = resp
                    response.ok = True
                    response.client = client  # need aclose
                else:
                    async with httpx.AsyncClient(proxies=proxies, event_hooks={'response': [self.log_response]},
                                                 verify=verify, http2=http2) as client:
                        resp = await client.request(
                            method=method, url=url, content=content, data=data, files=files, json=json, params=params,
                            headers=headers, cookies=cookies, auth=auth, follow_redirects=allow_redirects,
                            timeout=timeout
                        )
                        response.response = resp
                        response.ok = True
                # if resp.status_code == 403:
                #     return await self.tls_request(method=method, url=url, data=data, json=json, proxies=proxies)
                return response
            except ConnectError as e:
                response.message = 'ConnectError'
                logger.error(f'Failed to request {url}  ConnectError:{e}')
            except ConnectTimeout as e:
                response.message = 'ConnectTimeout'
                logger.error(f'Failed to request {url}  ConnectTimeout:{e}')
            except ProxyError as e:
                response.message = 'ProxyError'
                logger.error(f'Failed to request {url}  ProxyError:{e}')
            except ReadTimeout as e:
                response.message = 'ReadTimeout'
                logger.error(f'Failed to request {url}  ReadTimeout:{e}')
            except ReadError as e:
                response.message = 'ReadError'
                logger.error(f'Failed to request {url}  ReadError:{e}')
            except UnsupportedProtocol as e:
                response.message = 'UnsupportedProtocol'
                logger.error(f'Failed to request {url}  UnsupportedProtocol:{e}')
            except Exception as e:
                response.message = e
                logger.error(f'Failed to request {url}  {e}')
        return response
