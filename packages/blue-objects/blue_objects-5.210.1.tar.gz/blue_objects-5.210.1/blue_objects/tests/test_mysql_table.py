from blue_objects.mysql.table import Table


def test_mysql_table():
    table = Table(name="tags")

    assert table.connect()

    assert table.disconnect()
