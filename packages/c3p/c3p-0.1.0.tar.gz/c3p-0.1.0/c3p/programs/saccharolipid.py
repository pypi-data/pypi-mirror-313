"""
Classifies: CHEBI:166828 saccharolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_saccharolipid(smiles: str):
    """
    Determines if a molecule is a saccharolipid (lipid containing a carbohydrate moiety).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a saccharolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of carbohydrate moiety
    # Look for cyclic structures with multiple OH groups and O in ring
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found - carbohydrate moiety requires cyclic structure"

    # Find rings that could be carbohydrates (5-6 membered with oxygen)
    sugar_rings = []
    for ring in rings.AtomRings():
        if len(ring) in [5,6]:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'O' for atom in atoms):
                sugar_rings.append(ring)
                
    if not sugar_rings:
        return False, "No potential carbohydrate rings found"

    # Check for lipid characteristics - long carbon chain and/or fatty acid
    has_long_chain = False
    has_fatty_acid = False
    
    # Look for carbonyl groups (C=O) connected to O 
    pattern = Chem.MolFromSmarts('[CX3](=[OX1])[OX2]')
    if mol.HasSubstructMatch(pattern):
        has_fatty_acid = True
        
    # Look for alkyl chains of length >= 6
    pattern = Chem.MolFromSmarts('CCCCCC')
    if mol.HasSubstructMatch(pattern):
        has_long_chain = True

    if not (has_long_chain or has_fatty_acid):
        return False, "No lipid characteristics found (missing long carbon chain or fatty acid)"

    return True, "Contains both carbohydrate moiety and lipid characteristics"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:166828',
                          'name': 'saccharolipid',
                          'definition': 'Lipids that contain a carbohydrate '
                                        'moiety.',
                          'parents': ['CHEBI:18059']},
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
               "[('[C@H]1(OP(=O)(O)O)[C@H](O*)[C@@H](N*)[C@@H](O[C@@H]1CO)OC[C@@H]2[C@H]([C@@H]([C@H]([C@H](O2)OP(=O)(O)O)N*)O*)O', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H]1[C@H](O[C@H](CO)[C@@H](O)[C@@H]1OC(=O)CCCCCCCCCCCCCCCO)O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1OS(O)(=O)=O', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1OS([O-])(=O)=O', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H]1[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2OS(O)(=O)=O)O[C@H](CO)[C@@H](O)[C@@H]1OC(=O)C(\\\\C)=C\\\\[C@@H](C)C[C@@H](C)C[C@@H](C)CCCCCCCC', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('[H][C@@]1(O[C@@](C[C@@H](O)[C@H]1O)(O[C@@H]1C[C@@](OC[C@H]2O[C@@H](OC[C@H]3O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]3O)[C@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCC\\\\C=C/CCCCCC)[C@@H](OC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC)[C@@H]2OP(O)(O)=O)(O[C@]([H])([C@H](O)CO)[C@@H]1O)C(O)=O)C(O)=O)[C@H](O)CO', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('[C@H]1(OP(=O)(O)O[C@H]2OC[C@@H]([C@@H]([C@H]2O)O)N)[C@H](O*)[C@@H](N*)[C@@H](O[C@@H]1CO)OC[C@@H]3[C@H]([C@@H]([C@H]([C@H](O3)OP(=O)(O)O)N*)O*)O', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('OC[C@@H](O)C(=C)C(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Insufficient hydroxyl groups for carbohydrate moiety'), "
               "('CCCCCCCCCCC[C@@H](O)CC(=O)N[C@H]1[C@H](OC[C@H]2O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]2O)O[C@H](CO)[C@@H](O)[C@@H]1OC(=O)C[C@H](O)CCCCCCCCCCC', "
               "'Insufficient hydroxyl groups for carbohydrate moiety')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 308,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.7596153846153846}