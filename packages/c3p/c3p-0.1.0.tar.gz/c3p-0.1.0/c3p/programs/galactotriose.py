"""
Classifies: CHEBI:146179 galactotriose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Descriptors

def is_galactotriose(smiles: str):
    """
    Determines if a molecule is a galactotriose (trisaccharide of 3 galactose units).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a galactotriose, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check molecular formula matches C18H32O16 (galactotriose) 
    formula = rdMolDescriptors.CalcMolFormula(mol)
    if formula != "C18H32O16":
        return False, f"Molecular formula {formula} does not match galactotriose (C18H32O16)"

    # Count rings - should have 3 for a trisaccharide
    rings = mol.GetRingInfo()
    if len(rings.AtomRings()) != 3:
        return False, f"Found {len(rings.AtomRings())} rings, expected 3 for a trisaccharide"

    # Check each ring is 5 or 6-membered (galactose can be pyranose or furanose)
    for ring in rings.AtomRings():
        if len(ring) not in [5,6]:
            return False, f"Found {len(ring)}-membered ring, galactose rings must be 5 or 6-membered"

    # Count OH groups - should be 11 (4 per galactose minus 1 for each glycosidic bond)
    oh_pattern = Chem.MolFromSmarts("[OH]")
    oh_matches = len(mol.GetSubstructMatches(oh_pattern))
    if oh_matches != 11:
        return False, f"Found {oh_matches} OH groups, expected 11 for galactotriose"

    # Count glycosidic linkages
    glycosidic_pattern = Chem.MolFromSmarts("[C]-O-[C]")
    glycosidic_matches = len(mol.GetSubstructMatches(glycosidic_pattern))
    if glycosidic_matches < 2:
        return False, f"Found {glycosidic_matches} glycosidic linkages, expected at least 2 for trisaccharide"

    # Pattern for galactose unit (simplified)
    galactose_pattern = Chem.MolFromSmarts("[CH2]([OH])-[CH1]-1-O-[CH1]-[CH1](-[OH])-[CH1](-[OH])-[CH1]-1-[OH]")
    galactose_matches = len(mol.GetSubstructMatches(galactose_pattern))

    # Also check furanose form
    galactose_furanose = Chem.MolFromSmarts("[CH2]([OH])-[CH1]-1-O-[CH1]-[CH1](-[OH])-[CH1](-[OH])-[CH1]-1")
    galactose_furanose_matches = len(mol.GetSubstructMatches(galactose_furanose))

    total_galactose = galactose_matches + galactose_furanose_matches
    if total_galactose < 3:
        return False, f"Found only {total_galactose} galactose units, expected 3"

    return True, "Contains 3 galactose units connected by glycosidic bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:146179',
                          'name': 'galactotriose',
                          'definition': 'Any trisaccharide composed of 3 '
                                        'galactose moieties.',
                          'parents': ['CHEBI:24151', 'CHEBI:27150']},
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
               'False positives: '
               "[('O(C1(OC(C(O)C1O)CO)CO)C2OC(C(O)C(O)C2O)COC3OC(C(O)C(O)C3O)CO', "
               "'Molecule appears to be a galactotriose (trisaccharide of 3 "
               "galactose units)'), "
               "('OC[C@H]1O[C@H](OC[C@H]2O[C@@](CO)(O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Molecule appears to be a galactotriose (trisaccharide of 3 "
               "galactose units)'), "
               "('O([C@@]1(O[C@@H]([C@@H](O)[C@@H]1O)CO)CO)C2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)COC3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO', "
               "'Molecule appears to be a galactotriose (trisaccharide of 3 "
               "galactose units)'), "
               "('OC[C@H]1O[C@@H](OC[C@H]2O[C@H](O[C@]3(CO)O[C@H](CO)[C@@H](O)[C@@H]3O)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Molecule appears to be a galactotriose (trisaccharide of 3 "
               "galactose units)'), "
               "('OC[C@H]1O[C@H](OC[C@H]2O[C@H](O[C@]3(CO)O[C@H](CO)[C@@H](O)[C@@H]3O)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Molecule appears to be a galactotriose (trisaccharide of 3 "
               "galactose units)'), "
               "('OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC3(CO)O[C@H](CO)[C@@H](O)[C@@H]3O)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Molecule appears to be a galactotriose (trisaccharide of 3 "
               "galactose units)')]\n"
               'False negatives: '
               "[('O([C@H]1[C@@H](OC(O)[C@@H]1O)[C@H](O)CO)[C@H]2O[C@@H]([C@H](O[C@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2O)CO', "
               "'Found 5 glycosidic linkages, expected 2 for trisaccharide'), "
               "('O1[C@H]([C@H](O)[C@@H](O)[C@@H]1O[C@@H]([C@@H]2OC(O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@H](O)[C@H]3O)[C@H](O)CO)CO', "
               "'Found 5 glycosidic linkages, expected 2 for trisaccharide')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 74463,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.5,
    'f1': 0.019417475728155338,
    'accuracy': 0.9986454771005163}