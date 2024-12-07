"""
Classifies: CHEBI:26125 phytosterols
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

def is_phytosterols(smiles: str):
    """
    Determines if a molecule is a phytosterol based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phytosterol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for tetracyclic core structure (4 rings)
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 4:
        return False, "Does not contain required tetracyclic core structure"
        
    # Check for presence of hydroxyl group
    patt_oh = Chem.MolFromSmarts("[#6]-[OH]")
    if not mol.HasSubstructMatch(patt_oh):
        return False, "Missing hydroxyl group characteristic of sterols"

    # Check for cyclopentanoperhydrophenanthrene core
    steroid_core = Chem.MolFromSmarts("C1CC2CCC3C(C2)CCC4C3(CCC4)C1")
    if not mol.HasSubstructMatch(steroid_core):
        return False, "Missing steroid core structure"

    # Count carbons (phytosterols typically have 28-30 carbons)
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbons < 27 or num_carbons > 30:
        return False, f"Carbon count ({num_carbons}) outside typical range for phytosterols (27-30)"

    # Check for aliphatic side chain
    patt_side_chain = Chem.MolFromSmarts("CC(C)CCCC")
    if not mol.HasSubstructMatch(patt_side_chain):
        return False, "Missing characteristic aliphatic side chain"

    # Look for double bonds (most phytosterols have at least one)
    patt_db = Chem.MolFromSmarts("C=C")
    num_db = len(mol.GetSubstructMatches(patt_db))
    
    reason = f"Contains steroid core, hydroxyl group, {num_carbons} carbons, "
    reason += f"{num_db} double bond(s), and characteristic side chain"
    
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26125',
                          'name': 'phytosterols',
                          'definition': 'Sterols similar to cholesterol which '
                                        'occur in plants and vary only in '
                                        'carbon side chains and/or presence or '
                                        'absence of a double bond.',
                          'parents': ['CHEBI:15889', 'CHEBI:26124']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}