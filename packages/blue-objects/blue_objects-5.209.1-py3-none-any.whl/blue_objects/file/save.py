from typing import Any, Dict, List
import cv2
import yaml
import numpy as np
import json
import dill
import pandas as pd
import geopandas as gpd
import rasterio

from blueness import module
from blue_options.logger import crash_report
from blue_options import string
from blue_options.host import is_jupyter

from blue_objects import NAME
from blue_objects.file.classes import JsonEncoder
from blue_objects.file.functions import path as file_path
from blue_objects.file.load import load_text
from blue_objects.path import create as path_create
from blue_objects.logger import logger


NAME = module.name(__file__, NAME)


def prepare_for_saving(
    filename: str,
) -> bool:
    return path_create(file_path(filename))


def finish_saving(
    success: bool,
    message: str,
    log: bool = True,
) -> bool:
    if not success:
        crash_report(f"{message}: failed.")
    elif log:
        logger.info(message)

    return success


def save(
    filename: str,
    data: Any,
    log: bool = False,
) -> bool:
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        with open(filename, "wb") as fp:
            dill.dump(data, fp)
    except:
        success = False

    return finish_saving(
        success,
        "{}.save: {} -> {}".format(
            NAME,
            type(data),
            filename,
        ),
        log,
    )


def save_csv(
    filename: str,
    df: pd.DataFrame,
    log: bool = False,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    # https://stackoverflow.com/a/10250924/10917551
    try:
        df.to_csv(filename)
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_csv: {:,}X[{}] -> {}".format(
            NAME,
            len(df),
            ",".join(list(df.columns)),
            filename,
        ),
        log,
    )


def save_fig(
    filename: str,
    log: bool = False,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    # https://stackoverflow.com/a/10250924/10917551
    try:
        import matplotlib.pyplot as plt

        if is_jupyter():
            plt.show()
        plt.savefig(filename, bbox_inches="tight")
        plt.close()
    except:
        success = False

    return finish_saving(
        success,
        f"{NAME}.save_fig -> {filename}",
        log,
    )


def save_geoimage(
    filename: str,
    image: np.ndarray,
    template_filename: str,
    log: bool = False,
    dtype: str = rasterio.float32,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        with rasterio.open(template_filename) as src:
            profile = src.profile

            profile.update(
                dtype=dtype,
                count=image.shape[2],
                nodata=0,
            )
            with rasterio.open(filename, "w", **profile) as dst:
                dst.write(image)
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_geoimage: {} -> {}".format(
            NAME,
            string.pretty_shape_of_matrix(image),
            filename,
        ),
        log,
    )


def save_geojson(
    filename: str,
    gdf: gpd.GeoDataFrame,
    log: bool = False,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        gdf.to_file(filename, driver="GeoJSON")
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_geojson: {:,}X[{}] row(s) -> {}".format(
            NAME,
            len(gdf),
            ",".join(list(gdf.columns)),
            filename,
        ),
        log,
    )


def save_image(
    filename: str,
    image: np.ndarray,
    log: bool = False,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        data = image.copy()

        if len(data.shape) == 3:
            data = np.flip(data, axis=2)

        cv2.imwrite(filename, data)
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_image: {} -> {}".format(
            NAME,
            string.pretty_shape_of_matrix(image),
            filename,
        ),
        log,
    )


def save_json(
    filename: str,
    data: Any,
    log: bool = False,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        if hasattr(data, "to_json"):
            data = data.to_json()

        with open(filename, "w") as fh:
            json.dump(
                data,
                fh,
                sort_keys=True,
                cls=JsonEncoder,
                indent=4,
                ensure_ascii=False,
            )
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_json -> {}".format(
            NAME,
            filename,
        ),
        log,
    )


def save_matrix(
    filename: str,
    matrix: np.ndarray,
    log: bool = True,
) -> bool:
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        np.save(filename, matrix)
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_matrix({}) -> {}".format(
            NAME,
            string.pretty_shape_of_matrix(matrix),
            filename,
        ),
        log,
    )


def save_text(
    filename: str,
    text: List[str],
    if_different: bool = False,
    log: bool = False,
    remove_empty_lines: bool = False,
) -> bool:
    if remove_empty_lines:
        text = [
            line
            for line, next_line in zip(text, text[1:] + ["x"])
            if line.strip() or next_line.strip()
        ]

    if if_different:
        _, content = load_text(filename, ignore_error=True)

        if "|".join([line for line in content if line]) == "|".join(
            [line for line in text if line]
        ):
            return True

    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        with open(filename, "w") as fp:
            fp.writelines([string + "\n" for string in text])
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_text: {:,} line(s) -> {}".format(
            NAME,
            len(text),
            filename,
        ),
        log,
    )


def save_yaml(
    filename: str,
    data: Dict,
    log=True,
):
    if not prepare_for_saving(filename):
        return False

    success = True
    try:
        with open(filename, "w") as f:
            yaml.dump(data, f)
    except:
        success = False

    return finish_saving(
        success,
        "{}.save_yaml: {} -> {}.".format(
            NAME,
            ", ".join(data.keys()),
            filename,
        ),
        log,
    )
