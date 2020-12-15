import importlib
from importlib import resources

import ase
from ase import Atoms
import pytest
from pytest import approx

from functionalise_mof import find_pattern_in_structure
import tests


def test_find_pattern_in_structure__find_all_carbons_in_octane():
    # CH3 CH2 CH2 CH2 CH2 CH2 CH2 CH3 #
    with importlib.resources.path(tests, "octane.xyz") as octane_path:
        structure = ase.io.read(octane_path)
    pattern = Atoms('C', positions=[(0, 0, 0)])
    match_indices, match_atoms = find_pattern_in_structure(structure, pattern)
    assert len(match_atoms) == 8
    for pattern_found in match_atoms:
        assert pattern_found.get_chemical_symbols() == ["C"]


def test_find_pattern_in_structure__find_all_ch3_in_octane():
    # CH3 CH2 CH2 CH2 CH2 CH2 CH2 CH3 #
    with importlib.resources.path(tests, "octane.xyz") as octane_path:
        structure = ase.io.read(octane_path)
    print(structure)
    pattern = Atoms('CHHH', positions=[(0, 0, 0), (-0.538, -0.635,  0.672), (-0.397,  0.993,  0.052), (-0.099, -0.371, -0.998)])
    match_indices, match_atoms = find_pattern_in_structure(structure, pattern)
    assert len(match_atoms) == 2
    for pattern_found in match_atoms:
        assert pattern_found.get_chemical_symbols() == ["C", "H", "H", "H"]
        cpos = pattern_found[0].position
        assert ((pattern_found[1].position - cpos) ** 2).sum() == approx(1.18704299, 5e-2)
        assert ((pattern_found[2].position - cpos) ** 2).sum() == approx(1.18704299, 5e-2)
        assert ((pattern_found[3].position - cpos) ** 2).sum() == approx(1.18704299, 5e-2)

def test_find_pattern_in_structure__find_all_ch2_in_octane():
    # CH3 CH2 CH2 CH2 CH2 CH2 CH2 CH3 #
    with importlib.resources.path(tests, "octane.xyz") as octane_path:
        structure = ase.io.read(octane_path)
    print(structure)
    pattern = Atoms('CHH', positions=[(0, 0, 0),(-0.1  , -0.379, -1.017), (-0.547, -0.647,  0.685)])
    match_indices, match_atoms = find_pattern_in_structure(structure, pattern)

    # there are technically 12 matches, since each CH3 makes 3 variations of CH2
    assert len(match_atoms) == 12
    for pattern_found in match_atoms:
        assert pattern_found.get_chemical_symbols() == ["C", "H", "H"]
        cpos = pattern_found[0].position
        assert ((pattern_found[1].position - cpos) ** 2).sum() == approx(1.18704299, 5e-2)
        assert ((pattern_found[2].position - cpos) ** 2).sum() == approx(1.18704299, 5e-2)

#
# def find_pattern_in_structure():
#     pass


# def test_find_pattern_in_structure__find_all_ch2_in_octane_over_pbc():
#     # CH3 CH2 CH2 CH2 C|PBC| H2 CH2 CH2 CH3 #
#     structure = ... [octane]
#     pattern = ... [ch2]
#     search_results = find_pattern_in_structure(structure, pattern)
#     assert len(search_results) == 6
