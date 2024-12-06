import os
from typing import Union, Dict, List
from functools import reduce

from blue_objects import file
from blue_objects.mysql.table import Table
from blue_objects.logger import logger


_, inverse_of = file.load_json(
    os.path.join(
        file.path(__file__),
        "relations.json",
    )
)
inverse_of.update({inverse_of[relation]: relation for relation in inverse_of})
inverse_of[""] = ""

list_of = sorted(list(set(list(inverse_of.keys()) + list(inverse_of.values()))))


columns = "object_1,object_2,relation,timestamp".split(",")


def clone(
    object_1: str,
    object_2: str,
) -> bool:
    return reduce(
        lambda x, y: x and y,
        [
            reduce(
                lambda x, y: x and y,
                [set_(object_2, object, relation) for object in object_list],
                True,
            )
            for relation, object_list in search(object_1).items()
        ],
        True,
    )


def create() -> bool:
    return Table.Create(
        "relations",
        [
            "object_1 VARCHAR(256) NOT NULL",
            "object_2 VARCHAR(256) NOT NULL",
            "relation VARCHAR(256) NOT NULL",
        ],
    )


def get(
    object_1: str,
    object_2: str,
) -> str:
    if object_1 > object_2:
        return inverse_of[get(object_1=object_2, object_2=object_1)]

    table = Table(name="relations")

    if not table.connect():
        return ""

    success, output = table.execute(
        "SELECT r.relation "
        "FROM abcli.relations r "
        "INNER JOIN ( "
        "SELECT MAX(timestamp) AS max_timestamp "
        "FROM abcli.relations "
        f'WHERE object_1="{object_1}" AND object_2="{object_2}" '
        ") rm "
        "ON r.timestamp=rm.max_timestamp "
        f'WHERE object_1="{object_1}" AND object_2="{object_2}";'
    )
    if not success:
        return ""

    if not table.disconnect():
        return ""

    return "" if not output else output[-1][0]


def search(
    object: str,
    relation: str = "",
    count: int = -1,
) -> Union[
    Dict[str, List[str]],
    List[str],
]:
    table = Table(name="relations")

    output = [] if relation else {}

    if not table.connect():
        return output

    success, output_right = table.execute(
        "SELECT r.relation, r.object_2 "
        "FROM abcli.relations r "
        "INNER JOIN (  "
        "SELECT object_2, MAX(timestamp) AS max_timestamp "
        "FROM abcli.relations "
        f'WHERE object_1="{object}" GROUP BY object_2'
        ") rm  "
        "ON r.timestamp=rm.max_timestamp "
        f'WHERE object_1="{object}"; '
    )
    if not success:
        return {}

    success, output_left = table.execute(
        "SELECT r.relation, r.object_1 "
        "FROM abcli.relations r "
        "INNER JOIN (  "
        "SELECT object_1, MAX(timestamp) AS max_timestamp "
        "FROM abcli.relations "
        f'WHERE object_2="{object}" GROUP BY object_1'
        ") rm  "
        "ON r.timestamp=rm.max_timestamp "
        f'WHERE object_2="{object}"; '
    )
    if not success:
        return output

    if not table.disconnect():
        return output

    raw_output = {thing[1]: thing[0] for thing in output_right}
    raw_output.update({thing[1]: inverse_of[thing[0]] for thing in output_left})

    raw_output = {thing: relation for thing, relation in raw_output.items() if relation}

    output = {}
    for object_, relation_ in raw_output.items():
        output[relation_] = output.get(relation_, []) + [object_]

    if not relation:
        return output

    output = output.get(relation, [])

    if count != -1:
        output = output[-count:]

    return output


def set_(
    object_1: str,
    object_2: str,
    relation: str,
) -> bool:
    if relation not in list_of:
        logger.error(f"-relations: set: {relation}: relation not found.")
        return False

    if object_1 > object_2:
        return set_(object_2, object_1, inverse_of[relation])

    table = Table(name="relations")

    if not table.connect():
        return False

    if not table.insert(
        ["object_1", "object_2", "relation"],
        [object_1, object_2, relation],
    ):
        return False

    if not table.disconnect():
        return False

    logger.info("{} ={}=> {}".format(object_1, relation if relation else "X", object_2))

    return True
