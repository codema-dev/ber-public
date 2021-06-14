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
    heat_loss_coefficient = fabric_heat_loss + ventilation_heat_loss
    return heat_loss_coefficient / total_floor_area
