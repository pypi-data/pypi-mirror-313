import copy
import os
from pathlib import Path
from typing import BinaryIO, Dict, Literal, Optional, Union

from tqdm.auto import tqdm

from openi import OpenIApi
from openi.adaptor.om_hub.utils import om_raise_for_status, split_repo_id


def try_to_load_from_cache(
    repo_id: str,
    filename: str,
    cache_dir: Union[str, Path, None] = None,
    revision: Optional[str] = None,
    **kwargs,
) -> Union[str, None]:
    if not cache_dir:
        cache_dir = Path.cwd()
    file_path = os.path.join(cache_dir, filename)
    if os.path.exists(file_path):
        return file_path
    return


def om_hub_url(
    repo_id: str,
    filename: str,
    token: Optional[str] = None,
    **kwargs,
) -> None:
    try:
        openi_repo_id, openi_model_name = split_repo_id(repo_id)
        api = OpenIApi(token=token)
        return api.get_model_file_download_url(
            repo_id=openi_repo_id,
            model_name=openi_model_name,
            filename=filename,
        )

    except (BaseException, Exception) as e:
        raise e


import requests

from openi.constants import DOWNLOAD_RATES


def http_get(
    url: str,
    temp_file: BinaryIO,
    token: Optional[str] = None,
    proxies: Optional[Dict] = None,
    resume_size: float = 0,
    headers: Optional[Dict[str, str]] = None,
    displayed_filename: Optional[str] = None,
    **kwargs,
) -> None:
    initial_headers = headers
    headers = copy.deepcopy(headers) or {}
    if resume_size > 0:
        headers["Range"] = "bytes=%d-" % (resume_size,)

    r = requests.get(url=url, allow_redirects=True, stream=True, headers=headers)
    om_raise_for_status(r)
    content_length = r.headers.get("Content-Length")

    total = resume_size + int(content_length) if content_length is not None else None

    with tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        total=total,
        initial=resume_size,
        desc=displayed_filename,
        disable=None,
    ) as progress:
        new_resume_size = resume_size
        try:
            for chunk in r.iter_content(chunk_size=DOWNLOAD_RATES):
                if chunk:
                    progress.update(len(chunk))
                    temp_file.write(chunk)
                    new_resume_size += len(chunk)

        except (BaseException, Exception) as e:
            raise e


from openi.downloader import download_file, download_model_file


def om_hub_download(
    repo_id: str,
    filename: str,
    token: Optional[str] = None,
    local_dir: Optional[Union[str, Path]] = None,
    force_download: Optional[bool] = False,
    repo_type: Literal["dataset", "model"] = "model",
    **kwargs,
) -> Path:
    try:
        if repo_type == "dataset":
            cluster = kwargs.get("cluster", "npu")

            return download_file(
                repo_id=repo_id,
                file=filename,
                save_path=local_dir,
                force=force_download,
                cluster=cluster,
                token=token,
            )
        else:
            openi_repo_id, openi_model_name = split_repo_id(repo_id)

            return download_model_file(
                repo_id=openi_repo_id,
                model_name=openi_model_name,
                file=filename,
                save_path=local_dir,
                force=force_download,
                token=token,
            )

    except (BaseException, Exception) as e:
        raise e


from openi.downloader import download_model


def snapshot_download(
    repo_id: str,
    token: Optional[str] = None,
    local_dir: Optional[Union[str, Path]] = None,
    force_download: Optional[bool] = False,
    **kwargs,
) -> None:
    try:
        openi_repo_id, openi_model_name = split_repo_id(repo_id)

        return download_model(
            repo_id=openi_repo_id,
            model_name=openi_model_name,
            save_path=local_dir,
            force=force_download,
            token=token,
        )

    except (BaseException, Exception) as e:
        raise e
