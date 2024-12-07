"""
Classifies: CHEBI:24963 ketoaldonic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

def is_ketoaldonic_acid(smiles: str):
    """
    Determines if a molecule is a ketoaldonic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a ketoaldonic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Check for ketone group
    ketone_pattern = Chem.MolFromSmarts('[#6][CX3](=O)[#6]')
    if not mol.HasSubstructMatch(ketone_pattern):
        return False, "No ketone group found"
        
    # Check for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[OX2H1]')
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    if len(hydroxyl_matches) < 2:  # Need at least 2 hydroxyl groups (not counting COOH)
        return False, "Insufficient hydroxyl groups"
        
    # Check carbon chain length
    carbon_chain = Chem.MolFromSmarts('C-C-C')  # At least 3 carbons needed
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Carbon chain too short"

    # Check if molecule has expected formula pattern for ketoaldonic acid
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    # Ketoaldonic acids should have n carbons and n+1 oxygens (where n>=3)
    if num_carbons < 3 or num_oxygens != num_carbons + 1:
        return False, "Incorrect molecular formula pattern for ketoaldonic acid"

    # Additional check to ensure linear chain structure 
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        return False, "Contains rings - should be linear chain"

    # Check that the ketone is not at the carboxylic acid end
    ketone_matches = mol.GetSubstructMatches(ketone_pattern)
    carboxyl_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    
    if ketone_matches and carboxyl_matches:
        ketone_carbon = ketone_matches[0][1]  # Get the central carbon of ketone
        carboxyl_carbon = carboxyl_matches[0][0]  # Get the carbon of COOH
        
        # If ketone carbon is directly connected to carboxyl carbon, reject
        if ketone_carbon == carboxyl_carbon:
            return False, "Ketone group cannot be part of carboxylic acid group"
            
        # Check for alpha-keto acid pattern
        alpha_keto_pattern = Chem.MolFromSmarts('O=C-C(=O)O')
        if mol.HasSubstructMatch(alpha_keto_pattern):
            return False, "Alpha-keto acid pattern not allowed"

    # Check for branching - should be mostly linear
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and len([n for n in atom.GetNeighbors()]) > 4:
            return False, "Too much branching for ketoaldonic acid"

    return True, "Valid ketoaldonic acid structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24963',
                          'name': 'ketoaldonic acid',
                          'definition': 'Oxo carboxylic acids formally derived '
                                        'from aldonic acids by replacement of '
                                        'a secondary CHOH group by a carbonyl '
                                        'group.',
                          'parents': ['CHEBI:33720', 'CHEBI:35381']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.13333333333333333 is too low.\n'
               "True positives: [('OC[C@H](C(C(O)=O)=O)O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OCC(=O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain')]\n"
               "False positives: [('C([C@@](CC(C(O)=O)=O)(C(=O)O)O)C(O)=O', "
               "'Molecule contains required ketoaldonic acid features: "
               'carboxylic acid, ketone group, multiple hydroxyl groups in '
               "linear chain'), ('O[C@H](CC(=O)C(O)=O)[C@H](O)C(O)=O', "
               "'Molecule contains required ketoaldonic acid features: "
               'carboxylic acid, ketone group, multiple hydroxyl groups in '
               "linear chain'), ('OC(=O)CC(O)(CC(=O)C(O)=O)C(O)=O', 'Molecule "
               'contains required ketoaldonic acid features: carboxylic acid, '
               "ketone group, multiple hydroxyl groups in linear chain'), "
               "('O[C@@H](CC(=O)C(O)=O)[C@H](O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OC[C@@H](O)[C@@H](O)C(=O)[C@@H](O)C(O)=O', 'Molecule "
               'contains required ketoaldonic acid features: carboxylic acid, '
               "ketone group, multiple hydroxyl groups in linear chain'), "
               "('C(O)C(O)C(O)C(O)C(=O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('O[C@H](CC(=O)C(O)=O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('OCC(=O)[C@@H](O)[C@H](O)C(=O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OC(=O)CC(C(O)=O)C(=O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('OC[C@@H](O)[C@@H](O)[C@H](O)C(=O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OC(=O)C(=O)CC(=O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('OC(C(O)C(=O)CO)C(O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('[C@@H](C(C(O)=O)=O)([C@@H](CO)O)O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('O[C@@H](CC(=O)C(O)=O)[C@@H](O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OC(=O)CC(=O)C(O)=O', 'Molecule contains required ketoaldonic "
               'acid features: carboxylic acid, ketone group, multiple '
               "hydroxyl groups in linear chain'), ('OCC(=O)C(O)=O', 'Molecule "
               'contains required ketoaldonic acid features: carboxylic acid, '
               "ketone group, multiple hydroxyl groups in linear chain'), "
               "('OC(=O)C(=O)CCP(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('OC[C@H](O)[C@H](O)[C@@H](O)C(=O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('O[C@H]([C@@H](O)C(=O)CO)[C@H](O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OC(CC(=O)C(O)=O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('OCC(=O)[C@@H](O)[C@@H](O)[C@H](O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OC(=O)C[C@H](C(O)=O)C(=O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('OCC(=O)[C@@H](O)[C@H](O)[C@H](O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain'), "
               "('O[C@@H](CC(=O)C(O)=O)C(O)=O', 'Molecule contains required "
               'ketoaldonic acid features: carboxylic acid, ketone group, '
               "multiple hydroxyl groups in linear chain'), "
               "('OC[C@H](O)[C@@H](O)C(=O)C(=O)C(O)=O', 'Molecule contains "
               'required ketoaldonic acid features: carboxylic acid, ketone '
               "group, multiple hydroxyl groups in linear chain')]\n"
               "False negatives: [('OC[C@@H](O)[C@H](O)CC(=O)C(O)=O', "
               "'Incorrect molecular formula pattern for ketoaldonic acid')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 5,
    'num_true_negatives': 183899,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.16666666666666666,
    'recall': 0.3333333333333333,
    'f1': 0.2222222222222222,
    'accuracy': 0.9999619372835183}