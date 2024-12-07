"""
Classifies: CHEBI:16158 steroid sulfate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprint
from rdkit.Chem import rdMolDescriptors

def is_steroid_sulfate(smiles: str):
    """
    Determines if a molecule is a steroid sulfate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a steroid sulfate, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of sulfate group (-OSO3)
    sulfate_pattern = Chem.MolFromSmarts('OS(=O)(=O)O')
    if not mol.HasSubstructMatch(sulfate_pattern):
        return False, "No sulfate group found"

    # Basic steroid scaffold patterns
    steroid_patterns = [
        # Generic steroid core (4 fused rings)
        Chem.MolFromSmarts('[#6]~1~[#6]~[#6]~[#6]~2~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6]~[#6]~[#6]~[#6]~4~[#6]~[#6]~3~[#6]~[#6]~2~[#6]~1'),
        # Androstane skeleton
        Chem.MolFromSmarts('C12CCC3C(C1)CCC4C3(CCC4)C2'),
        # Estrane skeleton  
        Chem.MolFromSmarts('C12CCC3c4ccccc4CCC3C1CCC2'),
        # Pregnane skeleton
        Chem.MolFromSmarts('CC(C)CCCC(C)C1CCC2C1(CCC3C2CCC4=CC(=O)CCC34C)C')
    ]

    # Check if molecule contains any of the steroid patterns
    has_steroid = False
    for pattern in steroid_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            has_steroid = True
            break
            
    if not has_steroid:
        return False, "No steroid scaffold found"

    # Additional checks to confirm steroid nature
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 4:
        return False, "Insufficient number of rings for steroid"

    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if carbon_count < 17:  # Steroids typically have 17+ carbons
        return False, "Too few carbons for steroid structure"

    return True, "Contains steroid scaffold with sulfate group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16158',
                          'name': 'steroid sulfate',
                          'definition': 'A sulfuric ester obtained by the '
                                        'formal condensation of a hydroxy '
                                        'group of any steroid with sulfuric '
                                        'acid.',
                          'parents': [   'CHEBI:25704',
                                         'CHEBI:26819',
                                         'CHEBI:47880']},
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
    'num_true_positives': 1,
    'num_false_positives': 18,
    'num_true_negatives': 183836,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.05263157894736842,
    'recall': 0.125,
    'f1': 0.07407407407407407,
    'accuracy': 0.9998640284561247}