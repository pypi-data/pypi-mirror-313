"""
Classifies: CHEBI:26519 radical
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_radical(smiles: str):
    """
    Determines if a molecule is a radical (contains an unpaired electron).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a radical, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for atoms with radical electrons
    radical_atoms = []
    for atom in mol.GetAtoms():
        num_radical_electrons = atom.GetNumRadicalElectrons()
        if num_radical_electrons > 0:
            radical_atoms.append((atom.GetSymbol(), atom.GetIdx(), num_radical_electrons))
            
    if not radical_atoms:
        return False, "No radical electrons found"
        
    # Format reason string
    reasons = []
    for symbol, idx, num_electrons in radical_atoms:
        reasons.append(f"{symbol} atom at position {idx} has {num_electrons} radical electron(s)")
        
    return True, "; ".join(reasons)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26519',
                          'name': 'radical',
                          'definition': 'A molecular entity possessing an '
                                        'unpaired electron.',
                          'parents': ['CHEBI:23367']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 21,
    'num_false_positives': 100,
    'num_true_negatives': 47538,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.17355371900826447,
    'recall': 1.0,
    'f1': 0.29577464788732394,
    'accuracy': 0.997901760423005}