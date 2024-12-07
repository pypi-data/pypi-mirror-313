"""
Classifies: CHEBI:26493 quinic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_quinic_acid(smiles: str):
    """
    Determines if a molecule is a quinic acid derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a quinic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of core cyclohexane ring
    rings = mol.GetRingInfo()
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered ring found"
    
    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Pattern for quinic acid core structure
    # Cyclohexane ring with carboxylic acid and multiple OH groups
    quinic_core = Chem.MolFromSmarts('C1CC(C(=O)O)CC(O)C1')
    
    if mol.HasSubstructMatch(quinic_core):
        # Count hydroxyl groups
        oh_pattern = Chem.MolFromSmarts('[OH]')
        oh_matches = mol.GetSubstructMatches(oh_pattern)
        oh_count = len(oh_matches) if oh_matches else 0
        
        # Check for ester derivatives
        ester_pattern = Chem.MolFromSmarts('C(=O)OC')
        ester_matches = mol.GetSubstructMatches(ester_pattern)
        ester_count = len(ester_matches) if ester_matches else 0
        
        if ester_count > 0:
            return True, f"Quinic acid ester derivative with {oh_count} hydroxyl groups and {ester_count} ester groups"
        else:
            return True, f"Quinic acid with {oh_count} hydroxyl groups"
            
    return False, "Does not match quinic acid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26493',
                          'name': 'quinic acid',
                          'definition': 'A cyclitol carboxylic acid.',
                          'parents': ['CHEBI:36123']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetSubstructMatches(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 37130,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.99731421051218}