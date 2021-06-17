import pandas as pd
from pandas.testing import assert_series_equal
import pytest

from ber_public import calc


@pytest.fixture
def raw_ber(datadir) -> pd.DataFrame:
    return pd.read_csv(datadir / "BERPublicsearch.csv")


def test_calculate_fabric_heat_loss(raw_ber, datadir):
    expected_output = pd.read_csv(
        datadir / "fabric_heat_loss.csv", squeeze=True
    ).rename(None)
    output = calc.calculate_fabric_heat_loss(raw_ber=raw_ber)
    assert_series_equal(output, expected_output)


def test_calculate_ventilation_heat_loss(raw_ber, datadir):
    expected_output = pd.read_csv(
        datadir / "ventilation_heat_loss.csv", squeeze=True
    ).rename(None)
    output = calc.calculate_ventilation_heat_loss(raw_ber=raw_ber)
    assert_series_equal(output, expected_output)


def test_calculate_heat_loss_coefficient(raw_ber, datadir):
    expected_output = pd.read_csv(
        datadir / "heat_loss_coefficient.csv", squeeze=True
    ).rename(None)
    output = calc.calculate_heat_loss_coefficient(raw_ber=raw_ber)
    assert_series_equal(output, expected_output)


def test_calculate_heat_loss_parameter(raw_ber, datadir):
    expected_output = pd.read_csv(
        datadir / "heat_loss_parameter.csv", squeeze=True
    ).rename(None)
    output = calc.calculate_heat_loss_parameter(raw_ber=raw_ber)
    assert_series_equal(output, expected_output)


def test_calculate_annual_heat_loss(raw_ber, datadir):
    expected_output = pd.read_csv(
        datadir / "annual_heat_loss.csv", squeeze=True
    ).rename(None)
    output = calc.calculate_annual_heat_loss(raw_ber=raw_ber)
    assert_series_equal(output, expected_output)
