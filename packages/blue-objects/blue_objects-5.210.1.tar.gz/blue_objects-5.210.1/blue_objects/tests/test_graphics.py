import pytest

from blueness import module

from blue_objects import file, objects, NAME
from blue_objects.env import VANWATCH_TEST_OBJECT
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


@pytest.fixture
def test_image():
    object_name = VANWATCH_TEST_OBJECT

    assert objects.download(object_name)

    success, matrix = file.load_image(
        objects.path_of(
            "Victoria41East.jpg",
            object_name,
        )
    )
    assert success

    yield matrix

    logger.info(f"deleting {NAME}.test_object ...")
