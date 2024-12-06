from blue_objects.objects import unique_object

from blue_objects.mysql.tags.functions import get, set_


def test_mysql_tags_get_set():
    object_name = unique_object()

    assert set_(object_name, "this,that")

    tags_as_read = get(object_name)
    assert "this" in tags_as_read
    assert "that" in tags_as_read
