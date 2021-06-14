import pandas as pd
from pandas.testing import assert_series_equal

from ber_public.deap import fab


def test_calculate_fabric_heat_loss(building_area, building_fabric):
    """Output is equivalent to DEAP 4.2.0 example A"""
    floor_area, roof_area, wall_area, window_area, door_area = building_area
    (
        floor_uvalue,
        roof_uvalue,
        wall_uvalue,
        window_uvalue,
        door_uvalue,
        thermal_bridging_factor,
        *_,
    ) = building_fabric

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
    building_floor_dimensions_approx,
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
    (
        ground_floor_area,
        ground_floor_height,
        first_floor_area,
        first_floor_height,
        second_floor_area,
        second_floor_height,
        third_floor_area,
        third_floor_height,
    ) = building_floor_dimensions
    total_floor_area = (
        ground_floor_area
        + first_floor_area.fillna(0)
        + second_floor_area.fillna(0)
        + third_floor_area.fillna(0)
    )
    no_of_storeys, assumed_floor_height = building_floor_dimensions_approx

    expected_output = pd.Series([0.96], dtype="float64")

    output = fab.calculate_heat_loss_parameter(
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
        total_floor_area=total_floor_area,
        thermal_bridging_factor=thermal_bridging_factor,
        effective_air_rate_change=effective_air_rate_change,
        ground_floor_area=ground_floor_area,
        ground_floor_height=ground_floor_height,
        first_floor_area=first_floor_area,
        first_floor_height=first_floor_height,
        second_floor_area=second_floor_area,
        second_floor_height=second_floor_height,
        third_floor_area=third_floor_area,
        third_floor_height=third_floor_height,
        no_of_storeys=no_of_storeys,
        assumed_floor_height=assumed_floor_height,
    )
    rounded_output = output.round(2).astype("float64")

    assert_series_equal(rounded_output, expected_output)
