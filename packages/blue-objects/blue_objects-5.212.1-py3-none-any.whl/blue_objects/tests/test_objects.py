import pytest

from blueness import module

from blue_objects import file, path, objects, NAME
from blue_objects.env import VANWATCH_TEST_OBJECT
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


@pytest.fixture
def test_object():
    object_name = VANWATCH_TEST_OBJECT

    assert objects.download(object_name=object_name)

    yield object_name

    logger.info(f"deleting {NAME}.test_object ...")


@pytest.mark.parametrize(
    ["object_name", "filename"],
    [[VANWATCH_TEST_OBJECT, "vancouver.geojson"]],
)
def test_objects_download(
    object_name: str,
    filename: str,
):
    filename_fullpath = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    if file.exists(filename_fullpath):
        assert file.delete(filename_fullpath)

    assert not file.exists(filename_fullpath)

    assert objects.download(object_name=object_name)

    assert file.exists(filename_fullpath)


@pytest.mark.parametrize(
    ["object_name", "filename"],
    [[VANWATCH_TEST_OBJECT, "vancouver.geojson"]],
)
def test_objects_download_filename(
    object_name: str,
    filename: str,
):
    filename_fullpath = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    if file.exists(filename_fullpath):
        assert file.delete(filename_fullpath)

    assert not file.exists(filename_fullpath)

    assert objects.download(
        object_name=object_name,
        filename=filename,
    )

    assert file.exists(filename_fullpath)


@pytest.mark.parametrize(
    ["cloud"],
    [[True], [False]],
)
def test_objects_list_of_files(
    test_object,
    cloud: bool,
):
    list_of_files = [
        file.name_and_extension(filename)
        for filename in objects.list_of_files(
            object_name=test_object,
            cloud=cloud,
        )
    ]

    assert "vancouver.json" in list_of_files


def test_object_object_path():
    object_name = objects.unique_object("test_object_object_path")
    object_path = objects.object_path(object_name, create=True)
    assert object_path
    assert path.exists(object_path)


def test_objects_path_of(test_object):
    assert file.exists(
        objects.path_of(
            object_name=test_object,
            filename="vancouver.json",
        )
    )


@pytest.mark.parametrize(
    ["prefix"],
    [["test_objects_unique_object"]],
)
def test_objects_unique_object(prefix: str):
    object_name = objects.unique_object(prefix)
    assert object_name
    assert object_name.startswith(prefix)


@pytest.mark.parametrize(
    ["filename"],
    [["vancouver.geojson"]],
)
def test_objects_upload(
    filename: str,
):
    assert objects.download(object_name=VANWATCH_TEST_OBJECT)

    object_name = objects.unique_object("test_objects_upload_filename")

    source_filename = objects.path_of(
        filename=filename,
        object_name=VANWATCH_TEST_OBJECT,
    )
    destination_filename = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    assert file.copy(source_filename, destination_filename)

    assert objects.upload(object_name=object_name)

    assert file.delete(destination_filename)
    assert not file.exists(destination_filename)

    assert objects.download(object_name=object_name)

    assert file.exists(destination_filename)


@pytest.mark.parametrize(
    ["filename"],
    [["vancouver.geojson"]],
)
def test_objects_upload_filename(
    filename: str,
):
    assert objects.download(object_name=VANWATCH_TEST_OBJECT)

    object_name = objects.unique_object("test_objects_upload_filename")

    source_filename = objects.path_of(
        filename=filename,
        object_name=VANWATCH_TEST_OBJECT,
    )
    destination_filename = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    assert file.copy(source_filename, destination_filename)

    assert objects.upload(
        object_name=object_name,
        filename=filename,
    )

    assert file.delete(destination_filename)
    assert not file.exists(destination_filename)

    assert objects.download(
        object_name=object_name,
        filename=filename,
    )

    assert file.exists(destination_filename)
