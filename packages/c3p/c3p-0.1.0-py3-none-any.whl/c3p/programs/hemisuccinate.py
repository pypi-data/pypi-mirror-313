"""
Classifies: CHEBI:138979 hemisuccinate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hemisuccinate(smiles: str):
    """
    Determines if a molecule is a hemisuccinate (mono-esterified succinic acid derivative)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hemisuccinate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for hemisuccinate group: -O-C(=O)-CH2-CH2-C(=O)-OH
    # Using more general pattern that captures the core structure
    hemisuccinate_pattern = Chem.MolFromSmarts('[#6]-O-C(=O)-[CH2]-[CH2]-C(=O)-[OH]')
    
    # Pattern for diester (to exclude)
    diester_pattern = Chem.MolFromSmarts('[#6]-O-C(=O)-[CH2]-[CH2]-C(=O)-O-[#6]')
    
    if mol.HasSubstructMatch(hemisuccinate_pattern):
        # Check if it's not part of a diester
        if not mol.HasSubstructMatch(diester_pattern):
            return True, "Contains hemisuccinate group"
        else:
            # Additional check to see if there's at least one free acid group
            acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
            acid_matches = len(mol.GetSubstructMatches(acid_pattern))
            if acid_matches > 0:
                return True, "Contains hemisuccinate group"
            
    return False, "No hemisuccinate group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138979',
                          'name': 'hemisuccinate',
                          'definition': 'A succinate ester in which only one '
                                        'of the carboxy groups of succinic '
                                        'acid has been esterified.',
                          'parents': ['CHEBI:36181', 'CHEBI:36244']},
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
               "[('O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=C(C=3O[C@@H](CC(=O)C3C(O)=C2C)C4=CC=CC=C4)C)COC(=O)CC(O)(CC(O)=O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](C[C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5([C@H](C([C@H](OC(=O)C[C@@](O)(CC(=O)O)C)CC5)(C)C)CC4)C)C[C@@H]3O)(C)CC2)C)C)C(=C1C)C', "
               "'Contains hemisuccinate group'), "
               "('OC1C2(C(C3=C(C4(C(C(C(O)C(OC(=O)CC(O)(CC(O)=O)C)C4)(C)C)CC3)C)C1)(CCC2C(CCC(O)C(O)(C)C)C)C)C', "
               "'Contains hemisuccinate group'), "
               "('O[C@@H]1[C@]2([C@](C3=C([C@@]4(C(C([C@@H](O)[C@H](OC(=O)CC(O)(CC(O)=O)C)C4)(C)C)CC3)C)C1)(CC[C@@]2([C@@H](CC[C@@H](O)C(O)(C)C)C)[H])C)C', "
               "'Contains hemisuccinate group'), "
               "('O1C(C(O)C(O)C(O)C1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC=C(O)C=C4)COC(=O)CC(O)(CC(O)=O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)[C@@H](CC(=O)O[C@@H]([C@@H](OC(=O)C[C@H](C(=O)O)CC(=O)O)C[C@H](C[C@H](O)CCCCCC[C@@H](O)[C@@H](N)C)C)[C@@H](CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O([C@H]([C@H](OC(=O)C[C@@H](CC(O)=O)C(O)=O)[C@@H](CCCC)C)C[C@H](C[C@H](O)CCCC[C@H](O)C[C@@H](O)[C@H](NC(=O)C)C)C)C(=O)C[C@@H](CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)[C@H](C(=C)CC[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](OC(=O)C[C@@](O)(CC(=O)O)C)CC4)(C)C)CC3)C)C[C@@H]2O)(C)CC1)C)C)C', "
               "'Contains hemisuccinate group'), ('COC(=O)[C@@H](N)CCC(O)=O', "
               "'Contains hemisuccinate group'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CCC(O)=O)[C@H]3O', "
               "'Contains hemisuccinate group'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC([C@]3(COC(=O)C[C@@](O)(CC(=O)O)C)C)=O)C)[C@@]4(C(=O)C[C@@H]([C@]4(C1)C)[C@@H](CC/C=C(/C(=O)O)\\\\C)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)C[C@@H](O)CCCCCCC)CC(C)C)CCC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)[C@H](CC)C)=O)CC(C)C)=O)CCC(=O)N)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)C[C@@H](O)CCCCCCC)CC(C)C)CC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)[C@H](CC)C)=O)CC(C)C)=O)CCC(=O)N)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'Contains hemisuccinate group'), "
               "('C[C@H](N1C(=O)CCC1(O)C(O)=O)C(=O)NCCOC(=O)C[C@](O)(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](C[C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5([C@H](C([C@@H](OC(=O)C[C@@](O)(CC(=O)O)C)CC5)(C)C)[C@@H](C4)O)C)C[C@@H]3O)(C)CC2)C)C)C(=C1C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)C(CC(=O)O[C@@H]([C@@H](OC(=O)CC(C(=O)O)CC(=O)O)C[C@H](C[C@H](O)CCCCC[C@@H](O)[C@H](O)[C@@H](N)C)C)[C@@H](CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C1N(C(C(=O)O)C(OC(=O)CC(OC(=O)CC(CC(=O)O)C)CCCCCCCCCCC)CN(C1C(O[C@@H]2O[C@H](CN)[C@H](C2)O)[C@H]3O[C@@H](N4C(=O)NC(=O)C=C4)C[C@@H]3O)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1C([C@H]2[C@]([C@@H]3[C@@]([C@H](C4=CC[C@@H](C(C=5OC(C)(C)C(C5)=O)=C)O[C@H]4O)C(C3)=O)(C)CC2)(C)C[C@H]1OC(=O)CC(O)(CC(=O)O)C)(C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)C[C@@H](O)CCCCC)CC(C)C)CC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)[C@H](CC)C)=O)CC(C)C)=O)CCC(=O)N)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1OC(=O)C(=C1/C=C/CC)CC(CC=2C(=O)OC(C2CC(CC=3C(=O)OC(C3CCC(=O)O)=O)CC)=O)CC', "
               "'Contains hemisuccinate group'), "
               "('O=C(O[C@H]1[C@H](OC(=O)C)C(C2CCC3=C([C@]2(C1)C)CC[C@]4([C@]3(CC[C@@H]4C5[C@@H](O[C@@H](C(O)(C)C)CC5)O)C)C)(C)C)CC(O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1[C@]2([C@](C=3CC[C@@H]4[C@@](C3C1)(CC[C@@H](C4(C)C)OC(=O)C[C@@](O)(CC(=O)O)C)C)(CC[C@@H]2[C@@H](CCC(=C)[C@@H](C(=O)O)C)C)C)C', "
               "'Contains hemisuccinate group'), "
               "('S(=O)(=O)(OC1C(OC(C1O)CN)OC(C2N(CC(OC(=O)CC(OC(=O)CC(CC(=O)O)C)CCCC/C=C/C/C=C/CCCC)C(N(C2=O)C)C(=O)O)C)C3OC(N4C(=O)NC(=O)C=C4)C(C3O)O)O', "
               "'Contains hemisuccinate group'), "
               "('O1C(C(OC(=O)CC(O)(CC(O)=O)C)C(O)C(O)C1OC2=C(OC3=C(C2=O)C(OC)=C(OC)C(OC)=C3OC)C4=CC(OC)=C(OC)C=C4)CO', "
               "'Contains hemisuccinate group'), "
               "('P(OC[C@H](OC(=O)CCCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O(CCCC)C(=O)[C@@H](N)CCC(O)=O', 'Contains hemisuccinate "
               "group'), "
               "('O(CC(C(COC1OC(C(O)C(O)C1O)CO)CC2=CC(OC)=C(O)C=C2)CC3=CC(OC)=C(O)C=C3)C4OC(C(O)C(O)C4O)COC(=O)CC(O)(CC(O)=O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)C(CC(=O)OC(C(OC(=O)CC(C(=O)O)CC(=O)O)CC(CC(O)CCCCC(O)C(O)C(O)CNC(=O)C)C)C(CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O1C(C(C(C(=C1)C(OC)=O)CC(O)=O)C=O)C', 'Contains "
               "hemisuccinate group'), ('OC(CC(OCC(O)CO)=O)(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)C(CC(=O)OC(C(O)CC(CCCCCCCCC(O)CN)C)C(CC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O(C(C(OC(=O)CC(CC(O)=O)C(O)=O)C(CCCC)C)CC(CC(O)CCCCC(O)CC(O)C(N)C)C)C(=O)CC(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C(OC)[C@H](OC[C@H]1C(=C)CC[C@@H]2[C@@]1(CCC[C@]2(CO)C)C)[C@@H](C(=O)OC)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@H](CCC[C@@H](OC(=O)[C@@]2(OC(=O)C(=C2C3=CC=CC=C3)O)CCC(=O)O)CC(CC=4C1=C(O)C=C(O)C4)=O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O[C@H]1[C@H](OC(=O)C)C(C2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4C5[C@@H]6OC(C)(C)[C@@H](O6)CC5)C)C)(C)C)CC(O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@H]([C@H](NC(=O)[C@H](N(C(=O)[C@H]2N(C(=O)[C@@H](OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCC)CCC(=O)N)CCC(=O)N)CCC(=O)O)C)CCC2)C)CC(C)C)C(=O)N[C@H]([C@@H](O)CC(=O)O[C@@H](C(C)C)C([C@@H](C(N[C@H](C(N3[C@H](C(N([C@H]1CC4=CC=C(OC)C=C4)C)=O)CCC3)=O)CC(C)C)=O)C)=O)[C@H](CC)C)C', "
               "'Contains hemisuccinate group'), ('COC(=O)CCCC(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)C(CC(=O)OC(C(O)CC(CCCCCC(O)C(O)CC(O)CN)C)C(CC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C(OC[C@@H](O)C(O)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)C)\\\\C)\\\\C)C)CC(O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('C[C@H](CC(=O)O)CC(=O)O[C@H](CC(=O)[O-])C[N+](C)(C)C', "
               "'Contains hemisuccinate group'), "
               "('C/C(=C\\\\CC\\\\C(\\\\C)=C\\\\C[C@]12C(C=C([C@H]([C@H]1O2)O)COC(CC(CC(O)=O)(O)C)=O)=O)/CCC=C(C)C', "
               "'Contains hemisuccinate group'), "
               "('[C@H](OC(CCCC(=O)O)=O)(C[N+](C([2H])([2H])[2H])(C([2H])([2H])[2H])C)CC(=O)[O-]', "
               "'Contains hemisuccinate group'), "
               "('C[C@@H](CC(O)=O)CC(=O)OC[C@H](C)\\\\C=C(/C)C[C@@H]1O[C@]2(C)C[C@@H]3O[C@@H]4C[C@@H]5O[C@@H]6CC[C@@H]7O[C@@H]8C[C@@H]9O[C@H](C[C@H](O)C[C@@H]%10C[C@@H](C)[C@H](O%10)[C@@H](C)CC(O)=O)[C@@H](O)CC[C@H]9O[C@@]8(C)C[C@@]7(C)O[C@H]6C\\\\C=C/[C@@H](C)[C@H]5O[C@@]4(C)[C@H](O)[C@H]3O[C@H]2CC1=C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](C[C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5([C@H](C([C@@H](OC(=O)C[C@@](O)(CC(=O)O)C)CC5)(C)C)CC4)C)C[C@@H]3O)(C)CC2)C)C)C(=C1C)C', "
               "'Contains hemisuccinate group'), "
               "('P(OC[C@H](OC(=O)CCCC(O)=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'Contains hemisuccinate group'), "
               "('CC(C)CCCCCCCCC(CC(=O)OC1CN(C)C(C(O[C@@H]2O[C@H](CN)[C@@H](O)[C@H]2OS(O)(=O)=O)[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)C(=O)N(C)C1C(O)=O)OC(=O)CC(C)CC(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O1[C@](C(O)C(O)[C@H](O)[C@@H]1COC(=O)CC(O)(CC(O)=O)C)(C=2C(O)=C([C@@]3(OC([C@H](O)[C@H](O)C3O)C)[H])C(O)=C4C2OC(=CC4=O)C5=CC=C(O)C=C5)[H]', "
               "'Contains hemisuccinate group'), "
               "('O(C(C)(C)C)C(=O)[C@H](N)CCC(O)=O', 'Contains hemisuccinate "
               "group'), "
               "('O=C(O)C(CC(=O)OC(C(OC(=O)CC(C(=O)O)CC(=O)O)CC(CC(O)CCCCCC(O)C(O)CN)C)C(CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O([C@H]1[C@@]([C@@]2([C@@](C1)(/C(/CCC2)=C/C=C\\\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)([C@H](CCCC(O)(C)C)C)[H])C(=O)CCCC(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O1[C@](C(O)C(O)[C@H](O)[C@@H]1COC(=O)CC(O)(CC(O)=O)C)(C=2C=3OC(=CC(=O)C3C(O)=CC2O)C4=CC=C(O)C=C4)[H]', "
               "'Contains hemisuccinate group'), "
               "('OC[C@H]1O[C@@H](Oc2ccc(COC(=O)CC(O)(CC(O)=O)C(=O)OCc3ccc(O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)cc3)cc2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains hemisuccinate group'), "
               "('S(=O)(=O)(OC1C(OC(C1O)CN)OC(C2N(CC(OC(=O)CC(OC(=O)CC(CC(=O)O)C)CCC/C=C\\\\C/C=C\\\\CCCCC)C(N(C2=O)C)C(=O)O)C)C3OC(N4C(=O)NC(=O)C=C4)C(C3O)O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](/C=C/C=C/C)[C@@H](C)C=C1CCC(=O)O', 'Contains "
               "hemisuccinate group'), "
               "('O=C1OC[C@]2([C@H]3[C@@]([C@H](C(=C)CC3)CO[C@@H](C(=O)O)[C@@H](C(=O)OC[C@]4([C@H]5[C@@]([C@@H](CO[C@H]([C@@H]1CC(=O)O)C(=O)OC)C(=C)CC5)(CCC4)C)C)CC(=O)O)(CCC2)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O[C@H]1[C@H](OC(=O)C)C(C2CCC3=C([C@]2(C1)C)C[C@H](OC(=O)C)[C@]4([C@]3(CC[C@@H]4C5[C@@H](O[C@@H](C(O)(C)C)CC5)O)C)C)(C)C)CC(O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)[C@H](C(=C)CC[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H]([C@]([C@H](OC(=O)CC(O)(CC(=O)O)C)CC4)(CO)C)CC3)C)C[C@@H]2O)(C)CC1)C)C)C', "
               "'Contains hemisuccinate group'), "
               "('CC(CC(=O)O)(CC(=O)OCC1C(C(C(C(O1)OC2=C(C=C3C=C(C(=O)OC3=C2)OC4=CC5=C(C=C4)C=CC(=O)O5)OC)O)O)O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](/C=C/C=C/C)[C@@](O)(C)C=C1CCC(=O)O', 'Contains "
               "hemisuccinate group'), "
               "('O=C1OC(CCC(C(O)C(C=C(CC(C=C(COC(CC(C1)C(=O)O)=O)CCC(=O)C(CC(C(=O)O)C)CC)C)C)C)C)CCCC/C=C/C(CCC(OC(=O)CC(C(=O)O)CC(=O)O)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)C(CC(=O)O[C@@H]([C@@H](OC(=O)CC(C(=O)O)CC(=O)O)C[C@H](CCCCCCCC[C@H](O)CN)C)[C@@H](CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('OC=1C=CC(=CC1OC)C=2OC3=CC(=CC(=C3C(C2O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)COC(=O)C[C@@](CC(O)=O)(O)C)O)O)O[C@@H]5OC[C@@]([C@]5(O)[H])(CO)O)=O)O)OC', "
               "'Contains hemisuccinate group'), "
               "('O1C(O)[C@H](OC(CCCC(O)=O)=O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)O)(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C(O[C@H]1[C@H](O)C([C@@H]2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4[C@H](CO)CC[C@@H](O)C(O)(C)C)C)C)(C)C)CC(O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O)[C@@H](CC(=O)O[C@H]([C@H](O)[C@@H](CC)C)C[C@H](CCCCCCCC[C@H](O)CN)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('OC(CC(OC(C)C)=O)(CC(O)=O)C(O)=O', 'Contains hemisuccinate "
               "group'), "
               "('O=C(O)[C@@H](CC(=O)O[C@H](C(O)[C@@H](CC)C)C[C@H](CCCCCC[C@@H](O)C[C@H](O)CNC(=O)C)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)CC(C)C)=O)CC(C)C)CC(C)C)CCCCCCCC(CC)C', "
               "'Contains hemisuccinate group'), "
               "('C/C(=C\\\\CC\\\\C(\\\\C)=C\\\\C[C@]12C(C=C(C([C@H]1O2)=O)COC(CC(CC(O)=O)(O)C)=O)=O)/CCC=C(C)C', "
               "'Contains hemisuccinate group'), "
               "('CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCC(O)=O', "
               "'Contains hemisuccinate group'), "
               "('CCCC[C@H]([C@H]([C@H](C[C@H](C[C@@H](CCCC[C@H](C[C@@H]([C@H](C)N)O)O)O)C)OC(C[C@@H](CC(=O)O)C(=O)O)=O)OC(=O)C[C@@H](CC(O)=O)C(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C(O[C@@H]1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@H](CO)CC[C@@H](O)C(O)(C)C)CC4)(C)[C@H](C3)O)C)CC2)(C)C[C@H]1O)(C)C)C[C@@](O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O([C@@H]1C[C@]2([C@](C([C@H]1O)(C)C)(CCC=3[C@]4([C@@]([C@](CC4)([C@@H](CC[C@@H](O)C(O)(C)C)C)[H])(CCC23)C)C)[H])C)C(=O)CC(O)(CC(O)=O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H]([C@@]3(COC(=O)C[C@@](O)(CC(=O)O)C)C)O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1OC(=O)C)C)[C@@H](CCC=C(C(=O)O)C)C)C', "
               "'Contains hemisuccinate group'), "
               "('OC(CC(OCC=1OC(=CC1)C=O)=O)(CC(O)=O)C(O)=O', 'Contains "
               "hemisuccinate group'), "
               "('CCCCOC(=O)[C@H](CCC(O)=O)NC(=O)c1cc2c3ccccc3[nH]c2c(n1)C(C)=O', "
               "'Contains hemisuccinate group'), "
               "('O([C@@H]([C@@H](OC(=O)C[C@@H](CC(O)=O)C(O)=O)C[C@H](CCCCCCCC[C@H](O)C(=O)C)C)[C@@H](CCCC)C)C(=O)C[C@@H](CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=C(C=3OC(=CC(=O)C3C(O)=C2C)C4=CC=CC=C4)C)COC(=O)CC(O)(CC(O)=O)C', "
               "'Contains hemisuccinate group'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](COC(=O)C[C@@](C)(O)CC(O)=O)O[C@H]1OC[C@H]1O[C@@H](OC(=O)[C@]23CCC(C)(C)C[C@@]2([H])C2=CC[C@]4([H])[C@@]5(C)CC[C@H](O)[C@@](C)(C(=O)O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)[C@]5([H])CC[C@@]4(C)[C@]2(C)C[C@H]3O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains hemisuccinate group'), "
               "('O=C(O[C@H]1[C@H](OC(=O)C)C(C2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4C5[C@@H](O[C@@H](C(O)(C)C)CC5)OC(=O)C)C)C)(C)C)CC(O)(CC(=O)O)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](/C=C/C=C/C(=O)O)[C@@H](C)C=C1CCC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H](CCC(O)C(O)(C)C)C)CC4)(C)CC3)C)CC2)(C)C[C@H]1OC(=O)CC(O)(CC(=O)O)C)(C)C', "
               "'Contains hemisuccinate group'), "
               "('O(C(C(OC(=O)CC(CC(O)=O)C(O)=O)C(CCCC)C)CC(CC(O)CCCCCCC(O)C([N+]=1C=C(O)C=CC1)C)C)C(=O)CC(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O(C(C(OC(=O)CC(CC(O)=O)C(O)=O)C(CCCC)C)CC(CCCCCCC(O)CC(O)C([N+]=1C=C(O)C=CC1)C)C)C(=O)CC(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O([C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\\\3/C[C@@H](OC(=O)CCCC(O)=O)C[C@H](O)C3=C)[H])C)[H])C)CCC(O)(C)C', "
               "'Contains hemisuccinate group'), "
               "('O([C@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCC(O)=O', 'Contains "
               "hemisuccinate group'), "
               "('O=C(O)C(CC(=O)O[C@@H]([C@@H](OC(=O)CC(C(=O)O)CC(=O)O)C[C@H](C[C@H](O)CCCC[C@@H](O)C[C@H](O)CN)C)[C@@H](CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O(C(C(OC(=O)CC(CC(O)=O)C(O)=O)C(CCCC)C)CC(CCCCCCCCC(O)C(N)C)C)C(=O)CC(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C1OC(/C=C/CC/C=C\\\\C/C=C\\\\CCCCC)CC1C(O)(C(=O)OC(C(=O)O)C(C(=O)O)CC(=O)O)CC(=O)O', "
               "'Contains hemisuccinate group'), "
               "('CC(=O)OC(=O)CC(O)(CC(=O)O)C(=O)O', 'Contains hemisuccinate "
               "group'), "
               "('O(C(CC(CCCCCCC(O)CC(O)C(NC(=O)C)C)C)C(=O)C(CCCC)C)C(=O)CC(CC(O)=O)C(O)=O', "
               "'Contains hemisuccinate group'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC([C@]3(COC(=O)C[C@@](O)(CC(=O)O)C)C)=O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@H]1O)C)[C@@H](CC/C=C(/C(=O)O)\\\\C)C)C', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)CC(C)C)=O)CC(C)C)CC(C)C)CCCCCC(CC(CC)C)C', "
               "'Contains hemisuccinate group'), "
               "('C(C(C(C(C(=O)OC([C@@H](N)CCC(=O)O)=O)(N(C(=O)C=1C=CC(=CC1)NCC2=NC=3C(=O)NC(N)=NC3N=C2)C([C@@H](N)CCC(=O)O)=O)C([C@@H](N)CCC(=O)O)=O)(C([C@@H](N)CCC(=O)O)=O)C([C@@H](N)CCC(=O)O)=O)(C([C@@H](N)CCC(=O)O)=O)C([C@@H](N)CCC(=O)O)=O)(=O)O', "
               "'Contains hemisuccinate group'), "
               "('O1[C@@H](O[C@@H]2OC=C([C@H]([C@H]2C=C)CC(O)=O)C(OC)=O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1CO', "
               "'Contains hemisuccinate group'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)C[C@@H](O)CCCCCCC)CC(C)C)CC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CCC(=O)O)=O)CC(C)C)=O)CC(C)C)=O)CCC(=O)N)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'Contains hemisuccinate group'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@H]1[C@H](O)[C@@H](CO[C@@H]2O[C@H](COC(=O)C[C@@](C)(O)CC(O)=O)[C@@H](O)[C@H](O)[C@H]2O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)O[C@@H](OC(=O)[C@]23CCC(C)(C)C[C@@]2([H])C2=CC[C@]4([H])[C@@]5(C)CC[C@H](O)[C@@](C)(C(=O)O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)[C@]5([H])CC[C@@]4(C)[C@]2(C)CC3)[C@@H]1O', "
               "'Contains hemisuccinate group'), "
               "('O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC=2C=C3OC(=CC(=O)C3=C(O)C2)C4=CC=C(O)C=C4)COC(=O)CC(O)(CC(O)=O)C', "
               "'Contains hemisuccinate group'), "
               "('CC(CC(O)=O)CC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', 'Contains "
               "hemisuccinate group'), "
               "('O=C(O)C(CC(=O)OC(C(OC(=O)CC(C(=O)O)CC(=O)O)CC(CC(O)CCCCC(O)CC(O)CNC(=O)C)C)C(CCCC)C)CC(=O)O', "
               "'Contains hemisuccinate group')]\n"
               "False negatives: [('N[C@@H](CCOC(=O)CCC(O)=O)C(O)=O', 'No "
               "hemisuccinate group found'), "
               "('[H][C@@]12CC[C@@H](C)[C@]3([H])CC[C@@]4(C)OO[C@@]13[C@]([H])(O[C@@H](OC(=O)CCC(O)=O)[C@@H]2C)O4', "
               "'No hemisuccinate group found'), "
               "('[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](C[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O)OC(=O)CCC(O)=O', "
               "'No hemisuccinate group found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 69,
    'num_true_negatives': 183833,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.041666666666666664,
    'recall': 1.0,
    'f1': 0.07999999999999999,
    'accuracy': 0.9996248062858542}