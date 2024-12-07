"""
Classifies: CHEBI:22718 benzoates
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzoates(smiles: str):
    """
    Determines if a molecule is a benzoate (deprotonated benzoic acid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a benzoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of carboxylate group [O-]C(=O)
    carboxylate_pattern = Chem.MolFromSmarts('[O-]C(=O)')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate group found"
        
    # Check for benzene ring
    benzene_pattern = Chem.MolFromSmarts('c1ccccc1')
    if not mol.HasSubstructMatch(benzene_pattern):
        return False, "No benzene ring found"
        
    # Check if carboxylate is directly attached to benzene ring
    benzoate_pattern = Chem.MolFromSmarts('c1ccccc1C(=O)[O-]')
    if not mol.HasSubstructMatch(benzoate_pattern):
        return False, "Carboxylate group not directly attached to benzene ring"
        
    # Get substituents on benzene ring
    substituents = []
    match = mol.GetSubstructMatch(benzoate_pattern)
    if match:
        ring_atoms = match[:6]  # First 6 atoms are the benzene ring
        for ring_atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(ring_atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    if neighbor.GetSymbol() != 'C' or neighbor.GetIdx() != match[6]:  # Exclude the carboxylate carbon
                        substituents.append(neighbor.GetSymbol())
    
    if substituents:
        return True, f"Benzoate with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted benzoate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22718',
                          'name': 'benzoates',
                          'definition': 'A monocarboxylic acid anion obtained '
                                        'by deprotonation of the carboxy group '
                                        'of any benzoic acid.',
                          'parents': ['CHEBI:35757', 'CHEBI:91007']},
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
    'num_true_positives': 16,
    'num_false_positives': 100,
    'num_true_negatives': 107102,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.13793103448275862,
    'recall': 1.0,
    'f1': 0.2424242424242424,
    'accuracy': 0.9990673207856889}