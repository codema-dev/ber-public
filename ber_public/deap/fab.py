import pandas as pd
import numpy as np


from ber_public.deap import dim
from ber_public.deap import vent


def calculate_fabric_heat_loss(
    roof_area,
    roof_uvalue,
    wall_area,
    wall_uvalue,
    floor_area,
    floor_uvalue,
    window_area,
    window_uvalue,
    door_area,
    door_uvalue,
    thermal_bridging_factor=0.05,
):
    plane_elements_area = roof_area + floor_area + door_area + wall_area + window_area
    thermal_bridging = thermal_bridging_factor * plane_elements_area
    heat_loss_via_plane_elements = (
        wall_area * wall_uvalue
        + roof_area * roof_uvalue
        + floor_area * floor_uvalue
        + window_area * window_uvalue
        + door_area * door_uvalue
    )

    return thermal_bridging + heat_loss_via_plane_elements


def calculate_heat_loss_parameter(
    roof_area,
    roof_uvalue,
    wall_area,
    wall_uvalue,
    floor_area,
    floor_uvalue,
    window_area,
    window_uvalue,
    door_area,
    door_uvalue,
    total_floor_area,
    thermal_bridging_factor,
    effective_air_rate_change,
    building_volume,
) -> pd.DataFrame:
    fabric_heat_loss = calculate_fabric_heat_loss(
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
    ventilation_heat_loss = vent.calculate_ventilation_heat_loss(
        no_sides_sheltered=no_sides_sheltered,
        building_volume=building_volume,
        no_chimneys=no_chimneys,
        no_open_flues=no_open_flues,
        no_fans=no_fans,
        no_room_heaters=no_room_heaters,
        is_draught_lobby=is_draught_lobby,
        is_permeability_tested=is_permeability_tested,
        permeability_test_result=permeability_test_result,
        no_storeys=no_storeys,
        percentage_draught_stripped=percentage_draught_stripped,
        is_floor_suspended=is_floor_suspended,
        structure_type=structure_type,
        draught_lobby_boolean=draught_lobby_boolean,
        suspended_floor_types=suspended_floor_types,
        structure_types=structure_types,
        permeability_test_boolean=permeability_test_boolean,
        ventilation_method=ventilation_method,
        heat_exchanger_efficiency=heat_exchanger_efficiency,
        ventilation_method_names=ventilation_method_names,
        ventilation_heat_loss_constant=ventilation_heat_loss_constant,
    )
    heat_loss_coefficient = fabric_heat_loss + ventilation_heat_loss
    return heat_loss_coefficient / total_floor_area
