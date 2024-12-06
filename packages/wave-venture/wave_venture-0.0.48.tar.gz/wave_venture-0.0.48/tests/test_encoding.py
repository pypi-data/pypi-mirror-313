import json
import datetime

import pytest
import numpy as np
import pandas as pd
import xarray as xr

from wave_venture import serializer


@pytest.mark.parametrize(
    "input_,output",
    [
        [
            5,
            5,
        ],
        [
            "hello",
            "hello",
        ],
        [
            {"hello": "world"},
            {"hello": "world"},
        ],
        [
            datetime.datetime(2000, 1, 1),
            {"_type": "datetime", "epoch": 946684800.0},
        ],
        [
            [datetime.datetime(2000, 1, 1)],
            [{"_type": "datetime", "epoch": 946684800.0}],
        ],
        [
            np.datetime64("2000-01-01"),
            {"_type": "datetime", "epoch": 946684800.0},
        ],
        [
            np.array(np.datetime64("2000-01-01")),
            {"_type": "datetime", "epoch": 946684800.0},
        ],
        [
            np.array([np.datetime64("2000-01-01")]),
            [{"_type": "datetime", "epoch": 946684800.0}],
        ],
        [
            xr.DataArray(datetime.datetime(2000, 1, 1)),
            {"_type": "datetime", "epoch": 946684800.0},
        ],
        [
            xr.DataArray([datetime.datetime(2000, 1, 1)]),
            {
                "_type": "array",
                "fields": {
                    "unnamed": {
                        "epochs": [946684800.0],
                        "_type": "datetime"
                    }
                },
                "dimensions": [],
                "indices": {},
            },
        ],
        [
            np.array([np.datetime64("2000-01-01")]),
            [{"_type": "datetime", "epoch": 946684800.0}]
        ],
        [
            pd.Series([np.datetime64("2000-01-01")]),
            {
                "_type": "array",
                "fields": {
                    "unnamed": {
                        "epochs": [946684800.0],
                        "_type": "datetime"
                    }
                },
                "dimensions": ["index"],
                "indices": {
                    "index": {"values": [0], "_type": "number"}
                },
            },
        ],
    ],
)
def test_encoder(input_, output):
    candidate = json.loads(json.dumps(input_, cls=serializer.Encoder))
    assert candidate == output
