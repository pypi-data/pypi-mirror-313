"""
Classifies: CHEBI:25413 monounsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_monounsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a monounsaturated fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monounsaturated fatty acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxylic acid group found"
        
    # Count number of double and triple bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    triple_bond_pattern = Chem.MolFromSmarts('C#C') 
    
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    triple_bonds = len(mol.GetSubstructMatches(triple_bond_pattern))
    
    total_unsaturations = double_bonds + triple_bonds
    
    if total_unsaturations == 0:
        return False, "No unsaturations found - saturated fatty acid"
    elif total_unsaturations > 1:
        return False, f"Found {total_unsaturations} unsaturations - polyunsaturated fatty acid"
        
    # Check for aliphatic chain
    aliphatic = True
    for atom in mol.GetAtoms():
        if atom.GetIsAromatic():
            aliphatic = False
            break
            
    if not aliphatic:
        return False, "Contains aromatic groups"
        
    # Determine type of unsaturation
    if double_bonds == 1:
        return True, "Monounsaturated fatty acid with one double bond"
    else:
        return True, "Monounsaturated fatty acid with one triple bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25413',
                          'name': 'monounsaturated fatty acid',
                          'definition': 'Any fatty acid with one double or '
                                        'triple bond in the fatty acid chain '
                                        'and singly bonded carbon atoms in the '
                                        'rest of the chain. MUFAs have '
                                        'positive effects on the '
                                        'cardiovascular system, and in '
                                        'diabetes treatment.',
                          'parents': ['CHEBI:27208']},
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
    'num_true_positives': 23,
    'num_false_positives': 100,
    'num_true_negatives': 4648,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.18699186991869918,
    'recall': 0.9583333333333334,
    'f1': 0.3129251700680272,
    'accuracy': 0.9788348700754401}