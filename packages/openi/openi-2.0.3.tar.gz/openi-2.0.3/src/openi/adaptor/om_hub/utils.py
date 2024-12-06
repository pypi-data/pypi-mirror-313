from typing import Optional, Tuple

from openi._exceptions import RepoIdError


def split_repo_id(repo_id: str) -> Tuple[str, str]:
    """
    Split a repo_id into OpenI format of tuple(username/reponame,modelname)
    """
    names = repo_id.split("/")

    if len(names) == 3:
        return "/".join(names[:-1]), names[-1]

    if len(names) == 2:
        return repo_id, names[-1]

    raise RepoIdError(repo_id)


from openi._session import OpenISession


def build_om_headers(token: str, headers: Optional[dict] = None, **kwargs) -> None:
    sess = OpenISession()
    sess.set_basic_auth(token=token, endpoint=None)

    return sess._build_token_headers(headers=headers)


import requests

from openi._exceptions import PageNotFound, ServerError, TokenNotFoundError, UnauthorizedError
from openi.constants import TOKEN_FILE_PATH


def om_raise_for_status(response: requests.Response, **kwargs) -> None:
    status_code = response.status_code
    auth = TOKEN_FILE_PATH.exists()

    if status_code in [401, 403, 404]:
        if status_code == 404 and not auth:
            raise TokenNotFoundError()
        if status_code == 404:
            raise PageNotFound()
        else:
            raise UnauthorizedError(status_code)

    if status_code in [500, 502]:
        raise ServerError()
