# Wave Venture TEMPEST Client
This is the Python interface to the Wave Venture software.

## Advisory
This interface is for advanced users, and those comfortable in the Python programming language.

More so, because this interface is in a pre-release state, so is sparsely documented,
and may have breaking changes to the API with each release.

Additionally, care should to be taken when manipulating and plotting Results Paths that the data structures are understood, as its possible to misunderstand the data structures and produce incorrect plots / analytics.

Please contact [support@wave-venture.com](support@wave-venture.com) if you 
need some assistance.

## Prerequisites
You will need the following prerequisites:

- A active Wave Venture software account and license.
- The [Wave Venture TEMPEST software](https://docs.wave-venture.com/download/) installed on the machine.
- To be logged in to the Wave Venture TEMPEST software with your active account.
- [Python 3.8 or higher](https://www.python.org).

## Install
```console
$ pip install wave-venture
```

## Usage
You should be able to import it with:

```python
import wave_venture as wv
```

### Document Creation
`not yet implemented.`

### Document Loading
You can load existing documents with their `uid`. This can be found in the
Software by right clicking a document in the Document History Panel.

```python
import wave_venture as wv

doc = wv.load(uid="doc_0189c12160974f8482a25611728dea82")
```

### Resolving Results Paths
You can resolve results paths on a document using the `wv.resolve` function.

This returns a `list` of `dicts`, where each `list` entry is a permutation,
and each `dict` is that permutations results path values (keyed with the 
results paths name).

Results paths can also be copy and pasted from the software from the Results 
Path Browser. 

```python
import wave_venture as wv


# Load a finalised document
doc = wv.load(uid="doc_0189c12160974f8482a25611728dea82")

all_permutations = wv.resolve(doc, """
logistics.farm.from_date
logistics.farm.to_date
logistics.farm.availability
""")

for permutation in all_permutations:
    print(permutation["uid"], permutation["logistics.farm.from_date"])
```

Results on the results paths are returned as either native Python types such as
`int`, `float`, `datetime.datetime`, etc. For any of the array/matrix-like
results, these are put into a [`xarray.Dataset`](https://docs.xarray.dev/en/stable/).

| Results Path Type | Python Type |
| --- | --- |
| `array` | `xarray.Dataset` |
| `boolean` | `bool` |
| `complex` | `complex` |
| `datetime` | `datetime.datetime` |
| `number` | `int` or `float` |
| `string` | `str` |


### Plotting
You can use the plotter build into the software from this python interface
to generate plots that you may be unable to define within the software itself.

You can also just take the results and use them with your preferred plotting 
library, such as [`matplotlib`](https://matplotlib.org).

Otherwise you can make use of the software's plotter:

#### Line
```python
wv.plot(
    "line",
    data=[
        permutation["logistics.farm.availability"],
    ],
    style={
        "graph_styles": [
            {
                "color": 0,
                "line_style": "step_left",
                "line_pen": "solid",
                "line_width": 1,
                "point_shape": None,
                "point_size": 0,
                "name": None,
            },
        ],
        "label_x": "Date & Time",
        "label_y": "Availability (%)",
    },
    config={},
    size=(1280, 720),
    save_path="./availability.png",
    save_replace_existing=True,
)
```

#### Scatter
```python
wv.plot(
    "scatter",
    data=[
        permutation["resource.variables.swh"],
        permutation["resource.variables.tp"],
    ],
    style={
        "label_x": "SWH (m)",
        "label_y": "TP (s)",
        "color": "#58abd4",
        "line_pen": "solid",
        "line_style": "none",
        "line_width": 1,
        "point_shape": "x",
        "point_size": 7
    },
    config={},
    size=(1280, 720),
    save_path="./swh_tp_scatter.png",
    save_replace_existing=True,
)
```

#### Histogram
```python
wv.plot(
    "histogram",
    data=[
        permutation["resource.variables.swh"],
    ],
    style={},
    config={
        "bin_auto": True,
        "bin_min": 0,
        "bin_max": 10,
        "bin_count": 100,
        "bin_width": 0.1,
        "count_method": "normalised",
        "four_seasons": True,
        "start_month": 1,
        "show_cdf": True
    },
    size=(1280, 720),
    save_path="./swh_histogram.png",
    save_replace_existing=True,
)
```

#### Joint-Probability
```python
wv.plot(
    "joint_probability",
    data=[
        permutation["resource.variables.swh"],
        permutation["resource.variables.tp"],
    ],
    style={
        "label_x": "SWH (m)",
        "label_y": "TP (s)"
    },
    config={
        "bin_auto_x": True,
        "bin_min_x": 0,
        "bin_max_x": 10,
        "bin_count_x": 100,
        "bin_width_x": 0.1,
        "bin_auto_y": True,
        "bin_min_y": 0,
        "bin_max_y": 10,
        "bin_count_y": 100,
        "bin_width_y": 0.1,
        "count_method": "normalised",
        "four_seasons": True,
        "start_month": 1
    },
    size=(1280, 720),
    save_path="./swh_tp_joint_probability.png",
    save_replace_existing=True,
)
```

#### Seasonality
```python
wv.plot(
    "seasonality",
    data=[
        permutation["resource.variables.swh"],
    ],
    style={
        # For Line Type Only
        "min": {
            "color": "#58abd4",
            "line_pen": "solid",
            "line_style": "line",
            "line_width": 1,
            "point_shape": "",
            "point_size": 7
        },
        "p10": { ... },
        "p25": { ... },
        "mean": { ... },
        "p50": { ... },
        "p75": { ... },
        "p90": { ... },
        "max": { ... },  
        # For Box Type Only
        "color": "#58abd4",  
        # Valid for both types
        "label_y": "swh time series",
    },
    config={
        "period": "monthly",
        "type": "line",
    },
    size=(1280, 720),
    save_path="./swh_seasonality.png",
    save_replace_existing=True,
)
```

#### Box Plot
```python
wv.plot(
    "box",
    data=[
        permutation["resource.variables.swh"],
    ],
    style={
        "color": "#58abd4",
        "label_y": "swh time series",
    },
    config={},
    size=(1280, 720),
    save_path="./swh_box.png",
    save_replace_existing=True,
)
```

#### Rose Plot
```python
wv.plot(
    "rose",
    data=[
        permutation["resource.variables.wind_direction"],
        permutation["resource.variables.wind_speed"],
    ],
    style={
        "label_angular": "Wind Direction",
        "label_radial": "Wind Speed (m/s)"
    },
    config={
        "angle_type": "cardinal",  # or "angle"
        # only for cardinal angles
        "north": 0,
        "east": 90,
        # common
        "bin_auto_angular": True,
        "bin_min_angular": 0,
        "bin_max_angular": 10,
        "bin_count_angular": 100,
        "bin_width_angular": 0.1,
        "bin_auto_radial": True,
        "bin_min_radial": 0,
        "bin_max_radial": 10,
        "bin_count_radial": 100,
        "bin_width_radial": 0.1,
        "four_seasons": True,
        "start_month": 1
    },
    size=(1280, 720),
    save_path="./swh_seasonality.png",
    save_replace_existing=True,
)
```

#### Pie Plot
```python
wv.plot(
    "rose",
    data=[
        permutation["finance.cash_flow.cash_flow_node.capex#percentile:P90#time.sum#value"],
        permutation["finance.cash_flow.cash_flow_node.opex#percentile:P90#time.sum#value"],
        permutation["finance.cash_flow.cash_flow_node.decex#percentile:P90#time.sum#value"],
    ],
    style={
    },
    config={
    },
    size=(1280, 720),
    save_path="./swh_seasonality.png",
    save_replace_existing=True,
)
```
