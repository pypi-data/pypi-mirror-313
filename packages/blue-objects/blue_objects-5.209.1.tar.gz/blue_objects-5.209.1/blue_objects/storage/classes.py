from typing import Union, Tuple
import boto3
import botocore
import os
import os.path
import time

from blueness import module
from blue_options import string
from blue_options.logger import crash_report

from blue_objects import file, path, NAME
from blue_objects.env import (
    ABCLI_OBJECT_ROOT,
    ABCLI_AWS_S3_BUCKET_NAME,
    ABCLI_AWS_REGION,
    ABCLI_PATH_STATIC,
    ABCLI_AWS_S3_PREFIX,
    abcli_object_name,
)
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


class Storage:
    def __init__(self, bucket_name=ABCLI_AWS_S3_BUCKET_NAME):
        self.region = ABCLI_AWS_REGION

        try:
            self.s3 = boto3.client("s3", region_name=self.region)
        except:
            assert False, f"{NAME}.Storage: failed."

        self.bucket_name = bucket_name

        assert self.create_bucket()

    def create_bucket(
        self,
        bucket_name: str = "",
    ) -> bool:
        if not bucket_name:
            bucket_name = self.bucket_name

        try:
            if boto3.resource("s3").Bucket(bucket_name).creation_date is not None:
                logger.debug(f"-storage: create_bucket: {bucket_name}: already exists.")
                return True

            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.region},
            )
        except:
            crash_report(f"-storage: create_bucket: {bucket_name}: failed.")
            return False

        return True

    def download_file(
        self,
        object_name: str,
        filename: str = "",
        bucket_name: Union[None, str] = None,
        ignore_error: bool = False,
        log: bool = True,
        overwrite: bool = False,
    ) -> bool:
        if filename == "static":
            filename = os.path.join(
                ABCLI_PATH_STATIC,
                object_name.replace("/", "-"),
            )

        if filename == "object":
            filename = os.path.join(
                ABCLI_OBJECT_ROOT,
                "/".join(object_name.split("/")[1:]),
            )

        if not overwrite and file.exists(filename):
            return True

        if not path.create(file.path(filename)):
            return False

        if bucket_name is None:
            bucket_name = self.bucket_name

        success = True
        try:
            self.s3.download_file(bucket_name, object_name, filename)
        except:
            success = False

        message = "{}.Storage.downloaded_file: {}/{} -> {}".format(
            NAME,
            bucket_name,
            object_name,
            filename,
        )

        if not success:
            crash_report(f"{message}: failed.")
        elif log:
            logger.info(message)

        return success

    def list_of_objects(
        self,
        prefix: str,
        bucket_name: Union[None, str] = None,
        count: int = -1,
        suffix: str = "",
        recursive: bool = True,
        include_folders: bool = False,
    ):
        prefix = f"{ABCLI_AWS_S3_PREFIX}/{prefix}"

        if bucket_name is None:
            bucket_name = self.bucket_name

        output = []
        try:
            output = [
                string.after(object_summary.key, prefix)
                for object_summary in boto3.resource("s3")
                .Bucket(bucket_name)
                .objects.filter(Prefix=prefix)
                # .limit(count)
            ]
        except:
            crash_report("-storage: list_of_objects: failed.")

        output = [thing[1:] if thing.startswith("/") else thing for thing in output]

        if include_folders:
            output = sorted(list({thing.split("/")[0] for thing in output}))
        elif not recursive:
            output = [thing for thing in output if "/" not in thing]

        if suffix:
            output = [thing for thing in output if thing.endswith(suffix)]

        if count != -1:
            output = output[:count]

        return output

    def exists(
        self,
        object_name: str,
        bucket_name: Union[None, str] = None,
    ) -> bool:
        if bucket_name is None:
            bucket_name = self.bucket_name

        try:
            boto3.resource("s3").Object(
                bucket_name, "/".join([ABCLI_AWS_S3_PREFIX, object_name])
            ).load()
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] != "404":
                crash_report("-storage: exists: failed.")
            return False

        return True

    def upload_file(
        self,
        filename: str,
        object_name: Union[None, str] = None,
        bucket_name: Union[None, str] = None,
        overwrite: bool = False,
    ) -> Tuple[bool, str, str]:
        if bucket_name is None:
            bucket_name = self.bucket_name

        if not filename:
            logger.warning(f"{NAME}: Storage: upload_file(): upload_file: no file.")
            return False, bucket_name, ""

        if object_name is None:
            object_name = "{}/{}{}".format(
                ABCLI_AWS_S3_PREFIX,
                abcli_object_name,
                (
                    string.after(filename, abcli_object_name)
                    if abcli_object_name in filename
                    else filename
                ),
            )

        if not overwrite and self.exists(object_name):
            logger.info(f"✅ {object_name}.")
            return True, bucket_name, object_name

        success = True
        time_ = time.time()
        try:
            self.s3.upload_file(filename, bucket_name, object_name)
        except:
            success = False
        duration = time.time() - time_

        message = "{}.Storage.download_file: {}:{} -> {}/{}: {}.".format(
            NAME,
            filename,
            string.pretty_bytes(file.size(filename)),
            bucket_name,
            object_name,
            string.pretty_duration(
                duration,
                include_ms=True,
                short=True,
            ),
        )

        if not success:
            crash_report(f"{message}: failed.")
        else:
            logger.info(message)

        return success, bucket_name, object_name

    def url(self, object_name: str, filename: str) -> str:
        return "https://{}.s3.{}.amazonaws.com/{}/{}/{}".format(
            self.bucket_name,
            self.region,
            ABCLI_AWS_S3_PREFIX,
            object_name,
            filename,
        )
