#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Iterator, List, Literal, Optional, Union

from ._dataclass import (
    BasicResp,
    CreateRepoOption,
    DatasetFile,
    DatasetInfo,
    FileChunkInfo,
    ModelCreate,
    ModelFile,
    ModelInfo,
    MultipartUrl,
    NewMultipart,
    RepoInfo,
    UserInfo,
)
from ._exceptions import (
    DatasetNotFound,
    ModelCreateError,
    ModelNotFoundError,
    RepoExistsError,
    ServerFileExistsError,
    ServerFileNotFoundError,
    UploadError,
)
from ._file import file_chunk_by_part, file_chunk_iterator, get_file_size
from ._session import OpenISession
from .constants import AI_MODEL_VERSION_FILE, DOWNLOAD_RATES, UPLOAD_ENDPOINT, UPLOAD_ID_PARAM
from .log import setup_logger
from .utils import iter_by_step

logger = setup_logger("info")

UPLOAD_MAX_THREADING = 3


def filter_model_version_file(
    model_files: List[ModelFile],
) -> Optional[List[ModelFile]]:
    """
    Filter model version files from a list of model files.

    Args:
        model_files (List[ModelFile]): List of model files

    Returns:
        List[ModelFile]: List of model version files
    """
    filtered = [f for f in model_files if f.FileName != AI_MODEL_VERSION_FILE]
    if not filtered:
        return None
    return filtered


class OpenIApi:
    R"""
    OpenI API Wrapper Class

    This class provides a client session to the REST API of OpenI AiForge
    Project.

    All API endpoints are implemented as methods of this class. The class
    methods wrap the original API json response in Python dataclass format,
    with tiny changes on some variables names.

    For more information, refer to the official git repo source code:
        - https://openi.pcl.ac.cn/OpenI/aiforge

    Args:
        endpoint (str, optional):
            URL for the OpenI website.
            When not specified, will load from local machine at
            `/home/{usr}/.openi/token.json`

        token (str, optional):
            login user access token obtained by following url:
                - https://openi.pcl.ac.cn/user/settings/applications
            When not specified, will load from local machine at
            `/home/{usr}/.openi/token.json`
    """

    def __init__(
        self,
        token: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        self.session = OpenISession()
        self.session.set_basic_auth(token=token, endpoint=endpoint)

        logger.info(f"New OpenIApi Session @{self.session.endpoint}")

    def dev(self, mode: bool = False):
        self.session.dev_mode = mode

    def close(self):
        self.session.close()

    """
    Base API Endpoints
    """

    def get_user_info(self) -> UserInfo:
        """Retrieve user info for currently authenticated user

        Returns:
            UserInfo: UserInfo object containing metadata about current
            login user
        """
        with self.session.get("/user") as resp:
            data = resp.json()
            return UserInfo(**data)

    def get_repo_info(self, repo_id: str) -> RepoInfo:
        """Retrieve repository info for given repo id

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format

        Returns:
            RepoInfo: RepoInfo object containing metadata about given repo id
        """
        with self.session.get(f"/repos/{repo_id}") as resp:
            data = resp.json()
            return RepoInfo(**data)

    def get_repo_access_right(self, repo_id: str) -> str:
        """Retrieve current login user's operation right for a specific
        repository

        Args:
            repo_id (str): Repository ID in `Username/Reponame` format

        Returns:
            RepoPermission:
                access right information wrapped in RepoPermission object,
                containing three attributes: [`write` `read` or `none`]
        """
        with self.session.get(f"/repos/{repo_id}/right") as resp:
            data = resp.json()["right"]
            return data

    def create_repo(self, options: CreateRepoOption) -> RepoInfo:
        with self.session.post(f"/user/repos", json=asdict(options)) as resp:
            data = resp.json()

            if resp.status_code == 409:
                user = self.get_user_info()
                username = user.username
                raise RepoExistsError(f"{username}/{options.name}")

            return RepoInfo(**data)

    """
    Dataset API Endpoints
    """

    def get_dataset_url(self, repo_id: str) -> str:
        """Get dataset url"""
        return f"{self.session.endpoint}/{repo_id}/datasets"

    def get_dataset_info(
        self,
        repo_id: str,
        upload_type: int = 1,
    ) -> Optional[DatasetInfo]:
        params: dict = {"type": upload_type}

        with self.session.get(
            f"/{repo_id}/sdk/get_dataset",
            params=params,
        ) as resp:
            resp_obj = BasicResp(**resp.json())
            if resp_obj.code == -1:
                raise DatasetNotFound(repo_id, self.get_dataset_url(repo_id))

            resp_obj.data["repo_id"] = repo_id
            return DatasetInfo(**resp_obj.data) or None

    def list_dataset_files(
        self,
        repo_id: str,
        upload_type: int = 1,
    ) -> Optional[List[DatasetFile]]:
        dataset_info = self.get_dataset_info(repo_id=repo_id, upload_type=upload_type)

        if dataset_info is None:
            raise DatasetNotFound(repo_id, self.get_dataset_url(repo_id))

        return dataset_info.attachments

    def query_dataset_file(
        self,
        repo_id: str,
        filename: str,
        upload_type: int = 1,
    ) -> Optional[DatasetFile]:
        dataset_files = self.list_dataset_files(
            repo_id=repo_id,
            upload_type=upload_type,
        )

        if dataset_files is None:
            return None

        try:
            return next(f for f in dataset_files if f.name == filename)
        except StopIteration:
            return None

    """
    Model API Endpoints
    """

    def get_repo_models_url(self, repo_id: str) -> str:
        """Get model list url"""
        return f"{self.session.endpoint}/{repo_id}/modelmanage/show_model"

    def get_model_url(self, repo_id: str, model_name: str) -> str:
        """Get model url"""
        return f"{self.session.endpoint}/{repo_id}/modelmanage/model_filelist_tmpl?name={model_name}"

    def create_model(
        self,
        repo_id: str,
        model_name: str,
        upload_type: int = 1,
        engine: int = 0,
        is_private: bool = True,
        description: str = "",
        license: str = "",
    ) -> ModelCreate:
        """Create a new model in a specific repo"""
        with self.session.post(
            f"/repos/{repo_id}/modelmanage/create_local_model",
            params=dict(
                name=model_name,
                type=upload_type,
                engine=engine,
                isPrivate=is_private,
                description=description,
                license=license,
            ),
        ) as resp:
            info = ModelCreate(**resp.json())
            if info.code != "0":
                raise ModelCreateError(model_name, info.msg)
            return info

    def get_model_info(self, repo_id: str, model_name: str) -> Optional[ModelInfo]:
        params: dict = {"name": model_name}
        with self.session.get(
            f"/{repo_id}/sdk/get_model",
            params=params,
        ) as resp:
            resp_obj = BasicResp(**resp.json())
            if resp_obj.code == -1:
                raise ModelNotFoundError(model_name, self.get_repo_models_url(repo_id))

            resp_obj.data["repo_id"] = repo_id
            return ModelInfo(**resp_obj.data) or None

    def list_model_files(
        self,
        repo_id: str,
        model_name: str,
    ) -> Optional[List[ModelFile]]:
        model_info = self.get_model_info(repo_id=repo_id, model_name=model_name)

        if model_info is None:
            raise ModelNotFoundError(repo_id, self.get_repo_models_url(repo_id))

        return filter_model_version_file(model_info.modelFileList)

    def query_model_file(
        self,
        repo_id: str,
        model_name: str,
        filename: str,
    ) -> Optional[ModelFile]:
        model_files = self.list_model_files(repo_id=repo_id, model_name=model_name)

        if model_files is None:
            return None

        try:
            return next(f for f in model_files if f.FileName == filename)
        except StopIteration:
            return None

    """
    Download API Endpoint
    """

    def get_model_file_download_url(
        self,
        repo_id: str,
        model_name: str,
        filename: str,
    ):
        model_file = self.query_model_file(repo_id, model_name, filename)

        if not model_file:
            raise ServerFileNotFoundError(
                f"{repo_id}/{model_name} can not find file {filename}",
            )

        repo_id: str = model_file.repo_id
        model_id: str = model_file.model_id
        filename: str = model_file.FileName

        route = f"/{repo_id}/sdk/download_model_file/{model_id}"
        url = self.session._build_url(route)

        return f"{url}?fileName={filename}"

    def download_file_iterator(
        self,
        src_file: Union[DatasetFile, ModelFile],
        filepath: Union[Path, str],
        chunk_size: int = DOWNLOAD_RATES,
    ) -> Iterator[int]:
        """Download a specific file by filename

        Args:
            src_file (Union[DatasetFile, ModelFile]):
                file object containing metadata of the file
            filepath (Union[Path, str]):
                local file path to be downloaded
            chunk_size (int, optional):
                size of the chunk to download
        """
        if not isinstance(filepath, Path):
            filepath = Path(filepath).absolute()

        if not isinstance(src_file, (DatasetFile, ModelFile)):
            raise ValueError(f"Invalid file type: {type(src_file)}")

        if isinstance(src_file, DatasetFile):
            return self.download_dataset_file_iterator(
                dataset_file=src_file,
                filepath=filepath,
                chunk_size=chunk_size,
            )

        if isinstance(src_file, ModelFile):
            return self.download_model_file_iterator(
                model_file=src_file,
                filepath=filepath,
                chunk_size=chunk_size,
            )

    def download_dataset_file_iterator(
        self,
        dataset_file: DatasetFile,
        filepath: Path,
        chunk_size: int = DOWNLOAD_RATES,
    ) -> Iterator[int]:
        """Download a specific attachment file by uuid

        Args:
            dataset_file (DatasetFile): dataset_file object containing
            metadata of the file
            filepath (Path): local file path to be downloaded
            chunk_size (int, optional): size of the chunk to download,
            defaults to DOWNLOAD_RATES
        """
        if not filepath.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.touch()

        cache_size = get_file_size(filepath)
        yield cache_size

        if cache_size == dataset_file.size:
            return

        repo_id: str = dataset_file.repo_id
        uuid: str = dataset_file.uuid
        upload_type: int = dataset_file.type
        params: dict = {"type": upload_type}
        headers: dict = {"Range": "bytes=%d-" % cache_size}

        try:
            with self.session.get(
                f"/{repo_id}/sdk/download_dataset_file/{uuid}",
                params=params,
                headers=headers,
                allow_redirects=True,
                stream=True,
            ) as resp:
                with open(filepath, "ab") as f:
                    for chunk_data in resp.iter_content(chunk_size=chunk_size):
                        f.write(chunk_data)
                        yield len(chunk_data)

        except Exception as e:
            raise e

    def download_model_file_iterator(
        self,
        model_file: ModelFile,
        filepath: Path,
        chunk_size: int = DOWNLOAD_RATES,
    ) -> Iterator[int]:
        """Download a specific model file by filename

        Args:
            model_file (ModelFile): model_file object containing metadata
            of the file
            filepath (Path): local file path to be downloaded
            chunk_size (int, optional): size of the chunk to download
        """
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)

        cache_size = get_file_size(filepath) if filepath.exists() else 0
        yield cache_size

        if cache_size == model_file.Size:
            return

        repo_id: str = model_file.repo_id
        model_id: str = model_file.model_id
        filename: str = model_file.FileName
        params: dict = {"fileName": filename}
        headers: dict = {"Range": "bytes=%d-" % cache_size}

        try:
            with self.session.get(
                f"/{repo_id}/sdk/download_model_file/{model_id}",
                params=params,
                headers=headers,
                allow_redirects=True,
                stream=True,
            ) as resp:
                with open(filepath, "ab") as f:
                    for chunk_data in resp.iter_content(chunk_size=chunk_size):
                        f.write(chunk_data)
                        yield len(chunk_data)

        except Exception as e:
            raise e

    """
    File Upload API Endpoints
    """

    def upload_get_chunks(
        self,
        dataset_or_model_id: str,
        md5: str,
        filename: str,
        upload_type: int,
        size: int,
        upload_mode: Literal["dataset", "model"],
    ) -> FileChunkInfo:
        """Get chunks info for a specific file upload

        Args:
            dataset_or_model_id (str): dataset or model id
            md5 (str): md5 hash of the file
            filename (str): name of the file
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            FileChunkInfo: FileChunkInfo object containing metadata of the file
        """
        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/get_chunks"
        id_param = UPLOAD_ID_PARAM.get(upload_mode, None)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(file_name=filename, md5=md5, type=upload_type, size=size)
        params.update({id_param: dataset_or_model_id})

        with self.session.get(
            route,
            params=params,
        ) as resp:
            data = resp.json()
            #
            # if "result_code" in data and data["result_code"] == "-1":
            #     raise ValueError(f"Failed to get chunks info: {data['msg']}")

            data.update({"upload_mode": upload_mode})
            data.update({"md5": md5})
            return FileChunkInfo(**data)

    def upload_new_multipart(
        self,
        dataset_or_model_id: str,
        md5: str,
        filename: str,
        filesize: int,
        total_chunks_counts: int,
        upload_type: int,
        upload_mode: Literal["dataset", "model"],
    ) -> NewMultipart:
        """Create a new multipart upload of a specific file

        Args:
            dataset_or_model_id (str): dataset or model id
            md5 (str): md5 hash of the file
            filename (str): name of the file
            filesize (int): size of the file
            total_chunks_counts (int): total chunks count of the file
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            NewMultipart: NewMultipart object containing metadata of the file
        """
        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/new_multipart"
        id_param = UPLOAD_ID_PARAM.get(upload_mode, None)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(
            md5=md5,
            file_name=filename,
            size=filesize,
            totalChunkCounts=total_chunks_counts,
            type=upload_type,
        )
        params.update({id_param: dataset_or_model_id})

        with self.session.get(
            route,
            params=params,
        ) as resp:
            data = resp.json()
            return NewMultipart(**data)

    def upload_get_multipart_url(
        self,
        dataset_or_model_id: str,
        uuid: str,
        upload_id: str,
        upload_type: int,
        upload_mode: Literal["dataset", "model"],
        chunk_number: int,
        chunk_size: int,
        filename: Optional[str] = None,
    ) -> MultipartUrl:
        """Get upload url for a specific file_chunk

        Args:
            dataset_or_model_id (str): dataset or model id
            uuid (str): uuid of the file
            upload_id (str): upload id of the file
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            chunk_number (int): chunk number of the file
            chunk_size (int): size of the chunk
            filename (str): name of the file
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            MultipartUrl: MultipartUrl object containing metadata of the file
        """
        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/get_multipart_url"
        id_param = UPLOAD_ID_PARAM.get(upload_mode, None)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(
            uuid=uuid,
            uploadID=upload_id,
            type=upload_type,
            chunkNumber=chunk_number,
            size=chunk_size,
        )
        if upload_mode == "dataset":
            params.update({f"{id_param}": dataset_or_model_id, "file_name": filename})

        with self.session.get(
            route,
            params=params,
        ) as resp:
            data = dict()
            if resp.status_code == 200:
                data.update({"url": resp.json()["url"]})
            if resp.status_code in [400, 500]:
                data.update({"msg": resp.text})

            return MultipartUrl(**data)

    def upload_complete_multipart(
        self,
        dataset_or_model_id: str,
        upload_mode: Literal["dataset", "model"],
        upload_type: int,
        upload_id: str,
        uuid: str,
        filename: Optional[str] = None,
        filesize: Optional[int] = None,
    ) -> Union[bool, dict]:
        """Complete a multipart upload of a specific file

        Args:
            dataset_or_model_id (str): dataset or model id
            upload_type (int): storage of file; 0 for GPU(minio), 1 for NPU(
            obs)
            upload_id (str): upload id of the file
            uuid (str): uuid of the file
            filename (str): name of the file
            filesize (int): size of the file
            upload_mode (str): upload mode; "dataset" or "model"

        Returns:
            Union[bool, dict]: returns True if upload is successful,
            otherwise False
        """

        route = UPLOAD_ENDPOINT.get(upload_mode, "") + "/complete_multipart"
        id_param = UPLOAD_ID_PARAM.get(upload_mode)
        if not route or not id_param:
            raise ValueError(f"Invalid upload_mode: {upload_mode}")

        params = dict(
            uuid=uuid,
            uploadID=upload_id,
            type=upload_type,
        )
        params.update({id_param: dataset_or_model_id})
        if upload_mode == "dataset":
            params.update(dict(file_name=filename, size=filesize))

        with self.session.post(
            route,
            params=params,
        ) as resp:
            try:
                data = resp.json()
                if "result_code" in data.keys():
                    return data["result_code"] == "0"
            except:
                return False

            return False

    def upload_file_iterator(
        self,
        filepath: Union[Path, str],
        dataset_or_model_id: str,
        file_md5: str,
        file_size: int,
        total_chunks_count: int,
        upload_mode: Literal["model", "dataset"],
        upload_name: str,
        upload_type: int,
        chunk_size: int,
    ) -> Iterator[int]:
        """Upload single model file from local to OpenI

        Args:

        Returns:
            Iterator[int]:
                iterator of len(bytes) uploaded, for upload progress
                notification; generally should yield CHUNK_SIZE
                except the last chunk, whose len(bytes) might be <= CHUNK_SIZE.
        """

        # get chunk
        get_chunks = self.upload_get_chunks(
            dataset_or_model_id=dataset_or_model_id,
            md5=file_md5,
            filename=upload_name,
            upload_type=upload_type,
            upload_mode=upload_mode,
            size=file_size,
        )
        if not get_chunks or get_chunks.result_code == -1:
            if get_chunks.msg:
                msg = f"get chunks failed with error {get_chunks.msg}"
            else:
                msg = f"get chunks create failed with unknown error."
            logger.error(msg)
            raise UploadError(msg)
        logger.info(f"`{upload_name}` {get_chunks}")

        # 数据集重复上传
        if get_chunks.uploaded and upload_mode == "dataset":
            if get_chunks.datasetID != "":
                # 已存在
                if get_chunks.dataset_or_model_name != "" and get_chunks.realName != "":
                    existing_filename = get_chunks.realName
                    existing_repo_id = get_chunks.repo_id
                    # existing_dataset = get_chunks.dataset_or_model_name
                    logger.warning(f"{upload_name} already uploaded as {existing_filename}")
                    raise ServerFileExistsError(
                        filename=upload_name,
                        existing_repo_id=existing_repo_id,
                        existing_filename=existing_filename,
                    )
                # 秒传
                if get_chunks.dataset_or_model_name == "" and get_chunks.realName == "":
                    yield file_size
                    return

        # 模型重复上传
        if get_chunks.uploaded and upload_mode == "model":
            # 已存在
            if get_chunks.dataset_or_model_name != "" and get_chunks.realName != "":
                existing_filename = get_chunks.realName
                existing_repo_id = get_chunks.repo_id
                # existing_dataset = get_chunks.dataset_or_model_name
                logger.warning(f"{upload_name} already uploaded as {existing_filename}")
                raise ServerFileExistsError(
                    filename=upload_name,
                    existing_repo_id=existing_repo_id,
                    existing_filename=existing_filename,
                )

        # new multipart
        if not get_chunks.uuid or not get_chunks.uploadID:
            new_multipart = self.upload_new_multipart(
                dataset_or_model_id=dataset_or_model_id,
                filename=upload_name,
                upload_type=upload_type,
                md5=file_md5,
                filesize=file_size,
                total_chunks_counts=total_chunks_count,
                upload_mode=upload_mode,
            )
            if not new_multipart or new_multipart.result_code == -1:
                if new_multipart.msg:
                    msg = f"new multipart failed with error: {new_multipart.msg}"
                else:
                    msg = f"new multipart failed with unknown error."
                logger.error(msg)
                raise UploadError(msg)

            get_chunks.uploadID = new_multipart.uploadID
            get_chunks.uuid = new_multipart.uuid

            logger.info(f"`{upload_name}` {new_multipart}")

        etags: List = list()
        start_from_chunk = len(get_chunks.uploaded_chunks) or 1
        yield chunk_size * (start_from_chunk - 1)

        # get multipart url
        # put upload
        for chunk_number, chunk_data in file_chunk_iterator(
            filepath=filepath,
            chunk_size=chunk_size,
            start_from_chunk=start_from_chunk,
        ):
            multipart_url = self.upload_get_multipart_url(
                dataset_or_model_id=dataset_or_model_id,
                chunk_number=chunk_number,
                uuid=get_chunks.uuid,
                upload_id=get_chunks.uploadID,
                upload_mode=upload_mode,
                upload_type=upload_type,
                chunk_size=len(chunk_data),
                filename=upload_name,
            )
            if not multipart_url.url:
                msg = f"get multipart url failed with" f" error {multipart_url.msg}."
                logger.error(msg)
                raise UploadError(msg)
            logger.info(f"`{upload_name}` {multipart_url}")

            etag = self.session.put_upload(
                url=multipart_url.url,
                filedata=chunk_data,
                upload_type=upload_type,
            )
            if not etag:
                raise UploadError("put upload failed")

            yield len(chunk_data)
            etags.append(etag)

        if len(etags) != total_chunks_count - start_from_chunk + 1:
            msg = f"some chunk failed to upload, can not complete upload " f"process."
            logger.error(msg)
            raise UploadError(msg)

        # complete multipart
        complete = self.upload_complete_multipart(
            dataset_or_model_id=dataset_or_model_id,
            upload_mode=upload_mode,
            uuid=get_chunks.uuid,
            upload_id=get_chunks.uploadID,
            filename=upload_name,
            filesize=file_size,
            upload_type=upload_type,
        )
        if not complete:
            msg = f"complete multipart failed with unknown error."
            logger.error(msg)
            raise UploadError(msg)
        logger.info(f"`{upload_name}` complete_multipart: {complete}")

        logger.info("uploading success.")
