"""
Classifies: CHEBI:25513 neutral glycosphingolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_neutral_glycosphingolipid(smiles: str):
    """
    Determines if a molecule is a neutral glycosphingolipid.
    A neutral glycosphingolipid contains unsubstituted glycosyl moieties attached to a ceramide core.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a neutral glycosphingolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for ceramide core
    ceramide_substructure = "[CH2]OC1O[CH]([CH]O)[CH]([CH]O)[CH]([CH]1O)O" # Basic ceramide core pattern
    ceramide_pattern = Chem.MolFromSmarts(ceramide_substructure)
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "No ceramide core found"

    # Check for glycosyl groups
    glycosyl_substructure = "OC1[CH]([CH]O)[CH]([CH]O)[CH]O[CH]1" # Basic glycosyl pattern
    glycosyl_pattern = Chem.MolFromSmarts(glycosyl_substructure)
    if not mol.HasSubstructMatch(glycosyl_pattern):
        return False, "No glycosyl groups found"

    # Check for absence of charged/acidic groups that would make it non-neutral
    charged_groups = [
        "[O-]", # Carboxylate
        "[N+]", # Quaternary amine 
        "[S](=O)(=O)[O-]", # Sulfate
        "[P](=O)([O-])[O-]" # Phosphate
    ]
    
    for group in charged_groups:
        pattern = Chem.MolFromSmarts(group)
        if mol.HasSubstructMatch(pattern):
            return False, f"Contains charged group: {group}"

    # Count number of glycosyl units
    glycosyl_matches = len(mol.GetSubstructMatches(glycosyl_pattern))
    
    # Check for presence of ceramide and glycosyl parts
    if glycosyl_matches >= 1:
        return True, f"Neutral glycosphingolipid with {glycosyl_matches} glycosyl unit(s)"
    else:
        return False, "Missing required structural components"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25513',
                          'name': 'neutral glycosphingolipid',
                          'definition': 'Any glycosphingolipid containing '
                                        'unsubstituted glycosyl moieties.',
                          'parents': ['CHEBI:24402']},
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
    'num_true_negatives': 183235,
    'num_false_negatives': 75,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999590857018166}