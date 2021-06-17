"""Calculate DEAP properties on the BER dataset"""
from typing import Dict

import pandas as pd
from pandas.io.formats.format import buffer_put_lines

from ber_public.deap import fab
from ber_public.deap import htuse
from ber_public.deap import vent

# Map all expected column names to the ber_public column name convention
COLUMNS_NAMES = {
    "CountyName": "countyname",
    # Area
    "WallArea": "wall_area",
    "RoofArea": "roof_area",
    "FloorArea": "floor_area",
    "WindowArea": "window_area",
    "DoorArea": "door_area",
    "GroundFloorArea": "ground_floor_area",
    "FirstFloorArea": "first_floor_area",
    "SecondFloorArea": "second_floor_area",
    "ThirdFloorArea": "third_floor_area",
    # Floor Heights
    "GroundFloorHeight": "ground_floor_height",
    "FirstFloorHeight": "first_floor_height",
    "SecondFloorHeight": "second_floor_height",
    "ThirdFloorHeight": "third_floor_height",
    # Uvalues
    "UValueWall": "wall_uvalue",
    "UValueRoof": "roof_uvalue",
    "UValueFloor": "floor_uvalue",
    "UValueWindow": "window_uvalue",
    "UvalueDoor": "door_uvalue",
    # Ventilation
    "NoOfSidesSheltered": "no_sides_sheltered",
    "NoOfChimneys": "no_chimneys",
    "NoOfOpenFlues": "no_open_flues",
    "NoOfFansAndVents": "no_fans_and_vents",
    "NoOfFluelessGasFires": "no_flueless_gas_fires",
    "DraftLobby": "is_draft_lobby",
    "PermeabilityTest": "is_permeability_tested",
    "PermeabilityTestResult": "permeability_test_result",
    "NoStoreys": "no_storeys",
    "PercentageDraughtStripped": "percentage_draught_stripped",
    "SuspendedWoodenFloor": "is_suspended_wooden_floor",
    "StructureType": "structure_type",
    "VentilationMethod": "ventilation_method",
    "HeatExchangerEff": "heat_exchanger_efficiency",
}


def _extract_expected_columns(
    raw_ber: pd.DataFrame, column_names: Dict[str, str] = COLUMNS_NAMES
) -> pd.DataFrame:
    expected_column_names = list(column_names.keys())
    return raw_ber[expected_column_names].copy().rename(columns=column_names)


def calculate_fabric_heat_loss(
    raw_ber: pd.DataFrame, column_names: Dict[str, str] = COLUMNS_NAMES
) -> pd.Series:
    building_stock = raw_ber.copy().rename(columns=column_names)
    return fab.calculate_fabric_heat_loss(
        roof_area=building_stock["roof_area"],
        roof_uvalue=building_stock["roof_uvalue"],
        wall_area=building_stock["wall_area"],
        wall_uvalue=building_stock["wall_uvalue"],
        floor_area=building_stock["floor_area"],
        floor_uvalue=building_stock["floor_uvalue"],
        window_area=building_stock["window_area"],
        window_uvalue=building_stock["window_uvalue"],
        door_area=building_stock["door_area"],
        door_uvalue=building_stock["door_uvalue"],
        thermal_bridging_factor=0.05,
    )


def calculate_ventilation_heat_loss(
    raw_ber: pd.DataFrame, column_names: Dict[str, str] = COLUMNS_NAMES
) -> pd.Series:
    building_stock = raw_ber.copy().rename(columns=column_names)
    building_volume = (
        building_stock["ground_floor_area"].fillna(0)
        * building_stock["ground_floor_height"].fillna(0)
        + building_stock["first_floor_area"].fillna(0)
        * building_stock["first_floor_height"].fillna(0)
        + building_stock["second_floor_area"].fillna(0)
        * building_stock["second_floor_height"].fillna(0)
        + building_stock["third_floor_area"].fillna(0)
        * building_stock["third_floor_height"].fillna(0)
    )
    infiltration_rate = vent.calculate_infiltration_rate(
        no_sides_sheltered=building_stock["no_sides_sheltered"],
        building_volume=building_volume,
        no_chimneys=building_stock["no_chimneys"],
        no_open_flues=building_stock["no_open_flues"],
        no_fans=building_stock["no_fans_and_vents"],
        no_room_heaters=building_stock["no_flueless_gas_fires"],
        is_draught_lobby=building_stock["is_draft_lobby"],
        is_permeability_tested=building_stock["is_permeability_tested"],
        permeability_test_result=building_stock["permeability_test_result"],
        no_storeys=building_stock["no_storeys"],
        percentage_draught_stripped=building_stock["percentage_draught_stripped"],
        is_floor_suspended=building_stock["is_suspended_wooden_floor"],
        structure_type=building_stock["structure_type"],
    )
    effective_air_rate_change = vent.calculate_effective_air_rate_change(
        ventilation_method=building_stock["ventilation_method"],
        building_volume=building_volume,
        infiltration_rate=infiltration_rate,
        heat_exchanger_efficiency=building_stock["heat_exchanger_efficiency"],
    )

    return vent.calculate_ventilation_heat_loss(
        building_volume=building_volume,
        effective_air_rate_change=effective_air_rate_change,
        ventilation_heat_loss_constant=0.33,
    )


def calculate_heat_loss_coefficient(
    raw_ber: pd.DataFrame, column_names: Dict[str, str] = COLUMNS_NAMES
) -> pd.Series:
    fabric_heat_loss = calculate_fabric_heat_loss(
        raw_ber=raw_ber, column_names=column_names
    )
    ventilation_heat_loss = calculate_ventilation_heat_loss(
        raw_ber=raw_ber, column_names=column_names
    )
    return fabric_heat_loss + ventilation_heat_loss


def _calculate_total_floor_area(
    building_stock: pd.DataFrame,
) -> pd.Series:
    return (
        building_stock["ground_floor_area"].fillna(0)
        + building_stock["first_floor_area"].fillna(0)
        + building_stock["second_floor_area"].fillna(0)
        + building_stock["third_floor_area"].fillna(0)
    )


def calculate_heat_loss_parameter(
    raw_ber: pd.DataFrame, column_names: Dict[str, str] = COLUMNS_NAMES
) -> pd.Series:
    building_stock = raw_ber.copy().rename(columns=column_names)
    heat_loss_coefficient = calculate_heat_loss_coefficient(
        raw_ber=raw_ber, column_names=column_names
    )
    total_floor_area = _calculate_total_floor_area(
        building_stock=building_stock,
    )
    assert total_floor_area[
        total_floor_area.isna()
    ].empty, "Remove or replace zero floor areas!"
    return heat_loss_coefficient / total_floor_area


def calculate_annual_heat_loss(
    raw_ber: pd.DataFrame, column_names: Dict[str, str] = COLUMNS_NAMES
) -> pd.Series:
    heat_loss_coefficient = calculate_heat_loss_coefficient(
        raw_ber=raw_ber, column_names=column_names
    )
    return htuse.calculate_heat_loss_per_year(heat_loss_coefficient)
