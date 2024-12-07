"""
Classifies: CHEBI:26537 retinoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_retinoid(smiles: str):
    """
    Determines if a molecule is a retinoid based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a retinoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for basic carbon skeleton
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbons < 20:
        return False, "Too few carbons for retinoid skeleton"

    # Check for cyclohexene ring
    cyclohexene_pattern = Chem.MolFromSmarts('C1CCCC=C1')
    if not mol.HasSubstructMatch(cyclohexene_pattern):
        return False, "No cyclohexene ring found"

    # Check for conjugated double bond system
    conjugated_pattern = Chem.MolFromSmarts('C=CC=CC=C')
    if not mol.HasSubstructMatch(conjugated_pattern):
        return False, "Missing conjugated double bond system"

    # Check for oxygen-containing functional groups
    has_oxygen = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            has_oxygen = True
            break
    if not has_oxygen:
        return False, "No oxygen-containing groups found"

    # Check for methyl groups
    methyl_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[CH3]')))
    if methyl_count < 3:
        return False, "Insufficient methyl groups"

    # Identify specific functional groups
    functional_groups = []
    
    # Check for carboxylic acid
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)O')):
        functional_groups.append("carboxylic acid")
    
    # Check for alcohol
    if mol.HasSubstructMatch(Chem.MolFromSmarts('CO')):
        functional_groups.append("alcohol")
        
    # Check for aldehyde
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C=O')):
        functional_groups.append("aldehyde")

    # Check for ester
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)OC')):
        functional_groups.append("ester")

    if functional_groups:
        return True, f"Retinoid with {', '.join(functional_groups)} group(s)"
    else:
        return True, "Basic retinoid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26537',
                          'name': 'retinoid',
                          'definition': 'Oxygenated derivatives of '
                                        '3,7-dimethyl-1-(2,6,6-trimethylcyclohex-1-enyl)nona-1,3,5,7-tetraene '
                                        'and derivatives thereof.',
                          'parents': ['CHEBI:23849']},
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 22128,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.8,
    'f1': 0.13559322033898305,
    'accuracy': 0.9954132565878226}