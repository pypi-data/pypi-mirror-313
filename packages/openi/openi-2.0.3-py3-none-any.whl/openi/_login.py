import json
import os
import re
from typing import Optional

from pwinput import pwinput
from requests.exceptions import ConnectionError, ProxyError

from ._exceptions import UnauthorizedError
from .api import OpenIApi, UserInfo
from .constants import DEFAULT_BASE_URL, OPENI_LOGO_ASCII, TOKEN_FILE_PATH, TOKEN_REGEX


def _display_token_input_box(endpoint: str) -> str:
    """Display the token input prompt

    Args:
        endpoint (str): OpenI server endpoint

    Returns:
        str: input token
    """
    print(OPENI_LOGO_ASCII)
    print(f"点击链接获取令牌并复制粘贴到下列输入栏 {endpoint}/user/settings/applications \n")
    print(
        f"[WARNING] 若本机已保存登录令牌，本次输入的令牌会将其覆盖 \n",
        "          建议使用鼠标右键粘贴，避免输入多余字符\n",
    )
    return pwinput(prompt="  🔒 token: ")


def _save_token(endpoint: str, token: str, username: str) -> None:
    """Save the token to local machine

    Args:
        endpoint (str): OpenI server endpoint
        token (str): access_token
    """
    TOKEN_FILE_PATH.write_text(json.dumps({"endpoint": endpoint, "token": token}))
    print(f"\nYour token was saved to `{TOKEN_FILE_PATH}`")
    print(f"Successfully log in as `{username}` @{endpoint}!\n")


def _bad_token(token: str) -> None:
    if not re.match(TOKEN_REGEX, token):
        print(f"\n❌ 输入的令牌格式有误！\n")
        exit(1)


def _invalid_token(token: str) -> None:
    print(f"\n❌ 登陆失败！此令牌无效 `{token}`\n")


def _bad_network() -> None:
    print("\n❌ 登陆失败！请检查网络或代理设置\n")


def login(token: Optional[str] = None, endpoint: Optional[str] = DEFAULT_BASE_URL):
    """Login to OpenI on local machine

    For the first time use, you need to provide the token and endpoint.
    Will first check with the provided token and endpoint, if valid, save it to local machine
    on `/home/.openi/token.json` and print out the success message.
    If there is a saved token on local machine, will be replaced by the new one.

    Args:
        token (`str`):
            access_token for basic auth, if not provided, will prompt for input
        endpoint (`str`):
            Base URL for OpenI server, default to `https://openi.pcl.ac.cn`

    Examples:
        >>> from openi import login
        >>> login()
        ...
          🔒 token: *******
        Your token was saved to `/home/.openi/token.json`
        successfully logged in as `your_username` @ https://openi.pcl.ac.cn

        >>> login()
        ...
          🔒 token: *******
        登陆失败，请检查网络或令牌是否有效

        >>> login(token="your_token", endpoint="http://xxx.xxx.xxx.xx:8000")
        ...
        Your token was saved to `/home/.openi/token.json`
        successfully logged in as `your_username` @ http://xxx.xxx.xxx.xx:8000


    """

    endpoint = endpoint.rstrip("/")
    token = _display_token_input_box(endpoint) if token is None else token

    _bad_token(token)

    try:
        api = OpenIApi(token=token, endpoint=endpoint)
        username = api.get_user_info().username

    except UnauthorizedError as e:
        _invalid_token(token)

    except ConnectionError or ProxyError as e:
        _bad_network()

    except Exception as e:
        print(e)

    else:
        _save_token(endpoint, token, username)


def whoami_cli() -> None:
    """Print out current log in username and endpoint"""
    _ = whoami(display=True)


def whoami(display: bool = True) -> UserInfo:
    """Return username logged in on local machine, no print out message

    Args:
        display (`bool`):
            Default to `True`, either print out `{username}@{url}` message or not.

    Returns:
        `UserInfo`:
            UserInfo class of detailed user info
    """
    api = OpenIApi()
    user = api.get_user_info()
    if display:
        print(f"`{user.username}` @{api.session.endpoint}")
    return user


def logout():
    """Remove the token saved on local machine"""
    try:
        TOKEN_FILE_PATH.unlink()
        OPENI_TOKEN = os.environ.get("OPENI_TOKEN", None)
        if OPENI_TOKEN:
            del os.environ["OPENI_TOKEN"]

    except FileNotFoundError:
        print("You are not logged in yet!")
    else:
        print(f"Successfully logged out!")
