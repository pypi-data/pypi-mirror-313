"""
Classifies: CHEBI:23931 epoxy monocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_epoxy_monocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is an epoxy monocarboxylic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an epoxy monocarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    
    if len(carboxylic_matches) == 0:
        return False, "No carboxylic acid group found"
    elif len(carboxylic_matches) > 1:
        return False, "Multiple carboxylic acid groups found - not a monocarboxylic acid"

    # Check for epoxide group (3-membered ring with oxygen)
    epoxide_pattern = Chem.MolFromSmarts('[C-0;R]1[O-0;R][C-0;R]1')
    epoxide_matches = mol.GetSubstructMatches(epoxide_pattern)

    if len(epoxide_matches) == 0:
        return False, "No epoxide group found"

    # If we get here, molecule has exactly one carboxylic acid and at least one epoxide
    if len(epoxide_matches) == 1:
        return True, "Contains one carboxylic acid group and one epoxide group"
    else:
        return True, f"Contains one carboxylic acid group and {len(epoxide_matches)} epoxide groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23931',
                          'name': 'epoxy monocarboxylic acid',
                          'definition': 'Monocarboxylic acids containing at '
                                        'least one epoxy group.',
                          'parents': ['CHEBI:25384', 'CHEBI:32955']},
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
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 57758,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.9090909090909091,
    'f1': 0.1652892561983471,
    'accuracy': 0.9982546786707909}