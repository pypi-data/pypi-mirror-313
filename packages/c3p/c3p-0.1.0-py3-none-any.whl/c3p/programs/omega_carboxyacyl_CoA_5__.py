"""
Classifies: CHEBI:133241 omega-carboxyacyl-CoA(5-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_omega_carboxyacyl_CoA_5__(smiles: str):
    """
    Determines if a molecule is an omega-carboxyacyl-CoA(5-) based on structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an omega-carboxyacyl-CoA(5-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for CoA core structure components
    # - Adenine 
    adenine_pattern = Chem.MolFromSmarts('n1cnc2c(N)ncnc12')
    if not mol.HasSubstructMatch(adenine_pattern):
        return False, "Missing adenine moiety"

    # - Ribose with 3' phosphate and diphosphate
    ribose_diphosphate = Chem.MolFromSmarts('COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12')
    if not mol.HasSubstructMatch(ribose_diphosphate):
        return False, "Missing ribose-phosphate-diphosphate moiety"
        
    # - Pantetheine
    pantetheine = Chem.MolFromSmarts('CC(C)(COP)[C@@H](O)C(=O)NCCC(=O)NCCSC=O')
    if not mol.HasSubstructMatch(pantetheine):
        return False, "Missing pantetheine moiety"

    # Check for terminal carboxylate and thioester in a specific arrangement
    terminal_pattern = Chem.MolFromSmarts('SC(=O)CCCC([O-])=O')
    if not mol.HasSubstructMatch(terminal_pattern):
        return False, "Missing correct terminal carboxylate and thioester arrangement"

    # Count total negative charges - should be 5
    negative_charges = 0
    for atom in mol.GetAtoms():
        negative_charges += atom.GetFormalCharge()
    if negative_charges != -5:
        return False, f"Total negative charge is {negative_charges}, should be -5"

    # Check for absence of certain problematic features
    # No double bonds in the chain between thioester and terminal carboxylate
    problematic_pattern = Chem.MolFromSmarts('SC(=O)C=CC([O-])=O')
    if mol.HasSubstructMatch(problematic_pattern):
        return False, "Contains unsaturated bonds in the acyl chain"

    return True, "Contains all required structural components of omega-carboxyacyl-CoA(5-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133241',
                          'name': 'omega-carboxyacyl-CoA(5-)',
                          'definition': 'An acyl-CoA oxoanion obtained by '
                                        'deprotonation of the phosphate, '
                                        'diphosphate and carboxy groups of any '
                                        'omega-carboxyacyl-CoA; major species '
                                        'at pH 7.3.',
                          'parents': ['CHEBI:58946']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.03448275862068965 is too low.\n'
               'True positives: '
               "[('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)')]\n"
               'False positives: '
               "[('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@H](O)CCCCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCSC(=O)C(\\\\S)=C\\\\CC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)=CCC\\\\C(CC([O-])=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCSC(=O)C(=O)CCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N1C=NC2=C1N=CN=C2N)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)[C@@H](CC([O-])=O)[C@@H](O)C1=CC=CC=C1', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C(O)CCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C(\\\\CC([O-])=O)=C\\\\c1ccccc1', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CCC(C(CCC([O-])=O)=O)C)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@H](O)CCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[H]C(CCC([O-])=O)=C([H])C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC(C(=O)[O-])C=4C=CC=CC4)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C4=C([C@@H](CCC4=O)C)CCC([O-])=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=C)C([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@](C)(O)C([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(C)(O)C([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C=3C(=C(N=CN3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(/C=C/CCC([O-])=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC(C(=O)[O-])C=4C=CC=CC4N)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@](C)(O)C([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCC(=O)C=4C=CC=CC4C(=O)[O-])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C/CCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('C[C@@H](CC([O-])=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@H](O)CCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)[C@@H](CC([O-])=O)Cc1ccccc1', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(O)CCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C=3C(=C(N=CN3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)[C@@H](CCC(=O)[O-])O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@H](O)CCCCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N1C=NC2=C1N=CN=C2N)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)[C@@H](CC([O-])=O)C(=O)C1=CC=CC=C1', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCSC(=O)C(=S)CCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C(CC(=O)[O-])C=4C=CC=CC4N)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C\\\\C=C/CC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](CC(=O)[O-])CC4=CC=CC=C4)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C=CCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[H]C(CC([O-])=O)=C([H])CC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('C[C@@H]([C@@H](O)C([O-])=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CC(CCC(C(CCC([O-])=O)=O)C)=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C[C@@H](O)CCC([O-])=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('C[C@](O)(CC([O-])=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C(CC(=O)[O-])C=4C=CC=CC4)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@H](O)CCCCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@H](O)CCCCCCCCC([O-])=O', "
               "'Contains all required structural components of "
               "omega-carboxyacyl-CoA(5-)')]\n"
               'False negatives: '
               "[('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C([O-])=O', "
               "'Missing terminal carboxylate and/or thioester linkage')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 5,
    'num_true_negatives': 183910,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.16666666666666666,
    'recall': 0.5,
    'f1': 0.25,
    'accuracy': 0.9999673765883523}