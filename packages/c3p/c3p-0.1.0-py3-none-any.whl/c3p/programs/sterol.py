"""
Classifies: CHEBI:15889 sterol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_sterol(smiles: str):
    """
    Determines if a molecule is a sterol based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sterol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of OH group
    if '[OH]' not in Chem.MolToSmiles(mol, allHsExplicit=True) and 'O' not in Chem.MolToSmiles(mol):
        return False, "No hydroxyl group present"

    # Count rings
    ri = mol.GetRingInfo()
    if len(ri.AtomRings()) < 4:
        return False, "Does not have required 4-ring steroid core structure"
        
    # Check for tetracyclic structure characteristic of steroids
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[C]1~[C]~[C]~[C]2~[C]~[C]~[C]3~[C]~[C]~[C]4~[C]~[C]~[C](~[C]~4)~[C]~3~[C]~2~1'))
    if not matches:
        return False, "Does not match steroid core pattern"

    # Check for 3-hydroxyl group
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[CH2][CH2][CH](O)[CH2][CH2]'))
    if not matches:
        return False, "No 3-hydroxyl group found"

    # Look for cholestane-like skeleton
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('CC(C)CCC[CH]'))
    if not matches:
        matches = mol.GetSubstructMatches(Chem.MolFromSmarts('CC(C)=CCC[CH]'))
        if not matches:
            return False, "Side chain not similar to cholestane"

    return True, "Matches sterol structural requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15889',
                          'name': 'sterol',
                          'definition': 'Any 3-hydroxy steroid whose skeleton '
                                        'is closely related to cholestan-3-ol '
                                        '(additional carbon atoms may be '
                                        'present in the side chain).',
                          'parents': ['CHEBI:36834']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183744,
    'num_false_negatives': 19,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998966059544087}