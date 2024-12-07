"""
Classifies: CHEBI:26244 prenols
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_prenols(smiles: str):
    """
    Determines if a molecule is a prenol (alcohol with isoprene units).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a prenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of OH group(s)
    oh_pattern = Chem.MolFromSmarts("[OH]")
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "No hydroxyl group found"
        
    # Pattern for isoprene unit: -CH2-C(CH3)=CH-CH2-
    isoprene_pattern = Chem.MolFromSmarts("[CH2][C](C)=[CH][CH2]")
    if not mol.HasSubstructMatch(isoprene_pattern):
        return False, "No isoprene unit found"
        
    # Count carbons and double bonds
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_double_bonds = rdMolDescriptors.CalcNumAliphaticDoubleBonds(mol)
    
    # Check if carbon count follows isoprene rule (5n where n is number of units)
    if (num_carbons - 1) % 5 != 0:  # -1 because of terminal CH2OH
        return False, "Carbon count does not match isoprene rule"
        
    # Number of isoprene units
    n_units = (num_carbons - 1) // 5
    
    # Check number of double bonds (should be n for linear prenols)
    if num_double_bonds != n_units:
        return False, "Number of double bonds does not match expected for linear prenol"
        
    # Additional check for terminal CH2OH group
    terminal_oh_pattern = Chem.MolFromSmarts("[CH2]OH")
    if not mol.HasSubstructMatch(terminal_oh_pattern):
        return False, "No terminal CH2OH group found"
    
    return True, f"Prenol with {n_units} isoprene unit(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26244',
                          'name': 'prenols',
                          'definition': 'Any alcohol possessing the general '
                                        'formula H-[CH2C(Me)=CHCH2]nOH in '
                                        'which the carbon skeleton is composed '
                                        'of one or more isoprene units '
                                        '(biogenetic precursors of the '
                                        'isoprenoids).',
                          'parents': ['CHEBI:24913', 'CHEBI:30879']},
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