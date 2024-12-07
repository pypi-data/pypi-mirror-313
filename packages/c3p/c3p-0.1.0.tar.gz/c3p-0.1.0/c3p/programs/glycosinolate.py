"""
Classifies: CHEBI:24401 glycosinolate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glycosinolate(smiles: str):
    """
    Determines if a molecule is a glycosinolate based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycosinolate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for sulfate group [O-]S(=O)(=O)O
    sulfate_pattern = Chem.MolFromSmarts('[O,O-]S(=O)(=O)[O,O-]')
    if not mol.HasSubstructMatch(sulfate_pattern):
        return False, "Missing sulfate group"

    # Look for C=N-O-S pattern 
    cn_os_pattern = Chem.MolFromSmarts('[C]=[N]-[O]-[S]')
    if not mol.HasSubstructMatch(cn_os_pattern):
        return False, "Missing C=N-O-S linkage"

    # Look for pyranose sugar ring with S attachment
    sugar_pattern = Chem.MolFromSmarts('[C]1[O][C]([C]([O])[C]([O])[C]1[O])[S]')
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "Missing pyranose sugar ring with S attachment"

    # Look for thiohydroximate group
    thiohyd_pattern = Chem.MolFromSmarts('[S]-[C]=[N]-[O]-[S]')
    if not mol.HasSubstructMatch(thiohyd_pattern):
        return False, "Missing thiohydroximate group"
        
    # Check for negative charge
    if '[O-]' not in smiles and 'O-' not in smiles:
        return False, "Missing negatively charged oxygen"

    # If all patterns are found and has negative charge, it's a glycosinolate
    return True, "Contains glycosinolate core structure (sulfated thiohydroximate-O connected to pyranose sugar)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24401',
                          'name': 'glycosinolate',
                          'definition': 'An sulfur oxoanion resulting from the '
                                        'deprotonation of the hydroxy group '
                                        'attached to the sulfur of a '
                                        'glycosinolic acid.',
                          'parents': ['CHEBI:33482']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.21428571428571425 is too low.\n'
               'True positives: '
               "[('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCCCSC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](S\\\\C(CCCCOC(=O)C2=CC=CC=C2)=N\\\\OS([O-])(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CC2=CC(=CC=C2)OC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCC=C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCC2=CC=CC=C2', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CC2=CC=C(O)C=C2', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)')]\n"
               'False positives: '
               "[('CC(CO)C(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](SC(Cc2cn(c3ccccc23)S(O)(=O)=O)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('CS(=O)CCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCC=C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NOS(O)(=O)=O)CCCCCCS(C)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC(CC)C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCCCCCS(C)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS(O)(=O)=O)C[C@H](C=C)O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCS(C)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC2=CC(=CC=C2)OC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/C(C)C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/C(CC)C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC(C)C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('CSCCCCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](SC(CC(O)c2ccccc2)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](SC(CC(O)CC=C)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCSC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCC=C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCSC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('O1[C@@H]([C@H]([C@@H]([C@H]([C@@H]1SC(CCCCCCCS(C)=O)=NOS(O)(=O)=O)O)O)O)CO', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS(O)(=O)=O)C[C@@H](C=C)O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC=2C=CC=CC2', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('COc1cccc2[nH]cc(CC(S[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)=NOS(O)(=O)=O)c12', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('CCC(C)(O)CC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('COc1ccc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS(O)(=O)=O)cc1', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](SC(Cc2c[nH]c3ccccc23)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCS(C)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](SC(Cc2ccc(O)cc2)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('CS(=O)(=O)CCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('COn1cc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS(O)(=O)=O)c2ccccc12', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('CC(C)(O)CC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCSC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/*', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('CS(=O)(=O)CCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('OC[C@H]1O[C@@H](SC(Cc2c[nH]c3cccc(O)c23)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCCCCS(C)=O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCC=2C=CC=CC2', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC=C', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS(O)(=O)=O)CC(C=C)O', "
               "'Contains glycosinolate core structure (sulfated "
               "thiohydroximate-O connected to pyranose sugar)')]\n"
               'False negatives: []',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 3,
    'num_true_negatives': 183870,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.5714285714285714,
    'recall': 0.6666666666666666,
    'f1': 0.6153846153846153,
    'accuracy': 0.9999728082053959}