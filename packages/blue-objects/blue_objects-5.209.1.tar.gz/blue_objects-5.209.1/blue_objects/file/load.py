from typing import Tuple, Any, List, Any, Dict
import cv2
from copy import deepcopy
import geopandas
import geojson
import json
import numpy as np
import rasterio

from blueness import module
from blue_options import string
from blue_options.logger import crash_report

from blue_objects import NAME
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


def load(
    filename,
    ignore_error=False,
    default={},
) -> Tuple[bool, Any]:
    # https://wiki.python.org/moin/UsingPickle
    data = deepcopy(default)

    try:
        import dill

        with open(filename, "rb") as fp:
            data = dill.load(fp)

        return True, data
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load({filename}): failed.")

        return False, data


# https://stackoverflow.com/a/47792385/17619982
def load_geojson(
    filename,
    ignore_error=False,
) -> Tuple[bool, Any]:
    success = False
    data = {}

    try:
        with open(filename, "r") as fh:
            data = geojson.load(fh)

        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_geojson({filename}): failed.")

    return success, data


def load_dataframe(
    filename,
    ignore_error=False,
    log=False,
) -> Tuple[bool, Any]:
    success = False
    df = None

    try:
        import pandas

        df = pandas.read_csv(filename)

        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_dataframe({filename}): failed.")

    if success and log:
        logger.info(
            "loaded {} row(s) of {} from {}".format(
                len(df),
                ", ".join(df.columns),
                filename,
            )
        )

    return success, df


def load_geodataframe(
    filename: str,
    ignore_error: bool = False,
) -> Tuple[bool, Any]:
    success = False
    gdf = None

    try:
        gdf = geopandas.read_file(filename)
        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_geodataframe({filename}): failed.")

    return success, gdf


def load_geoimage(
    filename: str,
    ignore_error: bool = False,
    log: bool = False,
) -> Tuple[bool, np.ndarray, Dict[str, Any]]:
    success = False
    image = np.empty((0,))
    pixel_size = -1.0
    crs = "unknown"

    try:
        with rasterio.open(filename) as src:
            image = src.read()

            pixel_size = src.res

            crs = src.crs

        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_geoimage({filename}): failed.")

    if success and log:
        logger.info(
            "loaded {} @ {} m : {} from {}".format(
                string.pretty_shape_of_matrix(image),
                pixel_size,
                crs,
                filename,
            )
        )

    return (
        success,
        image,
        {
            "pixel_size": pixel_size,
            "crs": crs,
        },
    )


def load_image(
    filename,
    ignore_error=False,
    log=False,
) -> Tuple[bool, np.ndarray]:
    success = True
    image = np.empty((0,))

    try:
        image = cv2.imread(filename)

        if len(image.shape) == 3:
            if image.shape[2] == 4:
                image = image[:, :, :3]

            image = np.flip(image, axis=2)

    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_image({filename}): failed.")
        success = False

    if success and log:
        logger.info(
            "loaded {} from {}".format(
                string.pretty_shape_of_matrix(image),
                filename,
            )
        )

    return success, image


def load_json(
    filename,
    ignore_error=False,
    default={},
) -> Tuple[bool, Any]:
    success = False
    data = default

    try:
        with open(filename, "r") as fh:
            data = json.load(fh)

        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_json({filename}): failed.")

    return success, data


def load_matrix(
    filename: str,
    ignore_error=False,
    log: bool = False,
) -> Tuple[bool, np.ndarray]:
    success = True
    matrix: np.ndarray = np.empty((0,))

    try:
        matrix = np.load(filename)
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_matrix({filename}) failed.")
        success = False

    if success and log:
        logger.info(
            "loaded {} from {}".format(
                string.pretty_shape_of_matrix(matrix),
                filename,
            )
        )

    return success, matrix


def load_text(
    filename,
    ignore_error=False,
    count=-1,
    log=False,
) -> Tuple[bool, List[str]]:
    success = True
    text = []

    try:
        if count == -1:
            with open(filename, "r") as fp:
                text = fp.read()
            text = text.split("\n")
        else:
            # https://stackoverflow.com/a/1767589/10917551
            with open(filename) as fp:
                text = [next(fp) for _ in range(count)]
    except:
        success = False
        if not ignore_error:
            crash_report(f"{NAME}: load_text({filename}): failed.")

    if success and log:
        logger.info("loaded {} line(s) from {}.".format(len(text), filename))

    return success, text


def load_xml(
    filename,
    ignore_error=False,
    default={},
) -> Tuple[bool, Any]:
    success = False
    data = default

    try:
        import xml.etree.ElementTree as ET

        tree = ET.parse(filename)
        data = tree.getroot()

        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_xml({filename}): failed.")

    return success, data


def load_yaml(
    filename,
    ignore_error=False,
    default={},
) -> Tuple[bool, Any]:
    success = False
    data = default

    try:
        import yaml

        with open(filename, "r") as fh:
            data = yaml.safe_load(fh)

        success = True
    except:
        if not ignore_error:
            crash_report(f"{NAME}: load_yaml({filename}): failed.")

    return success, data
