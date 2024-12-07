"""
Classifies: CHEBI:24160 galactosaminyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_galactosaminyl_group(smiles: str):
    """
    Determines if a molecule contains a galactosaminyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains a galactosaminyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of amino group (-NH2 or -NH-)
    has_amino = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() > 0:
            has_amino = True
            break
    
    if not has_amino:
        return False, "No amino group found"

    # Check for presence of acetyl group (-C(=O)CH3)
    acetyl_pattern = Chem.MolFromSmarts('NC(=O)C')
    if not mol.HasSubstructMatch(acetyl_pattern):
        return False, "No N-acetyl group found"

    # Check for pyranose ring structure (6-membered ring with oxygen)
    pyranose_pattern = Chem.MolFromSmarts('C1OCCCC1')
    if not mol.HasSubstructMatch(pyranose_pattern):
        return False, "No pyranose ring found"

    # Check for hydroxyl groups
    hydroxy_pattern = Chem.MolFromSmarts('O[H]')
    if len(mol.GetSubstructMatches(hydroxy_pattern)) < 3:
        return False, "Insufficient hydroxyl groups"

    # Check for galacto configuration (OH groups in specific positions)
    # This is a simplified check - full stereochemistry verification would be more complex
    galacto_pattern = Chem.MolFromSmarts('OC1C(O)C(NC(=O)C)C(O)C(O)C1')
    if not mol.HasSubstructMatch(galacto_pattern):
        return False, "Does not match galactosamine configuration"

    # Check for hemiacetal modification
    if '[C@@H]1' not in smiles or '[C@H]1' not in smiles:
        return False, "Missing required stereochemistry"

    # Check for glycosidic linkage (indicated by * in examples)
    if '*' in smiles:
        return True, "Galactosaminyl group with glycosidic linkage found"
    else:
        return True, "Galactosaminyl group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24160',
                          'name': 'galactosaminyl group',
                          'definition': 'A glycosaminyl group obtained by '
                                        'removing the hydroxy group from the '
                                        'hemiacetal function of a '
                                        'galactosamine and, by extension, of a '
                                        'lower oligosaccharide having a '
                                        'galactosamine at the reducing end.',
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183900,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836870524135}