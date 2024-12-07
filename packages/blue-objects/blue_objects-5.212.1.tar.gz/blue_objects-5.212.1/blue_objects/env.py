from typing import Union
import os

from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)

HOME = os.getenv("HOME", "")

ABCLI_AWS_REGION = os.getenv(
    "ABCLI_AWS_REGION",
    "",
)

ABCLI_AWS_S3_BUCKET_NAME = os.getenv(
    "ABCLI_AWS_S3_BUCKET_NAME",
    "kamangir",
)


ABCLI_AWS_S3_PREFIX = os.getenv(
    "ABCLI_AWS_S3_PREFIX",
    "bolt",
)

ABCLI_AWS_S3_PUBLIC_BUCKET_NAME = os.getenv(
    "ABCLI_AWS_S3_PUBLIC_BUCKET_NAME",
    "",
)


abcli_object_path = os.getenv(
    "abcli_object_path",
    "",
)

ABCLI_PATH_STORAGE = os.getenv(
    "ABCLI_PATH_STORAGE",
    os.path.join(HOME, "storage"),
)

abcli_object_name = os.getenv(
    "abcli_object_name",
    "",
)

ABCLI_S3_OBJECT_PREFIX = os.getenv(
    "ABCLI_S3_OBJECT_PREFIX",
    f"s3://{ABCLI_AWS_S3_BUCKET_NAME}/{ABCLI_AWS_S3_PREFIX}",
)


ABCLI_OBJECT_ROOT = os.getenv(
    "ABCLI_OBJECT_ROOT",
    os.path.join(ABCLI_PATH_STORAGE, "abcli"),
)

abcli_path_git = os.getenv(
    "abcli_path_git",
    os.path.join(HOME, "git"),
)


ABCLI_PATH_STATIC = os.getenv(
    "ABCLI_PATH_STATIC",
    "",
)


ABCLI_PUBLIC_PREFIX = os.getenv(
    "ABCLI_PUBLIC_PREFIX",
    "",
)

VANWATCH_TEST_OBJECT = os.getenv(
    "VANWATCH_TEST_OBJECT",
    "",
)

# https://www.randomtextgenerator.com/
DUMMY_TEXT = "This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text. This is some dummy text."

ABCLI_AWS_RDS_DB = os.getenv("ABCLI_AWS_RDS_DB", "")
ABCLI_AWS_RDS_PORT = os.getenv("ABCLI_AWS_RDS_PORT", "")
ABCLI_AWS_RDS_USER = os.getenv("ABCLI_AWS_RDS_USER", "")

ABCLI_AWS_RDS_HOST = os.getenv("ABCLI_AWS_RDS_HOST", "")
ABCLI_AWS_RDS_PASSWORD = os.getenv("ABCLI_AWS_RDS_PASSWORD", "")

DATABRICKS_WORKSPACE = os.getenv("DATABRICKS_WORKSPACE", "")

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")

ABCLI_MLFLOW_EXPERIMENT_PREFIX = os.getenv("ABCLI_MLFLOW_EXPERIMENT_PREFIX", "")

BLUE_OBJECTS_FILE_LOAD_GEOIMAGE_TEST_OBJECT = os.getenv(
    "BLUE_OBJECTS_FILE_LOAD_GEOIMAGE_TEST_OBJECT",
    "",
)
BLUE_OBJECTS_FILE_LOAD_GEOIMAGE_TEST_FILENAME = os.getenv(
    "BLUE_OBJECTS_FILE_LOAD_GEOIMAGE_TEST_FILENAME",
    "",
)
