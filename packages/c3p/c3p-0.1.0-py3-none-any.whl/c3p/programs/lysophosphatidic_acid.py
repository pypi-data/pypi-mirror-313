"""
Classifies: CHEBI:132742 lysophosphatidic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMolFrags

def is_lysophosphatidic_acid(smiles: str):
    """
    Determines if a molecule is a lysophosphatidic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a lysophosphatidic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[P](=O)([OH])([OH])[O]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "Missing phosphate group"

    # Check for glycerol backbone with one ester linkage
    glycerol_ester_pattern = Chem.MolFromSmarts('[CH2][O]P(=O)([OH])[OH].[CH]([OH])[CH2][O]C(=O)')
    if not mol.HasSubstructMatch(glycerol_ester_pattern):
        return False, "Missing glycerol backbone with ester linkage"

    # Count number of ester groups
    ester_pattern = Chem.MolFromSmarts('[#6][C](=O)[O][#6]')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups - lysophosphatidic acid should have exactly 1"

    # Check for free hydroxyl on glycerol backbone
    glycerol_oh_pattern = Chem.MolFromSmarts('[CH2][O]P(=O)([OH])[OH].[CH]([OH])[CH2][O]')
    if not mol.HasSubstructMatch(glycerol_oh_pattern):
        return False, "Missing free hydroxyl group on glycerol backbone"

    # Check for fatty acid chain
    fatty_acid_pattern = Chem.MolFromSmarts('[#6][C](=O)[O][CH2][CH]([OH])[CH2][O]P')
    if not mol.HasSubstructMatch(fatty_acid_pattern):
        return False, "Missing fatty acid chain"

    return True, "Molecule contains phosphate group, glycerol backbone with one ester-linked fatty acid chain and one free hydroxyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132742',
                          'name': 'lysophosphatidic acid',
                          'definition': 'A member of the class of '
                                        'lysophosphatidic acids obtained by '
                                        'hydrolytic removal of one of the two '
                                        'acyl groups of any phosphatidic acid. '
                                        "A 'closed' class.",
                          'parents': ['CHEBI:32957']},
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
    'num_true_positives': 4,
    'num_false_positives': 1,
    'num_true_negatives': 183869,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.8,
    'recall': 0.5714285714285714,
    'f1': 0.6666666666666666,
    'accuracy': 0.9999782463277082}