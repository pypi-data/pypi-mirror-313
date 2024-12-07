from spyral_utils.nuclear.target import GasMixtureTarget, load_target
from spyral_utils.nuclear import NuclearDataMap
from pathlib import Path
import numpy as np

GAS_MIXTURE_PATH: Path = Path(__file__).parent.resolve() / "gas_mix_target.json"
nuclear_map = NuclearDataMap()
PROJ_Z: int = 1
PROJ_A: int = 1
PROJ_KE: float = 5.0  # MeV


def test_mix_target():
    PRECISION = 0.01  # 1% of LISE value
    LISE_VALUE = 0.585  # MeV
    LISE_MOLAR_MASS = 37.6
    LISE_DENSITY = 0.0001  # g/cm^3
    ERROR = PRECISION * LISE_VALUE
    target = load_target(GAS_MIXTURE_PATH, nuclear_map)

    assert isinstance(target, GasMixtureTarget)
    assert abs(target.average_molar_mass - LISE_MOLAR_MASS) < 0.1
    assert abs(target.density - LISE_DENSITY) < 0.0001
    print(f"Molar mass: {target.average_molar_mass}")
    print(f"Molar mass: {target.density}")
    print(f"Material: {target.material}")

    proj_data = nuclear_map.get_data(PROJ_Z, PROJ_A)

    eloss = target.get_energy_loss(proj_data, PROJ_KE, np.array([1.0]))

    assert abs(eloss[0] - LISE_VALUE) < ERROR
