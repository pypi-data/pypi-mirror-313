"""
Classifies: CHEBI:140322 triketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_triketone(smiles: str):
    """
    Determines if a molecule contains exactly three ketone groups (C=O).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains exactly 3 ketone groups, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find all ketone groups (C=O)
    # This pattern matches a carbon with a double bond to oxygen, excluding carboxylic acids, esters, and amides
    ketone_pattern = Chem.MolFromSmarts('[C;!$(C(=O)O);!$(C(=O)OC);!$(C(=O)N)](=O)')
    matches = mol.GetSubstructMatches(ketone_pattern)
    
    # Count number of ketone groups
    num_ketones = len(matches)
    
    if num_ketones == 3:
        # Get the atoms involved in each ketone group for detailed reporting
        ketone_details = []
        for match in matches:
            carbon = mol.GetAtomWithIdx(match[0])
            neighbors = [n.GetSymbol() for n in carbon.GetNeighbors() if n.GetAtomicNum() != 8]  # exclude oxygen
            ketone_details.append(f"C(=O) bonded to {','.join(neighbors)}")
            
        return True, f"Contains exactly 3 ketone groups: {'; '.join(ketone_details)}"
    elif num_ketones > 3:
        return False, f"Contains {num_ketones} ketone groups (more than 3)"
    else:
        return False, f"Contains only {num_ketones} ketone groups (less than 3)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140322',
                          'name': 'triketone',
                          'definition': 'A compound that contains three ketone '
                                        'functionalities.',
                          'parents': ['CHEBI:17087']},
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
               "[('[C@@]12([C@]3([C@](C[C@@]1([C@]4([H])CC[C@H]([C@]4(C3)[H])C)C=O)(C=C2C(C)C)[H])CO[C@]5([C@H]([C@@H]([C@@H]([C@H](O5)C)O)O)O)[H])C(O)=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('ClC1=C(O)C=C(O)C(=C1C)C(=O)O[C@H]2[C@@]3(O)C(=C[C@@H]4CC(C[C@@H]4[C@@]3(C)C2)(C)C)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O1[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO)[C@@H](N)C=O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), ('[H]C(=O)CCCC([O-])=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('FC1=CC=C(C=2N(C(C(C)C)=C(C2C3=CC=CC=C3)C(=O)NC4=CC=CC=C4)CCC=O)C=C1', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,N; C(=O) "
               "bonded to C,N; C(=O) bonded to C'), "
               "('[H]C(=O)C1=CC=C(C=C1)C([O-])=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) bonded to '
               "C'), "
               "('Cl[C@H]1[C@](C=C)([C@H]([N+]#[C-])[C@]2(O)C(=O)C=3C(NC=O)=CC=CC3C([C@H]2C1)(C)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to N'), "
               "('BrC1=C(O)C(=C(O)C=C1C)C(=O)C2=C(C(O)=CC(=C2CC=C(C)C)O)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('OC1C(C(CC/C=C(\\\\C)/C=O)C)=CC(=O)C(=C1)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to '
               "C,C; C(=O) bonded to C,C'), "
               "('CNC[C@@H]1CC[C@@H](N)[C@@H](O[C@@H]2[C@H](N)C[C@H](OC)[C@H]([C@H]2O)N(C)C(=O)CNC=O)O1', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to N'), "
               "('CC1(C)C2CCC1(C=O)C(=O)C2', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C,C; C(=O) bonded '
               "to C,C'), "
               "('O[C@@H]1[C@@H]([C@H](O[C@@H]([C@H]1NC([H])=O)C)O[C@@H]2[C@@H]([C@H](O[C@@H]([C@H]2NC([H])=O)C)O[C@@H]3[C@H](O[C@@H]([C@H]([C@@H]3O)NC([H])=O)C)*)O)O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N; C(=O) "
               "bonded to N; C(=O) bonded to N'), "
               "('[H][C@@]12C[C@@H](CC[C@@]1([H])[C@]1(C)CC[C@@H](O)C(C)(C)[C@@]1([H])[C@H](O)C2=O)C(=C)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C(O)C1=C(O)C(=C(O)C=C1C)C=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) bonded to '
               "C'), ('[H]C(=O)C1C(=O)Cc2ccccc12', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C,C; C(=O) bonded '
               "to C,C'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC[C@@]4([H])C(=O)C(NC=O)=CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)N(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to N'), ('[O-]C(=O)[*]C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to *; C(=O) "
               "bonded to *; C(=O) bonded to *'), "
               "('O=C(N[C@H]([C@@H](O)C=O)[C@@H](O)[C@H](O)C)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) bonded to '
               "N,C; C(=O) bonded to C'), ('OC(\\\\C=C\\\\C([O-])=O)=C/C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O1C(OC2=C(CCC=O)C=CC=C2O)C(O)C(O)C(O)C1C(O)=O', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('O=C(C1=C(C(O)=CC=C1CC=C(C)C)C=O)C2=C(O)C(OC[C@H](O)C(O)(C)C)=CC(=C2)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('C1CC(C(C(=O)[H])OC1)OC(C)=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) bonded to '
               "C'), ('CC(C)(C=O)[C@@H](O)C([O-])=O', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), "
               "('CSCC[C@H](NC=O)C(=O)O[C@@H]1[C@@H](COP([O-])(-*)=O)O[C@H]([C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C(O)CC(NC1=CC=C(C=O)C=C1)C(O)/C=C/C(O)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('ClC1=C(OC)C=C(O)C(=C1C)C(=O)O[C@H]2[C@@]3(OC)C(=C[C@@H]4CC(C[C@@H]4[C@@]3(C)C2)(C)C)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C1O[C@@H](OC)C2=C1C=C(O)C(=C2O)C=O', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), ('O=C1OC(=C(C=O)C(=C1C)OC)/C=C/C(=O)OC', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), ('O=C(N)[C@@H](NC=O)CCCCN', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to N'), "
               "('O=C1OC(=C)[C@H](C)C=2C1=C(O)C(=C(O)C2C=O)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), ('O=C1OCC2=CC=C(N2[C@H]1CC(C)C)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O([C@@H]1[C@](C2[C@@](C3[C@]([C@]4(C(C5[C@@](CC4)(CCC(C5)(C)C=O)C(O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)=O)=CC3)C)(CC2)C)(C[C@@H]1O)C)(CO)C)[C@@H]7OC[C@@H](O)[C@H](O)[C@H]7O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('N([C@H]1C[C@@H]([C@H](O1)CO*)O*)C=2NC(NC(C2N(C=O)C)=O)N', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to N'), "
               "('O=C([C@H](C1=C(C(O)=C(C)C(=C1C)O)C=O)C)C', 'Contains exactly "
               '3 ketone groups: C(=O) bonded to C,C; C(=O) bonded to C,C; '
               "C(=O) bonded to C'), "
               "('O=C(O[C@@H]1[C@@]2(O)C(C[C@@H]2C(=C[C@@H](C=C(C1)C)OC)C=O)(C)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C(OC)C1=C(O)C(=C(O)C=C1C)C=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) bonded to '
               "C'), "
               "('O=C1O[C@@H](CC=CC=CC(OC2OC(C(N(C)C)CC2)C)[C@@H](C[C@@H]([C@@H]([C@H](C(C1)O)OC)OC3OC(C(OC4OC(C(O)C(C4)(O)C)C)C(C3O)N(C)C)C)C(C=O)=C)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('Cl.N1=C(N=CC(=C1N)CN(C=O)/C(=C/2\\\\SC(OCC2)=O)/C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N; C(=O) "
               "bonded to S; C(=O) bonded to S'), "
               "('[H]C(=O)COCCOc1ccc(Nc2c(Cl)cccc2Cl)c(CC(O)=O)c1', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('OC1(C2CC3(C(C4(C(CC3)C(CCC4)(C)C=O)C)CC2)C1)COC(=O)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('[NH3+]\\\\C(=C\\\\C=C/C=O)C([O-])=O', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), ('O=C1C2=C(C=C(C)C=C2[C@H](C1)OC)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O[C@@H]1[C@]2([C@]([C@]3(C(C1)(C(CC3)C(=O)CO)C=O)[H])(CC[C@]4([C@@]2(CC[C@@H](O)C4)C)[H])[H])[H]', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O(C(=O)CCCCCCC/C=C\\\\CCCCCCCC)CC=1C(=C(O)C(C\\\\C=C(\\\\CCC=C(C)C)/C)=C(OC)C1)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C1C=C(C(C)C)[C@@H]2[C@]1(CC[C@@]3(C2=CC=C(C=O)C[C@@H]3O)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C1O[C@H](O)C=2C1=C(OC)C(=C(O)C2C=O)C', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), ('OC(=O)CCCCCCCCCCCCCCCCCCCCCCCCC=O', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('O=C/1C2=C(C=CC(=C2)O)O\\\\C1=C/C=C/C=C(/C=O)\\\\C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C1O[C@H]([C@@H](O)C=CC=2C(=C(O)C=CC2OC3=CC1=C(C=C3)C)C=O)CCCCC', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O(C1C(C2C(C(C(O)(CC2)C)C=O)(CC1)C)(C)C)C(=O)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('O=C(C1=C(O)C(=C(O)C(=C1)C(OC)C(C)C)C=O)C([C@@H]2O[C@@H](O)[C@]3(O[C@H]3CC)[C@@H](C2)O)C(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C1[C@]2([C@@H](C=O)[C@]3([C@@]1(CC[C@@H](C3)O)C)O)C[C@@]4([C@@H]([C@@H](/C=C/C(C(C)C)C)C)CCC4C2)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C1[C@@H]2C(=CC[C@H]3/C(=C(/C=C/C=C(C)C)\\\\C)/CC[C@@]3(C[C@@H]2[C@@](C1)(O)C)C)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('[H][C@@](O)(CO)[C@@]([H])(O)[C@]([H])(O)[C@]([H])(NC(=O)CO)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to C'), "
               "('O1C(C(O)C(O)C(O)C1OC2=C(OC)C=C(C=C2)C=3OC=4C(C(=O)C3)=C(O)C(OC)=C(O)C4OC)COC(=O)CC(O)(COC=O)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to '), "
               "('COc1c(C)c2O[C@@H](CC(=O)c2c(O)c1C=O)c1ccccc1', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) bonded to '
               "C,C; C(=O) bonded to C'), "
               "('O=C(O)/C=C/C=C/C=C/[C@@H]1[C@@](O)(C(=C[C@H]2[C@H]1CC=C(C2)C=O)C)[C@]3(O[C@@H]3[C@@H](CC)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O1[C@@H](O[C@@H]([C@H](O)[C@H](O)CO)[C@@H](NC(=O)C)C=O)[C@@H](O)[C@H](O)[C@H](O)[C@@H]1C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to C'), "
               "('C[C@]12CC[C@]3([C@]([C@@]1(CC[C@]2(C)O)[H])(CC[C@@]4([C@@]3(CC(C(=O)C4)C=O)C)[H])[H])[H]', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O[C@H](C=O)C(=O)COP(O)(O)=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C,C; C(=O) bonded '
               "to C,C'), "
               "('O1C(C(O)C(O)C1N2C3=NC(=NC(N)=C3N=C2)NCCC4=CC=C(C=C4)CCC(O)=O)C(O)N(CC)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to N'), "
               "('O=C(C=1O[C@H]2[C@H](O)[C@@](O)(C)CC[C@H]2C1C=O)C(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O(C\\\\C=C(\\\\CC\\\\C=C(\\\\CC\\\\C=C(\\\\CC/C=C(\\\\C)/C=O)/C)/C)/C)C(=O)/C(/C)=C/O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C1O[C@H](OC)C=2C1=C(OC)C(=C(OC[C@H]3[C@](O)(CC[C@@H]4[C@@]3(CCCC4(C)C)C)C)C2C=O)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)C)NC([H])=O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)C)*)O)O)O[C@@H]3[C@@H]([C@H](O[C@@H]([C@H]3NC([H])=O)C)O[C@@H]4[C@H](O[C@@H]([C@H]([C@@H]4O)NC([H])=O)C)OC)O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N; C(=O) "
               "bonded to N; C(=O) bonded to N'), "
               "('CC1(C)[C@H](CC[C@@]2(C)[C@H]1CC[C@]1(C)[C@@H]2C[C@H]2O[C@]22[C@@H]3C[C@@](C)(C=O)[C@H](C[C@]3(C)[C@@H](O)C[C@@]12C)OC(=O)c1ccccc1)O[C@@H]1OC[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('[H][C@]12CCNC[C@]1(OC[C@@]2(C(=O)OC)c1[nH]c2ccccc2c1C=O)C=C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('[H][C@@]12[C@@H](C[C@@H](C)[C@]3(CC\\\\C(O3)=C/C=O)[C@@]1(C)CCCC2(C)C)OC(C)=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C(O[C@H]1C2=C(C=O)[C@@H](O)[C@@H]3CC(C[C@@H]3[C@@]2(C)C1)(C)C)C4=C(O)C=C(O)C=C4C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C(CC1=C(C(O)=C(C)C(=C1)O)C=O)C[C@@H](OC)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) bonded to '
               "C,C; C(=O) bonded to C'), "
               "('C1CC([C@]2([C@](C1)([C@@]3([C@@](CC2)([C@]4([C@]([C@@H](C3)OC(=O)C)(CC(=CC4)C(=O)[H])C)[H])C)[H])C)[H])(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C(NNC1=CC(=C(O)C=C1)C=O)C', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to N,C; C(=O) bonded to N,C; C(=O) bonded '
               "to C'), "
               "('[H]C(=O)[C@@]1(O)CCC(=O)[C@@H](OC)[C@]1([H])[C@@]1(C)O[C@@H]1CC=C(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C,C; C(=O) bonded to C,C'), "
               "('[H]C(=O)C(\\\\C)=C(/O)\\\\C=C(/O)C(O)=O', 'Contains exactly "
               '3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), ('OC(CCCC/C(=N\\\\CC(O)=O)/C=O)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('O=C(N1C2N3C(C=4C=CC=C5C4C6(C2(C7=C(NC6N5C=O)C=CC=C7)CC1)CC3)C8OC8(C)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to N'), "
               "('[H]C(=O)\\\\C=C(C)/C=C/[C@@]1(O)C(C)=CC(=O)CC1(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C,C; C(=O) bonded to C,C'), "
               "('O=C1OC2=C(C(=CC(=C2C)O)C)OC3=C1C(=CC(=C3C=O)O)C', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('ClC1=C(O)C(=C2OC=3C(=CC(=C(C3OC(C2=C1C)=O)C)OC)C)C(=O)[H]', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=CC12C(C(C(CC1)C)(CC(O)=O)C)CCC=C2CO', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), "
               "('[H]C(=O)C1=C/C[C@@]2([H])[C@]([H])(CC[C@]2(C)C[C@@]2([H])[C@]\\\\1([H])C(=O)C[C@@]2(C)O)[C@@H](C)CCC=C(C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C,C; C(=O) bonded to C,C'), "
               "('S(O[C@H]([C@H](O)[C@@H](NC(=O)C)C=O)[C@H](O)CO)(O)(=O)=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to N,C; C(=O) "
               "bonded to N,C; C(=O) bonded to C'), "
               "('ClC1=C(OC)C(=C2OC(=O)C3=C(OC2=C1C)C(=C(O)C(=C3C)Cl)C=O)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('N[C@@H](\\\\C=C\\\\ONC=O)C(O)=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to N; C(=O) bonded to C; C(=O) bonded to '
               "C'), "
               "('O=C(O)[C@@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](O)CC4)(C)C)CC3)C)CC2)(C)CC1)C)CC/C=C(/C=O)\\\\C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('O=C1[C@@H]2C(=CC[C@H]3C([C@H](/C=C\\\\C=C(C)C)C)CC[C@@]3(C[C@@H]2[C@@](C1)(O)C)C)C=O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('C=1C2=C(C=CC1)NC(C(C2=O)C)C([H])=O', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C,C; C(=O) bonded to C,C; C(=O) '
               "bonded to C'), ('C1(=CN=C(C(=C1C(=O)[O-])O)C)C=O', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C; C(=O) bonded to C; '
               "C(=O) bonded to C'), "
               "('O=C(O[C@H]1[C@H](O)C([C@@H]2CC[C@H]([C@]3([C@]2(C1)C)OC=4C=C(CO)C(=C(C4C3)O)C=O)C)(C)C)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('OC(CCCCC)/C(=N\\\\CC(O)=O)/C=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) bonded to '
               "C'), "
               "('OC[C@H]1O[C@@H](O[C@H]([C@@H](O)C=O)[C@H](O)[C@H](O)C(O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('[H][C@]12C[C@]3(C)C([C@@H](O)C1=C(C)C(=O)O2)=C(C=O)[C@@]1([H])C[C@@]31[H]', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C'), "
               "('N1(CCN(CC1)C(=O)C(Cl)Cl)C=O', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to N,C; C(=O) bonded to N,C; C(=O) bonded '
               "to N'), ('O=C1OCC=2C1=C(OC)C(=CC2C)C=O', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), ('[H]C(=O)C(=O)O[*]', 'Contains exactly 3 "
               'ketone groups: C(=O) bonded to C; C(=O) bonded to C; C(=O) '
               "bonded to C'), ('O[C@H]([C@H](O)C)[C@H](O)C(=O)C=O', 'Contains "
               'exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) bonded to '
               "C,C; C(=O) bonded to C'), "
               "('O=C1C2=C(O)C(O)=C(O)C(=C2[C@H]3OC4=C([C@@H]1O3)C(=C(C)C(=C4O)O)C=O)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C(NCCCCCN1C(=CC=C1CO)C=O)C', 'Contains exactly 3 ketone "
               'groups: C(=O) bonded to N,C; C(=O) bonded to N,C; C(=O) bonded '
               "to C'), "
               "('O=C(C1=C(C(O)=CC=C1CC=C(C)C)C=O)C2=C(O)C(OC[C@@H]3OC3(C)C)=CC(=C2)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C,C; C(=O) "
               "bonded to C,C; C(=O) bonded to C'), "
               "('O=C\\\\C(=C\\\\CC1C(CCCC1=C)(C)C)\\\\C=C\\\\OC(=O)C', "
               "'Contains exactly 3 ketone groups: C(=O) bonded to C; C(=O) "
               "bonded to C; C(=O) bonded to C')]\n"
               'False negatives: '
               "[('[C@@H]1([C@H](CC[C@]2(O1)C[C@@H]3OC(C=C[C@H](C)[C@@H](O)[C@H](C)C(=O)[C@H](C)[C@@H](O)[C@H](C)C([C@@]([C@@H](O)[C@H](C)CC=CC=C[C@@H](CC[C@@H]([C@H]3C)O2)CC)(O)C)=O)=O)C)C[C@H](O)C', "
               "'Contains 6 ketone groups (more than 3)'), "
               "('[O-][N+](=O)c1cc(ccc1C(=O)C1C(=O)CCCC1=O)C(F)(F)F', "
               "'Contains 6 ketone groups (more than 3)')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 14331,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.5,
    'f1': 0.019417475728155338,
    'accuracy': 0.9930021478556087}