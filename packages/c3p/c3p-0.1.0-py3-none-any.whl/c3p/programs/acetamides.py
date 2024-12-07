"""
Classifies: CHEBI:22160 acetamides
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_acetamides(smiles: str):
    """
    Determines if a molecule is an acetamide (compounds with general formula RNHC(=O)CH3).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an acetamide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # SMARTS pattern for acetamide group: RNHC(=O)CH3
    acetamide_pattern = Chem.MolFromSmarts('[NX3;H1][CX3](=[OX1])[CH3]')
    
    # Find matches
    matches = mol.GetSubstructMatches(acetamide_pattern)
    
    if not matches:
        return False, "No acetamide group (RNHC(=O)CH3) found"
        
    # Get the number of acetamide groups
    num_acetamides = len(matches)
    
    # Get R groups connected to NH
    r_groups = []
    for match in matches:
        n_atom = mol.GetAtomWithIdx(match[0])
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetIdx() not in match:
                r_groups.append(neighbor.GetSymbol())
                
    return True, f"Contains {num_acetamides} acetamide group(s) with R = {', '.join(set(r_groups))}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22160',
                          'name': 'acetamides',
                          'definition': 'Compounds with the general formula '
                                        'RNHC(=O)CH3.',
                          'parents': ['CHEBI:37622']},
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
    'num_true_positives': 64,
    'num_false_positives': 100,
    'num_true_negatives': 1358,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.3902439024390244,
    'recall': 0.6881720430107527,
    'f1': 0.4980544747081712,
    'accuracy': 0.9168278529980658}