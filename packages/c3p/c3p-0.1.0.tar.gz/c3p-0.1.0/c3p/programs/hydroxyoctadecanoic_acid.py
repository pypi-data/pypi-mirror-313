"""
Classifies: CHEBI:24747 hydroxyoctadecanoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxyoctadecanoic_acid(smiles: str):
    """
    Determines if a molecule is a hydroxyoctadecanoic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is a hydroxyoctadecanoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH,O-]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
    
    # Count carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 18:
        return False, f"Carbon count is {carbon_count}, should be 18"
    
    # Check for rings
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        return False, "Contains ring structures"

    # Check for presence of other elements besides C, H, O
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'H', 'O']:
            return False, f"Contains disallowed element: {atom.GetSymbol()}"
            
    # Check for linear chain with carboxylic acid
    chain_pattern = Chem.MolFromSmarts('CCCCCCCCCCCCCCCCCC(=O)[OH,O-]')
    if not mol.HasSubstructMatch(chain_pattern):
        return False, "Does not contain required 18-carbon linear chain with terminal carboxylic acid"
        
    # Check for branching (excluding OH groups and carboxylic acid)
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            carbon_neighbors = len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'C'])
            if carbon_neighbors > 2:
                # Allow carboxylic acid carbon to have more neighbors
                carboxyl_match = mol.GetSubstructMatches(carboxylic_pattern)
                carboxyl_carbons = [match[0] for match in carboxyl_match]
                if atom.GetIdx() not in carboxyl_carbons:
                    return False, "Structure contains branching"

    # Count hydroxyl groups (excluding carboxylic acid OH)
    hydroxyl_pattern = Chem.MolFromSmarts('[CH2,CH][OH]')
    hydroxyl_matches = len(mol.GetSubstructMatches(hydroxyl_pattern))
    
    if hydroxyl_matches < 1:
        return False, "No hydroxyl groups found on the chain"
        
    return True, f"Hydroxyoctadecanoic acid with {hydroxyl_matches} hydroxyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24747',
                          'name': 'hydroxyoctadecanoic acid',
                          'definition': 'A hydroxy fatty acid that is '
                                        'ocatadecanoic acid (stearic acid) in '
                                        'which the aliphatic chain has been '
                                        'substituted by one or more hydroxy '
                                        'groups.',
                          'parents': ['CHEBI:15904', 'CHEBI:24654']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.07843137254901959 is too low.\n'
               "True positives: [('CCCCCCCCCCCCCCCCC(O)C(O)=O', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('OCCCCCCCCCCCCCCCCCC(O)=O', 'Hydroxyoctadecanoic acid with 1 "
               "hydroxyl group(s)')]\n"
               "False positives: [('OC(C(O)CCCCCCCC(O)=O)CCC(O)CCCCC', "
               "'Hydroxyoctadecanoic acid with 3 hydroxyl group(s)'), "
               "('OC(CCC(O)CCCCCC)CCCCCCCC(O)=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), "
               "('OC(C(O)CCCCCCCC(O)=O)CCCCCCCC(O)=O', 'Hydroxyoctadecanoic "
               "acid with 2 hydroxyl group(s)'), "
               "('[O-]C(=O)CCCCCCCCC(CCCCCCCC)O', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), "
               "('C(CCCCCCCC[C@@H](CCCCCCCC)O)([O-])=O', 'Hydroxyoctadecanoic "
               "acid with 1 hydroxyl group(s)'), "
               "('CCCCCCCC[C@@H](O)[C@@H](O)CCCCCCCC([O-])=O', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('OC(CCCCC(O)CCCC)CCCCCCCC(O)=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), ('OC(CCCCCCCCCC)C(O)CCCCCC(O)=O', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('OC(CCCCCCCCCCCCCC(O)=O)C(O)CC', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), ('OC(CCCCCCCCCCC(O)=O)C(O)CCCCC', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('OC(C(O)CCCCCCC)CCCCCCCCC(O)=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), ('OC(CCCCCCCCCCCC(O)=O)C(O)CCCC', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('OC(CCCCCCCCCCCCCCC(O)=O)CC', 'Hydroxyoctadecanoic acid with "
               "1 hydroxyl group(s)'), ('[O-]C(CCCCCCCCCCCC(CCCCC)O)=O', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('C(CCCCCCCC)CCCCCCC[C@@H](C([O-])=O)O', 'Hydroxyoctadecanoic "
               "acid with 1 hydroxyl group(s)'), "
               "('OC(CCCCCCCCCC(O)=O)CCCCCCC', 'Hydroxyoctadecanoic acid with "
               "1 hydroxyl group(s)'), ('[O-]C(CCCCCCCCCCC(CCCCCC)O)=O', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('O[C@@H]([C@H](O)CCCCCCCC(O)=O)CCCCCCCCO', "
               "'Hydroxyoctadecanoic acid with 3 hydroxyl group(s)'), "
               "('OC(CCCCCCCCC)CCCCCCCC(=O)[O-]', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), ('OC(CCCCCCCCCCCCCCCC(O)=O)C', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('C(CCCCCCCCCC)CCC(CCCC([O-])=O)O', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), ('OC(CCCCCCCCCCCCCC)CCC(O)=O', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('OC(CC(=O)CCCCCCCC(O)=O)CCCC(=O)C(=O)CC', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('[O-]C(CCCCCCCCCCC(CCCCCCO)O)=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), "
               "('C(CCCCCCC[C@H]([C@@H](CCCCCCCC)O)O)([O-])=O', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('OC(CCCCCCCCCC([O-])=O)CCCCCCC', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), "
               "('OC(CC(O)C(O)CCCCCCCC(O)=O)C(O)CC(O)C(O)CC', "
               "'Hydroxyoctadecanoic acid with 6 hydroxyl group(s)'), "
               "('[O-]C(=O)CCCCCC(CCCCCCCCCCC)O', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), ('OC(CCCCCCCCCC(O)CCC(O)=O)CCCC', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('OCCCCCCCCCCCCCCCCCC([O-])=O', 'Hydroxyoctadecanoic acid with "
               "1 hydroxyl group(s)'), "
               "('O[C@H]([C@H](O)CCCCCCCC(O)=O)CCCCCCCCO', "
               "'Hydroxyoctadecanoic acid with 3 hydroxyl group(s)'), "
               "('OC(CCCCCCCCCCCC)C(O)CCCC(O)=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), "
               "('O[C@@H]([C@H](O)CCCCCCCC(O)=O)CCCCCCCC', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('C(CCCCCCC[C@@H]([C@H](CCCCCCCC)O)O)([O-])=O', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('C(C(CCCCCCCC(O)=O)O)(CC(C(CCCCC)O)O)O', 'Hydroxyoctadecanoic "
               "acid with 4 hydroxyl group(s)'), "
               "('C(CCCCCCCC)CCCCCCC[C@H](C([O-])=O)O', 'Hydroxyoctadecanoic "
               "acid with 1 hydroxyl group(s)'), "
               "('CCCCCCCCCCCCCCCC(O)CC([O-])=O', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), ('OC(CCCCCCCCCCCCCC(O)=O)CCC', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('OC(CCCCCCCCCCCCCCC)C(O)C(O)=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), ('OC(=O)CCCCCCCCC(CCCCCCCC)O', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('O[C@@H]([C@@H](O)CCCCCCCC(O)=O)CCCCCCCCO', "
               "'Hydroxyoctadecanoic acid with 3 hydroxyl group(s)'), "
               "('[O-]C(=O)CCCCCCC(CCCCCCCCCC)O', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)'), ('CCCCCCCCCCCCCCCCC(O)C([O-])=O', "
               "'Hydroxyoctadecanoic acid with 1 hydroxyl group(s)'), "
               "('CCCCCC(O)CCC(O)CCCCCCCCC([O-])=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), "
               "('CCCCCCCCC(O)C(O)CCCCCCCC([O-])=O', 'Hydroxyoctadecanoic acid "
               "with 2 hydroxyl group(s)'), ('OCCCCCCCCCCCCCCCC(O)CC([O-])=O', "
               "'Hydroxyoctadecanoic acid with 2 hydroxyl group(s)'), "
               "('ClC(C(O)CCCCCCCC)CCCCCCCC(O)=O', 'Hydroxyoctadecanoic acid "
               "with 1 hydroxyl group(s)')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 46,
    'num_true_negatives': 183861,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.041666666666666664,
    'recall': 1.0,
    'f1': 0.07999999999999999,
    'accuracy': 0.9997498762975167}