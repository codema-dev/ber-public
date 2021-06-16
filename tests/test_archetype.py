import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

from ber_public import archetype


def test_flag_na_rows_in_columns():
    floor_areas = pd.DataFrame(
        {
            "dwelling_type": [
                "apartment",
                "detached house",
                "semi-detached house",
                "terraced house",
            ]
            * 3,
            "total_floor_area": 2 * [50, 200, 100, 80] + 4 * [np.nan],
        }
    )
    expected_output = pd.DataFrame(
        {
            "total_floor_area_isna": 8 * [False] + 4 * [True],
        },
    )

    output = archetype.flag_na_rows_in_columns(floor_areas)

    assert_frame_equal(output, expected_output)


def test_fillna_with_group_average():
    floor_areas = pd.DataFrame(
        {
            "dwelling_type": [
                "apartment",
                "detached house",
                "semi-detached house",
                "terraced house",
            ]
            * 3,
            "total_floor_area": 2 * [50, 200, 100, 80] + 4 * [np.nan],
        }
    )
    expected_output = pd.DataFrame(
        {
            "dwelling_type": 3
            * [
                "apartment",
                "detached house",
                "semi-detached house",
                "terraced house",
            ],
            "total_floor_area": pd.Series(3 * [50, 200, 100, 80], dtype="float64"),
        },
    )

    output = archetype.fillna_with_group_average(
        df=floor_areas, group_names="dwelling_type"
    )

    assert_frame_equal(output, expected_output)
