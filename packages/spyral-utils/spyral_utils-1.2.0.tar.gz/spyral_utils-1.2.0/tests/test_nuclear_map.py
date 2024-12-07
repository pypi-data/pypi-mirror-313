from spyral_utils.nuclear import NuclearDataMap


def test_nuclear_map():
    nuc_map = NuclearDataMap()

    carbon = nuc_map.get_data(6, 12)

    assert carbon.isotopic_symbol == "12C"
