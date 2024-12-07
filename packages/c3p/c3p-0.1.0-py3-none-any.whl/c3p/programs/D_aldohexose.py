"""
Classifies: CHEBI:17608 D-aldohexose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_D_aldohexose(smiles: str):
    """
    Determines if a molecule is a D-aldohexose (aldose with 6 carbons in D configuration).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a D-aldohexose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # First check for presence of non-C,H,O atoms
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'H', 'O']:
            return False, f"Contains non-C,H,O atoms ({atom.GetSymbol()})"

    # Count total carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 6:
        return False, "Does not contain exactly 6 carbons"

    # Check for presence of hemiacetal/acetal group (characteristic of cyclic sugars)
    hemiacetal_patt = Chem.MolFromSmarts('[CH]([OH])[O][CH]')
    acetal_patt = Chem.MolFromSmarts('[CH]([O][CH])([O])')
    if not (mol.HasSubstructMatch(hemiacetal_patt) or mol.HasSubstructMatch(acetal_patt)):
        return False, "No hemiacetal/acetal group found"

    # Check for CH2OH group
    ch2oh_patt = Chem.MolFromSmarts('[CH2][OH]')
    if not mol.HasSubstructMatch(ch2oh_patt):
        return False, "No CH2OH group found"

    # Check for proper ring structure
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings():
        return False, "No ring structure found"
        
    rings = ring_info.AtomRings()
    valid_ring = None
    ring_size = 0
    
    for ring in rings:
        if len(ring) in [5, 6]:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'O' for atom in ring_atoms):
                valid_ring = ring
                ring_size = len(ring)
                break
                
    if valid_ring is None:
        return False, "No valid pyranose/furanose ring found"

    # Count hydroxyl groups
    oh_patt = Chem.MolFromSmarts('[OH]')
    num_oh = len(mol.GetSubstructMatches(oh_patt))
    if num_oh < 4:  # At least 4 OH groups required for aldohexose
        return False, "Insufficient number of hydroxyl groups"

    # Check for chiral centers and their configurations
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    if len(chiral_centers) < 3:  # Aldohexoses should have at least 3 chiral centers
        return False, "Insufficient number of chiral centers"

    # Check for specific D-aldohexose structures
    d_aldohexose_furanose = Chem.MolFromSmarts('O1[C@H]([C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO')
    d_aldohexose_pyranose = Chem.MolFromSmarts('OC[C@H]1OC(O)[C@H](O)[C@H](O)[C@@H]1O')
    
    if mol.HasSubstructMatch(d_aldohexose_furanose) or mol.HasSubstructMatch(d_aldohexose_pyranose):
        if ring_size == 6:
            return True, "D-aldohexose in pyranose form"
        else:
            return True, "D-aldohexose in furanose form"
            
    return False, "Does not match D-aldohexose structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17608',
                          'name': 'D-aldohexose',
                          'definition': 'Any D-aldose having a chain of six '
                                        'carbon atoms in the molecule.',
                          'parents': ['CHEBI:33917', 'CHEBI:4194']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.11267605633802819 is too low.\n'
               'True positives: '
               "[('O1[C@H]([C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@H]1O', 'D-aldohexose in "
               "pyranose form'), ('OC[C@H]1OC(O)[C@@H](O)[C@@H](O)[C@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@H]1OC(O)[C@H](O)[C@H](O)[C@@H]1O', 'D-aldohexose in "
               "pyranose form')]\n"
               "False positives: [('O1C(C(O)C(O)C(O)C1O)CO', 'D-aldohexose in "
               "pyranose form'), ('[C@H]1([C@@H]([C@@H](CC(O1)O)O)O)CO', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@H]1OC(O)C(=O)[C@@H](O)[C@@H]1O', 'D-aldohexose in "
               "pyranose form'), "
               "('[H][C@]1(O[C@@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('O1[C@H]([C@@H](O)[C@H](O)[C@H]1O)[C@@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@H]1O)[C@@H](O)CO', 'D-aldohexose "
               "in furanose form'), ('OC[C@H]1OC(O)C(=O)[C@@H](O)[C@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('O1[C@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('[C@@H]1(O)[C@H](O)[C@@H](O)[C@H](O)[C@@H](O1)CO', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@@H]1OC(O)[C@@H](O)[C@@H](O)[C@H]1O', 'D-aldohexose in "
               "pyranose form'), ('OC[C@@H]1OC(O)[C@H](O)[C@H](O)[C@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@H]1OC(O)C[C@@H](O)[C@@H]1O', 'D-aldohexose in pyranose "
               "form'), ('[H][C@@]1(O[C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@H](O)[C@@H](O)[C@H](O)[C@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('OC[C@H](O)[C@H]1O[C@H](O)[C@H](O)[C@H]1O', 'D-aldohexose in "
               "furanose form'), "
               "('O1[C@H]([C@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@H](O)[C@H](O)[C@H](O)[C@H]1O', 'D-aldohexose in "
               "pyranose form'), "
               "('OC[C@@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('O1[C@@H]([C@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('[H][C@@]1(O[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('O1[C@H]([C@@H](O)[C@@H](O)C1O)[C@@H](O)CO', 'D-aldohexose in "
               "furanose form'), ('O1[C@@H]([C@H](O)[C@@H](O)C1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@@H]1O)[C@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@@H]([C@H](O)[C@H](O)C1O)[C@H](O)CO', 'D-aldohexose in "
               "furanose form'), "
               "('OC[C@@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('OC[C@@H]1OC(O)[C@@H](O)[C@@H](O)[C@@H]1O', 'D-aldohexose in "
               "pyranose form'), ('OC[C@@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('O1[C@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('O1[C@H]([C@H](O)[C@H](O)[C@@H](O)C1O)CO', 'D-aldohexose in "
               "pyranose form'), "
               "('O1[C@H]([C@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@@H]([C@H](O)[C@H](O)C1O)[C@@H](O)CO', 'D-aldohexose in "
               "furanose form'), ('OC[C@@H]1OC(O)[C@@H](O)[C@H](O)[C@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@H]1OC(O)[C@H](O)C(=O)[C@@H]1O', 'D-aldohexose in "
               "pyranose form'), "
               "('O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O)CO', "
               "'D-aldohexose in pyranose form'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('O1[C@H]([C@@H](O)[C@H](O)C1O)[C@@H](O)CO', 'D-aldohexose in "
               "furanose form'), ('OC[C@@H]1OC(O)[C@H](O)[C@H](O)[C@@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@H]1O)[C@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('O1[C@H]([C@H](O)[C@@H](O)C1O)[C@@H](O)CO', 'D-aldohexose in "
               "furanose form'), "
               "('[H][C@]1(O[C@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O)CO', "
               "'D-aldohexose in pyranose form'), "
               "('OC[C@@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('O1[C@H]([C@H](O)[C@H](O)[C@@H](O)[C@@H]1O)CO', 'D-aldohexose "
               "in pyranose form'), ('OC[C@H]1O[C@@H](O)[C@H](O)C(=O)[C@H]1O', "
               "'D-aldohexose in pyranose form'), "
               "('O1[C@@H]([C@@H](O)[C@@H](O)C1O)[C@@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@@H](O)CO', 'D-aldohexose in "
               "furanose form'), "
               "('[H][C@@]1(OC(O)[C@H](O)[C@@H]1O)[C@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@H]([C@@H](O)[C@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('[H][C@]1(OC(O)[C@@H](O)[C@H]1O)[C@@H](O)CO', 'D-aldohexose "
               "in furanose form'), "
               "('O1[C@@H]([C@@H](O)[C@@H](O)[C@@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('C1[C@H]([C@@H]([C@H](O[C@@H]1O)CO)O)O', 'D-aldohexose in "
               "pyranose form'), "
               "('O1[C@@H]([C@@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1O[C@H](O)[C@@H](O)[C@H](O)[C@@H]1O', 'D-aldohexose "
               "in pyranose form'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@H]1O)[C@@H](O)CO', "
               "'D-aldohexose in furanose form'), "
               "('OC[C@@H]1OC(O)[C@@H](O)[C@H](O)[C@@H]1O', 'D-aldohexose in "
               "pyranose form')]\n"
               'False negatives: '
               "[('OC[C@H]1OC(O)[C@H](OP(O)(=O)O[C@H]2[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O', "
               "'Contains non-C,H,O atoms (P)')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 55,
    'num_true_negatives': 183827,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.06779661016949153,
    'recall': 0.8,
    'f1': 0.125,
    'accuracy': 0.9996954651497931}