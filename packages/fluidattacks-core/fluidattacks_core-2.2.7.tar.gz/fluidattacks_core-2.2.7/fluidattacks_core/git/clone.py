import asyncio
import base64
import logging
import os
import uuid
from pathlib import Path

import aiofiles
import boto3
from botocore.exceptions import ClientError

from .codecommit_utils import (
    extract_region,
)
from .ssh_utils import (
    parse_ssh_url,
)
from .utils import (
    format_url,
)

LOGGER = logging.getLogger(__name__)
MSG = "Repo cloning failed"


async def ssh_clone(
    *,
    branch: str,
    credential_key: str,
    repo_url: str,
    temp_dir: str,
) -> tuple[str | None, str | None]:
    parsed_repo_url = parse_ssh_url(repo_url)
    ssh_file_name = Path(f"{temp_dir}/{uuid.uuid4()!s}")
    async with aiofiles.open(
        os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
        "w",
        encoding="utf-8",
    ) as ssh_file:
        await ssh_file.write(base64.b64decode(credential_key).decode())

    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "clone",
        "--branch",
        branch,
        "--single-branch",
        "--",
        parsed_repo_url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={
            **os.environ.copy(),
            "GIT_SSH_COMMAND": (
                f"ssh -i {ssh_file_name}"
                " -o UserKnownHostsFile=/dev/null"
                " -o StrictHostKeyChecking=no"
                " -o IdentitiesOnly=yes"
                " -o HostkeyAlgorithms=+ssh-rsa"
                " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
            ),
        },
        cwd=temp_dir,
    )
    _, stderr = await proc.communicate()

    os.remove(ssh_file_name)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(MSG, extra={"extra": {"message": stderr.decode()}})

    return (None, stderr.decode("utf-8"))


async def https_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    password: str | None = None,
    token: str | None = None,
    user: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
    follow_redirects: bool = True,
) -> tuple[str | None, str | None]:
    url = format_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        provider=provider,
        is_pat=is_pat,
    )
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        f"http.followRedirects={follow_redirects}",
        *(
            [
                "-c",
                "http.extraHeader=Authorization: Basic "
                + base64.b64encode(f":{token}".encode()).decode(),
            ]
            if is_pat
            else []
        ),
        "clone",
        "--branch",
        branch,
        "--single-branch",
        "--",
        url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        cwd=temp_dir,
    )
    _, stderr = await proc.communicate()

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(MSG, extra={"extra": {"message": stderr.decode()}})

    return (None, stderr.decode("utf-8"))


async def codecommit_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    follow_redirects: bool = True,
) -> tuple[str | None, str | None]:
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        f"http.followRedirects={follow_redirects}",
        "clone",
        "--branch",
        branch,
        "--single-branch",
        "--",
        repo_url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        cwd=temp_dir,
    )
    _, stderr = await proc.communicate()

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(MSG, extra={"extra": {"message": stderr.decode()}})

    return (None, stderr.decode("utf-8"))


async def call_codecommit_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    arn: str,
    org_external_id: str,
    follow_redirects: bool = True,
) -> tuple[str | None, str | None]:
    original_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    original_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    original_session_token = os.environ.get("AWS_SESSION_TOKEN")
    original_region = os.environ.get("AWS_DEFAULT_REGION")

    try:
        sts_client = boto3.client("sts")
        assumed_role = sts_client.assume_role(
            RoleArn=arn,
            RoleSessionName=f"session-{uuid.uuid4()}",
            ExternalId=org_external_id,
        )
        credentials = assumed_role["Credentials"]

        os.environ["AWS_ACCESS_KEY_ID"] = credentials["AccessKeyId"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = credentials["SecretAccessKey"]
        os.environ["AWS_SESSION_TOKEN"] = credentials["SessionToken"]
        os.environ["AWS_DEFAULT_REGION"] = extract_region(repo_url)

        return await codecommit_clone(
            branch=branch,
            repo_url=repo_url,
            temp_dir=temp_dir,
            follow_redirects=follow_redirects,
        )

    except ClientError as exc:
        LOGGER.exception(
            "Error cloning from codecommit",
            extra={
                "extra": {
                    "repo_url": repo_url,
                    "arn": arn,
                    "org_external_id": org_external_id,
                    "exc": exc,
                },
            },
        )

        return None, None

    finally:
        if original_access_key is not None:
            os.environ["AWS_ACCESS_KEY_ID"] = original_access_key
        else:
            os.environ.pop("AWS_ACCESS_KEY_ID", None)
        if original_secret_key is not None:
            os.environ["AWS_SECRET_ACCESS_KEY"] = original_secret_key
        else:
            os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
        if original_session_token is not None:
            os.environ["AWS_SESSION_TOKEN"] = original_session_token
        else:
            os.environ.pop("AWS_SESSION_TOKEN", None)
        if original_region is not None:
            os.environ["AWS_DEFAULT_REGION"] = original_region
        else:
            os.environ.pop("AWS_DEFAULT_REGION", None)
