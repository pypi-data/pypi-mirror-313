import re
from functools import wraps
from inspect import signature
from pathlib import Path
from typing import Callable, Type, TypeVar

from .constants import REPO_ID_REGEX
from .log import setup_logger

logger = setup_logger("info")


class TokenNotFoundWarn(Warning):
    def __init__(self):
        self.message = (
            "未找到本地 token；若遇到提示 PageNotFound 或 UnauthorizedError，"
            "则需要使用 `login` 保存启智账户 token 到本地以获取授权。"
        )

    def __str__(self):
        return repr(self.message)


class OpenIError(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "❌ " + self.msg

    def __repr__(self):
        return "❌ " + self.msg


class ServerError(OpenIError):
    def __init__(self, status_code: int):
        self.msg = f"{status_code} OpenI服务器暂时不可用，请联系社区管理员或稍后再试"


class HttpProxyError(OpenIError):
    def __init__(self):
        self.msg = "无法发送请求，请检查网络代理"


class HttpConnectionError(OpenIError):
    def __init__(self):
        self.msg = "无法连接网络，请检查网络设置"


class InvalidTokenError(OpenIError):
    def __init__(self):
        self.msg = f"Invalid or broken OpenI token."


class TokenNotFoundError(OpenIError):
    def __init__(self):
        token_help_doc_url = "https://openi.pcl.ac.cn/docs/index.html#/api/token"
        self.msg = f"未找到本地 token；请先使用 `openi login` 保存启智账户 token 到本地以获取授权。具体使用方法请参考: {token_help_doc_url}"


class UnauthorizedError(OpenIError):
    def __init__(self, status_code: int = 401):
        self.msg = f"{status_code} 您无权建立此连接。请确保您拥有对应的权限。"


class PageNotFound(OpenIError):
    def __init__(self):
        self.msg = "无效请求，请确保仓库路径填写正确并且您拥有对应的权限"


class ParamsTypeError(OpenIError):
    def __init__(
        self,
        arg_name: str,
        arg_value: any,
        accepted_type: Type[any],
    ):
        self.msg = f"`{arg_name}` 参数类型错误 {type(arg_value)}: `{arg_value}`. " f"正确的参数类型为 {accepted_type}"


class RepoIdError(OpenIError):
    def __init__(self, repo_id):
        self.msg = f"`{repo_id}` 参数格式错误. 正确的 `repo_id` 参数格式应为: `用户名/仓库名`"


class RepoNotFoundError(OpenIError):
    def __init__(self, repo_id):
        self.msg = f"仓库不存在: `{repo_id}`"


class RepoExistsError(OpenIError):
    def __init__(self, repo_id):
        self.msg = f"仓库已存在: `{repo_id}`，请勿重复创建"


class KeyboardInterruptError(OpenIError):
    def __init__(self, msg):
        self.msg = f"用户中断操作; {msg}"


class DatasetNotFound(OpenIError):
    def __init__(self, repo_id, dataset_url):
        self.msg = f"`{repo_id}` 仓库尚未创建数据集: {dataset_url}"


class EmptyDataset(OpenIError):
    def __init__(self, repo_id, dataset_url):
        self.msg = f"`{repo_id}` 仓库数据集内未找到任何文件: {dataset_url}"


class ModelCreateError(OpenIError):
    def __init__(self, model_name, msg):
        self.msg = f" `{model_name}` 模型创建失败: {msg}"


class ModelNotFoundError(OpenIError):
    def __init__(self, model_name, model_list_url):
        self.msg = f"模型不存在 `{model_name}`; 请在网页端查看正确模型名称: {model_list_url}"


class ServerFileExistsError(OpenIError):
    def __init__(
        self,
        filename: str,
        existing_filename: str,
        existing_repo_id: str = None,
    ):
        if existing_repo_id:
            self.msg = (
                f"`{filename}` 该文件已被上传为 {existing_repo_id} 仓库中的 `{existing_filename}` 文件, 无法重复上传"
            )
        else:
            self.msg = f"`{filename}` 文件已上传, 无法重复上传"


class ServerFileNotFoundError(OpenIError):
    def __init__(self, msg):
        self.msg = msg


class EmptyFolderError(OpenIError):
    def __init__(self, local_dir: Path):
        self.msg = f"空目录，未能找到任何本地文件: {local_dir.absolute()}"


class LocalPathNotFound(OpenIError):
    def __init__(self, filepath: Path):
        self.msg = f"本地文件或目录不存在: {filepath.absolute()}"


class LocalDirNotFound(OpenIError):
    def __init__(self, local_dir: Path):
        self.msg = f"本地目录不存在: {local_dir.absolute()}"


class FileTypeError(OpenIError):
    def __init__(self, filepath: Path):
        self.msg = f"非压缩文件(`.zip` 或 `.tar.gz`): {filepath.absolute()}"


class FileSizeError(OpenIError):
    def __init__(self, msg):
        self.msg = msg


class PutUploadError(OpenIError):
    def __init__(self, msg):
        self.msg = msg


class UploadError(OpenIError):
    def __init__(self, msg):
        self.msg = msg


CallableT = TypeVar("CallableT", bound=Callable)


def validate_openi_args(fn: CallableT) -> CallableT:
    """Decorator that retrieves and prints all input arguments of a function.

    Args:
        fn: The function to be decorated.

    Returns:
        A wrapper function that prints arguments and calls the original function.
    """

    @wraps(fn)
    def _inner_fn(*args, **kwargs):
        params = signature(fn).parameters
        arg_names = [param.name for param in params.values()]

        _kwargs = dict()

        for i, arg_name in enumerate(arg_names):
            if i < len(args):
                value = args[i]
            else:
                value = kwargs.get(arg_name, None)
            _kwargs.update({arg_name: value})

        repo_id = _kwargs.get("repo_id", None)
        if not repo_id or not isinstance(repo_id, str):
            raise ParamsTypeError(
                arg_name="repo_id",
                arg_value=repo_id,
                accepted_type=str,
            )
        if not re.match(REPO_ID_REGEX, repo_id):
            raise RepoIdError(
                repo_id=repo_id,
            )

        filename = _kwargs.get("file", None)
        if filename and not isinstance(filename, (Path, str)):
            raise ParamsTypeError(
                arg_name="file",
                arg_value=filename,
                accepted_type="either a pathlib.Path() object or str",
            )

        cluster = _kwargs.get("cluster", None)
        if cluster and (not isinstance(cluster, str) or cluster.lower() not in ["gpu", "npu"]):
            raise ParamsTypeError(
                arg_name="cluster",
                arg_value=cluster,
                accepted_type="['gpu', 'npu'] case insensitive",
            )

        save_path = _kwargs.get("save_path", None)
        if save_path and not isinstance(save_path, (Path, str)):
            raise ParamsTypeError(
                arg_name="save_path",
                arg_value=save_path,
                accepted_type="either a pathlib.Path() object or str",
            )

        force = _kwargs.get("force", None)
        if force and not isinstance(force, bool):
            raise ParamsTypeError(
                arg_name="force",
                arg_value=force,
                accepted_type=bool,
            )

        model_name = _kwargs.get("model_name", None)
        if model_name and not isinstance(model_name, str):
            raise ParamsTypeError(
                arg_name="model_name",
                arg_value=model_name,
                accepted_type=str,
            )

        upload_name = _kwargs.get("upload_name", None)
        if upload_name and not isinstance(upload_name, str):
            raise ParamsTypeError(
                arg_name="upload_name",
                arg_value=upload_name,
                accepted_type=str,
            )

        folder = _kwargs.get("folder", None)
        if folder and not isinstance(folder, (Path, str)):
            raise ParamsTypeError(
                arg_name="folder",
                arg_value=folder,
                accepted_type=str,
            )

        return fn(*args, **kwargs)

    return _inner_fn
