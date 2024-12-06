import json
import datetime

import numpy as np
import pandas as pd
import xarray as xr

from wave_venture import utils


def _decode_array_values(data):
    _type = data["_type"]

    if _type in {"number", "fraction", "degree", "radian", "boolean"}:
        return data["values"]
    elif _type == "complex":
        return np.array(data["real"]) + np.array(data["imag"]) * 1j
    elif _type == "string":
        return data["values"]
    elif _type == "datetime":
        return pd.to_datetime(data["epochs"], unit="s")
    else:
        raise NotImplementedError(data)


def decoder(obj):
    _type = obj.get("_type", None)  # safely get _type if it exists

    if _type == "datetime" and "epoch" in obj:
        return utils.from_epoch(obj["epoch"])
    elif _type == "array":
        array = xr.Dataset(
            data_vars={
                name: (obj["dimensions"], _decode_array_values(data))
                for name, data in obj["fields"].items()
            },
            coords={
                name: _decode_array_values(data)
                for name, data in obj["indices"].items()
            },
        )
        for name in obj["indices"].keys():
            array[name].attrs["interpolation"] = obj["indices"][name].get("interpolation")
            array[name].attrs["_type"] = obj["indices"][name]["_type"]
        for name in obj["fields"].keys():
            array[name].attrs["_type"] = obj["fields"][name]["_type"]
        return array
    else:
        return obj


_TYPE_CHECKS = {
    "number": lambda x: np.issubdtype(x.dtype, np.number),
    "fraction": lambda x: np.issubdtype(x.dtype, np.number),
    "degree": lambda x: np.issubdtype(x.dtype, np.number),
    "radian": lambda x: np.issubdtype(x.dtype, np.number),
    "datetime": lambda x: x.dtype == np.dtype("<M8[ns]"),
    "string": lambda x: pd.api.types.is_string_dtype(x),
    "boolean": lambda x: np.issubdtype(x, np.dtype("bool")),
    "complex": lambda x: np.issubdtype(x, np.dtype("complex")),
}

_TYPE_ENCODER = {
    "number": lambda x: {"values": x.to_numpy().tolist()},
    "fraction": lambda x: {"values": x.to_numpy().tolist()},
    "degree": lambda x: {"values": x.to_numpy().tolist()},
    "radian": lambda x: {"values": x.to_numpy().tolist()},
    "datetime": lambda x: {"epochs": (x.to_numpy().view(np.int64) / 10 ** 9).tolist()},
    "string": lambda x: {"values": list(map(str, x.to_numpy().tolist()))},
    "boolean": lambda x: {"values": x.to_numpy().tolist()},
    "complex": lambda x: {"real": x.real.to_numpy().tolist(), "imag": x.imag.to_numpy().tolist()},
}


def _encode_array_values(xarray, *, name):
    # get _type
    if (
        name in xarray.data_vars
        and "_type" in xarray.data_vars[name].attrs
    ):
        _type = xarray.data_vars[name].attrs["_type"]
    elif (
        name in xarray.coords
        and "_type" in xarray.coords[name].attrs
    ):
        _type = xarray.coords[name].attrs["_type"]
    else:
        _type = None

    if _type is None:
        # NOTE: order important here, as first match wins the inference battle
        inferable_type = ["datetime", "complex", "boolean", "number", "string"]
        for candidate_type in inferable_type:
            if _TYPE_CHECKS[candidate_type](xarray[name]):
                _type = candidate_type
                break

    if _type is None:
        raise ValueError(
            f"Unable to find associated _type for '{name}' "
            f"or able to infer a _type from its dtype '{xarray[name].dtype}'. "
        )

    if not _TYPE_CHECKS[_type](xarray[name]):
        raise ValueError(f"Values for '{name}' dont look like '{_type}'")

    result = _TYPE_ENCODER[_type](xarray[name])
    result = {**result, "_type": _type}

    # preserve interpolation attrs if exist
    if name in set(xarray.coords):
        if interpolation := xarray[name].attrs.get("interpolation"):
            result["interpolation"] = interpolation

    return result


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "shape") and obj.shape == ():
            # unwraps zero-shape scalars like np.array(1) into 1
            return obj.item()
        elif isinstance(obj, datetime.datetime) and utils.is_naive(obj):
            return {
                "_type": "datetime",
                "epoch": utils.to_epoch(obj),
            }
        elif isinstance(obj, datetime.datetime) and utils.is_utc(obj):
            return {
                "_type": "datetime",
                "epoch": utils.to_epoch(obj),
            }
        elif isinstance(obj, datetime.datetime):
            raise TypeError("Encountered unexpected timezone aware datetime.")
        elif isinstance(obj, np.datetime64):
            return self.default(pd.to_datetime(obj).to_pydatetime())
        elif isinstance(obj, pd.Timestamp):
            return self.default(obj.to_pydatetime())
        elif isinstance(obj, datetime.date):
            return self.default(datetime.datetime(obj.year, obj.month, obj.day))
        elif isinstance(obj, complex):
            return {"_type": "complex", "real": obj.real, "imag": obj.imag}
        # just those arrays that can be a scalar,
        # i.e. np.array(1), pd.DataArray(1)
        elif isinstance(obj, (np.ndarray, xr.DataArray)) and obj.shape == ():
            if np.issubdtype(obj.dtype, np.datetime64):
                # calling .item on a datetime scalar will return its
                # epoch float, we dont want that, we want a datetime
                # we can encode appropriately with _type: datetime.
                if hasattr(obj, "to_numpy"):
                    obj = obj.to_numpy()
                scalar = pd.to_datetime(obj).to_pydatetime()
            else:
                scalar = obj.item()
            return self.default(scalar)
        elif isinstance(obj, np.ndarray):
            return np.vectorize(self.default)(obj).tolist()
        elif isinstance(obj, (xr.Dataset, xr.DataArray, pd.Series, pd.DataFrame)):
            if isinstance(obj, xr.DataArray):
                obj = obj.to_dataset(name="unnamed")
            elif isinstance(obj, pd.Series):
                obj = obj.to_xarray().to_dataset(name="unnamed")
            elif isinstance(obj, pd.DataFrame):
                obj = obj.to_xarray()

            return {
                "_type": "array",
                "fields": {
                    column: _encode_array_values(obj, name=column)
                    for column in obj.data_vars
                },
                "dimensions": list(obj.coords),
                "indices": {
                    coord: _encode_array_values(obj, name=coord)
                    for coord in list(obj.coords)
                },
            }
        else:
            return json.JSONEncoder.default(self, obj)
