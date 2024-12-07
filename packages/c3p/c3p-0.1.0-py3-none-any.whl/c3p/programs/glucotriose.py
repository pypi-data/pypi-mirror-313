"""
Classifies: CHEBI:146180 glucotriose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_glucotriose(smiles: str):
    """
    Determines if a molecule is a glucotriose (trisaccharide composed of 3 glucose units).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glucotriose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check molecular formula - should be C18H32O16 for glucotriose
    formula = rdMolDescriptors.CalcMolFormula(mol)
    if formula != 'C18H32O16':
        return False, f"Incorrect molecular formula: {formula}, expected C18H32O16"

    # Count oxygen atoms with degree 2 (potential glycosidic bonds)
    glycosidic_oxygens = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 2:
            glycosidic_oxygens += 1
            
    # Should have 2 glycosidic bonds connecting 3 glucose units
    if glycosidic_oxygens < 2:
        return False, f"Found only {glycosidic_oxygens} potential glycosidic bonds, expected at least 2"

    # Check for 3 pyranose rings
    rings = mol.GetRingInfo()
    six_membered_rings = [ring for ring in rings.AtomRings() if len(ring) == 6]
    
    if len(six_membered_rings) != 3:
        return False, f"Found {len(six_membered_rings)} pyranose rings, expected 3"

    # For each ring, check if it matches glucose pattern
    for ring in six_membered_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Check ring composition - should be 5 carbons and 1 oxygen
        atom_symbols = [atom.GetSymbol() for atom in ring_atoms]
        if atom_symbols.count('C') != 5 or atom_symbols.count('O') != 1:
            return False, "Ring has incorrect composition for glucose"

        # Check for CH2OH group and hydroxyl groups
        ch2oh_found = False
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'C':
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
                        ch2oh_found = True
                        break
        
        if not ch2oh_found:
            return False, "Missing CH2OH group on glucose unit"

    return True, "Molecule is a glucotriose with 3 glucose units connected by glycosidic bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:146180',
                          'name': 'glucotriose',
                          'definition': 'Any trisaccharide composed of 3 '
                                        'glucose moieties.',
                          'parents': ['CHEBI:24268', 'CHEBI:27150']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               'False negatives: '
               "[('OC[C@H]1O[C@H](OC[C@H]2O[C@H](OC[C@H]3O[C@H](O)[C@H](O)[C@@H](O)[C@@H]3O)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Found 5 glycosidic bonds, expected 2'), "
               "('OC[C@H]1O[C@H](OC[C@H]2O[C@H](OC[C@H]3OC(O)[C@H](O)[C@@H](O)[C@@H]3O)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Found 5 glycosidic bonds, expected 2'), "
               "('O([C@H]1[C@H](O)[C@@H](O)C(O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO', "
               "'Found 6 glycosidic bonds, expected 2'), "
               "('OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@H]3[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]3CO)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Found 5 glycosidic bonds, expected 2'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)O)O)O)OC[C@H]3O[C@H]([C@@H]([C@H]([C@@H]3O)O)O)O', "
               "'Found 5 glycosidic bonds, expected 2'), "
               "('OC[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](OC[C@H]3OC(O)[C@H](O)[C@@H](O)[C@@H]3O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Found 5 glycosidic bonds, expected 2')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 48033,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9979226822327011}