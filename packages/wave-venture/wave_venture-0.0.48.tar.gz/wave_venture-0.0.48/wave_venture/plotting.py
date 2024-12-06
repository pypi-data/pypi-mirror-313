import os
import json
import tempfile
import itertools
import subprocess

import numpy as np
import pandas as pd
import xarray as xr

from PIL import Image

from wave_venture import serializer
from wave_venture import config as cfg


HERE = os.path.dirname(os.path.realpath(__file__))
WATERMARK_PATH = os.path.abspath(
    os.path.join(HERE, "resources", "wave-venture-logo.png"),
)
DEFAULT = object()


def _apply_watermark(
    *,
    image_path,
    save_path=None,
    watermark_path,
    position="bottom-left",
    scale=1,
    offset=(0, 0),
):
    watermark = Image.open(watermark_path)
    wm_width, wm_height = watermark.size
    watermark = watermark.resize(
        (int(wm_width // (1 / scale)), int(wm_height // (1 / scale)))
    )
    wm_width, wm_height = watermark.size

    base_image = Image.open(image_path)
    image_width, image_height = base_image.size

    position_options = {
        "top-left": (0, 0),
        "top-right": (image_width - wm_width, 0),
        "bottom-left": (0, image_height - wm_height),
        "bottom-right": (image_width - wm_width, image_height - wm_height),
    }

    try:
        position_anchor = position_options[position]
    except KeyError:
        raise ValueError(f"position should be one of: {position_options}")

    offset_directions = {
        "top-left": (1, 1),
        "top-right": (-1, 1),
        "bottom-left": (1, -1),
        "bottom-right": (-1, -1),
    }

    position = (
        position_anchor[0] + (offset[0] * offset_directions[position][0]),
        position_anchor[1] + (offset[1] * offset_directions[position][1]),
    )

    transparent = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(save_path or image_path)


def _normalise_data(data):
    if not isinstance(data, list):
        raise ValueError("data must be a list.")

    out = []

    for entry in data:
        if isinstance(entry, list):
            entry = xr.DataArray(entry, coords={"index": range(len(entry))})
        elif isinstance(entry, np.ndarray):
            entry = xr.DataArray(entry, coords={"index": range(len(entry))})
        elif isinstance(entry, pd.Series):
            idx_name = entry.index.name or ""
            entry = xr.DataArray(entry.values, coords={idx_name: entry.index})
        elif isinstance(entry, pd.DataFrame):
            idx_name = entry.index.name or ""
            data = {c: ([idx_name], entry[c].values) for c in entry.columns}
            entry = xr.Dataset(data, coords={idx_name: entry.index})
        elif isinstance(entry, xr.DataArray):
            pass
        elif isinstance(entry, xr.Dataset):
            pass
        else:
            pass  # good luck :crossed-fingers:

        out.append(entry)

    return out


def plot(
    plot_type: str,
    /,
    *,
    data: list,
    style: dict = None,
    config: dict = None,
    size=(1280, 720),
    image_size=None,
    save_path=None,
    save_replace_existing=False,
    scale=1,
    watermark=False,
    watermark_position=DEFAULT,
    watermark_offset=DEFAULT,
    watermark_scale=DEFAULT,
):
    # whitelisted plots that share same "data" data structures, and can be normalised
    if plot_type in {"line", "scatter", "histogram", "joint_probability", "seasonality", "box", "rose"}:
        data = _normalise_data(data)

    if style is None:
        style = {}

    if config is None:
        config = {}

    width, height = size

    # NOTE: GUI plotter can't natively handle min and max axis
    # values that are dates. We can hack this in by converting dates
    # to just the epoch timestamp
    # (without the "_type": "datetime" wrapper)
    style = json.loads(json.dumps(style, cls=serializer.Encoder))
    for bound in ["max_x", "max_y", "min_x", "min_y"]:
        if (
            isinstance(style.get(bound), dict)
            and style[bound].get("_type") == "datetime"
        ):
            style[bound] = style[bound]["epoch"]

    with tempfile.TemporaryDirectory(prefix="te-plotting") as dir_:
        style_fp = os.path.join(dir_, "style.json")
        config_fp = os.path.join(dir_, "config.json")
        data_fp = os.path.join(dir_, "data.json")

        with open(style_fp, "w+") as fp:
            json.dump(style, fp, cls=serializer.Encoder)

        with open(config_fp, "w+") as fp:
            json.dump(config, fp, cls=serializer.Encoder)

        with open(data_fp, "w+") as fp:
            json.dump(data, fp, cls=serializer.Encoder)

        args = []

        if save_replace_existing:
            args.append("--override")

        kwargs = {
            "--plot_type": plot_type,
            "--style_file": style_fp,
            "--config_file": config_fp,
            "--data_file": data_fp,
            "--window-size": f"{width}x{height}",
            "--scale": scale,
        }

        if image_size:
            kwargs["--image-size"] = image_size

        if save_path:
            kwargs["--save"] = save_path

        args = [str(i) for i in itertools.chain(args, *kwargs.items())]
        try:
            _ = subprocess.check_output([cfg.plotter, *args])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stdout.decode("utf8"))

        if watermark and save_path:
            kwargs = dict(
                image_path=save_path,
                save_path=save_path,
                watermark_path=WATERMARK_PATH,
            )
            if watermark_position is not DEFAULT:
                kwargs["position"] = watermark_position
            if watermark_offset is not DEFAULT:
                kwargs["offset"] = watermark_offset
            if watermark_scale is not DEFAULT:
                kwargs["scale"] = watermark_scale

            _apply_watermark(**kwargs)
