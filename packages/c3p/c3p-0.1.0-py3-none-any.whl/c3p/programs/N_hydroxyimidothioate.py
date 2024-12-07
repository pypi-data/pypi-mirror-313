"""
Classifies: CHEBI:136428 N-hydroxyimidothioate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_hydroxyimidothioate(smiles: str):
    """
    Determines if a molecule is an N-hydroxyimidothioate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-hydroxyimidothioate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for N-hydroxyimidothioate group: S-C(=N-O)
    # The pattern specifically looks for S-C(=N-O) where O is not part of a sulfonate group
    pattern = Chem.MolFromSmarts('[S;X2][C;X3](=[N;X2][O;X2;H1])')
    
    # Pattern for excluding cases where O is part of sulfonate
    exclude_pattern = Chem.MolFromSmarts('[S;X2][C;X3](=[N;X2][O;X2]S(=O)(=O)[O,N])')
    
    if mol.HasSubstructMatch(exclude_pattern):
        return False, "O is part of a sulfonate group"
    
    if not mol.HasSubstructMatch(pattern):
        # Try alternative pattern with explicit hydroxy group
        alt_pattern = Chem.MolFromSmarts('[S;X2][C;X3](=[N;X2][O;X2])')
        if not mol.HasSubstructMatch(alt_pattern):
            return False, "Does not contain N-hydroxyimidothioate group"
    
    # Get the matches
    matches = mol.GetSubstructMatches(pattern)
    if not matches:
        matches = mol.GetSubstructMatches(alt_pattern)
    
    # Check each potential match
    for match in matches:
        s_atom = mol.GetAtomWithIdx(match[0])
        c_atom = mol.GetAtomWithIdx(match[1])
        n_atom = mol.GetAtomWithIdx(match[2])
        o_atom = mol.GetAtomWithIdx(match[3])
        
        # Verify atom types
        if (s_atom.GetSymbol() != 'S' or 
            c_atom.GetSymbol() != 'C' or
            n_atom.GetSymbol() != 'N' or
            o_atom.GetSymbol() != 'O'):
            continue
            
        # Check for C=N double bond
        bond = mol.GetBondBetweenAtoms(match[1], match[2])
        if bond.GetBondType() != Chem.BondType.DOUBLE:
            continue
            
        # Check that O is not part of a sulfonate or other groups
        o_neighbors = [x.GetSymbol() for x in o_atom.GetNeighbors()]
        if len(o_neighbors) > 1 or (len(o_neighbors) == 1 and o_neighbors[0] != 'N'):
            continue
            
        return True, "Contains N-hydroxyimidothioate group"
        
    return False, "Structure does not match N-hydroxyimidothioate requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136428',
                          'name': 'N-hydroxyimidothioate',
                          'definition': 'An imidothioate in which the nitrogen '
                                        'is substituted by a hydroxy group.',
                          'parents': ['CHEBI:83991']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.038461538461538464 is too low.\n'
               'True positives: '
               "[('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NO)CCC=2C=CC=CC2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)C(=NO)CCCCCSC', "
               "'Contains N-hydroxyimidothioate group')]\n"
               'False positives: '
               "[('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCSC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCCSC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCS(C)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CC(C)(O)CC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CC(C)(O)CC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2c[nH]c3cccc(O)c23)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCSC', "
               "'Contains N-hydroxyimidothioate group'), ('CNC(=O)ON=C(C)SC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2c[nH]c3ccccc23)=NOS([O-])(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CC(C)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CCC(C)(O)CC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2cn(c3ccccc23)S(O)(=O)=O)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCO', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CCOC(=O)CCN(Cc1ccccc1)SN(C)C(=O)O\\\\N=C(\\\\C)SC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/C(CC)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[NH3+][C@@H](CCC(=O)N[C@@H](CS/C(=N\\\\O)/CC1=CC=CC=C1)C(=O)NCC(=O)[O-])C(=O)[O-]', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCCC2=CC=CC=C2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('N[C@@H](CS\\\\C(Cc1ccc(O)cc1)=N/O)C(O)=O', 'Contains "
               "N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)C(=NOS(O)(=O)=O)CC=2C3=C(NC2)C=CC=C3OC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CS(=O)(=O)CCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CSCCCCCCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CSCCCCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NOS(O)(=O)=O)CC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CC(CO)C(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CC(O)(CC)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('COc1ccc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS(O)(=O)=O)cc1', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCCC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCSC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC2=CC(=CC=C2)OC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('COc1cccc2[nH]cc(CC(S[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)=NOS(O)(=O)=O)c12', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NOS(O)(=O)=O)CC(C)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[NH3+][C@@H](CS/C(=N/O)/CC=1C=2C=CC=CC2NC1)C(=O)NCC(=O)[O-]', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2cn(c3ccccc23)S(O)(=O)=O)=NOS([O-])(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CS(=O)(=O)CCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCC=2C=CC=CC2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS([O-])(=O)=O)C[C@@H](C=C)O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2ccc(O)cc2)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CSC(=NO)C(=O)N(C)C', 'Contains N-hydroxyimidothioate "
               "group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/C(C)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCSC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCC(CC)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/*', "
               "'Contains N-hydroxyimidothioate group'), "
               "('COc1cccc2[nH]cc(CC(S[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)=NOS([O-])(=O)=O)c12', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CC=2C3=C(N(OC)C2)C=CC=C3OC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CC/C=C/S(=O)C', "
               "'Contains N-hydroxyimidothioate group'), ('*SC(*)=NO', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(CC(O)CC=C)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS(O)(=O)=O)CC(C=C)O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](S\\\\C([*])=N/O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCCCC2=CC=CC=C2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('N[C@@H](CS\\\\C([*])=N/O)C(O)=O', 'Contains "
               "N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/C(CC)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS([O-])(=O)=O)CC(C=C)O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CC(CC)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CSCCC\\\\C(SC[C@H](N)C(O)=O)=N\\\\O', 'Contains "
               "N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCSC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC(C)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCCS(C)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('COn1cc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS([O-])(=O)=O)c2ccccc12', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCS(C)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC(CC)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](S\\\\C(CCCOC(=O)C2=CC=CC=C2)=N\\\\OS([O-])(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[NH3+][C@@H](CS/C(=N\\\\O)/CC=1C=CC=CC1)C(=O)NCC(=O)[O-]', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/C[C@H](C=C)O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2c[nH]c3cccc(O)c23)=NOS([O-])(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CSCCCCCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS(O)(=O)=O)C[C@H](C=C)O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CC=2C=CC=CC2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCCCCCCS(C)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CS(=O)CCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/*C=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[NH3+][C@@H](CCC(=O)N[C@@H](CS\\\\C(=N\\\\O)\\\\CC1=CNC2=C1C=CC=C2)C(=O)NCC(=O)[O-])C(=O)[O-]', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/C(C)C', "
               "'Contains N-hydroxyimidothioate group'), ('CSC(C)=NO', "
               "'Contains N-hydroxyimidothioate group'), "
               "('C1=CC=C2C(=C1)C(C/C(=N\\\\OS(O)(=O)=O)/S[C@]3([C@]([C@@]([C@]([C@](CO)([H])O3)([H])O)([H])O)([H])O)[H])=CN2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('COn1cc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS(O)(=O)=O)c2ccccc12', "
               "'Contains N-hydroxyimidothioate group'), "
               "('N[C@@H](CS\\\\C(Cc1c[nH]c2ccccc12)=N/O)C(O)=O', 'Contains "
               "N-hydroxyimidothioate group'), "
               "('OC[C@H]1O[C@@H](SC(Cc2c[nH]c3ccccc23)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NOS(O)(=O)=O)CCCCCCS(C)=O', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('CSC(C)=NOC(=O)NSNC(=O)ON=C(C)SC', 'Contains "
               "N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCCCCC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCC=2C=CC=CC2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS(O)(=O)=O)/CCCC=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)/C(=N\\\\OS(O)(=O)=O)/C[C@H](O)C=C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CC(O)C2=CC=CC=C2', "
               "'Contains N-hydroxyimidothioate group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CC2=CC(=CC=C2)OC', "
               "'Contains N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)COC(=O)/C=C/C2=CC(OC)=C(O)C(OC)=C2)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CC/C=C/S(=O)C', "
               "'Contains N-hydroxyimidothioate group'), "
               "('N[C@@H](CS\\\\C(Cc1ccccc1)=N/O)C(O)=O', 'Contains "
               "N-hydroxyimidothioate group'), "
               "('S(C1OC(C(O)C(O)C1O)CO)\\\\C(=N\\\\OS(O)(=O)=O)\\\\CCC2=CC=CC=C2', "
               "'Contains N-hydroxyimidothioate group')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 25,
    'num_true_negatives': 183890,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9998640691181349}