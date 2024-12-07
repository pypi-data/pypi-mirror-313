from spyral_utils.nuclear import load_target, GasTarget, SolidTarget, NuclearDataMap
from pathlib import Path
import numpy as np

GAS_TARGET_PATH: Path = Path(__file__).parent.resolve() / "gas_target.json"
SOLID_TARGET_PATH: Path = Path(__file__).parent.resolve() / "solid_target.json"
PROJ_Z: int = 1
PROJ_A: int = 1
PROJ_KE: float = 5.0  # MeV


def test_gas_target():
    PRECISION = 0.01  # 1% of LISE value
    LISE_VALUE = 0.655  # MeV

    nuc_map = NuclearDataMap()
    target = load_target(GAS_TARGET_PATH, nuc_map)

    assert isinstance(target, GasTarget)
    assert target.ugly_string == "(Gas)1H2"

    proj_data = nuc_map.get_data(PROJ_Z, PROJ_A)

    eloss = target.get_energy_loss(proj_data, PROJ_KE, np.array([1.0]))

    assert abs(eloss[0] - LISE_VALUE) < PRECISION * LISE_VALUE


def test_gas_target_range():
    PRECISION = 0.01  # 1% of LISE value
    LISE_VALUE = 4.476  # m

    nuc_map = NuclearDataMap()
    target = load_target(GAS_TARGET_PATH, nuc_map)

    assert isinstance(target, GasTarget)
    assert target.ugly_string == "(Gas)1H2"

    proj_data = nuc_map.get_data(PROJ_Z, PROJ_A)

    range = target.get_range(proj_data, PROJ_KE)

    assert abs(range - LISE_VALUE) < PRECISION * LISE_VALUE


def test_solid_target():
    PRECISION = 0.01  # 1% of LISE value
    LISE_VALUE = 0.00512  # MeV

    nuc_map = NuclearDataMap()
    target = load_target(SOLID_TARGET_PATH, nuc_map)

    assert isinstance(target, SolidTarget)
    assert target.ugly_string == "(Solid)12C1"

    proj_data = nuc_map.get_data(PROJ_Z, PROJ_A)

    eloss = target.get_energy_loss(proj_data, PROJ_KE, np.array([np.pi * 0.25]))

    assert abs(eloss[0] - LISE_VALUE) < PRECISION * LISE_VALUE


def test_solid_target_range():
    PRECISION = 0.01  # 1% of LISE value
    LISE_VALUE = 39.6871e-3  # g/cm^2

    nuc_map = NuclearDataMap()
    target = load_target(SOLID_TARGET_PATH, nuc_map)

    assert isinstance(target, SolidTarget)
    assert target.ugly_string == "(Solid)12C1"

    proj_data = nuc_map.get_data(PROJ_Z, PROJ_A)

    range = target.get_range(proj_data, PROJ_KE)
    print(target.material.density())

    assert abs(range - LISE_VALUE) < PRECISION * LISE_VALUE
