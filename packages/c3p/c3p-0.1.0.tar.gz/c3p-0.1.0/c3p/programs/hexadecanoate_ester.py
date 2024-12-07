"""
Classifies: CHEBI:25835 hexadecanoate ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hexadecanoate_ester(smiles: str):
    """
    Determines if a molecule is a hexadecanoate (palmitate) ester.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hexadecanoate ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for ester group (-C(=O)O-)
    ester_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group found"
    
    # Find all ester groups
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    for match in ester_matches:
        carbonyl_carbon = mol.GetAtomWithIdx(match[0])
        
        # Check for C16 saturated chain attached to carbonyl carbon
        chain_pattern = Chem.MolFromSmarts('CCCCCCCCCCCCCCCC(=O)O')
        if mol.HasSubstructMatch(chain_pattern):
            # Verify the chain is connected to the ester group
            chain_matches = mol.GetSubstructMatches(chain_pattern)
            for chain_match in chain_matches:
                if chain_match[-3] == match[0]:  # Check if carbonyl carbon is the same
                    # Check what's on the other side of the ester oxygen
                    oxygen_atom = mol.GetAtomWithIdx(match[2])
                    for neighbor in oxygen_atom.GetNeighbors():
                        if neighbor.GetIdx() != match[0]:  # Not the carbonyl carbon
                            if neighbor.GetSymbol() in ['C', 'c']:  # Connected to carbon
                                return True, "Hexadecanoate ester found with C16 saturated chain"
    
    return False, "No hexadecanoate ester pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25835',
                          'name': 'hexadecanoate ester',
                          'definition': 'A fatty acid ester obtained by '
                                        'condensation of the carboxy group of '
                                        'palmitic acid with a hydroxy group of '
                                        'an alcohol or phenol.',
                          'parents': ['CHEBI:35748']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 3878,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9748743718592965}