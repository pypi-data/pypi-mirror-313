"""
Classifies: CHEBI:23219 bile acid taurine conjugate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_bile_acid_taurine_conjugate(smiles: str):
    """
    Determines if a molecule is a bile acid taurine conjugate by checking for:
    1. Presence of taurine group (-NHCH2CH2SO3H)
    2. Steroid core structure (cyclopentanoperhydrophenanthrene)
    3. Connection via amide bond
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a bile acid taurine conjugate, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for taurine group
    taurine_pattern = Chem.MolFromSmarts('[NH]-[CH2]-[CH2]-[SX4](=[OX1])(=[OX1])[OX2H]')
    if not mol.HasSubstructMatch(taurine_pattern):
        return False, "No taurine group found"

    # Check for steroid core (simplified)
    steroid_core = Chem.MolFromSmarts('C1CC2CCC3C(C2)CCC4C3(C)CCC4C1')
    if not mol.HasSubstructMatch(steroid_core):
        return False, "No steroid core structure found"

    # Check for amide linkage between taurine and bile acid
    amide_pattern = Chem.MolFromSmarts('[CX3](=[OX1])[NX3H]-[CH2]-[CH2]-[SX4]')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide linkage between taurine and bile acid found"

    # Count typical oxygen atoms (usually 2-4 OH groups)
    o_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OH1]')))
    if o_count < 1:
        return False, "Insufficient hydroxyl groups for bile acid structure"

    # Additional checks could be added for specific bile acid features
    # but this covers the main structural requirements

    return True, "Contains taurine group conjugated to bile acid core via amide bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23219',
                          'name': 'bile acid taurine conjugate',
                          'definition': 'A bile acid conjugate resulting from '
                                        'the formal condensation of a bile '
                                        'acid with the amino group of taurine.',
                          'parents': ['CHEBI:36249']},
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
    'num_true_negatives': 183893,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999782486935621}