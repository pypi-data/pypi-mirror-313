from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, List, Literal, Optional, Union

from openi.adaptor.om_hub.utils import split_repo_id


@dataclass
class CommitOperationAdd:
    path_in_repo: str
    path_or_fileobj: Union[str, Path, bytes, BinaryIO]


def create_branch(
    repo_id: str,
    branch: str,
    token: Optional[str] = None,
    exist_ok: bool = False,
    **kwargs,
) -> None:
    return None


from openi._dataclass import CreateRepoOption, ModelCreate, RepoInfo
from openi._exceptions import ModelCreateError, RepoExistsError
from openi.api import OpenIApi


def create_repo(
    repo_id: str,
    token: Optional[str] = None,
    private: bool = False,
    exist_ok: bool = False,
    desc: Optional[str] = None,
    license: Optional[str] = None,
    **kwargs,
) -> str:
    try:
        openi_repo_id, openi_model_name = split_repo_id(repo_id)
        api = OpenIApi(token=token)

        try:
            # create repo
            repo_name = openi_repo_id.split("/")[-1]
            options = CreateRepoOption(
                name=repo_name,
                private=private,
            )
            _: RepoInfo = api.create_repo(options=options)

        except RepoExistsError as e:
            if not exist_ok:
                raise e

        try:
            # create model
            _: ModelCreate = api.create_model(
                repo_id=openi_repo_id,
                model_name=openi_model_name,
                is_private=private,
                description=desc,
                license=license,
            )

            return api.get_model_url(repo_id=openi_repo_id, model_name=openi_model_name)

        except ModelCreateError as e:
            if not exist_ok:
                raise e

    except (BaseException, Exception) as e:
        raise e


from openi.uploader import upload_file, upload_model_file


def create_commit(
    repo_id: str,
    operations: List[CommitOperationAdd],
    token: Optional[str] = None,
    repo_type: Literal["dataset", "model"] = "model",
    **kwargs,
) -> str:
    try:
        url: str = ""
        for op in operations:
            if repo_type == "dataset":
                url = upload_file(
                    repo_id=repo_id,
                    file=op.path_or_fileobj,
                    token=token,
                )
            else:
                openi_repo_id, openi_model_name = split_repo_id(repo_id)
                url = upload_model_file(
                    repo_id=openi_repo_id,
                    model_name=openi_model_name,
                    file=op.path_or_fileobj,
                    upload_name=op.path_in_repo,
                    token=token,
                )

        return url

    except (BaseException, Exception) as e:
        raise e


from openi.uploader import upload_model


def upload_folder(
    repo_id: str,
    folder_path: Union[str, Path],
    token: Optional[str] = None,
    repo_type: Literal["dataset", "model"] = "model",
    **kwargs,
) -> None:
    try:
        if repo_type == "dataset":
            return upload_file(
                repo_id=repo_id,
                file=folder_path,
                token=token,
            )
        else:
            openi_repo_id, openi_model_name = split_repo_id(repo_id)
            return upload_model(
                repo_id=openi_repo_id,
                model_name=openi_model_name,
                folder=folder_path,
                token=token,
            )

    except (BaseException, Exception) as e:
        raise e
