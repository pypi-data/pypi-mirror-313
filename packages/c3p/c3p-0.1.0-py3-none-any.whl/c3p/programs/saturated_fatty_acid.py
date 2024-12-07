"""
Classifies: CHEBI:26607 saturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_saturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a saturated fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a saturated fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for presence of carbon chain
    carbon_chain = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            carbon_chain = True
            break
    if not carbon_chain:
        return False, "No carbon chain found"
        
    # Check for absence of multiple bonds
    for bond in mol.GetBonds():
        if bond.GetBondType() not in [Chem.BondType.SINGLE]:
            if not (bond.GetBeginAtom().GetSymbol() == 'O' and 
                   bond.GetEndAtom().GetSymbol() == 'C' and
                   bond.GetBondType() == Chem.BondType.DOUBLE):  # Allow C=O bond
                return False, "Contains carbon-carbon multiple bonds"
                
    # Count carbons in main chain
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Check if molecule contains only C, H, O
    valid_atoms = {'C', 'H', 'O'}
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in valid_atoms:
            return False, f"Contains non C/H/O atom: {atom.GetSymbol()}"
            
    # Success - classify based on chain length
    if carbon_count < 2:
        return False, "Carbon chain too short to be a fatty acid"
    elif carbon_count <= 4:
        return True, "Short-chain saturated fatty acid"
    elif carbon_count <= 12:
        return True, "Medium-chain saturated fatty acid"
    else:
        return True, "Long-chain saturated fatty acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26607',
                          'name': 'saturated fatty acid',
                          'definition': 'Any fatty acid containing no carbon '
                                        'to carbon multiple bonds. Known to '
                                        'produce adverse biological effects '
                                        'when ingested to excess.',
                          'parents': ['CHEBI:35366']},
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
    'num_true_positives': 0,
    'num_false_positives': 89,
    'num_true_negatives': 183742,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9994614911798783}