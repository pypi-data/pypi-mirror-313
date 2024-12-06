import pytest

from blue_options.options import Options

from blue_objects.objects import unique_object
from blue_objects.mlflow import objects
from blue_objects.mlflow import tags
from blue_objects.mlflow import testing


def test_from_and_to_experiment_name():
    object_name = unique_object()

    assert (
        objects.to_object_name(objects.to_experiment_name(object_name)) == object_name
    )


def test_mlflow():
    assert testing.test()


@pytest.mark.parametrize(
    ["tags_str"],
    [["x=1,y=2,z=3"]],
)
def test_mlflow_tag_set_get(tags_str: str):
    object_name = unique_object("test_mlflow_tag_set")

    assert tags.set_tags(
        object_name,
        tags_str,
        log=False,
    )

    success, tags_read = tags.get_tags(object_name)
    assert success

    tags_option = Options(tags_str)
    for keyword, value in tags_option.items():
        assert tags_read[keyword] == value
