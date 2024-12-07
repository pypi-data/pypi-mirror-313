from spyral_utils.plot import Cut2D, deserialize_cut, CutHandler
from pathlib import Path
import polars as pl

CUT_JSON_PATH: Path = Path(__file__).parent.resolve() / "cut.json"
CUT_NOAXIS_JSON_PATH: Path = Path(__file__).parent.resolve() / "cut_noaxis.json"


def test_cut():
    cut = deserialize_cut(CUT_JSON_PATH)
    handler = CutHandler()
    df = pl.DataFrame({"x": [0.4, 0.2], "y": [0.4, 0.2]})

    assert isinstance(cut, Cut2D)
    assert cut.is_point_inside(0.5, 0.5)
    assert not cut.is_point_inside(-1.0, -1.0)
    df_gated = df.filter(
        pl.struct([cut.get_x_axis(), cut.get_y_axis()]).map_batches(cut.is_cols_inside)
    )
    rows = len(df_gated.select("x").to_numpy())
    assert rows == 2


def test_cut_noaxis():
    cut = deserialize_cut(CUT_NOAXIS_JSON_PATH)
    handler = CutHandler()
    df = pl.DataFrame({"x": [0.4, 0.2], "y": [0.4, 0.2]})

    assert isinstance(cut, Cut2D)
    assert cut.is_point_inside(0.5, 0.5)
    assert not cut.is_point_inside(-1.0, -1.0)
    df_gated = df.filter(pl.struct(["x", "y"]).map_batches(cut.is_cols_inside))
    rows = len(df_gated.select("x").to_numpy())
    assert rows == 2
    assert cut.is_default_x_axis()
    assert cut.is_default_y_axis()
