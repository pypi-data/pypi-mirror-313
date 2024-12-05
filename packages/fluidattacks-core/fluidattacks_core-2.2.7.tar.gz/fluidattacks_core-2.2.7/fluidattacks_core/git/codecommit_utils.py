import asyncio
import logging
import os
import re
import uuid

import boto3
from botocore.exceptions import (
    ClientError,
)

LOGGER = logging.getLogger(__name__)


def extract_region(url: str) -> str:
    pattern = r"codecommit::([a-z0-9-]+)://"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return "us-east-1"


async def assume_role_and_execute_git(
    arn: str,
    repo_url: str,
    branch: str,
    org_external_id: str,
    *,
    follow_redirects: bool = True,
) -> str | None:
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

        return await codecommit_ls_remote(
            repo_url=repo_url,
            branch=branch,
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

        return None

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


async def _execute_git_command(
    url: str,
    branch: str,
    *,
    follow_redirects: bool = True,
) -> tuple[bytes, bytes, int | None]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        f"http.followRedirects={follow_redirects}",
        "ls-remote",
        "--",
        url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, _stderr = await asyncio.wait_for(proc.communicate(), 20)
    return stdout, _stderr, proc.returncode


async def codecommit_ls_remote(
    repo_url: str,
    branch: str = "HEAD",
    *,
    follow_redirects: bool = True,
) -> str | None:
    try:
        stdout, _stderr, return_code = await _execute_git_command(
            repo_url,
            branch,
            follow_redirects=follow_redirects,
        )
        if _stderr and return_code != 0:
            LOGGER.error(
                "failed git ls-remote",
                extra={
                    "extra": {
                        "error": _stderr.decode(),
                        "repo_url": repo_url,
                    },
                },
            )
    except asyncio.exceptions.TimeoutError:
        LOGGER.warning(
            "git remote-ls time out",
            extra={"extra": {"repo_url": repo_url}},
        )
        return None

    if return_code != 0:
        return None
    return stdout.decode().split("\t")[0]


async def call_codecommit_ls_remote(
    repo_url: str,
    arn: str,
    branch: str,
    org_external_id: str,
    *,
    follow_redirects: bool = True,
) -> str | None:
    return await assume_role_and_execute_git(
        repo_url=repo_url,
        arn=arn,
        branch=branch,
        org_external_id=org_external_id,
        follow_redirects=follow_redirects,
    )
