from _auth import access_token, endpoint
from openi import caltime, upload_file

repo_id = "chenzh01/llms"
file = "data/upload.zip"


@caltime
def upload():
    r = upload_file(
        repo_id=repo_id,
        file=file,
        token=access_token,
        endpoint=endpoint,
    )


@caltime
def upload_thread_3():
    r = upload_file(
        repo_id=repo_id,
        file=file,
        token=access_token,
        endpoint=endpoint,
        use_thread=True,
        thread_worker=3,
    )


@caltime
def upload_thread_5():
    r = upload_file(
        repo_id=repo_id,
        file=file,
        token=access_token,
        endpoint=endpoint,
        use_thread=True,
        thread_worker=5,
    )


@caltime
def upload_thread_10():
    r = upload_file(
        repo_id=repo_id,
        file=file,
        token=access_token,
        endpoint=endpoint,
        use_thread=True,
        thread_worker=10,
    )


if __name__ == "__main__":
    upload()
