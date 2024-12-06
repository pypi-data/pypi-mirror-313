from typing import List, Union
import numpy as np
from functools import reduce
import textwrap

from blueness import module

from blue_objects import NAME
from blue_objects.graphics.text import render_text

NAME = module.name(__file__, NAME)


def justify_text(
    text: Union[List[str], str],
    line_width: int = 80,
    return_str: bool = False,
) -> Union[List[str], str]:
    output = reduce(
        lambda x, y: x + y,
        [
            textwrap.wrap(line, width=line_width)
            for line in (text if isinstance(text, list) else [text])
        ],
    )

    return "\n".join(output) if return_str else output


def add_signature(
    image: np.ndarray,
    header: List[str],
    footer: List[str] = [],
    word_wrap: bool = True,
    line_width: int = 80,
) -> np.ndarray:
    if image is None or not image.shape:
        return image

    if word_wrap:
        header = justify_text(header, line_width=line_width)
        footer = justify_text(footer, line_width=line_width)

    justify_line = lambda line: (
        line if len(line) >= line_width else line + (line_width - len(line)) * " "
    )

    return np.concatenate(
        [
            render_text(
                text=justify_line(line),
                image_width=image.shape[1],
                color_depth=image.shape[2],
            )
            for line in header
        ]
        + [image]
        + [
            render_text(
                text=justify_line(line),
                image_width=image.shape[1],
                color_depth=image.shape[2],
            )
            for line in footer
        ],
        axis=0,
    )
