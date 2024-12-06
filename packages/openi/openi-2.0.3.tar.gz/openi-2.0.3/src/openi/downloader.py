from pathlib import Path
from typing import Literal, Optional, Union

from ._dataclass import DatasetFile, ModelFile
from ._exceptions import KeyboardInterruptError, OpenIError, ServerFileNotFoundError, validate_openi_args
from ._file import CacheFile, split_subdir_name
from ._tqdm import FileProgressBar, create_pbar
from .api import OpenIApi
from .constants import DEFAULT_SAVE_PATH, UPLOAD_TYPE
from .log import setup_logger

logger = setup_logger()


def single_file_downloader(
    api: OpenIApi,
    src_file: Union[DatasetFile, ModelFile],
    filename: str,
    filesize: int,
    filepath: Path,
    pbar: Optional[FileProgressBar] = None,
) -> Optional[Union[BaseException, OpenIError]]:
    """Download a file from the OpenI platform using tqdm.

    Args:
        api (OpenIApi):
            The OpenI API instance.
        src_file (Union[DatasetFile, ModelFile]):
            The dataset or model file to download.
        filename (str):
            The name of the file to download.
        filesize (int):
            The size of the file to download.
        filepath (Path):
            The path to save the downloaded file.
        pbar (Optional[FileProgressBar], optional):
            The progress bar to display. Defaults to None.

    Returns:
        bool: Whether the download was successful.

    Raises:
        Exception: If an error occurs during the download.
    """

    err: Optional[Union[BaseException, OpenIError]] = None

    if pbar is None:
        pbar: FileProgressBar = create_pbar(
            display_name=filename,
            size=filesize,
        )

    try:
        pbar.downloading()

        for data in api.download_file_iterator(
            src_file=src_file,
            filepath=filepath,
        ):
            pbar.update(data)

        if pbar.n == filesize:
            pbar.completed()

    except KeyboardInterrupt:
        pbar.failed()
        err = KeyboardInterruptError(
            "文件下载未完成，缓存内容已保存; 再次下载到相同路径时，文件将会被断点续传",
        )

    except Exception as e:
        pbar.failed()
        err = e

    finally:
        pbar.refresh()
        pbar.close()

    return err


@validate_openi_args
def download_file(
    repo_id: str,
    file: str,
    cluster: Literal["gpu", "npu"] = "npu",
    save_path: Union[Path, str] = None,
    force: bool = False,
    token: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> Optional[Path]:
    """Download a dataset file

    Args:
        file (str): The name of the file to download.
        repo_id (str): The ID of the repository to download from.
        cluster (Literal["gpu", "npu"], optional): The cluster to download from. Defaults to "npu".
        save_path (Union[Path, str], optional): The path to save the downloaded file. Defaults to DEFAULT_SAVE_PATH.
        force (bool, optional): Whether to force download the file. Defaults to False.
        token (Optional[str], optional): The OpenI API token. Defaults to None.
        endpoint (Optional[str], optional): The OpenI API endpoint. Defaults to None.

    Returns:
        Optional[Path]: The path to the downloaded file if successfully downloaded.

    Raises:
        ServerFileNotFoundError: If the file is not found in the dataset.
    """
    api = OpenIApi(token=token, endpoint=endpoint)

    upload_type = UPLOAD_TYPE.get(cluster.lower())

    dataset_file = api.query_dataset_file(
        repo_id=repo_id,
        filename=file,
        upload_type=upload_type,
    )
    if not dataset_file:
        dataset_url = api.get_dataset_url(repo_id=repo_id)
        raise ServerFileNotFoundError(
            f"`{file}` 数据集文件不存在 ; 请在网页端查看: {dataset_url}",
        )

    if not save_path:
        save_path = DEFAULT_SAVE_PATH
    cache_file: CacheFile = CacheFile(
        name=dataset_file.name,
        size=dataset_file.size,
        save_path=save_path,
        force=force,
    )

    err = single_file_downloader(
        api=api,
        src_file=dataset_file,
        filename=cache_file.name,
        filesize=cache_file.size,
        filepath=cache_file.cache_path,
    )

    api.close()

    if err is not None:
        raise err

    completed = cache_file.as_completed()
    if completed:
        print(f"文件已下载到: {cache_file.file_path}")
        return cache_file.file_path
    else:
        print(f"文件下载出错，请使用 `force=True` 参数重新下载")
        return None


@validate_openi_args
def download_model_file(
    repo_id: str,
    model_name: str,
    file: str,
    save_path: Union[Path, str] = None,
    force: bool = False,
    token: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> Optional[Path]:
    """Download a model file.

    Args:
        file (str):
            The name of the file to download.
        repo_id (str):
            The ID of the repository to download from.
        model_name (str):
            The name of the model to download from.
        save_path (Union[Path, str], optional):
            The path to save the downloaded file. Defaults to DEFAULT_SAVE_PATH.
        force (bool, optional):
            Whether to force download the file. Defaults to False.
        token (Optional[str], optional):
            The OpenI API token. Defaults to None.
        endpoint (Optional[str], optional):
            The OpenI API endpoint. Defaults to None.

    Returns:
        Optional[Path]: The path to the downloaded file if successfully downloaded.

    Raises:
        ServerFileNotFoundError: If the file is not found in the model.
    """
    api = OpenIApi(token=token, endpoint=endpoint)

    filename = file.lstrip("/")
    model_file = api.query_model_file(
        filename=filename,
        repo_id=repo_id,
        model_name=model_name,
    )
    if not model_file:
        model_url = api.get_model_url(repo_id=repo_id, model_name=model_name)
        raise ServerFileNotFoundError(
            f" `{model_name}` 模型内未找到 `{file}` 文件; 请在网页端查看: {model_url}",
        )

    if not save_path:
        save_path = DEFAULT_SAVE_PATH

    if not isinstance(save_path, Path):
        save_path = Path(save_path)

    subdir, filename = split_subdir_name(model_file.FileName)
    save_path = save_path / subdir

    cache_file: CacheFile = CacheFile(
        name=filename,
        size=model_file.Size,
        save_path=save_path,
        force=force,
    )

    err = single_file_downloader(
        api=api,
        src_file=model_file,
        filename=cache_file.name,
        filesize=cache_file.size,
        filepath=cache_file.cache_path,
    )

    api.close()

    if err is not None:
        raise err

    completed = cache_file.as_completed()
    if completed:
        print(f"文件已下载到: {cache_file.file_path}")
        return cache_file.file_path
    else:
        print(f"文件下载出错，请使用 `force=True` 参数重新下载")
        return None


@validate_openi_args
def download_model(
    repo_id: str,
    model_name: str,
    save_path: Optional[Union[Path, str]] = None,
    force: bool = False,
    token: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> Optional[Path]:
    """Download an entire model.

    Args:
        repo_id (str):
            The ID of the repository to download from.
        model_name (str):
            The name of the model to download.
        save_path (Union[Path, str], optional):
            The path to save the downloaded file. Defaults to DEFAULT_SAVE_PATH.
        force (bool, optional):
            Whether to force download the file. Defaults to False.
        token (Optional[str], optional):
            The OpenI API token. Defaults to None.
        endpoint (Optional[str], optional):
            The OpenI API endpoint. Defaults to None.

    Returns:
        Optional[Path]: The path to the downloaded file if successfully downloaded.
    """
    api = OpenIApi(token=token, endpoint=endpoint)

    model_file_list = api.list_model_files(
        repo_id=repo_id,
        model_name=model_name,
    )
    if not model_file_list:
        model_url = api.get_model_url(repo_id=repo_id, model_name=model_name)
        raise ServerFileNotFoundError(
            f"模型 `{model_name}` 内无任何文件; 请在网页端查看: {model_url}",
        )

    if not save_path:
        save_path = DEFAULT_SAVE_PATH / model_name

    if not isinstance(save_path, Path):
        save_path = Path(save_path)

    model_file_list.sort(key=lambda x: x.Size)
    pbar_list = list()
    cache_file_list = list()
    for pos, f in enumerate(model_file_list):
        subdir, filename = split_subdir_name(f.FileName)
        file_save_path = save_path / subdir

        cache_file: CacheFile = CacheFile(
            name=filename,
            size=f.Size,
            save_path=file_save_path,
            force=force,
        )
        cache_file_list.append(cache_file)

        pbar: FileProgressBar = create_pbar(
            display_name=f.FileName,
            size=cache_file.size,
            position=pos,
        )
        pbar_list.append(pbar)

    completed_count = 0
    raise_err = None
    for model_file, cache_file, pbar in zip(
        model_file_list,
        cache_file_list,
        pbar_list,
    ):
        if cache_file.file_path.exists():
            cache_file.cache_path.unlink(missing_ok=True)
            pbar.update(cache_file.size)
            pbar.completed()
            pbar.close()
            completed_count += 1
            continue

        err = single_file_downloader(
            api=api,
            src_file=model_file,
            filename=cache_file.name,
            filesize=cache_file.size,
            filepath=cache_file.cache_path,
            pbar=pbar,
        )
        if err is not None:
            raise_err = err
        if isinstance(err, KeyboardInterruptError):
            api.close()
            raise err
        else:
            completed = cache_file.as_completed(rename_existing=False)
            if completed:
                completed_count += 1

    api.close()

    # close_all_pbar(pbar_list)
    if completed_count == len(model_file_list):
        print(f"\n模型 `{model_name}` 已成功下载到: {save_path}")
        return save_path
    else:
        print(f"\n{raise_err}; 模型下载出错，请重新下载")
        return None
