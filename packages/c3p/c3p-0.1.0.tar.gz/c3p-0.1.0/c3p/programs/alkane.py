"""
Classifies: CHEBI:18310 alkane
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_alkane(smiles: str):
    """
    Determines if a molecule is an alkane (acyclic saturated hydrocarbon with formula CnH2n+2).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains only C and H atoms
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if not all(symbol in ['C', 'H'] for symbol in atoms):
        return False, "Contains atoms other than C and H"

    # Check if molecule is cyclic
    rings = mol.GetRingInfo()
    if rings.NumRings() > 0:
        return False, "Contains rings"

    # Check if all carbons are sp3 hybridized (saturated)
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            if atom.GetHybridization() != Chem.HybridizationType.SP3:
                return False, "Contains unsaturated carbons"

    # Count carbons and hydrogens
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    total_hydrogens = sum(atom.GetTotalNumHs() for atom in mol.GetAtoms())

    # Check if formula matches CnH2n+2
    expected_hydrogens = 2 * num_carbons + 2
    if total_hydrogens != expected_hydrogens:
        return False, f"Formula does not match CnH2n+2 pattern (expected {expected_hydrogens} H, found {total_hydrogens} H)"

    # Get branching information
    branching_points = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'C']) > 2)
    
    if branching_points > 0:
        return True, f"Branched alkane with {num_carbons} carbons and {branching_points} branching points"
    else:
        return True, f"Straight-chain alkane with {num_carbons} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18310',
                          'name': 'alkane',
                          'definition': 'An acyclic branched or unbranched '
                                        'hydrocarbon having the general '
                                        'formula CnH2n+2, and therefore '
                                        'consisting entirely of hydrogen atoms '
                                        'and saturated carbon atoms.',
                          'parents': ['CHEBI:24632', 'CHEBI:33653']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.Descriptors' has no "
               "attribute 'NumImplicitHs'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 8,
    'num_true_negatives': 183786,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6363636363636364,
    'recall': 1.0,
    'f1': 0.7777777777777778,
    'accuracy': 0.9999564763231198}