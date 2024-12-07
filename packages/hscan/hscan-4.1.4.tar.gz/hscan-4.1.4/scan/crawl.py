from typing import (TYPE_CHECKING, Any, AsyncIterable, Iterable, Literal,
                    Optional, Union)

from scan.common import ProjectInfo, logger
from scan.downloade.aiohttp_downloader import Downloader as AioHttpDownloader
from scan.downloade.downloader import Downloader
from scan.downloade.dp_downloader import DrissionpageDownloader

if TYPE_CHECKING:
    from http.cookiejar import CookieJar

    RequestContent = Union[str, bytes, Iterable[bytes], AsyncIterable[bytes]]


class Crawl:
    def __init__(self):
        self.downloader = Downloader()
        self.aiohttp_downloader = AioHttpDownloader()
        self.dp_downloader = None

    async def fetch(self,  url, params=None, data=None, files=None, json=None, content=None, headers=None, cookies=None,
                    verify=True, http2=False, auth=None, proxies=None, allow_redirects=True, stream=False,
                    session=False, timeout=30, cycle=1, tls=False, use_aiohttp=False):
        if use_aiohttp:
            res = await self.aiohttp_downloader.request(
                url, params=params, data=data, files=files, json=json, content=content, headers=headers,
                proxies=proxies,
                verify=verify, http2=http2, cookies=cookies, auth=auth, allow_redirects=allow_redirects,
                timeout=timeout,
                cycle=cycle, stream=stream, tls=tls, session=session
            )
        else:
            res = await self.downloader.request(
                url, params=params, data=data, files=files, json=json, content=content, headers=headers,
                proxies=proxies, verify=verify, http2=http2, cookies=cookies, auth=auth,
                allow_redirects=allow_redirects, timeout=timeout, cycle=cycle, stream=stream, tls=tls, session=session
            )
        return res

    def create_dp(
        self,
        headless: bool = True,
        user_agent: str = ProjectInfo.default_user_agent,
        no_imgs: bool = False,
        browser_path: Optional[str] = None,
        proxy: Optional[str] = None,
        local_port: int = 9222,
    ):
        self.dp_downloader = DrissionpageDownloader()
        self.dp_downloader.create_dp(
            headless=headless,
            user_agent=user_agent,
            no_imgs=no_imgs,
            proxy=proxy,
            browser_path=browser_path,
            local_port=local_port,
        )
        logger.info("DrissionPage created")

    def open(
        self,
        url: str,
        params: Optional[dict] = None,
        data: Union[dict, str] = None,
        files: Any = None,
        json: Union[dict, str] = None,
        content: "RequestContent" = None,
        headers: Optional[dict] = None,
        cookies: Union[dict, "CookieJar"] = None,
        verify: bool = True,
        http2: bool = False,
        auth: Any = None,
        proxies: Optional[Union[str, Literal[False]]] = None,
        allow_redirects: bool = True,
        stream: bool = False,
        session=False,
        timeout: Optional[Union[int, float]] = None,
        cycle: int = 1,
        tls: bool = False,
        use_aiohttp: bool = False,
        show_errmsg: bool = False,
        interval: Union[int, float] = 2,
        hooks: Any = None,
        load_mode: Literal["normal", "eager", "none"] = "normal",
        clear_cache: bool = False,
        is_cloudflare: bool = False,
        connect_dp: bool = True,
    ):
        if not self.dp_downloader:
            logger.info("未先使用 crawl.creat_dp 创建 DrissionPage，将使用默认设置！")
            self.dp_downloader = DrissionpageDownloader()
            self.dp_downloader.create_dp()

        res = self.dp_downloader.request(
            url=url,
            headers=headers,
            proxies=proxies,
            timeout=timeout,
            retry=cycle,
            show_errmsg=show_errmsg,
            interval=interval,
            load_mode=load_mode,
            clear_cache=clear_cache,
            is_cloudflare=is_cloudflare,
            connect_dp=connect_dp,
        )
        return res

    def close_dp(self):
        self.dp_downloader.close_dp()

    def clear_dp_cache(self, cache=True, cookies=True):
        self.dp_downloader.clear_cache(cache, cookies)

    async def close(self):
        await self.downloader.close_all()


crawl: Crawl = Crawl()
__all__ = crawl
