from blue_options import string

from blue_objects.mysql.cache.functions import read, write


def test_mysql_cache_write_read():
    keyword = string.random()
    value = string.random()

    assert write(keyword, value)

    value_as_read = read(keyword)

    assert value_as_read == value
