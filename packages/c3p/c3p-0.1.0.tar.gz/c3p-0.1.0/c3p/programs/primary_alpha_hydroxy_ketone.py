"""
Classifies: CHEBI:139590 primary alpha-hydroxy ketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_primary_alpha_hydroxy_ketone(smiles: str):
    """
    Determines if a molecule contains a primary alpha-hydroxy ketone group.
    This is defined as a carbonyl group and hydroxy group linked by a CH2 (methylene) group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains primary alpha-hydroxy ketone group, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for primary alpha-hydroxy ketone:
    # [OH]-[CH2]-C(=O)-[#6] 
    # This matches:
    # - OH group
    # - Connected to CH2 (methylene)
    # - Connected to C=O (carbonyl)
    # - Carbonyl connected to any carbon
    pattern = Chem.MolFromSmarts('[OH]-[CH2]-C(=O)-[#6]')
    
    if mol.HasSubstructMatch(pattern):
        matches = mol.GetSubstructMatches(pattern)
        # Get atoms involved in match
        match_atoms = matches[0]
        oh_atom = mol.GetAtomWithIdx(match_atoms[0])
        ch2_atom = mol.GetAtomWithIdx(match_atoms[1]) 
        co_atom = mol.GetAtomWithIdx(match_atoms[2])
        
        # Verify CH2 group has exactly 2 hydrogens
        if ch2_atom.GetTotalNumHs() != 2:
            return False, "Methylene carbon does not have exactly 2 hydrogens"
            
        # Verify carbonyl oxygen
        for atom in co_atom.GetNeighbors():
            if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 0:
                return True, "Contains primary alpha-hydroxy ketone group"
                
        return False, "Carbonyl group not found"
    
    return False, "No primary alpha-hydroxy ketone pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139590',
                          'name': 'primary alpha-hydroxy ketone',
                          'definition': 'An alpha-hydroxy ketone in which the '
                                        'carbonyl group and the hydroxy group '
                                        'are linked by a -CH2 (methylene) '
                                        'group.',
                          'parents': ['CHEBI:139588', 'CHEBI:15734']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 82007,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9987821957011508}