from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .utils import parse_time


@dataclass
class UserInfo:
    """
    User Info Dataclass

    Attributes:
        username (str):
            username for OpenI links and repo_id
        id (int):
            unique number id of user
        login (str):
            username used for login purpose
        full_name (str):
            self-defined name for display
        email (str):
            registered email address
        avatar_url (str):
            user avatar url
        language (str):
            user default language
        is_admin (bool):
            whether the user is admin or not
        is_active (bool):
            whether the user is active or not
        last_login (str):
            last login time
        created (str):
            created time
    """

    username: str
    id: Optional[int]
    login: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    avatar_url: Optional[str]
    language: Optional[str]
    is_admin: Optional[bool]
    is_active: Optional[bool]
    last_login: Optional[str]
    created: Optional[str]


@dataclass
class RepoPermission:
    """
    Permission Info Dataclass

    Attributes:
        admin (bool):
            whether the user is admin or not
        push (bool):
            whether the user can push to the repository or not
        pull (bool):
            whether the user can pull from the repository or not
    """

    admin: bool
    push: bool
    pull: bool


@dataclass
class RepoInfo:
    """
    Repo Info Dataclass

    Attributes:
        id (int):
            repo id
        owner (UserInfo):
            owner info
        name (str):
            repo name
        repo_id (str):
            repo id in `Username/Reponame` format
        size (int):
            repo size
        html_url (str):
            repo url
        permissions (RepoPermission):
            repo permissions
        created_at (str):
            created time
        updated_at (str):
            updated time
    """

    id: int
    owner: UserInfo
    name: str
    repo_id: str
    size: Optional[int]
    html_url: Optional[str]
    permissions: Optional[RepoPermission]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id")
        self.owner = UserInfo(**kwargs.pop("owner"))
        self.name = kwargs.pop("name")
        self.repo_id = kwargs.pop("full_name")

        self.size = kwargs.pop("size", None)
        self.html_url = kwargs.pop("html_url", None)
        permissions = kwargs.pop("permissions", None)
        self.permissions = RepoPermission(**permissions) if permissions else None

        created_at = kwargs.pop("created_at", None)
        self.created_at = parse_time(created_at) if created_at else None
        updated_at = kwargs.pop("updated_at", None)
        self.updated_at = parse_time(updated_at) if updated_at else None


@dataclass
class DatasetFile:
    """TODO"""

    uuid: str
    name: str
    size: int
    type: int
    id: int
    datasetId: int
    repo_id: str
    uploaderId: Optional[int]
    isPrivate: Optional[bool]
    decompressState: Optional[int]

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop("uuid")
        self.name = kwargs.pop("name")
        self.size = kwargs.pop("size")
        self.type = kwargs.pop("type")
        self.id = kwargs.pop("id")
        self.datasetId = kwargs.pop("datasetId")
        self.repo_id = kwargs.pop("repo_id")

        self.uploaderId = kwargs.pop("uploaderId", None)
        self.isPrivate = kwargs.pop("isPrivate", None)
        self.decompressState = kwargs.pop("decompressState", None)


@dataclass
class DatasetInfo:
    """TODO"""

    id: str
    userId: int
    repoId: int
    title: str
    repo_id: str
    attachments: Optional[List[DatasetFile]]
    status: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id")
        self.userId = kwargs.pop("userId")
        self.repoId = kwargs.pop("repoId")
        self.title = kwargs.pop("title")
        self.repo_id = kwargs.pop("repo_id")

        attachments = kwargs.pop("attachments", [])
        if attachments:
            for data in attachments:
                data.update({"repo_id": self.repo_id})
            self.attachments = [DatasetFile(**data) for data in attachments]
        else:
            self.attachments = None

        self.status = kwargs.pop("status", None)
        self.recommend = kwargs.pop("recommend", None)


@dataclass
class FileChunkInfo:
    """
    File Chunk Info Dataclass

    API Response (dict):
        - dataset "/attachments/get_chunks"
            "uuid":        fileChunk.UUID,
            "uploaded":    strconv.Itoa(fileChunk.IsUploaded),
            "uploadID":    fileChunk.UploadID,
            "chunks":      string(chunks),
            "attachID":    "0",
            "datasetID":   "0",
            "fileName":    "",
            "datasetName": "",

        - model "/attachments/model/get_chunks"
            "uuid":      fileChunk.UUID,
            "uploaded":  strconv.Itoa(fileChunk.IsUploaded),
            "uploadID":  fileChunk.UploadID,
            "chunks":    string(chunks),
            "attachID":  "0",
            "modeluuid": modeluuid,
            "datasetID": "0",
            "fileName":  "",
            "modelName": "",

        - error response
            "result_code": "-1",
            "msg":         errStr,

    Attributes:
        result_code (int):
            return 0 when success, otherwise return -1 with error message
        msg (str):
            return plain string error message, return "success" when None
        uploaded (Optional[bool]):
            whether the file is uploaded or not
        attachID (Optional[int]):
            attachment id
        uploaded_chunks (Optional[list]):
            list of uploaded chunks
        uploadID (Optional[str]):
            upload id
        uuid (Optional[str]):
            file uuid
        repo_id (Optional[str]):
            repo id in `Username/Reponame` format
        dataset_or_model_name (Optional[str]):
            dataset or model name
    """

    result_code: int
    msg: str
    uploaded: Optional[bool]
    md5: Optional[str]
    fileName: Optional[str]
    attachID: Optional[int]
    uploaded_chunks: Optional[list]
    uploadID: Optional[str]
    uuid: Optional[str]
    repo_id: Optional[str]
    dataset_or_model_name: Optional[str]
    realName: Optional[str]
    datasetID: Optional[str]
    upload_mode: Optional[str]

    def __init__(self, **kwargs):
        result_code = kwargs.pop("result_code", 0)
        self.result_code = int(result_code)
        self.msg = kwargs.pop("msg", "success")

        uploaded = kwargs.pop("uploaded", "")
        self.uploaded = True if uploaded == "1" else False
        self.attachID = kwargs.pop("attachID", None)

        raw_chunks = kwargs.pop("chunks", "")
        uploaded_chunks = [i for i in raw_chunks.split(",") if i != ""]
        self.uploaded_chunks = uploaded_chunks

        uploadID = kwargs.pop("uploadID", "")
        self.uploadID = uploadID if uploadID != "" else None
        uuid = kwargs.pop("uuid", "")
        self.uuid = uuid if uuid != "" else None

        repo = kwargs.pop("repoName", None)
        owner = kwargs.pop("repoOwner", None)
        self.repo_id = owner + "/" + repo if owner and repo else None

        if kwargs.pop("upload_mode") == "dataset":
            self.dataset_or_model_name = kwargs.pop("datasetName", "")
        else:
            self.dataset_or_model_name = kwargs.pop("modelName", "")

        self.fileName = kwargs.pop("fileName", "")
        self.realName = self.fileName
        self.datasetID = kwargs.pop("datasetID", "")
        self.md5 = kwargs.pop("md5", None)
        self.upload_mode = kwargs.pop("upload_mode", None)


@dataclass
class NewMultipart:
    """TODO"""

    result_code: int
    msg: str
    uuid: Optional[str]
    uploadID: Optional[str]

    def __init__(self, **kwargs):
        result_code = kwargs.pop("result_code", 0)
        self.result_code = int(result_code)
        self.msg = kwargs.pop("msg", "success")
        self.uuid = kwargs.pop("uuid", None)
        self.uploadID = kwargs.pop("uploadID", None)


@dataclass
class MultipartUrl:
    """TODO"""

    url: Optional[str] = None
    msg: Optional[str] = None


@dataclass
class ModelFile:
    FileName: Optional[str]
    ModTime: Optional[str]
    IsDir: Optional[bool]
    Size: Optional[int]
    ParenDir: Optional[str]
    UUID: Optional[str]
    RelativePath: Optional[str]
    repo_id: Optional[str]
    model_id: Optional[str]


@dataclass
class ModelInfo:
    id: Optional[str]
    name: Optional[str]
    size: Optional[int]
    path: Optional[str]
    repo_id: Optional[str]
    repoId: Optional[int]
    userId: Optional[int]
    userName: Optional[str]
    isCanOper: Optional[bool]
    isCanDelete: Optional[bool]
    isCanDownload: Optional[bool]
    repoName: Optional[str]
    repoOwnerName: Optional[str]
    modelFileList: Optional[List[ModelFile]]
    modelType: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id", None)
        self.name = kwargs.pop("name", None)
        self.size = kwargs.pop("size", None)
        self.path = kwargs.pop("path", None)
        self.repo_id = kwargs.pop("repo_id", None)
        self.repoId = kwargs.pop("repoId", None)
        self.userId = kwargs.pop("userId", None)
        self.userName = kwargs.pop("userName", None)
        self.isCanOper = kwargs.pop("isCanOper", None)
        self.isCanDelete = kwargs.pop("isCanDelete", None)
        self.isCanDownload = kwargs.pop("isCanDownload", None)
        self.repoName = kwargs.pop("repoName", None)
        self.repoOwnerName = kwargs.pop("repoOwnerName", None)

        modelFileList = kwargs.pop("modelFileList", [])
        if modelFileList:
            for data in modelFileList:
                data.update({"repo_id": self.repo_id, "model_id": self.id})
            self.modelFileList = [ModelFile(**data) for data in modelFileList]
        else:
            self.modelFileList = None

        self.modelType = kwargs.pop("modelType", None)


@dataclass
class ModelCreate:
    code: str
    msg: Optional[str] = None
    id: Optional[int] = None


@dataclass
class BasicResp:
    code: int
    msg: str
    data: any


@dataclass
class CreateRepoOption:
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    private: bool = False
    issue_labels: Optional[str] = None
    auto_init: bool = False
    gitignores: Optional[str] = None
    license: Optional[str] = None
    readme: Optional[str] = None
    default_branch: Optional[str] = None

    def __post_init__(self):
        if len(self.name) > 100:
            raise ValueError("Name must be at most 100 characters long")
        if self.alias and len(self.alias) > 100:
            raise ValueError("Alias must be at most 100 characters long")
        if self.description and len(self.description) > 255:
            raise ValueError("Description must be at most 255 characters long")
        if self.default_branch and len(self.default_branch) > 100:
            raise ValueError("Default branch must be at most 100 characters long")
