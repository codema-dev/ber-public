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
    building_volume: pd.Series,
    fabric_heat_loss: pd.Series,
    ventilation_heat_loss: pd.Series,
    total_floor_area: pd.Series,
) -> pd.DataFrame:
    heat_loss_coefficient = fabric_heat_loss + ventilation_heat_loss
    return heat_loss_coefficient / total_floor_area
