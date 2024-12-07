"""
Classifies: CHEBI:26208 polyunsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polyunsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a polyunsaturated fatty acid (PUFA).
    A PUFA contains a carboxylic acid group and multiple carbon-carbon double bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a PUFA, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Count carbon-carbon double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    if double_bonds < 2:
        return False, f"Only {double_bonds} carbon-carbon double bonds found (needs 2+ for PUFA)"

    # Check carbon chain length (should be at least 12 carbons for typical PUFAs)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Calculate the number of rings
    ring_info = mol.GetRingInfo()
    ring_count = ring_info.NumRings()
    
    # Additional information about double bond configuration
    cis_double_bonds = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C/C=C\C')))
    trans_double_bonds = len(mol.GetSubstructMatches(Chem.MolFromSmarts('C/C=C/C')))
    
    description = f"PUFA with {double_bonds} double bonds ({cis_double_bonds} cis, {trans_double_bonds} trans), "
    description += f"{carbon_count} carbons"
    if ring_count > 0:
        description += f", {ring_count} rings"

    return True, description


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26208',
                          'name': 'polyunsaturated fatty acid',
                          'definition': 'Any fatty acid containing more than '
                                        'one double bond. Acids in this group '
                                        'are reported to have cardioprotective '
                                        'effects; and levels are lowered in '
                                        'chronic fatigue syndrome.',
                          'parents': ['CHEBI:27208']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 75,
    'num_false_positives': 100,
    'num_true_negatives': 3741,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.42857142857142855,
    'recall': 0.9615384615384616,
    'f1': 0.5928853754940712,
    'accuracy': 0.9737177851492728}