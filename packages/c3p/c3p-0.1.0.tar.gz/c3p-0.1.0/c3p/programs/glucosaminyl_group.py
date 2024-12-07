"""
Classifies: CHEBI:24272 glucosaminyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_glucosaminyl_group(smiles: str):
    """
    Determines if a molecule is a glucosaminyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glucosaminyl group, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Look for key structural features:
    # 1. Must have N-acetyl group (-NC(=O)CH3)
    # 2. Must have pyranose ring structure
    # 3. Must have a free position where hemiacetal OH was removed (marked with *)
    
    # Check for N-acetyl group
    nacetyl_pattern = Chem.MolFromSmarts('[NH][C](=O)[CH3]')
    if not mol.HasSubstructMatch(nacetyl_pattern):
        return False, "Missing N-acetyl group"
        
    # Check for pyranose ring
    pyranose_pattern = Chem.MolFromSmarts('[C][O][C]1[C][C][C][C][O]1')
    if not mol.HasSubstructMatch(pyranose_pattern):
        return False, "Missing pyranose ring structure"
        
    # Check for * marking position of removed hemiacetal OH
    has_star = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == '*':
            has_star = True
            break
    if not has_star:
        return False, "Missing * indicating position of removed hemiacetal OH"
        
    # Additional check for connectivity - * should be connected to pyranose ring
    star_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == '*':
            star_atom = atom
            break
            
    if star_atom:
        neighbor_atoms = [n for n in star_atom.GetNeighbors()]
        if len(neighbor_atoms) != 1:
            return False, "* must be connected to exactly one atom"
        neighbor = neighbor_atoms[0]
        if neighbor.GetSymbol() != 'C':
            return False, "* must be connected to carbon atom"
    
    return True, "Contains N-acetylglucosamine with removed hemiacetal OH"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24272',
                          'name': 'glucosaminyl group',
                          'definition': 'A glycosaminyl group obtained by '
                                        'removing the hydroxy group from the '
                                        'hemiacetal function of a glucosamine '
                                        'and, by extension, of a lower '
                                        'oligosaccharide having a glucosamine '
                                        'at the reducing end.',
                          'parents': ['CHEBI:24399']},
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 12724,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9922069825436409}