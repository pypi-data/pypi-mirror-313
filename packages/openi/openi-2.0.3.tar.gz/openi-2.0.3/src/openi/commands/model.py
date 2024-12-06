from argparse import SUPPRESS, Namespace, _SubParsersAction
from pathlib import Path
from typing import Optional

from openi.commands import BaseOpeniCLICommand

from .._exceptions import LocalPathNotFound
from ..downloader import download_model, download_model_file
from ..log import setup_logger
from ..uploader import upload_model, upload_model_file

logger = setup_logger()


class ModelCommands(BaseOpeniCLICommand):
    @staticmethod
    def register_subcommand(parser: _SubParsersAction):
        """
        model command
        """
        parser_model = parser.add_parser(
            "model",
            help="{upload,download} 上传/下载启智AI协作平台的模型",
            description="上传/下载启智AI协作平台的模型",
            aliases=["m"],
        )
        parser_model._action_groups.pop()
        subparsers_model = parser_model.add_subparsers(
            title="commands",
            dest="commands",
        )
        subparsers_model.required = True

        # Add subcommand
        DownloadCommand.register_subcommand(subparsers_model)
        UploadCommand.register_subcommand(subparsers_model)


class BaseModelCommand:
    def __init__(self, args):
        self.args = args


class DownloadCommand(BaseModelCommand):
    @staticmethod
    def register_subcommand(subparsers_model):
        """
        download subcommand
        """
        download_parser = subparsers_model.add_parser(
            "download",
            help="下载模型, openi model download -h 查看更多说明",
            usage="openi model download REPO_ID MODEL_NAME  [--filename FILENAME] [--save_path PATH] [--force]",
            description="下载模型或模型文件，需指定仓库路径及模型名称，下载公开模型无需登录",
        )
        download_parser._action_groups.pop()

        """
        arguments
        """
        download_parser_args = download_parser.add_argument_group("arguments")
        download_parser_args.add_argument(
            "repo_id",
            help="所在仓库路径，格式为`拥有者/仓库名`，用户需要拥有此仓库权限；可在网页端一键复制",
        )
        download_parser_args.add_argument(
            "model_name",
            help="网页端模型名称，可在网页端一键复制；注意区分大小写，否则无法找到模型",
        )

        """
        optional arguments
        """
        download_parser_optional_args = download_parser.add_argument_group("optional arguments")
        download_parser_optional_args.add_argument(
            "-f",
            "--filename",
            dest="filename",
            metavar="",
            required=False,
            help="选填: 指定下载模型中的某个文件，不填写此参数则会下载模型内所有文件",
        )
        download_parser_optional_args.add_argument(
            "-p",
            "--save_path",
            dest="save_path",
            metavar="",
            required=False,
            help="选填: 指定本地的保存目录，默认为当前目录；若下载整个模型，则会在当前目录默认创建 `模型名称` 文件夹",
        )
        download_parser_optional_args.add_argument(
            "--force",
            dest="force",
            action="store_true",
            required=False,
            help="选填: 添加此参数将删除本地的缓存与同名文件，强行重新下载文件",
        )
        download_parser_optional_args.add_argument(
            "-t",
            "--token",
            dest="token",
            required=False,
            help=SUPPRESS,
        )
        download_parser_optional_args.add_argument(
            "-e",
            "--endpoint",
            dest="endpoint",
            required=False,
            help=SUPPRESS,
        )
        download_parser.set_defaults(func=lambda args: DownloadCommand(args))

    def __init__(self, args: Namespace) -> None:
        self.repo_id: str = args.repo_id
        self.model_name: str = args.model_name

        self.filename: Optional[str] = args.filename
        self.save_path: Optional[str] = args.save_path
        self.force: bool = args.force

        self.token: Optional[str] = args.token
        self.endpoint: Optional[str] = args.endpoint

    def run(self):
        if self.filename is not None:
            download_model_file(
                file=self.filename,
                repo_id=self.repo_id,
                model_name=self.model_name,
                save_path=self.save_path,
                force=self.force,
                token=self.token,
                endpoint=self.endpoint,
            )
        else:
            download_model(
                repo_id=self.repo_id,
                model_name=self.model_name,
                save_path=self.save_path,
                force=self.force,
                token=self.token,
                endpoint=self.endpoint,
            )


class UploadCommand(BaseModelCommand):
    @staticmethod
    def register_subcommand(subparsers_model):
        """
        upload subcommand
        """
        upload_parser = subparsers_model.add_parser(
            "upload",
            help="上传模型, openi model upload -h 查看更多说明",
            usage="openi model upload REPO_ID MODEL_NAME FILE_PATH [--upload_name FILENAME]",
            description="上传本地模型或模型文件，需指定仓库路径、模型名称及本地路径",
        )
        upload_parser._action_groups.pop()

        """
        arguments
        """
        upload_parser_args = upload_parser.add_argument_group("arguments")
        upload_parser_args.add_argument(
            "repo_id",
            help="所在仓库路径，格式为`拥有者/仓库名`，用户需要拥有此仓库权限；可在网页端一键复制",
        )
        upload_parser_args.add_argument(
            "model_name",
            help="网页端模型名称，可在网页端一键复制；注意区分大小写，否则无法找到模型",
        )
        upload_parser_args.add_argument(
            "file_path",
            help="本地路径，可传入`本地文件`或`本地文件夹`路径；上传`文件夹`时将包含所有文件与子目录文件",
        )

        """
        optional arguments
        """
        upload_parser_optional_args = upload_parser.add_argument_group("optional arguments")
        upload_parser_optional_args.add_argument(
            "-n",
            "--upload_name",
            dest="upload_name",
            metavar="",
            required=False,
            help="选填: 自定义上传文件名，当上传`文件夹`时，本参数失效",
        )
        upload_parser_optional_args.add_argument(
            "-t",
            "--token",
            dest="token",
            required=False,
            help=SUPPRESS,
        )
        upload_parser_optional_args.add_argument(
            "-e",
            "--endpoint",
            dest="endpoint",
            required=False,
            help=SUPPRESS,
        )
        upload_parser.set_defaults(func=lambda args: UploadCommand(args))

    def __init__(self, args: Namespace) -> None:
        self.repo_id: str = args.repo_id
        self.model_name: str = args.model_name
        self.file_path: Path = Path(args.file_path).absolute()

        self.upload_name: Optional[str] = args.upload_name
        self.token: Optional[str] = args.token
        self.endpoint: Optional[str] = args.endpoint

    def run(self):
        if not self.file_path.exists():
            raise LocalPathNotFound(self.file_path)

        if self.file_path.is_dir():
            upload_model(
                folder=self.file_path,
                repo_id=self.repo_id,
                model_name=self.model_name,
                token=self.token,
                endpoint=self.endpoint,
            )
        else:
            upload_model_file(
                file=self.file_path,
                repo_id=self.repo_id,
                model_name=self.model_name,
                upload_name=self.upload_name,
                token=self.token,
                endpoint=self.endpoint,
            )
