from openi.adaptor.om_hub import *

token = ""
repo_id = "FoundationModel/coqui/XTTS-v2"
filename = "model.pth"


def get_download():
    url = om_hub_url(
        repo_id=repo_id,
        filename=filename,
        token=token,
    )
    temp_file = open(f"./testing/data/{filename}", "wb")
    headers = build_om_headers(token=token)
    print(url, headers)

    http_get(url, temp_file, token=token, headers=headers, displayed_filename=filename)


def hub_download():
    om_hub_download(
        repo_id=repo_id,
        filename=filename,
        token=token,
        local_dir="./testing/data",
    )


def snapshot():
    snapshot_download(
        repo_id=repo_id,
        token=token,
        local_dir="./testing/data/xtts",
    )


def upload(filenames: list = None):
    up_repo_id = "chenzh/test_om_v2/model2"
    create_repo(
        repo_id=up_repo_id,
        token=token,
        exist_ok=True,
    )
    if filenames:
        ops = [
            CommitOperationAdd(
                path_in_repo=f,
                path_or_fileobj=f"./testing/data/xtts/{f}",
            )
            for f in filenames
        ]

        create_commit(
            repo_id=up_repo_id,
            operations=ops,
            token=token,
        )
    else:
        upload_folder(
            repo_id=up_repo_id,
            folder_path="./testing/data/xtts",
            token=token,
        )


upload(["readme.md", "vocab.json"])
