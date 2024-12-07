"""
Classifies: CHEBI:134363 tertiary amine oxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tertiary_amine_oxide(smiles: str):
    """
    Determines if a molecule is a tertiary amine oxide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a tertiary amine oxide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Find N-oxide substructure
    # Pattern matches N+ with exactly 4 bonds, one to O-, and three to C
    n_oxide_pattern = Chem.MolFromSmarts('[NX4+;$([N](-[OX1-])(-[#6])(-[#6])(-[#6]))]')
    
    if not mol.HasSubstructMatch(n_oxide_pattern):
        return False, "No tertiary amine oxide group found"
    
    # Check for presence of N-oxide group that's not part of N-oxide functionality
    n_oxide_false_pos = Chem.MolFromSmarts('[N]-[O]')
    matches_false_pos = mol.GetSubstructMatches(n_oxide_false_pos)
    matches_true = mol.GetSubstructMatches(n_oxide_pattern)
    
    # If we have N-O bonds that aren't part of our N-oxide pattern, it might be a different type
    if len(matches_false_pos) > len(matches_true):
        return False, "Contains N-O bond but not in tertiary amine oxide configuration"
        
    # Check each match to verify it's a proper tertiary amine oxide
    for match in matches_true:
        n_idx = match[0]  # Index of nitrogen atom
        n_atom = mol.GetAtomWithIdx(n_idx)
        
        # Verify formal charge is +1
        if n_atom.GetFormalCharge() != 1:
            continue
            
        # Count number of carbons directly bonded to nitrogen
        carbon_count = sum(1 for neighbor in n_atom.GetNeighbors() 
                         if neighbor.GetAtomicNum() == 6)
        
        # Must have exactly 3 carbons bonded to the nitrogen
        if carbon_count != 3:
            continue
            
        # Count number of oxygens with -1 charge bonded to nitrogen
        oxide_count = sum(1 for neighbor in n_atom.GetNeighbors() 
                        if neighbor.GetAtomicNum() == 8 and 
                        neighbor.GetFormalCharge() == -1)
        
        # Must have exactly one oxide oxygen
        if oxide_count != 1:
            continue
            
        return True, "Tertiary amine oxide found"
    
    return False, "No valid tertiary amine oxide group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134363',
                          'name': 'tertiary amine oxide',
                          'definition': 'An N-oxide where there are three '
                                        'organic groups bonded to the nitrogen '
                                        'atom.',
                          'parents': ['CHEBI:35580']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.1111111111111111 is too low.\n'
               'True positives: '
               "[('C[N+]1(CCC2=CC(=C(C=C2[C@@H]1CC3=CC(=C(C=C3)OC)O)O)OC)[O-]', "
               "'Tertiary amine oxide found'), "
               "('[C@@]12([N+]3(CC[C@H]1OC(/C(/CC(=C)[C@@](C(OCC2=CC3)=O)(C)O)=C/C)=O)[O-])[H]', "
               "'Tertiary amine oxide found'), "
               "('C(CCCCCCCC)CCC[N+](C)([O-])C', 'Tertiary amine oxide "
               "found'), "
               "('[C@@]12([N+]3(CC[C@H]1OC(/C(/CC(=C)[C@](C(OCC2=CC3)=O)(OC(=O)C)C)=C\\\\C)=O)[O-])[H]', "
               "'Tertiary amine oxide found')]\n"
               'False positives: '
               "[('O=C1N([C@]23[C@H](C(C)(C)[C@@]4(C2)C(=O)NC5=C4C=CC6=C5C(=O)CC(O6)(C)C)C[C@]17[N+]([O-])(C[C@@H](C7)C)C3)C', "
               "'Tertiary amine oxide found'), "
               "('C(CC[N+](C)(C)[O-])=C1C=2C(CCC3=C1C=CC=C3)=CC=CC2', "
               "'Tertiary amine oxide found'), "
               "('S(=O)(=O)(N1CC[N+]([O-])(CC1)C)C2=CC(=C(OCC)C=C2)C=3NC(=O)C=4N(N=C(C4N3)CCC)C', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]1(C2C=3C(CC1)=CC=4OCOC4C3C=5C(C2O)=CC=CC5)C', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]1(C2CCC1CC(OC(=O)/C(/C)=C/C)C2)C', 'Tertiary amine "
               "oxide found'), "
               "('O=C1N([C@]23[C@H](C(C)(C)[C@@]4(C2)C(=O)NC5=C4C=CC6=C5OC=CC(O6)(C)C)C[C@]17[N+]([O-])(CC[C@]7(O)C)C3)C', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]12C(C(CC1)COC(=O)C(O)(C(C)C)C(O)C)CCC2', 'Tertiary "
               "amine oxide found'), "
               "('O=C(NC1=C(C=CC=C1C)C)C[N+]([O-])(CC)CC', 'Tertiary amine "
               "oxide found'), "
               "('[O-][N+]12C(C(O)CC1)C(=CC2)COC(=O)C(O)(C(C)C)C(O)C', "
               "'Tertiary amine oxide found'), "
               "('O[C@]1([C@H](CCCC1)C[N+]([O-])(C)C)C2=CC(OC)=CC=C2', "
               "'Tertiary amine oxide found'), "
               "('S(=O)(=O)(C1=C(N)C=C(OC)C(=C1)C(=O)NCC2[N+]([O-])(CCC2)CC)CC', "
               "'Tertiary amine oxide found'), "
               "('O=C(N(O)CCC[C@H]([N+]([O-])(C)C)C(=O)O)/C=C(/CCOC1OC(C(OC)C(C1O)O)CO)\\\\C', "
               "'Tertiary amine oxide found'), "
               "('O[C@@]12C34N(=O)(CCC1)CCC[C@]3(O)C(=O)C[C@@]2(C[C@](C4)(C)[H])[H]', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]1([C@@]2(C=3C(CC1)=CC(OC)=C(OC)C3OC=4C=C5C(N(CCC5=CC4OC)C)CC6=CC=C(OC=7C=C(C2)C=CC7OC)C=C6)[H])C', "
               "'Tertiary amine oxide found'), "
               "('ClC=1C(NC(=O)C=2SC(NC=3N=C(N=C(N4CC[N+]([O-])(CC4)CCO)C3)C)=NC2)=C(C=CC1)C', "
               "'Tertiary amine oxide found'), "
               "('O=C1C2=C(O)C(=CC=C2C(=O)C3=C1[C@H](O[C@H]4[C@@H]3OC(=O)C4)C)[C@@H]5O[C@@H]([C@@H](O)[C@@H](C5)[N+]([O-])(C)C)C', "
               "'Tertiary amine oxide found'), "
               "('C[N+]1([C@H]2C[C@@H](C[C@@H]1CC2)OC(C(CO)C3=CC=CC=C3)=O)[O-]', "
               "'Tertiary amine oxide found'), "
               "('O(CC[N+]([O-])(C)C)C(=O)C1=CC=C(NCCCC)C=C1', 'Tertiary amine "
               "oxide found'), "
               "('ClC1=CN=C(N2C(=O)C=3N=CC=NC3[C@@H]2OC(=O)N4CC[N+]([O-])(C)CC4)C=C1', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]1(CCN(CC1)C(=O)N(CC)CC)C', 'Tertiary amine oxide "
               "found'), ('O=C1N2C(C3C4[N+]([O-])(CCC3)CCCC4C2)CC=C1', "
               "'Tertiary amine oxide found'), "
               "('[O-][N@+]12[C@]34N5C(=O)C[C@]3(CC[C@]4([C@](CC1)(C=6C5=CC(OC)=C(OC)C6)[H])[H])C=CC2', "
               "'Tertiary amine oxide found'), "
               "('O=C1N[C@H](C(=O)N[C@H]1CCCN(O)C(=O)/C=C(/CCOC(=O)[C@@H]([N+]([O-])(C)C)CCCN(O)C(=O)/C=C(/CCO)\\\\C)\\\\C)CCCN(O)C(=O)/C=C(/CCO[C@@H]2O[C@@H]([C@@H](O)[C@@H]([C@@H]2O)O)CO)\\\\C', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]12CC(CCC1)(CCC3=NC=4C(C3(O)CC2)=CC=CC4)CC', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+](CCC=1C2=C(NC1)C=CC(OC)=C2)(C)C', 'Tertiary amine "
               "oxide found'), ('C(C[N+](CCCl)([O-])C)Cl.Cl', 'Tertiary amine "
               "oxide found'), "
               "('S1C=CNC(=O)[C@@H](NC([C@@H](NC([C@H](C1)NC(=O)[C@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)CNC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)/C(/NC(=O)[C@@H]2N(C(=O)/C(/NC(=O)[C@H](NC(=O)[C@@H]3N(C(=O)/C(/NC(=O)[C@@H]([N+]([O-])(C)C)C)=C/C)CCC3)C)=C/C)CCC2)=C/C)C)C)CCC(=O)N)CC4=CC=CC=C4)C(C)C)[C@@H](CC)C)CCC(=O)N)CO)=C/C)[C@@H](CC)C)=O)CC(C)C)=O)C(C)C', "
               "'Tertiary amine oxide found'), "
               "('C(CC[N+](C)(C)[O-])N1C=2C(CCC3=C1C=CC=C3)=CC=CC2', 'Tertiary "
               "amine oxide found'), "
               "('[O-][N+]12C([C@@H](CC1)COC(=O)C(O)(C(C)C)C(O)C)CCC2', "
               "'Tertiary amine oxide found'), "
               "('C\\\\C=C1\\\\C[C@@H](C)[C@](O)(CO)C(=O)OCC2=CCN3(=O)CC[C@@H](OC1=O)[C@@H]23', "
               "'Tertiary amine oxide found'), "
               "('O1[C@@]2([C@]34[C@](O)([C@]([N@@+]([O-])(CC3)C)(CC5=C4C1=C(OC)C=C5)[H])CC[C@@H]2O)[H]', "
               "'Tertiary amine oxide found'), ('CN(=O)(CCCl)CCCl', 'Tertiary "
               "amine oxide found'), "
               "('[O-][N+]1(CC2N(C3=NC=CC=C3CC4=C2C=CC=C4)CC1)C', 'Tertiary "
               "amine oxide found'), "
               "('O=C1N[C@H](C(=O)N[C@H]1CCCN(O)C(=O)/C=C(/CCOC(=O)[C@@H]([N+]([O-])(C)C)CCCN(O)C(=O)/C=C(/CCO[C@@H]2O[C@@H]([C@@H](O)[C@@H]([C@@H]2O)O)CO)\\\\C)\\\\C)CCCN(O)C(=O)/C=C(/CCO[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@@H]3O)O)CO)\\\\C', "
               "'Tertiary amine oxide found'), "
               "('OC1C2([N+]([O-])(CCC=3C2=CC(O)=C(OC)C3)C)CC4=C1C=5OCOC5C=C4', "
               "'Tertiary amine oxide found'), "
               "('O=C(N1[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)NCCC(=O)N[C@H](C[N+]([O-])(C)C)C)(C)C)(C)C)CC(C)C)CC(C)C)(C)C)[C@@H](O)C(C)C)CC(C)C)C[C@@H](C1)C)/C=C\\\\[C@@H](CC)C', "
               "'Tertiary amine oxide found'), "
               "('ClC1=CC=2N(CCC[N+]([O-])(C)C)C=3C(CCC2C=C1)=CC=CC3', "
               "'Tertiary amine oxide found'), "
               "('OC1(C(C[N+]([O-])(C)C)C2=CC=C(OC)C=C2)CCCCC1', 'Tertiary "
               "amine oxide found'), "
               "('O=C(NC=CC1=CC=CC=C1)C2[N+]([O-])(CCCC2)C', 'Tertiary amine "
               "oxide found'), "
               "('O=C1N[C@H](C(=O)N[C@H]1CCCN(O)C(=O)/C=C(/CCOC(=O)[C@@H]([N+]([O-])(C)C)CCCN(O)C(=O)/C=C(/CCO[C@@H]2O[C@@H]([C@@H](OC)[C@@H]([C@@H]2O)O)CO)\\\\C)\\\\C)CCCN(O)C(=O)/C=C(/CCO[C@@H]3O[C@@H]([C@@H](OC)[C@@H]([C@@H]3O)O)CO)\\\\C', "
               "'Tertiary amine oxide found'), "
               "('ClC1=CC=2N=C(N3CC[N+]([O-])(CC3)C)C=4C(NC2C=C1)=CC=CC4', "
               "'Tertiary amine oxide found'), ('[N+]1(CCOCC1)(C)[O-]', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+](CCC(C1=CC=CC=C1)C=2N=CC=CC2)(C)C', 'Tertiary amine "
               "oxide found'), "
               "('O1[C@@]2([C@]34[C@]([C@]([N@@+]([O-])(CC3)C)(CC5=C4C1=C(OC)C=C5)[H])(C=C[C@@H]2O)[H])[H]', "
               "'Tertiary amine oxide found'), "
               "('O=C(N1[C@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)NCCC(=O)N[C@H](C[N+]([O-])(C)C)C)(C)C)(C)C)CC(C)C)CC(C)C)(C)C)[C@H](O)C(C)C)C[C@H](C[C@H](O)CC(=O)CC)C)C[C@@H](C1)C)/C=C/[C@@H](CC)C', "
               "'Tertiary amine oxide found'), "
               "('CN(C)(=O)CCCC1(OCc2cc(ccc12)C#N)c1ccc(F)cc1', 'Tertiary "
               "amine oxide found'), "
               "('FC1=C(N2CC[N+]([O-])(CC2)C)C=3OCC(N4C3C(=C1)C(=O)C(=C4)C(O)=O)C', "
               "'Tertiary amine oxide found'), "
               "('S(=O)(=O)(N1CC[N+]([O-])(CC1)CC)C2=CC(=C(OCC)C=C2)C=3NC(=O)C=4N(N3)C(=NC4C)CCC', "
               "'Tertiary amine oxide found'), "
               "('O=C1OC(C(O)(C(O)C(C(=O)C(C)CC(C(C(C(C1C)OC2OC(C(O)C(C2)(OC)C)C)C)OC3OC(CC(C3O)[N+]([O-])(C)C)C)(O)C)C)C)CC', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]1(CCN(CC1)CC2=CC=C(C=C2)C(=O)NC3=CC(NC=4N=C(C=5C=CC=NC5)C=CN4)=C(C=C3)C)C', "
               "'Tertiary amine oxide found'), "
               "('O1CC=2C(/C(=C\\\\CC[N+]([O-])(C)C)/C=3C1=CC=CC3)=CC=CC2', "
               "'Tertiary amine oxide found'), "
               "('C=1[C@H]([C@H](OC([C@@H]([C@H]([C@H](C[C@H](C(C1)=O)C)C)OC2O[C@@H](C[C@@H]([C@H]2O)[N+](C)(C)[O-])C)C)=O)C(C)=O)C', "
               "'Tertiary amine oxide found'), "
               "('S(=O)(=O)(CCC1=CC=2C(C[C@@H]3[N+]([O-])(CCC3)C)=CNC2C=C1)C4=CC=CC=C4', "
               "'Tertiary amine oxide found'), "
               "('O([C@@H]1[C@@]2([N+]([O-])(CC1)CC=C2COC(=O)[C@@](O)(C(O)(C)C)[C@@H](O)C)[H])C(=O)/C(/C)=C\\\\C', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+](CCCCCCCCCC)(CCCCCCCCCC)C', 'Tertiary amine oxide "
               "found'), ('CNC(NCCSCc1ccc(CN(C)(C)=O)o1)=C[N+]([O-])=O', "
               "'Tertiary amine oxide found'), "
               "('C(CC[N@@+]1([O-])CC[C@](CC1)(O)C2=CC=C(C=C2)Cl)(C(N(C)C)=O)(C3=CC=CC=C3)C4=CC=CC=C4', "
               "'Tertiary amine oxide found'), "
               "('[O-][N+]12[C@@]([C@@H](O)CC1)(C(=CC2)COC(=O)[C@](O)(C(C)C)[C@H](OC)C)[H]', "
               "'Tertiary amine oxide found'), "
               "('ClC1=CC=C(C(N2CC[N+]([O-])(CC2)CCOCC(O)=O)C3=CC=CC=C3)C=C1', "
               "'Tertiary amine oxide found'), "
               "('C/C=C\\\\1/C[N+]2(CC[C@@]34CC=5C=C6C(=CC5O[C@@]74[C@@]2(C[C@@]1([C@@](C(=O)OC)(N7C8=CC=CC=C83)[H])[H])[H])N[C@]9%10CC[C@@]%11(CC)CCC[N@+]%10(CC[C@@]69O)C%11)[O-]', "
               "'Tertiary amine oxide found'), "
               "('FC1=C(N2CCN(CC2)C)C=C3[N+]([O-])(CC)C=C(C(=O)C3=C1)C(O)=O', "
               "'Tertiary amine oxide found'), "
               "('[O-][N@@+]12[C@@]3([C@H]([C@@](C[C@]1(C=4NC=5C(C4C3)=CC=CC5)[H])(/C(/C2)=C\\\\C)[H])C(OC)=O)[H]', "
               "'Tertiary amine oxide found'), "
               "('C/C=C\\\\1/C2CC[N@+]3(CC[C@]4(C5=CC=CC=C5NC4=C2C(=O)OC)[C@@]13[H])[O-]', "
               "'Tertiary amine oxide found'), "
               "('COC([C@@H]1C[C@@]23CCC[N+]4(CCC5(C6=CC=CC=C6N(C(=O)OC)[C@]15CC2)[C@]34[H])[O-])=O', "
               "'Tertiary amine oxide found')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 59,
    'num_true_negatives': 183830,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06349206349206349,
    'recall': 1.0,
    'f1': 0.11940298507462686,
    'accuracy': 0.9996791612513799}