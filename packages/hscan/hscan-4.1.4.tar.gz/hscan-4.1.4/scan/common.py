import os
import platform
import sys
from pathlib import Path

from scan.log import get_logger


class ProjectInfo:
    ROOT_DIR_PATH = Path(__file__).parent
    DOCS_DIR_PATH = ROOT_DIR_PATH / "docs"

    is_linux = platform.system().lower() == "linux"
    is_macos = platform.system().lower() == "darwin"
    is_windows = platform.system().lower() == "windows"

    if is_linux:
        _ua_platform_id = "X11; Linux x86_64"
    elif is_macos:
        _ua_platform_id = "Macintosh; Intel Mac OS X 10_15_7"
    elif is_windows:
        _ua_platform_id = "Windows NT 10.0; Win64; x64"
    else:
        _ua_platform_id = "X11; Linux x86_64"
    default_user_agent = f"Mozilla/5.0 ({_ua_platform_id}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


class Settings:
    # dp 排队请求重试次数
    dp_request_wait_times = 100
    # dp 排队请求重试时间设置
    dp_wait_min_seconds = 1
    dp_wait_max_seconds = 2
    # dp 最大标签页
    dp_max_tabs_count = 4
    co_set_timeouts = 1


if ProjectInfo.is_windows:
    sn = "hscan"
else:
    try:
        file_path = os.path.abspath(sys.argv[0])
        sn = file_path.split("/")[-1].replace(".py", "")
    except:
        sn = "hscan"

logger = get_logger(sn)
