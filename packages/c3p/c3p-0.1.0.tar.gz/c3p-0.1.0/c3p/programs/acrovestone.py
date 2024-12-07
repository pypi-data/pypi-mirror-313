"""
Classifies: CHEBI:2440 acrovestone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_acrovestone(smiles: str):
    """
    Determines if a molecule is an acrovestone - a polyphenol isolated from Acronychia pedunculata.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an acrovestone, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of chromene/chromenone core
    chromene_pattern = Chem.MolFromSmarts('O1c2ccccc2C=CC1')
    chromenone_pattern = Chem.MolFromSmarts('O1c2ccccc2C(=O)C=C1')
    
    if not mol.HasSubstructMatch(chromene_pattern) and not mol.HasSubstructMatch(chromenone_pattern):
        return False, "Missing chromene/chromenone core structure"
        
    # Check for polyphenol characteristics
    oh_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('cOH')))
    if oh_count < 1:
        return False, "Missing phenolic OH groups"
        
    # Check for glycoside/glucuronide/malonate substituents
    glycoside_pattern = Chem.MolFromSmarts('OC1OC(CO)C(O)C(O)C1O')
    glucuronide_pattern = Chem.MolFromSmarts('OC1OC(C(=O)O)C(O)C(O)C1O')
    malonate_pattern = Chem.MolFromSmarts('OC(=O)CC(=O)')
    
    has_glycoside = mol.HasSubstructMatch(glycoside_pattern)
    has_glucuronide = mol.HasSubstructMatch(glucuronide_pattern)
    has_malonate = mol.HasSubstructMatch(malonate_pattern)
    
    if not (has_glycoside or has_glucuronide or has_malonate):
        return False, "Missing characteristic glycoside/glucuronide/malonate substituents"
    
    # Check molecular weight range
    mw = Descriptors.ExactMolWt(mol)
    if not (300 < mw < 1000):
        return False, "Molecular weight outside expected range"
        
    substituents = []
    if has_glycoside:
        substituents.append("glycoside")
    if has_glucuronide:
        substituents.append("glucuronide") 
    if has_malonate:
        substituents.append("malonate")
        
    return True, f"Acrovestone with {', '.join(substituents)} substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2440',
                          'name': 'acrovestone',
                          'definition': 'A polyphenol that is isolated from '
                                        'Acronychia pedunculata and exhibits '
                                        'moderate antioxidant and '
                                        'antityrosinase activities.',
                          'parents': [   'CHEBI:22187',
                                         'CHEBI:26195',
                                         'CHEBI:35618',
                                         'CHEBI:78840']},
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
    'success': False,
    'best': True,
    'error': 'Python argument types in\n'
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
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}