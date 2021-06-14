from numpy import exp
import pandas as pd
from pandas.testing import assert_series_equal

from ber_public.deap import vent


def test_calculate_infiltration_rate_due_to_openings():
    building_volume = pd.Series([0, 100, 200])
    no_chimneys = pd.Series([0, 0, 1])
    no_open_flues = pd.Series([0, 0, 1])
    no_fans = pd.Series([0, 0, 1])
    no_room_heaters = pd.Series([0, 0, 1])
    is_draught_lobby = pd.Series(["NO", "YES", "NO"])
    draught_lobby_types = vent.DRAUGHT_LOBBY_TYPES
    expected_output = pd.Series([0, 0.05, 0.55])

    output = vent._calculate_infiltration_rate_due_to_openings(
        building_volume=building_volume,
        no_chimneys=no_chimneys,
        no_open_flues=no_open_flues,
        no_fans=no_fans,
        no_room_heaters=no_room_heaters,
        is_draught_lobby=is_draught_lobby,
        draught_lobby_types=draught_lobby_types,
    )

    assert_series_equal(output, expected_output)


def test_calculate_infiltration_rate_due_to_structure():
    pass


def test_calculate_outside_ventilation_air_rate_change():
    infiltration_rate = pd.Series([0.15, 1])
    expected_output = pd.Series([0.5, 1.25])
    output = vent._calculate_outside_ventilation_air_rate_change(infiltration_rate)
    assert_series_equal(output, expected_output)


def test_calculate_natural_ventilation_air_rate_change():
    infiltration_rate = pd.Series([2, 0.5])
    expected_output = pd.Series([2, 0.625])
    output = vent._calculate_natural_ventilation_air_rate_change(infiltration_rate)
    assert_series_equal(output, expected_output)


def test_calculate_effective_air_rate_change():

    nrows = 6
    ventilation_method = pd.Series(vent.VENTILATION_METHODS.keys())
    building_volume = pd.Series([100] * nrows)
    infiltration_rate = pd.Series([0.15] * nrows)
    heat_exchanger_efficiency = pd.Series([0.9] * nrows)
    expected_output = pd.Series([0.51125, 0.7112499999999999, 0.5, 0.5, 0.65, 0.1505])

    output = vent.calculate_effective_air_rate_change(
        ventilation_method=ventilation_method,
        building_volume=building_volume,
        infiltration_rate=infiltration_rate,
        heat_exchanger_efficiency=heat_exchanger_efficiency,
        ventilation_method_names=vent.VENTILATION_METHODS,
    )

    assert_series_equal(output, expected_output)


def test_calculate_ventilation_heat_loss(building_floor_dimensions, building_fabric):
    """Output is equivalent to DEAP 4.2.0 example A"""
    effective_air_rate_change = building_fabric[-1]
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

    expected_output = pd.Series([53], dtype="int64")

    output = vent.calculate_ventilation_heat_loss(
        effective_air_rate_change=effective_air_rate_change,
        ground_floor_area=ground_floor_area,
        ground_floor_height=ground_floor_height,
        first_floor_area=first_floor_area,
        first_floor_height=first_floor_height,
        second_floor_area=second_floor_area,
        second_floor_height=second_floor_height,
        third_floor_area=third_floor_area,
        third_floor_height=third_floor_height,
    )
    rounded_output = output.round().astype("int64")

    assert_series_equal(rounded_output, expected_output)
