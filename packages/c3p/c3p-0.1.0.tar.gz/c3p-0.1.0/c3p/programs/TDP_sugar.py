"""
Classifies: CHEBI:22080 TDP-sugar
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_TDP_sugar(smiles: str):
    """
    Determines if a molecule is a TDP-sugar.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a TDP-sugar, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for thymine substructure
    thymine_pattern = Chem.MolFromSmarts('Cc1cn([C,c])c(=O)[nH]c1=O')
    if not mol.HasSubstructMatch(thymine_pattern):
        return False, "Missing thymine nucleobase"

    # Check for deoxyribose substructure connected to thymine
    deoxyribose_pattern = Chem.MolFromSmarts('[C,c]1[C,c][C,c](O)[C,c](CO)[O,o]1')
    if not mol.HasSubstructMatch(deoxyribose_pattern):
        return False, "Missing deoxyribose sugar"

    # Check for diphosphate linkage
    diphosphate_pattern = Chem.MolFromSmarts('OP(O)(=O)OP(O)(=O)O')
    if not mol.HasSubstructMatch(diphosphate_pattern):
        return False, "Missing diphosphate linkage"

    # Check for sugar moiety (looking for multiple OH groups and ring structure)
    # This is a simplified check for a sugar structure
    sugar_pattern = Chem.MolFromSmarts('[C,c]1[C,c][C,c][C,c][C,c][O,o]1')
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "Missing sugar moiety"

    # Count OH groups (excluding phosphate OH groups)
    oh_pattern = Chem.MolFromSmarts('[C,c]O')
    oh_matches = len(mol.GetSubstructMatches(oh_pattern))
    if oh_matches < 2:  # Most sugars have multiple OH groups
        return False, "Insufficient hydroxyl groups for sugar moiety"

    # Check connectivity - the diphosphate should connect the deoxyribose to the sugar
    # This is a complex check that would require more sophisticated analysis
    # Here we just verify basic structural elements are present

    return True, "Contains thymine, deoxyribose, diphosphate linkage and sugar moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22080',
                          'name': 'TDP-sugar',
                          'definition': 'A pyrimidine nucleotide-sugar having '
                                        'TDP as the nucleotide component '
                                        'attached to an unspecified sugar via '
                                        'an anomeric diphosphate linkage.',
                          'parents': ['CHEBI:61109']},
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
    'num_true_positives': 5,
    'num_false_positives': 86,
    'num_true_negatives': 183780,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.054945054945054944,
    'recall': 0.8333333333333334,
    'f1': 0.10309278350515463,
    'accuracy': 0.9995268447615733}