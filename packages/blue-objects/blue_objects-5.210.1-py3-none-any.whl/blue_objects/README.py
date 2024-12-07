from typing import List, Dict, Union, Callable
import os

from blueness import module
from blue_options import fullname

from blue_objects import NAME as MY_NAME, ICON as MY_ICON
from blue_objects import file
from blue_objects import markdown
from blue_objects.logger import logger

MY_NAME = module.name(__file__, MY_NAME)


def build(
    NAME: str,
    VERSION: str,
    REPO_NAME: str,
    items: List[str] = [],
    template_filename: str = "",
    filename: str = "",
    path: str = "",
    cols: int = 3,
    ICON: str = "",
    MODULE_NAME: str = "",
    macros: Dict[str, str] = {},
    help_function: Union[Callable[[List[str]], str], None] = None,
) -> bool:
    if path:
        if path.endswith(".md"):
            filename = path
            template_filename = file.add_suffix(path, "template")
        else:
            filename = os.path.join(path, "README.md")
            template_filename = os.path.join(path, "template.md")

    if not MODULE_NAME:
        MODULE_NAME = REPO_NAME

    logger.info(
        "{}.build: {}-{}: {}[{}]: {} -> {}".format(
            MY_NAME,
            NAME,
            VERSION,
            REPO_NAME,
            MODULE_NAME,
            template_filename,
            filename,
        )
    )

    table = markdown.generate_table(items, cols=cols) if cols > 0 else items

    signature = [
        # f'to use on [AWS SageMaker](https://aws.amazon.com/sagemaker/) replace `<plugin-name>` with "{NAME}" and follow [these instructions](https://github.com/kamangir/notebooks-and-scripts/blob/main/SageMaker.md).',
        "",
        " ".join(
            [
                f"[![pylint](https://github.com/kamangir/{REPO_NAME}/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/{REPO_NAME}/actions/workflows/pylint.yml)",
                f"[![pytest](https://github.com/kamangir/{REPO_NAME}/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/{REPO_NAME}/actions/workflows/pytest.yml)",
                f"[![bashtest](https://github.com/kamangir/{REPO_NAME}/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/{REPO_NAME}/actions/workflows/bashtest.yml)",
                f"[![PyPI version](https://img.shields.io/pypi/v/{MODULE_NAME}.svg)](https://pypi.org/project/{MODULE_NAME}/)",
                f"[![PyPI - Downloads](https://img.shields.io/pypi/dd/{MODULE_NAME})](https://pypistats.org/packages/{MODULE_NAME})",
            ]
        ),
        "",
        "built by {} [`{}`]({}), based on {}[`{}-{}`]({}).".format(
            MY_ICON,
            fullname(),
            "https://github.com/kamangir/awesome-bash-cli",
            f"{ICON} " if ICON else "",
            NAME,
            VERSION,
            f"https://github.com/kamangir/{REPO_NAME}",
        ),
    ]

    success, template = file.load_text(template_filename)
    if not success:
        return success

    content: List[str] = []
    for template_line in template:
        content_section: List[str] = [template_line]

        if "--table--" in template_line:
            content_section = table
        elif "--signature" in template_line:
            content_section = signature
        elif "--include--" in template_line:
            include_filename_relative = template_line.split(" ")[1].strip()
            include_filename = file.absolute(
                include_filename_relative,
                file.path(template_filename),
            )

            success, content_section = file.load_text(include_filename)
            if not success:
                return success

            content_section = [
                line for line in content_section if not line.startswith("used by:")
            ]

            include_title = (template_line.split(" ", 2) + ["", "", ""])[2]
            if include_title:
                content_section = [f"## {include_title}"] + content_section[1:]

            content_section += [
                "using [{}]({}).".format(
                    file.name(include_filename),
                    include_filename_relative,
                )
            ]

            logger.info(f"{MY_NAME}.build: including {include_filename} ...")
        elif "--help--" in template_line:
            if help_function is not None:
                help_command = template_line.split("--help--")[1].strip()

                tokens = help_command.strip().split(" ")[1:]

                help_content = help_function(tokens)
                if not help_content:
                    logger.warning(f"help not found: {help_command}: {tokens}")
                    return False

                logger.info(f"+= help: {help_command}")
                print(help_content)
                content_section = [
                    "```bash",
                    help_content,
                    "```",
                ]
        else:
            for macro, macro_value in macros.items():
                if macro in template_line:
                    content_section = macro_value
                    break

        content += content_section

    return file.save_text(filename, content)


def build_me() -> bool:
    from blue_objects import NAME, VERSION, REPO_NAME, ICON

    return build(
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
