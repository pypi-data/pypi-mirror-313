from typing import List, Union, Tuple, Any
import pymysql

from blueness import module

from blue_objects import NAME
from blue_objects.env import (
    ABCLI_AWS_RDS_DB,
    ABCLI_AWS_RDS_PORT,
    ABCLI_AWS_RDS_USER,
    ABCLI_AWS_RDS_HOST,
    ABCLI_AWS_RDS_PASSWORD,
)
from blue_options.logger import crash_report

NAME = module.name(__file__, NAME)


class Table:
    def __init__(self, name):
        self.name = name

        self.db = ABCLI_AWS_RDS_DB
        self.port = int(ABCLI_AWS_RDS_PORT)
        self.user = ABCLI_AWS_RDS_USER

        self.host = ABCLI_AWS_RDS_HOST
        self.password = ABCLI_AWS_RDS_PASSWORD

        self.connection = None

    def connect(
        self,
        create_command: str = "",
    ) -> bool:
        if self.connection is not None:
            self.disconnect()

        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.db,
            )
        except:
            crash_report(f"-{NAME}: connect: failed on host: {self.host}.")
            return False

        return True if not create_command else self.create(create_command)

    @staticmethod
    def Create(
        table_name: str,
        create_command: List[str],
    ) -> bool:
        table = Table(name=table_name)

        return table.disconnect() if table.connect(create_command) else False

    def create(
        self,
        create_command: List[str],
    ) -> bool:
        return self.execute(
            "CREATE TABLE IF NOT EXISTS {} ({})".format(
                self.name,
                ",".join(
                    [
                        "id INT(24) NOT NULL AUTO_INCREMENT",
                        "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                    ]
                    + create_command
                    + ["PRIMARY KEY (`id`)", "INDEX `index_timestamp` (`timestamp`)"]
                ),
            ),
            commit=True,
        )

    def disconnect(self) -> bool:
        if self.connection is None:
            return True

        success = True
        try:
            self.connection.close()
        except:
            crash_report(f"-{NAME}: disconnect: failed.")
            success = False

        self.connection = None
        return success

    def drop(self) -> bool:
        return self.execute(f"DROP table {self.name};")

    def execute(
        self,
        sql: str,
        commit: bool = False,
        returns_output: bool = True,
    ) -> Union[bool, Tuple[bool, Any]]:
        output = []
        success = False
        try:
            with self.connection.cursor() as cursor:
                if isinstance(sql, tuple):
                    cursor.execute(sql[0], sql[1])
                else:
                    cursor.execute(sql)

                if returns_output:
                    output = cursor.fetchall()

                if commit:
                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    self.connection.commit()

            success = True
        except:
            crash_report(f"-{NAME}: execute({sql}): failed.")

        return (success, output) if returns_output else success

    def insert(
        self,
        columns: List[str],
        values: List[Any],
    ) -> bool:
        return self.execute(
            (
                f"INSERT INTO {self.name}"
                + " ("
                + ", ".join(columns)
                + ") VALUES ("
                + ", ".join(len(columns) * ["%s"])
                + ")",
                values,
            ),
            commit=True,
            returns_output=True,
        )
