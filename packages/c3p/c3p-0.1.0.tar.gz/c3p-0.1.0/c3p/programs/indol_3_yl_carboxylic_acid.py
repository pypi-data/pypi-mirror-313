"""
Classifies: CHEBI:24810 indol-3-yl carboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_indol_3_yl_carboxylic_acid(smiles: str):
    """
    Determines if a molecule is an indol-3-yl carboxylic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an indol-3-yl carboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Basic indole core with carboxylic acid at position 3
    # [#6] represents any carbon (aliphatic or aromatic)
    # The carboxylic acid can be connected through a carbon chain
    patterns = [
        # Indole core with carboxylic acid or ester at position 3
        '[nH,n]1c([CH2,CH]C([OH,O-,OC])=O)c2ccccc2c1',
        '[nH,n]1c(CC([OH,O-,OC])=O)c2ccccc2c1',
        '[nH,n]1c(CCC([OH,O-,OC])=O)c2ccccc2c1',
        # Include substituted variants
        '[nH,n]1c([CH2,CH]C([OH,O-,OC])=O)c2cc([*,H])c([*,H])c([*,H])c2c1',
        '[nH,n]1c(CC([OH,O-,OC])=O)c2cc([*,H])c([*,H])c([*,H])c2c1',
        '[nH,n]1c(CCC([OH,O-,OC])=O)c2cc([*,H])c([*,H])c([*,H])c2c1',
        # Alternative indole representation
        '[nH,n]1cc([CH2,CH]C([OH,O-,OC])=O)c2ccccc12',
        '[nH,n]1cc(CC([OH,O-,OC])=O)c2ccccc12',
        '[nH,n]1cc(CCC([OH,O-,OC])=O)c2ccccc12',
        # Include substituted variants for alternative representation
        '[nH,n]1cc([CH2,CH]C([OH,O-,OC])=O)c2cc([*,H])c([*,H])c([*,H])c12',
        '[nH,n]1cc(CC([OH,O-,OC])=O)c2cc([*,H])c([*,H])c([*,H])c12',
        '[nH,n]1cc(CCC([OH,O-,OC])=O)c2cc([*,H])c([*,H])c([*,H])c12'
    ]

    for pattern in patterns:
        substructure = Chem.MolFromSmarts(pattern)
        if substructure is not None and mol.HasSubstructMatch(substructure):
            return True, "Contains indol-3-yl carboxylic acid or derivative"

    return False, "No indol-3-yl carboxylic acid pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24810',
                          'name': 'indol-3-yl carboxylic acid',
                          'definition': 'Any indolyl carboxylic acid carrying '
                                        'an indol-3-yl or substituted '
                                        'indol-3-yl group.',
                          'parents': ['CHEBI:46867']},
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
               "[('C12=C(C=CC=C1)NC=3[C@]([C@@]4(/C(/CN(CC4)CCC32)=C\\\\C)[H])(C(=O)OC)CO', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)O)CC=2NC=3C=CC=CC3C2)CCC(=O)NCCCC[C@@H]4NC(=O)C(CCCNC(=N)N)NC([C@@H]([C@H](OC(CC5C(N[C@H](C(N[C@@H]1CCC(=O)OC[C@H](NC(=O)[C@H]6N(C(=O)[C@H](CC7=CC=C(O)C=C7)NC4=O)CCC6)C(=O)N5)=O)CC=8C9=C(C=CC=C9)NC8)=O)=O)C)NC(=O)[C@@H](NC(=O)C(NC(=O)C)C(CC)C)CO)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(O)C[C@@]1(OCCC2=C1NC=3C(=CC=CC23)CO)CC', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('COC1=CC=CC2=C1C(=C(N2)C(=O)OC)NC(=O)CCN3CCN(CC3)C4=CC(=CC=C4)Cl', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('Cc1c([nH]c2cccc(C)c12)C(O)=O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('OC(=O)c1cc(C(O)=O)c2c(n1)c(O)c(O)c1cc([nH]c21)C(O)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1OC2=C(O1)C=C(C=C2)C=CC(=O)NC3=C(NC4=CC=CC=C43)C(=O)O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('OC(=O)C1(NC(CC2=C1NC=3C2=CC=CC3)C(O)=O)C', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('O[C@H]([C@@H](O)C(O)=O)C(O)=O.O[C@H]([C@@H](O)C(O)=O)C(O)=O.[H][C@]12CN(CC(CC)=C1)Cc1c([nH]c3ccccc13)[C@@](C2)(C(=O)OC)c1cc2c(cc1OC)N(C)[C@@]1([H])[C@@](O)([C@H](OC(C)=O)[C@]3(CC)C=CCN4CC[C@]21[C@]34[H])C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O(C(=O)[C@@]12[C@@]3(N(C[C@](C1)(C=C3CC)[H])CCC4=C2NC=5C4=CC=CC5)[H])C.O(C(=O)[C@@]12[C@@]3(N(C[C@](C1)(C=C3CC)[H])CCC4=C2NC=5C4=CC=CC5)[H])C.O[C@H]([C@@H](O)C(O)=O)C(O)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('OC1=CC2=C(NC(=C2)C(O)=O)C=C1', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('[O-]C(=O)c1cc2cc([O-])c([O-])cc2[nH]1', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('CCOC(=O)C1=C(C2=CC=CC=C2N1)NC(=S)NC3=CC=CC(=C3C)C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@]1(C[C@]2(C[C@]3(C4=C(CCN(C2)C13)C5=CC(=C(C=C5N4)OC)OC)C(=O)OC)[H])[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('OS(O)(=O)=O.[H][C@@]12N3CC[C@@]11c4cc(c(OC)cc4N(C)[C@@]1([H])[C@](O)([C@H](OC(C)=O)[C@]2(CC)C=CC3)C(=O)OC)[C@]1(C[C@@H]2C[N@](CCc3c1[nH]c1ccccc31)C[C@](O)(CC)C2)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCOC(=O)C1=C(C2=CC=CC=C2N1)NC(=O)C3=CC=CO3', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('O=C(O)C[C@@]1(OCCC2=C1NC=3C(=C(O)C=CC23)CC)CC', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('O=C1C=2NC=3C=CC=CC3C2C(=C1C4=C(NC5=C4C=CC=C5)/C(/C(=O)OC)=C\\\\C6=CC=C(O)C=C6)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O([C@@H]1[C@]2([C@@]3(N(CC[C@@]34[C@@](NC=5C4=CC(=C(OC)C5)[C@]6(C[C@]7(C[C@](O)(CN(C7)CCC8=C6NC=9C8=CC=CC9)CC)[H])C(OC)=O)([C@@]1(OC(=O)C)O)[H])CC=C2)[H])CC)C(=O)C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('Oc1c(O)c2nc(cc(C([O-])=O)c2c2[nH]c(cc12)C([O-])=O)C([O-])=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1=CC=C(C=C1)NC(=O)C=CC2=C(NC3=CC(=CC(=C32)Cl)Cl)C(=O)O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@H]1C[C@@H]2CN3CCc4c([nH]c5cc([C@H]6C[C@@H]7C([C@@H](Cc8c6[nH]c6ccccc86)NC\\\\C7=C\\\\C)C(=O)OC)c(OC)cc45)[C@](C2)([C@H]13)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('OC(=O)C1=CC2=CC(O)=C(O)C=C2N1', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('Cc1c([nH]c2cccc(C)c12)C([O-])=O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('C1=CC2=C(C=C1F)C=C(N2)C(=O)O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('CCC1(CC2CC(C3=C(CCN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)C78CCN9C7C(C=CC9)(C(C(C8N6C)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC)O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('Oc1cc2cc([nH]c2cc1O)C([O-])=O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('Oc1c([O-])c2nc(cc(C([O-])=O)c2c2[nH]c(cc12)C([O-])=O)C([O-])=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1=CC=C2C(=C1)C=CC3=C2C=C(N3)C(=O)O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('[C@@]12([C@@]3([C@H](C[C@](C1)(C[N+]3(CCC=4C5=C(C=CC(=C5)O)NC42)[H])[H])CC)[H])C(OC)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCC1=C[C@H]2C[N@@](C1)CCc1c([nH]c3ccccc13)[C@@](C2)(C(=O)OC)c1cc2c(cc1OC)N(C)[C@@H]1[C@]22CCN3CC=C[C@](CC)([C@@H]23)[C@@H](OC(C)=O)[C@]1(O)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1=CC2=C(C=C1)C(CCN3C=C(C=CC3)CC)=C(N2)C(C(OC)=O)=C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(O)C[C@@]1(OCCC2=C1NC=3C(=CC=CC23)CCO)CC', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('[O-]C(=O)C[C@H]1CCC2=C1NC1=C2C=C(OCC2=CC(=C(C=C2)C2CCCC2)C(F)(F)F)C=C1', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('OC(=O)C1NC(C=2NC=3C(C2C1)=CC=CC3)C(O)=O', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('FC=1C=C(C(=O)N2CC(C3=C(NC=4C3=CC=CC4)C(=C2)C(OC(C)C)=O)(C)C)C=CC1F', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1=C(C(=CC2=C1N([C@@]3([C@@]24[C@@]5([C@]([C@H]([C@]3(O)C(=O)OC)OC(C)=O)(C=CC[NH+]5CC4)CC)[H])[H])C=O)[C@@]6(C=7NC8=CC=CC=C8C7CC[NH+]9C[C@](C[C@@H](C9)C6)(O)CC)C(OC)=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@@]4(/C(/C[NH+](CC4)CCC32)=C\\\\C)[H])(C(=O)OC)COC(C)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('S1C/2=NC(=C1)C(=O)N[C@@H]3C=4SC=C(N4)C(=O)N[C@H](C=5SC=C(C6=C(C7=NC(C(N[C@H](C(N\\\\C2=C(\\\\OC)/C)=O)[C@H](O)C)=O)=CS7)C=C(O)C(=N6)C=8SC=C(N8)C(=O)NC(=O)C(=O)N)N5)COC(C9=C%10CO[C@@H]3[C@H](O[C@@H]%11O[C@H]([C@@H](N)[C@](C%11)(O)C)C)C(=O)OCC%12=C%10C(=CC=C%12)N9)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCOC(=O)C1=C(C2=C(N1)C=CC(=C2)Br)NC(=O)CCN3CCCC(C3)(C)C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCC1=CC2CC(C3=C(CN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)C78CCN9C7C(C=CC9)(C(C(C8N6C)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C1N(C2=CC=C(OC(=O)C(NC(C(=O)O)C(CC)C)CC=3C4=C(C=CC=C4)NC3C(C(=O)O)C)C=C2)C(OC)CC1', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(O)[C@@H](N)CC=1NC=2C=CC=CC2C1', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@@]4(/C(/CN(CC4)CCC32)=C\\\\C)[H])(C(=O)OC)C=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('S(C1=C(N(C2=C1C=C(OCC3=NC=C(C=C3)C)C=C2)CC4=CC=C(C=C4)C=5C=CC(OCC)=NC5)CC(C)(C)C(O)=O)C(C)(C)C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(NC1C=2C3=C(C(=CC=C3)CC)NC2C(CC(=O)OCC)OC1)N', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@@]1(O)C[C@H]2C[N@@](C1)CCc1c([nH]c3ccccc13)[C@@](C2)(C(=O)OC)c1cc2c(cc1OC)N(C)[C@@H]1[C@]22CCN3CC=C[C@](CC)([C@@H]23)[C@@H](OC(C)=O)[C@]1(O)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@@]4(/C(/C[NH+](CC4)CCC32)=C\\\\C)[H])(C(=O)OC)CO', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('COC(=O)C1=C(C2=C(N1)C=CC(=C2)Br)NC(=O)CN3CCN(CC3)C4CCCCC4', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O(C(=O)C12[C@]3(N(C[C@@](C1)(C[C@@H]3CC)[H])CCC4=C2NC5=C4C=C(OC)C=C5)[H])C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(O)C1=C(NC2=C1C=CC=C2)/C(/C(=O)OC)=C\\\\C3=CC=C(O)C=C3', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@@]4(C(C=[N+](CC4)CCC32)CC)[H])(C(=O)OC)COC(C)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O[C@@H]([C@H](O)C(O)=O)C(O)=O.O[C@@H]([C@H](O)C(O)=O)C(O)=O.[H][C@]12CN(CC(CC)=C1)Cc1c([nH]c3ccccc13)[C@@](C2)(C(=O)OC)c1cc2c(cc1OC)N(C)[C@@]1([H])[C@@](O)([C@H](OC(C)=O)[C@]3(CC)C=CCN4CC[C@]21[C@]34[H])C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('OC(=O)C[C@H]1CCC2=C1NC1=C2C=C(OCC2=CC(=C(C=C2)C2CCCC2)C(F)(F)F)C=C1', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CS(=O)(=O)C1=CC=C(C=C1)CN2C3=C(CCCC3CC(=O)O)C4=CC(=CC(=C42)F)F', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('[C@@]12([C@@]3([C@H](C[C@](C1)(C[N+]3(CCC=4C5=C(C=CC(=C5)O)NC42)[H])[H])CC)[H])C([O-])=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O(C(=O)C12C3N(CC(C1)C=C3CC)CCC4=C2NC=5C4=CC=CC5)C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O(C=1C=C2C(NC(=C2)C(O)=O)=CC1O)C', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('[C@@]12([C@@]3([C@H](C[C@](C1)(C[NH+]3CCC=4C5=C(C=CC=C5)NC42)[H])CC)[H])C(OC)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(O)C[C@@H]1OCCC2=C1NC=3C(=CC=CC23)CC', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('CCOC(=O)C1=C(C2=CC=CC=C2N1)NC(=O)CN3CCCCC3', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@H]1C[C@]2(C[C@]3(C4=C(CC[NH+](C2)[C@@]13[H])C=5C=C(C=CC5N4)OC)C(=O)OC)[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@@]4(C(=C[NH+](CC4)CCC32)CC)[H])(C(=O)OC)COC(C)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCC1(CC2CC(C3=C(CCN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)C78CCN9C7C(C=CC9)(C(C(C8N6C)(C(=O)OC)O)C(=O)OC)CC)OC)C(=O)OC)O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('COC(=O)C12COCC=C3CN(CCC13)Cc1c2[nH]c2ccccc12', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('S1C2=NC(=C1)C(=O)N[C@@H]3C=4SC=C(N4)C(=O)N[C@H](C=5SC=C(C6=C(C7=NC(C(N[C@H](C(NC2=C(OC)C)=O)[C@H](O)C)=O)=CS7)C=C(O)C(=N6)C=8SC=C(N8)C(=O)NC(C(=O)N)=C)N5)COC(C9=C%10CO[C@@H]3[C@H](O)C(=O)OCC%11=C%10C(=CC=C%11)N9)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@@]1(C[C@@]2(C[C@@]3(C4=C(CCN(C2)[C@]13[H])C5=CC(=C(C=C5N4)OC)[C@]6(C[C@]7([C@H](CC)CN(C)[C@@](CC=8C9=CC=CC=C9NC86)(C7C(=O)OC)[H])[H])O)C(=O)OC)[H])[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O=C(NC(C(=O)NC(C(=O)O)CC=1NC=2C=CC=CC2C1)CC3=CC=C(O)C=C3)C4N(C(=O)C(NC(=O)C(O)C(NC)CCCCCCC)C(O)C)CCC4', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1[C@@]2(C=C([C@@]3([C@@]1(C(OC)=O)C4=C(C5=C(C=CC=C5)N4)CC[NH+]3C2)[H])CC)[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O(C(=O)C=1NC=2C(C1CCN3CCN(CC3)C4=CC=CC=C4)=CC(OC)=C(OC)C2)CC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('S1C2=NC(=C1)C(=O)N[C@@H]3C=4SC=C(N4)C(=O)N[C@H](C=5SC=C(C6=C(C7=NC(C(N[C@H](C(NC2=C(OC)C)=O)[C@H](O)C)=O)=CS7)C=C(O)C(=N6)C=8SC=C(N8)C(=O)N)N5)COC(C9=C%10CO[C@@H]3[C@H](O[C@@H]%11O[C@H]([C@@H](N(C)C)[C@](C%11)(O)C)C)C(=O)OCC%12=C%10C(=CC=C%12)N9)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCC1=C(NC2=C1C=C(C=C2)Br)C(=O)O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('N[C@@H](CCCNC(N)=N)C(O)=O.OC(=O)C[C@H]1CCC2=C1NC1=C2C=C(OCC2=CC(=C(C=C2)C2CCCC2)C(F)(F)F)C=C1', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@H]1C[C@]2(C[C@]3(C4=C(CCN(C2)[C@@]13[H])C=5C=C(C=CC5N4)OC)C(=O)OC)[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C(C)[C@@]12[C@]3([C@]4(C=5C(N(C)[C@]4([C@](C(NNC(OCCSSC[C@H](NC([C@@H](NC([C@@H](NC([C@@H](NC([C@@H](NC(CC[C@H](NC(=O)C6=CC=C(NCC=7N=C8C(=NC(N)=NC8=O)NC7)C=C6)C(O)=O)=O)CC(O)=O)=O)CCCNC(=N)N)=O)CC(O)=O)=O)CC(O)=O)=O)C(O)=O)=O)=O)(O)[C@@H]1O)[H])=CC(OC)=C([C@]9(C(OC)=O)C%10=C(C=%11C(=CC=CC%11)N%10)CCN%12C[C@](C[C@](C%12)(CC)O)([H])C9)C5)CCN3CC=C2)[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O1C(C=2NC=3C(C2CC1)=CC=CC3CC)(CC(O[C@@H]4OC([C@@H](O)C(O)C4O)C(O)=O)=O)CC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('N12C[C@@](C[C@H](C1)C[C@](C(=O)OC)(C3=C(C=C4C(=C3)[C@]56[C@@H]7[C@]([C@@]([C@@]([C@@]5(N4C)[H])(C(=O)OC)O)([H])OC(C)=O)(C=CCN7CC6)CC)OC)C=8NC=9C(=CC=CC9)C8C2)(C(C)(F)F)[H]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCOC(=O)C1=C(C2=CC=CC=C2N1)NC(=O)CC(C)(C)C', 'Contains "
               "indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@@H]([C@@]4(/C(/C[NH+](CC4)CCC32)=C\\\\C)[H])C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('O[C@]1([C@@]2(N(C=3C(C42[C@]5(N(CC4)CC=C[C@]5([C@H]1O)CC)[H])=CC(=C(OC)C3)[C@]6(C[C@]7(C[C@](O)(CN(C7)CCC8=C6NC=9C8=CC=CC9)CC)[H])C(OC)=O)C)[H])C(OC)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('N1C(=CC2=C1C=CC(=C2)OC)C(=O)O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('O=C(NC(C(=O)NC(C(=O)O)CC=1NC=2C=CC=CC2C1)CC3=CC=C(O)C=C3)C4N(C(=O)C(NC(=O)C(O)C(N)CCCCCCC)C(O)C)CCC4', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCC1=C[C@@H]2CN(C1)CC3=C([C@@H]([C@H]2C4=C(C=C5C(=C4)[C@]67CCN8[C@H]6C(C=CC8)([C@H]([C@@](C7N5C)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC)NC9=CC=CC=C39', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC(C)c1ccc2n(Cc3ccc(Cl)cc3)c(CC(C)(C)C(O)=O)c(SC(C)(C)C)c2c1', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCN(CC(=O)NC1=C(NC2=C1C=C(C=C2)Cl)C(=O)OC)C3=CC4=C(C=C3)OCO4', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('COC1=CC=CC(=C1)C(=O)NC2=C(NC3=CC(=C(C=C32)OC)OC)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCC1=C[C@H]2C[C@@](C3=C(CN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)[C@]78CCN9[C@H]7[C@](C=CC9)([C@H]([C@@]([C@@H]8N6C)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('COC1=CC=C(C=C1)N2C(=O)C(=CC3=C(NC4=CC=CC=C43)C(=O)OC)C(=O)NC2=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('COC(=O)C1=C(\\\\N=N\\\\N2CC3C[C@H](C2)C2=CC=CC(=O)N2C3)C2=C(N1)C=CC=C2', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@@]4(/C(/CN(CC4)CCC32)=C\\\\C)[H])(C(=O)OC)COC(C)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1=CC2=C(C=C1)C(CCN3C=C(CCC3)CC)=C(N2)C(C(OC)=O)=C', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('[O]c1c(O)c2nc(cc(C(O)=O)c2c2[nH]c(cc12)C(O)=O)C(O)=O', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('[H][C@@]12N3CC[C@@]11c4cc(c(OC)cc4N(C)[C@@]1([H])[C@](O)([C@H](OC(C)=O)[C@]2(CC)C=CC3)C(=O)OC)[C@]1(C[C@@H]2CN(CCc3c1[nH]c1ccccc31)C[C@](O)(CC)C2)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@H]1C[C@@H]2CN3CCc4c([nH]c5cc(OC)c(cc45)[C@H]4C[C@@H]5C([C@@H](Cc6c4[nH]c4ccccc64)NC\\\\C5=C\\\\C)C(=O)OC)[C@](C2)([C@H]13)C(=O)OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('Cc1c([nH]c2ccccc12)C([O-])=O', 'Contains indol-3-yl "
               "carboxylic acid or derivative'), "
               "('COC(=O)C1[C@H]2Cc3c([nH]c4ccccc34)[C@H](C[C@H]1\\\\C(CN2C)=C/C)c1cc2[nH]c3c(CCN4C[C@H]5C[C@H]([C@@H](C)O)[C@H]4[C@]3(C5)C(=O)OC)c2cc1OC', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C12=C(C=CC=C1)NC=3[C@]([C@]4(/C(/CN(CC4)CCC32)=C\\\\C)[H])(C(=O)OC)CO', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('C1=C(C(=CC2=C1N([C@@]3([C@@]24[C@@]5([C@]([C@H]([C@]3(O)C(=O)OC)OC(C)=O)(C=CC[NH+]5CC4)CC)[H])[H])C=O)[C@@]6(C=7NC8=CC=CC=C8C7CC[NH+]9C[C@](C[C@@H](C9)C6)(O)CC)C(OC)=O)OC.O=S(=O)([O-])[O-]', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CC[C@]12C[N@@]3C[C@@H](C[C@@](C(=O)OC)(c4[nH]c5ccccc5c4CC3)c3cc4c(cc3OC)N(C)[C@@H]3[C@]44CCN5CC=C[C@](CC)([C@@H]45)[C@@H](OC(C)=O)[C@]3(O)C(=O)OC)[C@H]1O2', "
               "'Contains indol-3-yl carboxylic acid or derivative'), "
               "('CCOC1=CC2=C(C=C1)NC(=C2NC(=O)CN3CCC4(CC3)OCCO4)C(=O)OCC', "
               "'Contains indol-3-yl carboxylic acid or derivative')]\n"
               'False negatives: '
               "[('COc1ccc2n(cc(CC(O)=O)c2c1)C(=O)c1ccc(Cl)cc1', 'No "
               "indol-3-yl carboxylic acid pattern found'), "
               "('OC1=CC=2C(=C(NC2C=C1)C)CC(O)=O', 'No indol-3-yl carboxylic "
               "acid pattern found'), ('O(C)C1=CC2=C(NC=C2CC(O)=O)C=C1', 'No "
               "indol-3-yl carboxylic acid pattern found'), "
               "('COC(=O)CC1=CN(C2=CC=CC=C21)C3=C(C=C(C=N3)C(F)(F)F)Cl', 'No "
               "indol-3-yl carboxylic acid pattern found')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 27548,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 0.75,
    'f1': 0.056074766355140186,
    'accuracy': 0.9963474613047881}