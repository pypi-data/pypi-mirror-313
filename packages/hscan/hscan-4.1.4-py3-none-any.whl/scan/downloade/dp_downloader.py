from threading import Lock
from typing import Literal, NamedTuple, Optional, Union

from DrissionPage import ChromiumOptions, ChromiumPage
from tenacity import retry, retry_if_result, stop_after_attempt, wait_random

from scan.common import ProjectInfo, Settings, logger
from scan.response import Response


def create_retry_decorator():
    """用于解决 retry 无法动态设置重试参数的问题"""
    max_attempts = int(Settings.dp_request_wait_times)

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_random(
            min=Settings.dp_wait_min_seconds, max=Settings.dp_wait_max_seconds
        ),
        retry=retry_if_result(lambda x: any([x.response.err_msg == "too many tabs"])),
    )


class DrissionpageResponse(NamedTuple):
    content: Optional[bytes] = None
    status_code: Optional[int] = None
    text: Optional[str] = None
    cookies: Optional[dict] = None
    err_msg: Optional[str] = None
    url: Optional[str] = None


class DrissionpageSingletonMeta(type):
    _instance = None
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class DrissionpageDownloader(metaclass=DrissionpageSingletonMeta):
    def __init__(self):
        self.page = None
        self.driver = None

    def create_dp(
        self,
        headless: bool = True,
        user_agent: str = ProjectInfo.default_user_agent,
        no_imgs: bool = False,
        proxy: Optional[str] = None,
        browser_path: Optional[str] = None,
        local_port: int = 9222,
    ):
        if browser_path is None:
            co = ChromiumOptions()
        else:
            co = ChromiumOptions(browser_path)
        co.set_timeouts(base=Settings.co_set_timeouts)
        if local_port:
            co.set_local_port(local_port)
        co.set_argument("--no-sandbox")
        if no_imgs:
            co.no_imgs(True)
        if headless:
            co.headless(True)
        if user_agent:
            co.set_user_agent(user_agent)

        turnstile_extension_path = ProjectInfo.DOCS_DIR_PATH / "turnstilePatch"
        proxy_switch_extension_path = (
            ProjectInfo.DOCS_DIR_PATH / "proxy_switchyomega-2.5.20"
        )
        co.add_extension(turnstile_extension_path)
        co.add_extension(proxy_switch_extension_path)
        if proxy:
            co.set_proxy(proxy)
        self.driver = ChromiumPage(addr_or_opts=co)

    def connect_dp(self, local_port: int = 9222):
        self.driver = ChromiumPage(addr_or_opts=local_port)

    def switch_ip(self, ip_port=None):
        if ip_port:
            # 设置代理
            ip, port = ip_port.split(":")
            tab = self.driver.new_tab()
            tab.get(
                "chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy"
            )
            tab.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(
                ip, clear=True
            )
            tab.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(
                port, clear=True
            )
            tab.ele('x://a[@ng-click="applyOptions()"]').click()
            tab.close()

            # 开启代理
            tab = self.driver.new_tab()
            tab.get(
                "chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#"
            )
            tab.ele('x://span[text()="proxy"]').click()
            tab.close()
        else:
            # 直接连接
            tab = self.driver.new_tab()
            tab.get(
                "chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#"
            )
            tab.ele('x://span[text()="[直接连接]" or text()="[Direct]"]').click()
            tab.close()

    def turnstile(self, url, headers=None, is_cloudflare=False):
        if headers:
            self.page.set.headers(headers=headers)
        self.page.get(url=url)
        if is_cloudflare:
            for i in range(25):
                try:
                    curr_title = self.page.title
                    if all(
                        ["just a moment" not in curr_title.lower(), "请稍候" not in curr_title, "لحظات" not in curr_title]
                    ):
                        break

                    challengeSolution = self.page.ele("@name=cf-turnstile-response")
                    challengeWrapper = challengeSolution.parent()
                    challengeIframe = challengeWrapper.shadow_root.ele("tag:iframe")
                    challengeIframeBody = challengeIframe.ele("tag:body").shadow_root
                    challengeButton = challengeIframeBody.ele("tag:input")
                    challengeButton.click()
                except Exception as e:
                    # 这里会因为没有找到元素而报错，不用管，元素可能还没有渲染出来，遍历查询即可
                    pass

        content = self.page.html
        cookie = self.get_cookie()
        self.page.close()
        return content, cookie

    def get_cookie(self) -> dict:
        return self.page.cookies

    def request(
        self,
        url,
        headers=None,
        proxies: Optional[Union[str, Literal[False]]] = None,
        timeout=30,
        retry=1,
        show_errmsg=False,
        interval=2,
        session=True,
        load_mode="normal",
        clear_cache=False,
        is_cloudflare=False,
        connect_dp=True,
    ):
        @create_retry_decorator()
        def inner_request():
            if connect_dp:
                if ProjectInfo.is_windows:
                    self.create_dp()
                else:
                    try:
                        self.connect_dp()
                    except Exception as e:
                        self.create_dp()

            response = Response()
            response.request_url = url
            response.response = DrissionpageResponse(
                err_msg="too many tabs",
                url=url,
            )
            tabs_count = self.driver.tabs_count
            if tabs_count >= Settings.dp_max_tabs_count:
                logger.info(f"标签页超过 {Settings.dp_max_tabs_count} 个，重试等待中。")
                return response

            if proxies:
                self.switch_ip(proxies)
            # 当关闭代理时配置直接连接
            if proxies is False:
                self.switch_ip()

            self.page = self.driver.new_tab()
            if load_mode == "none":
                self.page.set.load_mode.none()
            elif load_mode == "eager":
                self.page.set.load_mode.eager()
            if clear_cache:
                self.clear_cache(cache=True, cookies=False)
            content, cookies = self.turnstile(
                url=url, headers=headers, is_cloudflare=is_cloudflare
            )
            response.response = DrissionpageResponse(
                content=bytes(content, encoding="utf-8"),
                status_code=200,
                text=content,
                cookies=cookies,
                url=url,
            )
            return response

        return inner_request()

    def close_dp(self):
        if self.driver:
            self.driver.quit(force=False)
            logger.info("DrissionPage closed")

    def clear_cache(self, cache=True, cookies=True):
        if self.driver:
            self.driver.clear_cache(cache, cookies)
