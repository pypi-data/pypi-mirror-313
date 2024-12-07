from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2

from blueness import module
from blue_options import string
from abcli.host import signature

from blue_objects import NAME
from blue_objects import file
from blue_objects.graphics.signature import add_signature, justify_text
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


def log_matrix(
    matrix: np.ndarray,
    header: List[str],
    footer: List[str],
    filename: str,
    dynamic_range: Tuple[float] = (-100, 100),
    line_width: int = 80,
    min_width: int = 1200,
    colorbar_width: int = 20,
    colormap: int = -1,  # example: cv2.COLORMAP_JET
    verbose: bool = False,
    log: bool = True,
    log_range: bool = False,
) -> bool:
    if log:
        logger.info(
            "{}.log_matrix({})".format(
                NAME,
                string.pretty_shape_of_matrix(matrix),
            )
        )

    shape_of_matrix = string.pretty_shape_of_matrix(matrix)

    range_signature: List[str] = (
        [f"range: {string.pretty_range_of_matrix(matrix)}"] if log_range else []
    )

    scale = 1
    if min_width != -1 and matrix.shape[1] < min_width and matrix.shape[1] > 0:
        scale = int(math.ceil(min_width / matrix.shape[1]))

        if verbose:
            logger.info(f"scale: {scale}")

        matrix = cv2.resize(
            matrix,
            (
                scale * matrix.shape[1],
                scale * matrix.shape[0],
            ),
            interpolation=cv2.INTER_NEAREST_EXACT,
        )

    if colormap != -1:
        normalized_matrix = (matrix - dynamic_range[0]) / (
            dynamic_range[1] - dynamic_range[0]
        )
        normalized_matrix[normalized_matrix < 0] = 0
        normalized_matrix[normalized_matrix > 1] = 1

        colored_matrix = cv2.applyColorMap(
            ((1 - normalized_matrix) * 255).astype(np.uint8),
            colormap,
        )

        gradient = (
            255
            * np.linspace(0, 1, colored_matrix.shape[0]).reshape(-1, 1)
            * np.ones((1, colorbar_width))
        ).astype(np.uint8)
        colorbar = cv2.applyColorMap(gradient, colormap)
        colored_matrix = np.hstack(
            (
                colored_matrix,
                np.zeros(
                    (colored_matrix.shape[0], colorbar_width // 2, 3),
                    dtype=np.uint8,
                ),
                colorbar,
            )
        )

        matrix = colored_matrix

    matrix = add_signature(
        matrix,
        header=[
            " | ".join(
                header
                + [
                    shape_of_matrix,
                    f"scale: {scale}X",
                ]
                + (
                    []
                    if colormap == -1
                    else [
                        "dynamic-range: ( {:.03f} , {:.03f} )".format(
                            dynamic_range[0],
                            dynamic_range[1],
                        ),
                    ]
                )
                + range_signature
            )
        ],
        footer=[" | ".join(footer + signature())],
        word_wrap=True,
        line_width=line_width,
    )

    return file.save_image(filename, matrix, log=verbose)


def log_matrix_hist(
    matrix: np.ndarray,
    dynamic_range: Tuple[float],
    filename: str,
    header: List[str] = [],
    footer: List[str] = [],
    line_width: int = 80,
    bins: int = 64,
    ylabel: str = "frequency",
    log: bool = True,
    verbose: bool = False,
) -> bool:
    if log:
        logger.info(
            "{}.log_matrix_hist({})".format(
                NAME,
                string.pretty_shape_of_matrix(matrix),
            )
        )

    plt.figure(figsize=(10, 6))
    plt.hist(
        matrix.ravel(),
        bins=bins,
        range=dynamic_range,
    )
    plt.title(
        justify_text(
            " | ".join(
                header
                + [
                    string.pretty_shape_of_matrix(matrix),
                    f"dynamic-range: {dynamic_range}",
                    f"bins: {bins}",
                ]
            ),
            line_width=line_width,
            return_str=True,
        )
    )
    plt.xlabel(
        justify_text(
            " | ".join(footer + signature()),
            line_width=line_width,
            return_str=True,
        )
    )
    plt.ylabel(ylabel)
    plt.grid(True)

    return file.save_fig(filename, log=verbose)
