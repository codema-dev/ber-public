import pandas as pd
from pandas.testing import assert_series_equal

from ber_public.deap import fab


def test_calculate_fabric_heat_loss():
    """Output is equivalent to DEAP 4.2.0 example A"""
    floor_area = pd.Series([63])
    roof_area = pd.Series([63])
    wall_area = pd.Series([85.7])
    window_area = pd.Series([29.6])
    door_area = pd.Series([1.85])
    floor_uvalue = pd.Series([0.14])
    roof_uvalue = pd.Series([0.11])
    wall_uvalue = pd.Series([0.13])
    window_uvalue = pd.Series([0.87])
    door_uvalue = pd.Series([1.5])
    thermal_bridging_factor = pd.Series([0.05])

    expected_output = pd.Series([68], dtype="int64")

    output = fab.calculate_fabric_heat_loss(
        roof_area=roof_area,
        roof_uvalue=roof_uvalue,
        wall_area=wall_area,
        wall_uvalue=wall_uvalue,
        floor_area=floor_area,
        floor_uvalue=floor_uvalue,
        window_area=window_area,
        window_uvalue=window_uvalue,
        door_area=door_area,
        door_uvalue=door_uvalue,
        thermal_bridging_factor=thermal_bridging_factor,
    )
    rounded_output = output.round().astype("int64")

    assert_series_equal(rounded_output, expected_output)


def test_calculate_heat_loss_parameter(
    building_area,
    building_fabric,
    building_floor_dimensions,
):
    """Output is equivalent to DEAP 4.2.0 example A"""
    floor_area, roof_area, wall_area, window_area, door_area = building_area
    (
        floor_uvalue,
        roof_uvalue,
        wall_uvalue,
        window_uvalue,
        door_uvalue,
        thermal_bridging_factor,
        effective_air_rate_change,
    ) = building_fabric
    total_floor_area = pd.Series([126])
    building_volume = pd.Series([321])
    expected_output = pd.Series([0.96], dtype="float64")

    output = fab.calculate_heat_loss_parameter(
        building_volume=building_volume,
        roof_area=roof_area,
        roof_uvalue=roof_uvalue,
        wall_area=wall_area,
        wall_uvalue=wall_uvalue,
        floor_area=floor_area,
        floor_uvalue=floor_uvalue,
        window_area=window_area,
        window_uvalue=window_uvalue,
        door_area=door_area,
        door_uvalue=door_uvalue,
        thermal_bridging_factor=thermal_bridging_factor,
        effective_air_rate_change=effective_air_rate_change,
        total_floor_area=total_floor_area,
    )

    assert_series_equal(output.round(2), expected_output)
