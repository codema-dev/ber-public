def calculate_ventilation_heat_loss(
    building_volume,
    effective_air_rate_change,
):
    ventilation_heat_loss_constant = 0.33  # SEAI, DEAP 4.2.0
    return building_volume * ventilation_heat_loss_constant * effective_air_rate_change
