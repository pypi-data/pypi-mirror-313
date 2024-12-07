"""
Classifies: CHEBI:24591 hexuronate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_hexuronate(smiles: str):
    """
    Determines if a molecule is a hexuronate.
    A hexuronate is a uronate obtained via deprotonation of the carboxy group of any hexuronic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hexuronate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate group ([O-])C(=O)
    carboxylate_pattern = Chem.MolFromSmarts('[O-]C(=O)')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate group found"

    # Count carbons and oxygens
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')

    # Hexuronates should have 6 carbons (hex-)
    if num_carbons != 6:
        return False, f"Incorrect number of carbons: {num_carbons} (should be 6)"

    # Should have at least 6 oxygens (one carboxylate + at least 4 hydroxyls + ring oxygen)
    if num_oxygens < 6:
        return False, f"Insufficient number of oxygens: {num_oxygens} (should be at least 6)"

    # Check for hydroxyl groups (excluding the carboxylate)
    hydroxyl_pattern = Chem.MolFromSmarts('[OH]')
    num_hydroxyls = len(mol.GetSubstructMatches(hydroxyl_pattern))
    if num_hydroxyls < 3:  # Should have at least 3 hydroxyl groups
        return False, f"Insufficient number of hydroxyl groups: {num_hydroxyls}"

    # Check for aldehyde group or pyranose/furanose ring
    aldehyde_pattern = Chem.MolFromSmarts('[CH](=O)')
    ring_pattern_6 = Chem.MolFromSmarts('C1OOOOC1')  # Pyranose
    ring_pattern_5 = Chem.MolFromSmarts('C1OOOC1')   # Furanose
    
    if not (mol.HasSubstructMatch(aldehyde_pattern) or 
            mol.HasSubstructMatch(ring_pattern_6) or 
            mol.HasSubstructMatch(ring_pattern_5)):
        return False, "No aldehyde group or proper ring structure found"

    # Check carbon chain connectivity
    carbon_chain = Chem.MolFromSmarts('CCCCCC')
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Carbon atoms not properly connected in a chain"

    return True, "Valid hexuronate structure with required features: 6 carbons in chain, carboxylate group, and proper ring/aldehyde structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24591',
                          'name': 'hexuronate',
                          'definition': 'A uronate obtained via deprotonation '
                                        'of the carboxy group of any hexuronic '
                                        'acid.',
                          'parents': ['CHEBI:33549']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.08 is too low.\n'
               'True positives: '
               "[('OC[C@@]1(O)O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O', 'Molecule "
               'contains required hexuronate features: 6 carbons, carboxylate '
               "group, ring structure, and multiple hydroxyl groups')]\n"
               'False positives: '
               "[('O1[C@H](C([O-])=O)[C@H]([C@H](O)[C@H]([C@H]1O)O)O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[C@@H]([C@H]1O)C([O-])=O)OP([O-])([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[C@@H]([C@@H]1O)C([O-])=O)OP([O-])([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1[C@@H](O)[C@@H](O[*])O[C@@H]([C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('OC1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@H]1[C@H](O)[C@H](OC(=O)[C@@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O1[C@H]([C@@H](O)C(O)(C1=O)C([O-])=O)CO', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@@H]([C@@H]1OC(=O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('[C@@H]1(*)O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]1O)O)O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@@H]([C@@H]1OC[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[*])O[C@@H]([C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('O[C@@H]1[C@@H](O)C(O[C@@H]([C@H]1O)C([O-])=O)OP(O)(O)=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@H]1[C@@H](O)[C@H](OC(=O)[C@@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@@H]([C@H]1OC(=O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O1[C@H]([C@@H](O)C(=O)C1(O)C([O-])=O)CO', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('OC1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), ('O[C@H]1COC(O)(C[C@@H]1O)C([O-])=O', 'Molecule "
               'contains required hexuronate features: 6 carbons, carboxylate '
               "group, ring structure, and multiple hydroxyl groups'), "
               "('[C@H]1([C@@H]([C@@H]([C@@H]([C@H](O1)O)O)O)O)C(=O)[O-]', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups'), "
               "('[C@H]1([C@H]([C@@H]([C@@H]([C@H](O1)O)O)O)O)C(=O)[O-]', "
               "'Molecule contains required hexuronate features: 6 carbons, "
               'carboxylate group, ring structure, and multiple hydroxyl '
               "groups')]\n"
               'False negatives: '
               "[('O[C@@H](C=O)[C@@H](O)[C@H](O)[C@@H](O)C([O-])=O', 'No ring "
               "structure found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 2,
    'num_true_negatives': 183911,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.3333333333333333,
    'recall': 0.5,
    'f1': 0.4,
    'accuracy': 0.9999836881167931}