import pandas as pd
from pandas.testing import assert_series_equal

from ber_public.deap import vent


def test_calculate_ventilation_heat_loss(building_volume, building_fabric):
    """Output is equivalent to DEAP 4.2.0 example A"""
    effective_air_rate_change = building_fabric[-1]

    expected_output = pd.Series([53], dtype="int64")

    output = vent.calculate_ventilation_heat_loss(
        building_volume=building_volume,
        effective_air_rate_change=effective_air_rate_change,
    )
    rounded_output = output.round().astype("int64")

    assert_series_equal(rounded_output, expected_output)
