from blue_objects import NAME, VERSION, DESCRIPTION, REPO_NAME
from blueness.pypi import setup

setup(
    filename=__file__,
    repo_name=REPO_NAME,
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[
        NAME,
        f"{NAME}.file",
        f"{NAME}.graphics",
        f"{NAME}.help",
        f"{NAME}.host",
        f"{NAME}.logger",
        f"{NAME}.metadata",
        f"{NAME}.mlflow",
        f"{NAME}.mysql",
        f"{NAME}.mysql.cache",
        f"{NAME}.mysql.relations",
        f"{NAME}.mysql.tags",
        f"{NAME}.storage",
        f"{NAME}.tests",
    ],
    include_package_data=True,
    package_data={
        NAME: [
            "config.env",
            "sample.env",
            ".abcli/**/*.sh",
        ],
    },
)
