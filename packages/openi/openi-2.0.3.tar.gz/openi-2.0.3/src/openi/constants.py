from pathlib import Path
from typing import Literal

OPENI_LOGO_ASCII = """\n
         ██████╗   ██████╗  ███████╗  ███╗   ██╗  ██████╗
        ██╔═══██╗  ██╔══██╗ ██╔════╝  ████╗  ██║    ██╔═╝
        ██║   ██║  ██████╔╝ █████╗    ██╔██╗ ██║    ██║
        ██║   ██║  ██╔═══╝  ██╔══╝    ██║╚██╗██║    ██║
        ╚██████╔╝  ██║      ███████╗  ██║ ╚████║  ██████╗
         ╚═════╝   ╚═╝      ╚══════╝  ╚═╝  ╚═══╝  ╚═════╝\n
"""
CLI_DESCRIPTION = "         OpenI command line tool 启智AI协作平台命令行工具"

REPO_ID_REGEX = r"^[.a-zA-Z0-9_-]+/[.a-zA-Z0-9_-]+$"
REPO_INFO_REGEX = r"[\w\d]+/[\w\d]+"
TOKEN_REGEX = r"^[0-9a-z]{40}$"

DEFAULT_BASE_URL = "https://openi.pcl.ac.cn"
AI_MODEL_VERSION_FILE = "openi_resource.version"
FILE_CACHE_PREFIX = ".openi-cache-"

HTTP_MAX_RETRIES: int = 3
HTTP_RETRY_DELAY: float = 1

# file storage
UPLOAD_TYPE = {"gpu": 0, "npu": 1}
CHUNK_SIZE = 1024 * 1024 * 64  # 64MB
MAX_FILE_SIZE = 1024 * 1024 * 1024 * 200  # 200GB
DOWNLOAD_RATES = 1024 * 1024 * 5

# api
OPENI_ROOT = Path.home() / ".openi"
if not OPENI_ROOT.exists():
    OPENI_ROOT.mkdir(parents=True)

TOKEN_FILE_PATH = Path(OPENI_ROOT) / "token.json"

LOG_FILE_ROOT = Path(OPENI_ROOT) / "logs"
if not LOG_FILE_ROOT.exists():
    LOG_FILE_ROOT.mkdir(parents=True)

LOG_FILE = LOG_FILE_ROOT / "openi.log"
if not LOG_FILE.exists():
    LOG_FILE.touch()

DEFAULT_SAVE_PATH = Path.cwd()
if not DEFAULT_SAVE_PATH.exists():
    DEFAULT_SAVE_PATH.mkdir(parents=True)

UPLOAD_MODE = Literal["dataset", "model"]
UPLOAD_ENDPOINT = dict(dataset="/attachments", model="/attachments/model")
UPLOAD_ID_PARAM = dict(dataset="dataset_id", model="modeluuid")
