from argparse import SUPPRESS, Namespace, _SubParsersAction
from pathlib import Path
from typing import Optional

from openi.commands import BaseOpeniCLICommand

from .._exceptions import LocalPathNotFound
from ..constants import DEFAULT_SAVE_PATH
from ..downloader import download_file
from ..log import setup_logger
from ..uploader import upload_file

logger = setup_logger()


class DatasetCommands(BaseOpeniCLICommand):
    @staticmethod
    def register_subcommand(parser: _SubParsersAction):
        """
        dataset command
        """
        parser_dataset = parser.add_parser(
            "dataset",
            help="{upload,download} 上传/下载启智AI协作平台的数据集",
            description="上传/下载启智AI协作平台的数据集",
            aliases=["d"],
        )
        parser_dataset._action_groups.pop()
        subparsers_dataset = parser_dataset.add_subparsers(
            title="commands",
            dest="commands",
        )
        subparsers_dataset.required = True

        # Add subcommand
        DownloadCommand.register_subcommand(subparsers_dataset)
        UploadCommand.register_subcommand(subparsers_dataset)


class BaseDatasetCommand:
    def __init__(self, args):
        self.args = args


class DownloadCommand(BaseDatasetCommand):
    @staticmethod
    def register_subcommand(subparsers_dataset):
        """
        download subcommand
        """
        download_parser = subparsers_dataset.add_parser(
            "download",
            help="下载数据集, openi dataset download -h 查看更多说明",
            usage="openi dataset download REPO_ID FILENAME [--cluster CLUSTER] [--save_path PATH] [--force]",
            description="下载数据集，需指定仓库路径及文件，下载公开数据集无需登录",
        )
        download_parser._action_groups.pop()

        """
        arguments
        """
        download_parser_args = download_parser.add_argument_group("arguments")
        download_parser_args.add_argument(
            "repo_id",
            help="所在仓库路径，格式为`拥有者/仓库名`，用户需要拥有此仓库权限",
        )
        download_parser_args.add_argument(
            "filename",
            help="数据集文件名称",
        )

        """
        optional arguments
        """
        download_parser_optional_args = download_parser.add_argument_group("optional arguments")
        download_parser_optional_args.add_argument(
            "-c",
            "--cluster",
            dest="cluster",
            metavar="",
            required=False,
            default="npu",
            help="选填: 指定数据集文件存储类型，可填写`npu` 或 `gpu`; 默认 `npu`",
        )
        download_parser_optional_args.add_argument(
            "-p",
            "--save_path",
            dest="save_path",
            metavar="",
            default=DEFAULT_SAVE_PATH,
            required=False,
            help="选填: 指定本地的保存目录，默认为当前目录",
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
        self.filename: str = args.filename

        self.cluster: str = args.cluster
        self.save_path: Optional[str] = args.save_path
        self.force: bool = args.force

        self.token: Optional[str] = args.token
        self.endpoint: Optional[str] = args.endpoint

    def run(self):
        download_file(
            repo_id=self.repo_id,
            file=self.filename,
            cluster=self.cluster,
            save_path=self.save_path,
            force=self.force,
            token=self.token,
            endpoint=self.endpoint,
        )


class UploadCommand(BaseDatasetCommand):
    @staticmethod
    def register_subcommand(subparsers_dataset):
        """
        upload subcommand
        """
        upload_parser = subparsers_dataset.add_parser(
            "upload",
            help="上传数据集, openi dataset upload -h 查看更多说明",
            usage="openi dataset upload REPO_ID FILE_PATH",
            description="上传数据集，需指定仓库路径、本地路径",
        )
        upload_parser._action_groups.pop()

        """
        arguments
        """
        upload_parser_args = upload_parser.add_argument_group("arguments")
        upload_parser_args.add_argument(
            "repo_id",
            help="所在仓库路径，格式为`拥有者/仓库名`，用户需要拥有此仓库权限",
        )
        upload_parser_args.add_argument(
            "file_path",
            help="本地路径，可传入`本地文件`路径；若传入`本地目录`，将自动打包成zip文件并上传",
        )

        """
        optional arguments
        """
        upload_parser_optional_args = upload_parser.add_argument_group("optional arguments")
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
        self.file_path: Path = Path(args.file_path).absolute()

        self.token: Optional[str] = args.token
        self.endpoint: Optional[str] = args.endpoint

    def run(self):
        if not self.file_path.exists():
            raise LocalPathNotFound(self.file_path)

        upload_file(
            file=self.file_path,
            repo_id=self.repo_id,
            token=self.token,
            endpoint=self.endpoint,
        )
