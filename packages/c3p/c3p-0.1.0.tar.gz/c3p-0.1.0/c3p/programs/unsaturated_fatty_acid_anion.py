"""
Classifies: CHEBI:2580 unsaturated fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_unsaturated_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is an unsaturated fatty acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an unsaturated fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylate anion
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion found"
        
    # Count number of carboxylate groups
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    if len(carboxylate_matches) > 1:
        return False, "Multiple carboxylate groups found"

    # Check for carbon chain
    carbon_chain = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            carbon_chain = True
            break
    if not carbon_chain:
        return False, "No carbon chain found"

    # Check for unsaturation (C=C double bonds)
    unsaturation_patterns = [
        Chem.MolFromSmarts('C=C'),  # explicit double bond
        Chem.MolFromSmarts('C/C=C/C'),  # trans double bond
        Chem.MolFromSmarts('C/C=C\C'),  # cis double bond
    ]
    
    total_unsaturations = 0
    for pattern in unsaturation_patterns:
        if pattern is not None:  # ensure pattern was created successfully
            matches = mol.GetSubstructMatches(pattern)
            total_unsaturations += len(matches)
    
    if total_unsaturations == 0:
        return False, "No C-C unsaturation found"

    return True, f"Unsaturated fatty acid anion with {total_unsaturations} unsaturation(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2580',
                          'name': 'unsaturated fatty acid anion',
                          'definition': 'Any fatty acid anion containing at '
                                        'least one C-C unsaturated bond; '
                                        'formed by deprotonation of the '
                                        'carboxylic acid moiety.',
                          'parents': ['CHEBI:28868']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 55,
    'num_false_positives': 100,
    'num_true_negatives': 12241,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.3548387096774194,
    'recall': 0.9016393442622951,
    'f1': 0.5092592592592593,
    'accuracy': 0.9914529914529915}