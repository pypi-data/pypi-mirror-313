from blue_objects.objects import unique_object

from blue_objects.mysql.relations.functions import set_, get, list_of


def test_mysql_cache_write_read():
    object_1 = unique_object()
    object_2 = unique_object()

    relation = list_of[0]

    assert set_(object_1, object_2, relation)

    relation_as_Read = get(object_1, object_2)

    assert relation_as_Read == relation
