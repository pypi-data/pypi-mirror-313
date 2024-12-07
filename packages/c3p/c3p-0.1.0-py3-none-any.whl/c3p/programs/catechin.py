"""
Classifies: CHEBI:23053 catechin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_catechin(smiles: str):
    """
    Determines if a molecule is a catechin (flavan-3-ol skeleton and substituted derivatives).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a catechin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for basic flavan skeleton (C6-C3-C6)
    flavan_pattern = Chem.MolFromSmarts('[#6]1~[#6]~[#6]~[#6]~[#6]~[#6]1~[#6]~[#6]~[#6]2~[#6]~[#6]~[#6]~[#6]~[#6]2')
    if not mol.HasSubstructMatch(flavan_pattern):
        return False, "Does not contain basic flavan skeleton"

    # Check for flavan-3-ol pattern
    flavan3ol_pattern = Chem.MolFromSmarts('O[C@H]1Cc2c(O)cc(O)cc2O[C@@H]1c1ccc(O)cc1')
    if not mol.HasSubstructMatch(flavan3ol_pattern):
        # Check alternative stereochemistry
        flavan3ol_alt = Chem.MolFromSmarts('O[C@@H]1Cc2c(O)cc(O)cc2O[C@H]1c1ccc(O)cc1')
        if not mol.HasSubstructMatch(flavan3ol_alt):
            return False, "Does not contain flavan-3-ol core structure"

    # Check for pyran ring (characteristic of flavan structure)
    pyran_pattern = Chem.MolFromSmarts('O1CCCC(C)1')
    if not mol.HasSubstructMatch(pyran_pattern):
        return False, "Does not contain pyran ring"

    # Count hydroxyl groups (catechins typically have multiple OH groups)
    oh_pattern = Chem.MolFromSmarts('[OH]')
    num_oh = len(mol.GetSubstructMatches(oh_pattern))
    if num_oh < 2:
        return False, "Insufficient hydroxyl groups for catechin"

    # Check for aromatic rings (should have at least 2)
    aromatic_rings = 0
    for atom in mol.GetAtoms():
        if atom.IsInRing() and atom.GetIsAromatic():
            aromatic_rings += 1
    if aromatic_rings < 12:  # Each aromatic ring contributes 6 atoms
        return False, "Insufficient aromatic system"

    # Additional structural features that may be present
    features = []
    
    # Check for gallate ester
    gallate_pattern = Chem.MolFromSmarts('OC(=O)c1cc(O)c(O)c(O)c1')
    if mol.HasSubstructMatch(gallate_pattern):
        features.append("gallate ester")
        
    # Check for methylation
    methoxy_pattern = Chem.MolFromSmarts('OC')
    if mol.HasSubstructMatch(methoxy_pattern):
        features.append("methoxy group")
        
    # Check for glycosylation
    glycosyl_pattern = Chem.MolFromSmarts('O[CH]1O[CH][CH][CH][CH][CH]1')
    if mol.HasSubstructMatch(glycosyl_pattern):
        features.append("glycosyl group")

    if features:
        return True, f"Catechin derivative with {', '.join(features)}"
    else:
        return True, "Basic catechin structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23053',
                          'name': 'catechin',
                          'definition': 'Members of the class of hydroxyflavan '
                                        'that have a flavan-3-ol skeleton and '
                                        'its substituted derivatives.',
                          'parents': ['CHEBI:72010']},
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
    'num_true_negatives': 183807,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999347183914612}