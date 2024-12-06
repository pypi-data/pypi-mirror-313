from abcli.tests.test_env import test_abcli_env

from blue_objects import env


def test_required_env():
    test_abcli_env()


def test_blue_objects_env():
    assert env.ABCLI_PUBLIC_PREFIX
    assert env.VANWATCH_TEST_OBJECT

    assert env.ABCLI_AWS_RDS_DB
    assert env.ABCLI_AWS_RDS_PORT
    assert env.ABCLI_AWS_RDS_USER

    assert env.ABCLI_AWS_RDS_HOST
    assert env.ABCLI_AWS_RDS_PASSWORD

    assert env.DATABRICKS_WORKSPACE
    assert env.DATABRICKS_HOST
    assert env.DATABRICKS_TOKEN

    assert env.ABCLI_MLFLOW_EXPERIMENT_PREFIX

    assert env.BLUE_OBJECTS_FILE_LOAD_GEOIMAGE_TEST_OBJECT
    assert env.BLUE_OBJECTS_FILE_LOAD_GEOIMAGE_TEST_FILENAME
