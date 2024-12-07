"""
Classifies: CHEBI:2468 secondary alpha-hydroxy ketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_secondary_alpha_hydroxy_ketone(smiles: str):
    """
    Determines if a molecule contains a secondary alpha-hydroxy ketone group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains secondary alpha-hydroxy ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for secondary alpha-hydroxy ketone:
    # [OH]-[CH]([#6,#7,#8,#9,#15,#16,#17,#35,#53])-C(=O)-[#6]
    # Explicitly defines the non-hydrogen substituent types and requires carbon after carbonyl
    pattern = Chem.MolFromSmarts('[OH][CH]([#6,#7,#8,#9,#15,#16,#17,#35,#53])C(=O)[#6]')
    
    if pattern is None:
        return None, "Invalid SMARTS pattern"
        
    matches = mol.GetSubstructMatches(pattern)
    
    if not matches:
        return False, "No secondary alpha-hydroxy ketone group found"
        
    # Verify each match
    for match in matches:
        # Get the relevant atoms
        oh_oxygen = mol.GetAtomWithIdx(match[0])
        alpha_carbon = mol.GetAtomWithIdx(match[1])
        r_group = mol.GetAtomWithIdx(match[2])
        carbonyl_carbon = mol.GetAtomWithIdx(match[3])
        
        # Check that alpha carbon has exactly one hydrogen
        if alpha_carbon.GetTotalNumHs() != 1:
            continue
            
        # Check that alpha carbon has exactly three neighbors
        if len(list(alpha_carbon.GetNeighbors())) != 3:
            continue
            
        # Check that the carbonyl carbon is not part of an ester, amide, or acid
        is_valid = True
        for neighbor in carbonyl_carbon.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                is_valid = False
                break
            if neighbor.GetSymbol() == 'N':
                is_valid = False
                break
                
        if is_valid:
            substituent_type = r_group.GetSymbol()
            return True, f"Contains secondary alpha-hydroxy ketone with {substituent_type} substituent"
            
    return False, "No valid secondary alpha-hydroxy ketone group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2468',
                          'name': 'secondary alpha-hydroxy ketone',
                          'definition': 'An alpha-hydroxy ketone in which the '
                                        'carbonyl group and the hydroxy group '
                                        'are linked by a carbon bearing one '
                                        'hydrogen and one organyl group. '
                                        'Secondary alpha-hydroxy ketones are '
                                        'also known as acyloins, and are '
                                        'formally derived from reductive '
                                        'coupling of two carboxylic acid '
                                        'groups.',
                          'parents': ['CHEBI:139588', 'CHEBI:35681']},
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
               "[('O=C1C2=C(OC([C@H]1O)(C)C)[C@H](O)[C@]3(O)C[C@@H](O[C@H]3C2)C(O)(C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O1CC(O)C(=O)C(O)=C1C', 'Contains secondary alpha-hydroxy "
               "ketone group'), "
               "('CO[C@@H]([C@@H]1Cc2cc3cc(O[C@H]4C[C@@H](O[C@H]5C[C@@H](O)[C@H](O)[C@@H](C)O5)[C@H](O)[C@@H](C)O4)c(C)c(O)c3c(O)c2C(=O)[C@H]1O[C@H]1C[C@@H](O[C@H]2C[C@@H](O[C@H]3C[C@](C)(O)[C@H](O)[C@@H](C)O3)[C@@H](O)[C@@H](C)O2)[C@H](O)[C@@H](C)O1)C(=O)[C@@H](O)C(C)=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('[H][C@]12[C@H](CO)[C@@]1(C)CC[C@@]1(O)[C@]22OC(=O)[C@@]11CCCC(C)(C)[C@]1([H])C(=O)[C@@H]2O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O[C@H](COP([O-])([O-])=O)C([O-])=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('S1C2=NC(C1)C(=O)N/C(/C(=O)N3C(C(=O)NC(C(=O)N(C(C(C)C)C(OCC(C(NC(C(NC(C(N4C2CC4C)=O)CC(C)C)=O)C)=O)O)=O)C)C(O)C)CCCC3)=C\\\\C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1C2=C(OC([C@@H]1O)(C)C)C=C(OC)C(=C2)OC', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('ClC1=C(O)C=CC(=C1)C[C@@H]2N(C(=O)[C@@H](N3C(=O)[C@H](NC(=O)[C@H](CCCN=C(N)N)NC([C@H]([C@H](OC([C@@H](NC2=O)C(CC)C)=O)C)NC(=O)[C@H](O)COS(=O)(=O)O)=O)CC[C@H]3O)C(CC)C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O(CC(O)C(O)=O)C=1C(OCC=C)=CC=CC1', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('OC[C@H](O)[C@@H](O)C(=O)[C@H](O)C(O)=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), ('OC(COP(O)(O)=O)C(O)=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('OC[C@@H](O)[C@@H](O)C(=O)[C@@H](O)C(O)=O', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('O(P(O)(O)=O)CC([C@H](C(=O)O)O)=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O=C1NC(=O)C(=C1C2=CC=C(OC[C@H](O)C(=O)OC)C=C2)CC(C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(O)[C@]1(O[C@@H]2[C@@H](O)[C@H](N3C4=NC=NC(=C4N=C3)N)OC2=C1)[C@H](O)C(=O)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O[C@H](C(O)=O)C(=O)S[*]', 'Contains secondary alpha-hydroxy "
               "ketone group'), "
               "('O(CC(O)C(O)=O)C(=O)\\\\C=C\\\\C1=CC(O)=C(OC)C=C1', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('C(C(COP(=O)([O-])[O-])O)([O-])=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O=C(NCCCCCCCC/C=C\\\\CCCCCC)[C@H](O)CO[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1NC(=O)C)O)CO', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('OC(C(O)=O)C(=C)OP(O)(O)=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('CC(C(C(N1C2=CC=CC=C2[C@]34CCN5C[C@]6([C@@H](C)OC[C@]([C@]6(C[C@@]35O)[H])([C@@]41[H])[H])[H])=O)O)=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O(C[C@@H](C(CO)=O)O)P([O-])(=O)[O-]', 'Contains secondary "
               "alpha-hydroxy ketone group'), ('C([C@@H](C(CO)=O)O)([O-])=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O[C@@H](COP([O-])([O-])=O)[C@@H](O)C(=O)[C@H](O)C([O-])=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1C(OC)=C(OC[C@@H]1O)C', 'Contains secondary alpha-hydroxy "
               "ketone group'), "
               "('C1=2N(C3=CC(=CC=C3C=C1C([N-]C(N2)=O)=O)O)C[C@@H]([C@@H]([C@@H](COP(OC[C@H](C([O-])=O)O)(=O)[O-])O)O)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('CO[C@H](CO)CC1O[C@@H]2[C@@H](NC(=O)[C@@H](O)[C@]3(CC(=C)[C@@H](C)[C@@H](C)O3)OC)OCO[C@@H]2[C@@H](OC)C1(C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1C2=C(OC([C@H]1O)(C)C)C=3C(=O)[C@@H]4[C@H](C)[C@H](C3C(=C2)CC=C(C)C)C4', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1C2=C(O[C@]([C@@H]1O)([C@H]3OC(=O)CC3)C)C=C(CO)C=C2O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(NCCCCCCCC/C=C\\\\CCCCCCC)[C@H](O)CO[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1NC(=O)C)O)CO', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1O[C@@H]2N([C@@H](/C=C/C)[C@@H]([C@@H](NC3=C(C(=O)O)C=CC=C3)C4=C5OC([C@H](O)C(C5=CC(=C4/C=C/C=C/C)CC=C(C)C)=O)(C)C)C=6C2=C7OC([C@H](O)C(C7=CC6CC=C(C)C)=O)(C)C)C8=C1C=CC=C8', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1OC[C@@]23[C@@]4([C@@]5(O)[C@H](O[C@@H]2[C@@H]([C@](O)(C)CC3)C5)C[C@H]4OC(=O)C=CCCC67[C@@H](C(=C1)CCO6)OC(=O)[C@H]7O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O(C[C@H](C(CO)=O)O)P([O-])(=O)[O-]', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O1[C@]23[C@@]([C@@H](OC(=O)C)C[C@]([C@]4([C@@]1(C[C@H](OC(=O)C)C([C@@H]4CC(OC)=O)(C)C)[H])C)(C2=C)[H])([C@H](OC(=O)[C@H]3O)C=5C=COC5)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('OC(C([O-])=O)C(=O)CCC([O-])=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), ('OC(C(=O)CCC(O)=O)C(=O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('[H][C@@]1(OC(=O)[C@@H](O)C1=O)[C@@H](O)CO', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('OCC([C@@H](C(O)=O)O)=O', 'Contains secondary alpha-hydroxy "
               "ketone group'), "
               "('O=C1O[C@H](CCC[C@@H]([C@]2(C(=O)[C@H](OC3=C(C(O)=CC(=C3)C)C)[C@](OC)(C)[C@@H](C2=O)O)C)CC(C4=C(C1)C=C(O)C=C4O)=O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OCC(O)C(=O)N[C@@H]1C(=O)NC(C(=O)NC2C(=O)N([C@@H](CC3=CC=CC=C3)C(N(C(C(NC(C(O[C@@H]1C)=O)C(C)C)=O)CC4=CC=C(O)C=C4)C)=O)C(O)CC2)CCCN=C(N)N)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(O)[C@H](O)[C@]1(O[C@H]([C@@](OC)(C)[C@H]([C@@H]1C)OC)C[C@H]2O[C@]3(O[C@@]([C@@H]4O[C@H]([C@@H]5O[C@@H]([C@H]6O[C@](O)([C@H](C)[C@H]([C@@H]6C)O[C@@H]7O[C@@H]([C@@H](OC)CC7)C)C)CC5)CC4)(C)[C@@H]([C@H]3C)OC)[C@H](C)[C@@H](C2)OC)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1N(C=2C=CC=C3C2[C@@]14O[C@]5(O)[C@@H](O)C(=O)N6[C@@]5([C@@H]4[C@H](C6(C)C)C3)O)CCCC(=O)OC', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(N1[C@H]([C@H](O)CC(=O)N)CCC1)C([C@H](O)C(/C=C/NC(=O)[C@H](O)[C@@]2(O[C@@H]([C@H](C)C(C2)=C)C)OC)CO)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O(C(=O)CCCCCCCC/C=C\\\\CCC)C[C@H](O)C(O)=O', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('OCC([C@@H](C([O-])=O)O)=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('P(OCC(O)C([O-])=O)([O-])(=O)O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O=C1O[C@H](CCC=CC=CCC[C@H](O)CC(O)C[C@H]2O[C@@](O)(C(O)C(=O)O[C@H](CCC=CC=CCC[C@@H](CC(C[C@H]3O[C@](C1O)(O)[C@@H](CC3)C)=O)O)C)[C@H](C)CC2)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OCC(O)C(=O)NC1C(=O)NC(C(=O)NC2C(=O)N(C(CC(C)C)C(N(C(C(NC(C(OC1C)=O)C(C)C)=O)CC3=CC=CC=C3)C)=O)C(O)CC2)CCCN=C(N)N)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O1[C@]2(O)[C@@H](CC[C@]1(C(C(=O)CC(O)CCC=CC=CCCC(OC(=O)C(O)[C@@]3(O[C@@](CC[C@H]3C)(C(C(=O)CC(O)CCC=CC=CCCC(OC(=O)C2O)C)C)[H])O)C)C)[H])C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1O[C@H]2[C@@]3([C@@]4([C@@H](C=C(C)CC4)OC(C2)C35OC5)COC(=O)C6[C@@]7([C@@H]8[C@](C=CC=C1)(OCC7)C(O)C(=O)O8)O6)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('N([C@@H](CCCC[NH2+]CC(=O)[C@H](O)COP([O-])(=O)[O-])C(*)=O)*', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1O[C@H](CCC=CC=CCC[C@H](O)CC(=O)C[C@H]2O[C@@](O)(C(O)C(=O)O[C@H](CCC=CC=CCC[C@@H](CC(C[C@H]3O[C@](C1O)(O)[C@@H](CC3)C)=O)O)C)[C@H](C)CC2)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1N(C=2C=CC=C3C2[C@@]14O[C@]5(O)[C@@H](O)C(=O)N6[C@@]5([C@@H]4[C@H](C6(C)C)C3)O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O[C@@H](COP(O)(O)=O)[C@@H](O)C(=O)[C@H](O)C(O)=O', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('OC(C([O-])=O)C(=O)C([O-])=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), ('C([C@@H](C(CO)=O)O)(O)=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O1C(C(O)C(=O)C2=C1C=CC(OC)=C2)(C)C', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O=C(NCCCCCCCCCCCCCCCCC)[C@H](O)CO[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1NC(=O)C)O)CO', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('CO[C@@H]1[C@H]2OCO[C@H](NC(=O)[C@@H](O)[C@]3(CC(=C)[C@@H](C)[C@@H](C)O3)OC)[C@H]2O[C@H](C[C@H](O)CCC\\\\C=C\\\\C=C\\\\C=C\\\\C(=O)NC(CCCNC(N)=N)C(O)=O)C1(C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1N2[C@@]3(O[C@@]([C@@H]1O)(O)C)C(=O)O[C@]45[C@H]3[C@H](C2(C)C)CC=6C=CC=C(C46)N(C5=O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('P(=O)([O-])(OC[C@@H](O)C(=O)O[As](=O)([O-])[O-])[O-]', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OC[C@@H](O)C(=O)N[C@@H]1C(=O)N[C@H](C(=O)N[C@@H]2C(=O)N([C@@H]([C@H](CC)C)C(N([C@H](C(N[C@H](C(O[C@@H]1C)=O)[C@H](CC)C)=O)CC3=CC=CC=C3)C)=O)[C@H](OC)CC2)CCCN=C(N)N)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OC[C@@H](O)C(=O)N[C@@H](C(=O)N[C@@H]1C(=O)N[C@H](C(=O)N[C@@H]2C(=O)N([C@@H](CC(C)C)C(N([C@H](C(N[C@H](C(O[C@@H]1C)=O)C(C)C)=O)CC3=CC=C(O)C=C3)C)=O)[C@H](O)CC2)CCCN=C(N)N)CC(C)C)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(O)[C@H](O)[C@]1(O[C@H]([C@@H](C)C([C@@H]1C)OC)C[C@H]2O[C@]3(OC([C@@H]4O[C@H]([C@@H]5O[C@@H]([C@H]6O[C@](O)([C@H](C)C[C@@H]6C)C)CC5)C[C@H]4O[C@@H]7O[C@@H]([C@@H](OC)CC7)C)(C)C[C@H]3C)[C@H](C)[C@@H](C2)OC)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C([C@H](O)[C@]1(O[C@H]([C@@](OC)(C)[C@H]([C@@H]1C)OC)C[C@H]2O[C@]3(O[C@@]([C@@H]4O[C@H]([C@@H]5O[C@@H]([C@H]6O[C@](OC)([C@H](C)[C@H]([C@@H]6C)O[C@@H]7O[C@@H]([C@@H](OC)CC7)C)C)CC5)CC4)(C)[C@@H]([C@H]3C)OC)[C@H](C)[C@@H](C2)OC)O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O1C23C(C(OC(=O)C)CC(C4(C1CC(OC(=O)C)C(C4C(O)C(OC)=O)(C)C)C)C2=C)(C(OC(=O)C3O)C=5C=COC5)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1C2=C(OC([C@@H]1O)(C)C)C(=C(\\\\C=C/C=C/C)C(=C2)CC=C(C)C)CO', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(C1=NC=C(C)C2=C1NC=3C=CC=CC23)C(O)CO[C@@H]4O[C@H]([C@H](O)[C@H]([C@H]4O)O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OC[C@@H](O)C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H]1C(=O)N/C(/C(=O)N[C@@H]2C(=O)N([C@@H](CC3=CC=CC=C3)C(N([C@H](C(N[C@H](C(O[C@@H]1C)=O)C(C)C)=O)CC4=CC=C(O)C=C4)C)=O)[C@H](OC)CC2)=C\\\\C)CCC5=CC=C(O)C=C5)C)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('C(=O)(COP(=O)(O)O)[C@@H](C(O)=O)O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O(CC(O)C(O)=O)C=1C(OC)=CC=CC1', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OCC(O)C(=O)N[C@@H]1C(=O)N[C@H](C(=O)N[C@@H]2C(=O)N([C@@H]([C@H](CC)C)C(N([C@H](C(N[C@H](C(O[C@@H]1C)=O)[C@H](CC)C)=O)CC3=CC=CC=C3)C)=O)[C@H](O)CC2)CCCCN(C)C)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(NCCCCCCCCCCCCCCCC)[C@H](O)CO[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1NC(=O)C)O)CO', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1OC[C@@]23[C@@]4([C@@]5(OC5)[C@H](O[C@@H]2C=C(C)CC3)C[C@H]4OC(=O)C=CC=CC67C(C(=C1)CCO6)OC(=O)C7O)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(OCC(O)C(=O)NC(C(=O)OC(C(C(=O)NC(C(=O)NO)CCCN(O)C(=N)N)C)CCCCCCCCCCC)CCCN(O)C=O)C1=C(O)C=CC=C1', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1C2=C(OC([C@@H]1O)(C)C)C=3C(=O)[C@@H]4[C@H](C)[C@H](C3C(=C2)CC=C(C)C)C4', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(OC[C@@H](O)C(=O)N[C@@H](C(=O)O)CC1=CC=C(O)C=C1)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)C[C@H](N)CCCCCC(C)C)CC(=O)N)[C@@H](O)C(=O)N)[C@@H](O)C2=CC=CC=C2', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C(NCC(=O)N)[C@H]1N(C(=O)C([C@H](O)C(/C=C/NC(=O)[C@@H](O)[C@@]2(O[C@@H]([C@H](C)C(C2)=C)C)O)C)C)CCC1', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OCC(O)C([O-])=O)[C@@H](O)[C@H]1O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O[C@H]1COc2cc(O)ccc2C1=O', 'Contains secondary alpha-hydroxy "
               "ketone group'), ('OC(C([O-])=O)C([O-])=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), ('O[C@H](COP(O)(O)=O)C(O)=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1O[C@H](CCC=CC=CCC[C@H](O)CC(O)C[C@H]2O[C@@](O)(C(O)C(=O)O[C@H](CCC=CC=CCC[C@@H](CC(C[C@H]3O[C@](C1O)(O)[C@@H](CC3)C)O)O)C)[C@H](C)CC2)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O(C1(C(O)C(OC2=C(C(O)=C(C(=C2)C)C(OC)=O)C)=C(C(=O)C1O)C)C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1O[C@@H](C[C@H]2O[C@@H]3[C@H](OCO[C@@H]3[C@H](C2(C)C)OC)NC(=O)[C@H](O)[C@@]4(O[C@@H]([C@H](C)C(C4)=C)C)OC)CC1', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('CCC(C)C1NC(=O)C(Cc2ccccc2)N(C)C(=O)C(C(C)CC)N2C(O)CCC(NC(=O)C(CCCNC(N)=N)NC(=O)C(NC(=O)C(O)COS(O)(=O)=O)C(C)OC1=O)C2=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('CC(=O)[C@@H](O)COP([O-])([O-])=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O[C@@H]6OC[C@@H](O)C(=O)[C@H]6O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C(O)=O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('S(=O)(=O)(OC[C@@H](O)C(=O)N[C@H](C(=O)N[C@@H]1C(=O)N[C@H](C(=O)N[C@@H]2C(=O)N([C@@H]([C@H](O)C)C(N([C@H](C(N[C@H](C(O[C@@H]1C)=O)[C@@H](CC)C)=O)CC3=CC=C(O)C=C3)C)=O)[C@H](O)CC2)CCCN=C(N)N)CC4=CC=C(O)C=C4)O', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('C1([C@@H]([C@H]([C@@H](C([C@@H]1O)=O)O)O)O)=O', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('O(P([O-])([O-])=O)CC([C@H](C(=O)[O-])O)=O', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('O[C@H](COP([O-])([O-])=O)C(=O)OP([O-])([O-])=O', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('BrC1=C(C=C(O)C=C1)[C@@H](OC)CC[C@@H]([C@H]2O[C@@]34OC(=C(C)CC3(C)C)C(O)C(=O)O[C@H](CC(O[C@H]([C@@H]2C)C4)=O)[C@H](O)C)C', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('CSC(=O)[C@H](O)COP(O)(O)=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('O=C(OCC(O)C(=O)NC(C(=O)OC(C(C(=O)NC(C(=O)NO)CCCN(O)C(=N)N)C)CCCCCCCC)CCCN(O)C=O)C1=C(O)C=CC=C1', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O=C1OC2(C(=CC(C2O)=O)C)C=3C1=C(O)C=C(OC)C3', 'Contains "
               "secondary alpha-hydroxy ketone group'), "
               "('O=C1C2=C(OC([C@@H]1O)(C)C)C(=C(/C=C/C=C/C)C(=C2)CC=C(C)C)CO', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O[C@H](COP(O)(O)=O)C(=O)OP(O)(O)=O', 'Contains secondary "
               "alpha-hydroxy ketone group'), "
               "('ClC1=CC=C(C[C@@H]2N3C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C(O)COS(=O)(=O)O)[C@@H](OC(C(NC([C@@H](N(C2=O)C)CC4=CC=C(O)C=C4)=O)C(CC)C)=O)C)CCCN=C(N)N)CC[C@H]3O)C=C1', "
               "'Contains secondary alpha-hydroxy ketone group'), "
               "('O(P([O-])([O-])=O)CC([C@@H](C(=O)[O-])O)=O', 'Contains "
               "secondary alpha-hydroxy ketone group')]\n"
               'False negatives: '
               "[('C[C@@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](NC(C)=O)[C@H](O)C1=O', "
               "'No secondary alpha-hydroxy ketone group found'), "
               "('COC1=C(O)C=CC(=C1)C1OC2=CC(O)=CC(O)=C2C(=O)C1O', 'No "
               "secondary alpha-hydroxy ketone group found'), "
               "('[H][C@@]12C[C@H](O)C(=O)C(C)(C)C1=CC[C@@]1([H])[C@]3(C)C[C@@H](O)[C@]([H])([C@@](C)(O)C(=O)CCC(C)(C)OC(C)=O)[C@@]3(C)CC(=O)[C@@]21C', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('[H][C@]1(Cc2cc3cc(O[C@H]4C[C@@H](O[C@@H]5C[C@@H](O)[C@@H](OC)[C@@H](C)O5)[C@@H](OC(C)=O)[C@@H](C)O4)cc(O)c3c(O)c2C(=O)[C@H]1O[C@H]1C[C@@H](O[C@H]2C[C@@H](O[C@H]3C[C@](C)(O)[C@@H](OC(=O)C(C)C)[C@H](C)O3)[C@H](O)[C@@H](C)O2)[C@H](O)[C@@H](C)O1)[C@H](OC)C(=O)[C@@H](O)[C@@H](C)O', "
               "'No secondary alpha-hydroxy ketone group found'), "
               "('O[C@H]1[C@@H](OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1', 'No "
               "secondary alpha-hydroxy ketone group found'), "
               "('O[C@H]1[C@@H](Oc2cc(O)cc(O)c2C1=O)c1ccc(O)c(O)c1', 'No "
               "secondary alpha-hydroxy ketone group found'), "
               "('CC1(C)[C@@H](O)C(=O)c2c1[nH]c1cc(O)ccc21', 'No valid "
               "secondary alpha-hydroxy ketone group found'), "
               "('[H][C@@]12C[C@@H](O)C(=O)[C@@]1(C)CC[C@]1([H])C3=C(CC[C@@]21[H])C=C(O)C=C3', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('O=C1C=C(N)C[C@@]1(O)C=C', 'No secondary alpha-hydroxy ketone "
               "group found'), "
               "('[H][C@@]12C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]3([H])[C@@H](O)[C@H](O)[C@@]4(C)OC[C@@]13[C@@]4([H])[C@@H](OC(=O)C=C(C)C)C(=O)O2', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('C[C@H]1C\\\\C=C/C(=O)[C@@H](O)[C@@H](O)C\\\\C=C\\\\c2cc(O)cc(O)c2C(=O)O1', "
               "'No secondary alpha-hydroxy ketone group found'), "
               "('[H][C@@]12C=C(O)C(=O)C(C)(C)C1=CC[C@@]1([H])[C@]3(C)C[C@@H](O)[C@]([H])([C@@](C)(O)C(=O)CCC(C)(C)OC(C)=O)[C@@]3(C)CC(=O)[C@@]21C', "
               "'No secondary alpha-hydroxy ketone group found'), "
               "('O=C([C@@]1([C@@H]2C(=C)CC[C@]2(O)C1)C)[C@H](O)C=C(C)C', 'No "
               "secondary alpha-hydroxy ketone group found'), "
               "('CCCCCCCCCC\\\\C=C(/[C@H](O)C(C)=O)C(=O)OC', 'No valid "
               "secondary alpha-hydroxy ketone group found'), "
               "('C[C@@]1([C@H]2[C@H](C(O)=O)[C@@]34CC(=C)[C@@](O)(C3)CC[C@H]4C2=CC(=O)[C@@H]1O)C(O)=O', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('C[C@H]1[C@H]2[C@H](Cc3c[nH]c4ccccc34)NC(=O)[C@@]22[C@@H](\\\\C=C\\\\C[C@H](C)\\\\C=C(C)\\\\[C@@H](O)C(=O)\\\\C=C\\\\C2=O)[C@H](O)C1=C', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('OC1C(OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1', 'No secondary "
               "alpha-hydroxy ketone group found'), ('OCC(O)C(=O)COP(O)(O)=O', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('[H][C@@]1(Oc2cc(O)cc(O)c2C(=O)[C@@H]1O)c1cc(O)c2O[C@]([H])([C@H](CO)c2c1)c1ccc(O)c(OC)c1', "
               "'No secondary alpha-hydroxy ketone group found'), "
               "('OC[C@@H](O)C(=O)CO', 'No valid secondary alpha-hydroxy "
               "ketone group found'), "
               "('O.O.O.[H][C@@]1(C[C@@]2(O)[C@@H](OC(=O)c3ccccc3)[C@]3([H])[C@@]4(CO[C@@H]4C[C@H](O)[C@@]3(C)C(=O)[C@H](O)C(=C1C)C2(C)C)OC(C)=O)OC(=O)[C@H](O)[C@@H](NC(=O)OC(C)(C)C)c1ccccc1', "
               "'No valid secondary alpha-hydroxy ketone group found'), "
               "('OC1(C(O)=C(C(O)=C(C1=O)C(=O)C(C)C)CC=C(C)C)CC=C(C)C', 'No "
               "secondary alpha-hydroxy ketone group found'), "
               "('C=1C=CC=CC1C(C(C)=O)O', 'No valid secondary alpha-hydroxy "
               "ketone group found'), ('BrC=1C(=O)[C@](O)(C=C)CC1N', 'No "
               "secondary alpha-hydroxy ketone group found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 20,
    'num_false_positives': 100,
    'num_true_negatives': 13248,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.16666666666666666,
    'recall': 0.8333333333333334,
    'f1': 0.2777777777777778,
    'accuracy': 0.9922225545916841}