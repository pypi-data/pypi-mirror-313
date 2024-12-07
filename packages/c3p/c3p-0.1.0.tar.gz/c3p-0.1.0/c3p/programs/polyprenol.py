"""
Classifies: CHEBI:26199 polyprenol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_polyprenol(smiles: str):
    """
    Determines if a molecule is a polyprenol based on the general formula H-[CH2C(Me)=CHCH2]nOH
    where n > 1 (more than one isoprene unit).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyprenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of OH group
    if not any(atom.GetSymbol() == 'O' and atom.GetTotalNumHs() > 0 for atom in mol.GetAtoms()):
        return False, "No hydroxyl (OH) group found"

    # Count number of carbon atoms
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Count number of double bonds
    double_bonds = rdMolDescriptors.CalcNumAliphaticDoubleBonds(mol)
    
    # Count number of methyl groups
    methyl_pattern = Chem.MolFromSmarts("[CH3]")
    methyl_matches = len(mol.GetSubstructMatches(methyl_pattern))

    # Each isoprene unit (C5H8) should contribute:
    # - 5 carbons
    # - 1 double bond
    # - 1 methyl group
    
    # Calculate potential number of isoprene units
    # Account for the terminal CH2OH group (subtract 1 carbon)
    potential_units = (num_carbons - 1) / 5

    # Check if the numbers align with isoprene pattern
    if (potential_units % 1 != 0 or  # Must be whole number of units
        double_bonds != int(potential_units) or  # One double bond per unit
        methyl_matches < int(potential_units)):  # At least one methyl per unit
        return False, "Structure does not match polyprenol pattern"

    # Check for minimum of 2 isoprene units
    if potential_units < 2:
        return False, "Less than 2 isoprene units found"

    # Check for isoprene pattern using SMARTS
    isoprene_pattern = Chem.MolFromSmarts("CC(=C)CC")
    if not mol.HasSubstructMatch(isoprene_pattern):
        return False, "No isoprene pattern found"

    return True, f"Polyprenol with approximately {int(potential_units)} isoprene units"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26199',
                          'name': 'polyprenol',
                          'definition': 'Any member of the class of  prenols '
                                        'possessing the general formula '
                                        'H-[CH2C(Me)=CHCH2]nOH in which the '
                                        'carbon skeleton is composed of more '
                                        'than one isoprene units.',
                          'parents': ['CHEBI:26244']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.rdMolDescriptors' has no attribute "
             "'CalcNumAliphaticDoubleBonds'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}