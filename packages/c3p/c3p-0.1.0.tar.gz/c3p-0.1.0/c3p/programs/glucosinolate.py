"""
Classifies: CHEBI:24279 glucosinolate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_glucosinolate(smiles: str):
    """
    Determines if a molecule is a glucosinolate based on structural requirements:
    - Contains thioglucoside core
    - Has a central C atom bonded to S, N, and a side group
    - Contains sulfonated oxime group
    - Anti stereochemistry across C=N double bond (where specified)
    
    Args:
        smiles (str): SMILES string of molecule
        
    Returns:
        bool: True if molecule is a glucosinolate, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS patterns for key structural features
    thioglucoside = "[OX2H1][CH]1[CH]([OH])[CH]([OH])[CH]([OH])[CH]([OH])[OX2][CH]1[SX2]" # Sugar-S pattern
    sulfonated_oxime = "[NX2]=[CX3][SX2]-[OX2]-[NX2]-[SX4](=[OX1])(=[OX1])[OX1,OX2-]" # C=N-O-S(=O)(=O)[O-] pattern
    
    # Check for thioglucoside core
    if not mol.HasSubstructMatch(Chem.MolFromSmarts(thioglucoside)):
        return False, "Missing thioglucoside core structure"
        
    # Check for sulfonated oxime group
    if not mol.HasSubstructMatch(Chem.MolFromSmarts(sulfonated_oxime)):
        return False, "Missing sulfonated oxime group"

    # Find central carbon with S, N bonds
    central_c_pattern = "[CX3]([SX2])([NX2]=*)*" # C bonded to S, N=, and something else
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts(central_c_pattern))
    
    if not matches:
        return False, "Missing central carbon with required connectivity"

    # Check stereochemistry where specified
    for match in matches:
        central_c = mol.GetAtomWithIdx(match[0])
        # Get connected atoms
        neighbors = [x.GetIdx() for x in central_c.GetNeighbors()]
        
        # If stereochemistry is specified, should be E/Z (anti)
        bonds = mol.GetBonds()
        double_bonds = [b for b in bonds if b.GetBondType() == Chem.BondType.DOUBLE and 
                       (b.GetBeginAtomIdx() == match[0] or b.GetEndAtomIdx() == match[0])]
        
        if double_bonds:
            if double_bonds[0].GetStereo() == Chem.BondStereo.STEREOE:
                return True, "Valid glucosinolate with E (anti) stereochemistry"
            elif double_bonds[0].GetStereo() == Chem.BondStereo.STEREOZ:
                return False, "Invalid Z (syn) stereochemistry across C=N"
    
    # If we get here, basic structure is present but stereochemistry not specified
    return True, "Valid glucosinolate structure (stereochemistry not fully specified)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24279',
                          'name': 'glucosinolate',
                          'definition': 'Water-soluble anionic substituted '
                                        'thioglucosides. Glucosinolates have a '
                                        'central C atom which is bonded via an '
                                        'S atom to a glycone group and via an '
                                        'N atom to a sulfonated oxime group, '
                                        'and which also carries a side-group. '
                                        'The side-chain and sulfate group have '
                                        'an anti stereochemical configuration '
                                        'across the C=N double bond.',
                          'parents': ['CHEBI:24401']},
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
    'num_true_negatives': 183873,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673698464752}