import os

from blue_options import string

from blue_objects import file, path
from blue_objects.env import (
    ABCLI_OBJECT_ROOT,
    abcli_object_name,
    ABCLI_S3_OBJECT_PREFIX,
)
from blue_objects.host import shell
from blue_objects.logger import logger


def download(
    object_name: str,
    filename: str = "",
) -> bool:
    if not ABCLI_S3_OBJECT_PREFIX:
        logger.error("ABCLI_S3_OBJECT_PREFIX is not set.")
        return False

    if not object_name:
        logger.error("object_name not found.")
        return False

    return (
        shell(
            "aws s3 cp {}/{}/{} {}".format(
                ABCLI_S3_OBJECT_PREFIX,
                object_name,
                filename,
                object_path(object_name, create=True),
            )
        )
        if filename
        else shell(
            "aws s3 sync {}/{}/ {}".format(
                ABCLI_S3_OBJECT_PREFIX,
                object_name,
                object_path(object_name, create=True),
            )
        )
    )


def list_of_files(
    object_name: str,
    cloud: bool = False,
    **kwargs,
):
    if cloud:
        from blue_objects.storage import instance as storage

        return storage.list_of_objects(
            object_name,
            **kwargs,
        )

    return file.list_of(
        os.path.join(
            ABCLI_OBJECT_ROOT,
            object_name,
            "*",
        ),
        **kwargs,
    )


def object_path(
    object_name=".",
    create=False,
):
    output = os.path.join(
        ABCLI_OBJECT_ROOT,
        abcli_object_name if object_name == "." else object_name,
    )

    if create:
        os.makedirs(output, exist_ok=True)

    return output


def path_of(
    filename,
    object_name=".",
    create=False,
):
    return os.path.join(
        object_path(object_name, create),
        filename,
    )


def signature(info=None, object_name="."):
    return [
        "{}{}".format(
            abcli_object_name if object_name == "." else object_name,
            "" if info is None else f"/{str(info)}",
        ),
        string.pretty_date(include_time=False),
        string.pretty_date(include_date=False, include_zone=True),
    ]


def unique_object(
    prefix: str = "",
    include_time: bool = True,
):
    object_name = string.pretty_date(
        as_filename=True,
        include_time=include_time,
        unique=True,
    )
    if prefix:
        object_name = f"{prefix}-{object_name}"

    path.create(object_path(object_name))

    logger.info(f"📂 {object_name}")

    return object_name


def upload(
    object_name: str,
    filename: str = "",
) -> bool:
    if not ABCLI_S3_OBJECT_PREFIX:
        logger.error("ABCLI_S3_OBJECT_PREFIX is not set.")
        return False

    if not object_name:
        logger.error("object_name not found.")
        return False

    return (
        shell(
            "aws s3 cp {} {}/{}/".format(
                path_of(filename=filename, object_name=object_name),
                ABCLI_S3_OBJECT_PREFIX,
                object_name,
            )
        )
        if filename
        else shell(
            "aws s3 sync {} {}/{}/".format(
                object_path(object_name, create=True),
                ABCLI_S3_OBJECT_PREFIX,
                object_name,
            )
        )
    )
