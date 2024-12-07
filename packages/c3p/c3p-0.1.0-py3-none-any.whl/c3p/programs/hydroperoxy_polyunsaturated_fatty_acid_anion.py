"""
Classifies: CHEBI:134019 hydroperoxy polyunsaturated fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_hydroperoxy_polyunsaturated_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a hydroperoxy polyunsaturated fatty acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroperoxy polyunsaturated fatty acid anion, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate anion
    carboxylate_pattern = Chem.MolFromSmarts('[C](=[O])[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"

    # Check for hydroperoxy group (-OOH or -OO-)
    hydroperoxy_pattern = Chem.MolFromSmarts('[C,c]OO')
    if not mol.HasSubstructMatch(hydroperoxy_pattern):
        return False, "No hydroperoxy group found"

    # Count conjugated double bonds in carbon chain
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    matches = mol.GetSubstructMatches(double_bond_pattern)
    if len(matches) < 2:
        return False, "Not polyunsaturated (less than 2 double bonds)"

    # Check if it's a fatty acid by verifying the presence of a long aliphatic chain
    aliphatic_chain = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetIsAromatic() == False:
            chain = Chem.FindAtomEnvironmentOfRadiusN(mol, 6, atom.GetIdx())
            if chain:
                atoms_in_chain = set()
                for bid in chain:
                    bond = mol.GetBondWithIdx(bid)
                    atoms_in_chain.add(bond.GetBeginAtomIdx())
                    atoms_in_chain.add(bond.GetEndAtomIdx())
                if len(atoms_in_chain) >= 8:
                    aliphatic_chain = True
                    break

    if not aliphatic_chain:
        return False, "No long aliphatic chain characteristic of fatty acids"

    # Additional check to filter out non-fatty acid structures
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 1:  # Allow max 1 ring as some fatty acids can be cyclic
        return False, "Structure contains too many rings for a fatty acid"

    return True, f"Contains carboxylate anion, hydroperoxy group, and aliphatic chain with multiple double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134019',
                          'name': 'hydroperoxy polyunsaturated fatty acid '
                                  'anion',
                          'definition': 'Any polyunsaturated fatty acid anion '
                                        'carrying one or more hydroperoxy '
                                        'substituents.',
                          'parents': ['CHEBI:64012', 'CHEBI:76567']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.13793103448275862 is too low.\n'
               'True positives: '
               "[('CCCCC\\\\C=C/C[C@H](OO)\\\\C=C\\\\CCCCCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), ('CCCCC\\\\C=C/CC(OO)\\\\C=C\\\\C=C/CCCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('C(=C\\\\[C@H](C/C=C\\\\C/C=C\\\\CCCCC)OO)/C=C\\\\CCCC(=O)[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C=C/[C@H](C\\\\C=C/CCCC([O-])=O)OO', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('C(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(CCCC(=O)[O-])OO)CC', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('CC\\\\C=C/C\\\\C=C/CC(OO)\\\\C=C\\\\C=C/C\\\\C=C/CCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('[O-]C(CC/C=C\\\\CC/C=C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\C/C=C\\\\CC)OO)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), "
               "('C(=C\\\\[C@@H](/C=C\\\\CCCCC)OO)\\\\CCCCCCCC(=O)[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds')]\n"
               'False positives: '
               "[('CC(C)CCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Contains "
               "carboxylate anion, hydroperoxy group, and 2 double bonds'), "
               "('[C@H]1(O[C@@H]([C@H](O)[C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O[C@@H]3[C@H]([C@H](O[C@@H]4[C@H]([C@H](O[C@@H]5[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]5O)O)CO)O[C@@H]([C@@H]4O)CO[C@H]6[C@@H]([C@H]([C@H](O[C@@H]7O[C@@H]([C@H](O)[C@@H]([C@H]7O)O)CO)[C@H](O6)CO)O[C@@H]8O[C@H]([C@@H](O)[C@H]([C@@H]8O)O)C)NC(C)=O)O)O[C@H](CO)[C@H]3O[C@@H]9O[C@H]([C@@H](O)[C@H]([C@@H]9O)O)C)NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('[NH3+][C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1O[C@@H](CC([O-])=O)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O[C@@]5(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O5)[C@H](O)[C@H](O)CO)C([O-])=O)[C@H]4O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C([O-])=O)C([O-])=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 9 double "
               "bonds'), "
               "('C1[C@H]2[C@@H]([C@H]([C@@H]1OO2)/C=C/[C@H](CCCCC)O)CCCCCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('O(C[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O)NC(=O)C)O)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C)NC(C)=O)O)O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('C[C@]1(CC([O-])=O)[C@H](CCC([O-])=O)\\\\C2=C\\\\c3[nH]c(Cc4[nH]c(c(CC([O-])=O)c4CCC([O-])=O)[C@](C)(O)[C@@]45N\\\\C(=C/C1=[NH+]2)[C@@H](CCC([O-])=O)[C@]4(C)CC(=O)O5)c(CCC([O-])=O)c3CC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 11 double "
               "bonds'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](OC[C@H](NC([*])=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O)C([O-])=O)[C@H](O)[C@H](O)CO', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)O)O)O)NC(C)=O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(C)=O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](COC(=O)C)O)O)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 9 double "
               "bonds'), ('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCCCCC', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)O)O)O)NC(C)=O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(C)=O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O*)OP(OC[C@@H]([C@@H](O*)O)NC(*)=O)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO*)O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)COP([O-])(=O)OCCNC([C@@H](N*)CC(=O)[O-])=O)O)O)O*)O*)O*)O*', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('P(=O)(OC[C@H](OC(CCCCCCCCCCCCCCC)=O)COC(CCCCCCCCCCCCCCC)=O)(OC[C@@H](C([O-])=O)[NH3+])[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('C1[C@H]2[C@@H]([C@H](O[C@@H]1C2)/C=C/[C@H](CCCC(C)O)O)C/C=C\\\\CCCC(=O)[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@H]5[C@@H]([C@@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)[C@H]([C@H](O5)CO)O)O)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 10 double "
               "bonds'), "
               "('C[C@H]1O[C@H](O[C@H]2[C@H](O)[C@H](NC(C)=O)[C@H](O[C@H]3[C@H](O)[C@@H](NC(C)=O)[C@H](O[C@@H]3CO)OP([O-])(=O)OP([O-])(=O)OC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)O[C@@H]2C([O-])=O)[C@H](O)[C@@H](O)[C@H]1NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 17 double "
               "bonds'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(=O)C)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)NC(=O)C)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O)[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])(C([O-])=O)O[C@H]4[C@H]([C@H](O[C@H]([C@@H]4O)O[C@@H]5[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]5O)O)CO)CO)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O[C@H]7[C@@H]([C@@H](O)[C@H]([C@H](O7)CO)O)O)NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 9 double "
               "bonds'), "
               "('C([C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(CO)=O)O)C([O-])=O)O)O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C([O-])=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('Nc1c([nH+]cn1[C@@H]1O[C@H](COP([O-])([O-])=O)[C@@H](O)[C@H]1O)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](OC[C@H](NC([*])=O)[C@H](O)[*])[C@@H]1O)C([O-])=O)[C@H](O)[C@H](O)CO', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O[C@@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)NC(C)=O)O[C@H]7[C@H]([C@@H]([C@@H]([C@@H](O7)C)O)O)O)O[C@H]8[C@H]([C@@H]([C@@H]([C@@H](O8)C)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O[C@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O[C@]%11(O[C@]([C@@H]([C@H](C%11)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]%12[C@@H]([C@H]([C@@H](O[C@@H]%12CO)O[C@@H]%13[C@H]([C@@H](O[C@@H]([C@@H]%13O)CO)O[C@H]%14[C@@H]([C@H]([C@@H](O[C@@H]%14CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('O([C@H]1[C@H]([C@@H]([C@@H]([C@@H](O1)C)O)O)O)[C@@H]2[C@H]([C@@H](O[C@@H]([C@H]2O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)NC(C)=O)O)CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@@H](C)CCOC[C@@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OCC[C@H](C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('[Na+].O(C1C2C(C(C=CC2=CC(C1)C)C)CCC(O)CC(O)CC([O-])=O)C(=O)C(CC)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('[C@H]12[C@H](C[C@H]([C@@H]1/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC([O-])=O)/C=C/C)O2', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O[C@H]4[C@@H]([C@@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)[C@H]([C@H](O4)CO)O)O)NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('C[C@H](NC(=O)[C@@H](C)O[C@H]1[C@H](O)[C@@H](CO)OC(OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@@H]1NC(C)=O)C(=O)N[C@H](CCC([O-])=O)C(=O)NCCCC[C@@H]([NH3+])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 10 double "
               "bonds'), "
               "('O([C@@H]1[C@H]([C@H](O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)O[C@@H]([C@@H]1O)CO)O)[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@H](O[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](COC(C)=O)O)O)[H])C(=O)[O-])CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C)O)NC(=O)C)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[Na+].[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(OC)cccc1OC)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@H]1(O[C@@H]([C@H](O)[C@@H]([C@H]1O)O[C@@H]2O[C@H](CO)[C@H]([C@@H]([C@H]2NC(=O)C)O)O[C@@H]3O[C@@H]([C@H](O)[C@@H]([C@H]3O)O)CO[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O[C@H]5[C@@H]([C@@H](NC(=O)C)[C@H](O[C@@H]6[C@H]([C@H](O[C@H]7[C@@H]([C@H]([C@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(*)=O)O[C@@H]7CO)O)O)O[C@@H]([C@@H]6O)CO)O)O[C@@H]5CO)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('[Na+].COc1c(C)c2COC(=O)c2c(O)c1C\\\\C=C(/C)CCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCC(O)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O[C@@H]5O[C@H]([C@H]([C@H]([C@@H]5O)O)O)C)O)[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('C=1C=C(C=CC1C[C@](O)(C([O-])=O)[C@H](OC(/C=C/C=2C=CC(=C(C2)OC)O)=O)C([O-])=O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('C1(C2=C(C(=CC(=C2)C([O-])=O)O)O)=C(C(=CC(=C1)C(=O)[O-])OC)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('C[C@@H]1O[C@@H](OCCCCCCC(=O)CC([O-])=O)[C@H](O)C[C@H]1O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('OC1C(C(C(=O)C1)C/C=C/CCC(OC(C[N+](C)(C)C)CC([O-])=O)=O)/C=C/C(O)C/C=C\\\\C/C=C/CC', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), ('O([C@H]([N+](C)(C)C)CCC([O-])=O)C(=O)/C=C/CCCCC', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('C(CCC)C[C@@H](/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(NCCCC([O-])=O)=O)OO', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('[C@H]1(N2C=CC(=O)NC2=O)[C@@H]([C@@H]([C@@]([C@H]([C@H]([NH3+])C(=O)[O-])O)(O1)[H])O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), ('CCCCCCCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', 'Contains "
               "carboxylate anion, hydroperoxy group, and 2 double bonds'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCC(=O)OC(CC([O-])=O)C[N+](C)(C)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), ('C([C@@H](CC([O-])=O)OC(=O)*C([O-])=O)[N+](C)(C)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('O[C@@H]1[C@@H](COC(=O)CC([O-])=O)O[C@@H](Oc2cc3c([O-])cc(O)cc3[o+]c2-c2cc(O)c(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O[C@H]7[C@@H]([C@H]([C@@H](O)[C@H](O7)CO)O)NC(C)=O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), "
               "('[C@@H]1([C@H](O[C@@H]([C@@H]([C@@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)O)CO[C@@]3(C[C@@H]([C@H]([C@](O3)([H])[C@@H]([C@@H](CO)O)O)NC(=O)C)O)C([O-])=O)O*)NC(=O)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@@H](O)CCCCCCCCCCCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), "
               "('COC(=O)[C@]1(C[C@@H](O)[C@@H](O)[C@H](O1)[C@H](O)CO)OC[C@@H](O)[C@H]1O[C@@](C[C@@H](O)[C@H]1O)(OCC=C)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@@H]1([C@@H](C[C@H]([C@@H](O1)C)O)O)OCCCCCCCCC\\\\C=C\\\\C(=O)[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('O([C@H]1[C@H]([C@@H]([C@@H]([C@@H](O1)C)O)O)O)[C@@H]2[C@H]([C@@H](O[C@@H]([C@H]2O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@@]([C@@H]([C@H](C7)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])O)NC(C)=O)O)CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O)O)CO)O)NC(=O)C)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(=O)C)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/COP([O-])(=O)OP([O-])(=O)O[C@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@H](O)[C@H]3O)C([O-])=O)[C@H]2O)[C@H](O)[C@H]1O', "
               "'Contains carboxylate anion, hydroperoxy group, and 14 double "
               "bonds'), "
               "('C=1(C(CCC(C1C)=O)(C)C)/C=C/C(=C/C=C/C(=C/C(O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(=O)[O-])O)O)O)=O)/C)/C', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('C[C@H](CCCC(=O)CC([O-])=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('C1(/C(/NC([C@@H](N1)CCCNC(N)=[NH2+])=O)=C/C2=CC=C(C(=C2)OCC[C@H]([NH3+])C(=O)[O-])O)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[H+].[H+].[O-]C(=O)\\\\C=C/C([O-])=O.CN(CCOc1ccc(CC2SC(=O)NC2=O)cc1)c1ccccn1', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)COc1ccccc1)C([O-])=O.[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)COc1ccccc1)C([O-])=O.[H][N+]([H])(CC[N+]([H])([H])C[C@]1(C)CCC[C@]2(C)c3ccc(cc3CC[C@@]12[H])C(C)C)C[C@]1(C)CCC[C@]2(C)c3ccc(cc3CC[C@@]12[H])C(C)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@@H]4O[C@@H]([C@@H]([C@@H]([C@H]4O)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O)NC(=O)C)O)CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(=O)C)O)O)NC(=O)C)[C@@H]%10O[C@H]([C@H]([C@H]([C@@H]%10O)O)O)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('[C@H]1([C@@H]([C@H](CO[C@H]1C/C(=C/C(OCCCCCCCC([O-])=O)=O)/C)C/C=C/[C@H]([C@H](C)O)C)O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O[C@H]4[C@@H]([C@@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)[C@H]([C@H](O4)CO)O)O)NC(C)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(*)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O[C@@H]5O[C@H]([C@H]([C@H]([C@@H]5O)O)O)C)NC(C)=O)O[C@@]6(C[C@@H]([C@H]([C@@](O6)([C@@H]([C@@H](CO)O)O)[H])NC(CO)=O)O)C(=O)[O-])O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[C@H]1(O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]1O)O)O)OC(\\\\C=C\\\\C=2C=CC(=C(C2)OC)O)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('C(=O)(OC[C@H](COP(OC[C@@H](C(=O)[O-])[NH3+])(=O)[O-])OC(=O)CCCCCCCC1C(CCCCCCCC)O1)CCCCCCCCCCCCCCCCC', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('[C@H](CCC([O-])=O)([N+](C)(C)C)OC(CC(CCCCCCC/C=C\\\\CCCCCC)O)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)OC(=O)C)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)NC(C)=O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCCCCCCCCCCCCCCCCCCCCCC', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('C([C@@H](CC([O-])=O)OC(CCCC)=O)[N+](C([2H])([2H])[2H])(C([2H])([2H])[2H])C([2H])([2H])[2H]', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('C(C([O-])=O)C/C=C\\\\C\\\\C=C/C=C/[C@H](C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)OO', "
               "'Contains carboxylate anion, hydroperoxy group, and 7 double "
               "bonds'), "
               "('C1O[C@]([C@H]([C@@H]([C@@H]1O)O)O)(O)/C=N/CC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 2 double "
               "bonds'), "
               "('C12(C(CCCC1(C)O2)(C)C)/C=C/C(=C/C=C/C(=C/C([O-])=O)/C)/C', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), ('O([C@@H](C[N+](C)(C)C)CC([O-])=O)C(=O)CCC(O)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), ('C=1C=C(C=CC1C(=O)OCCO)C(=O)[O-]', 'Contains "
               "carboxylate anion, hydroperoxy group, and 2 double bonds'), "
               "('C1[C@H]2[C@@H]([C@H](O[C@@H]1C2)/C=C/[C@H](CCCCC)O)C/C=C\\\\CCCC(=O)[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('CC(=O)N[C@@H]1[C@@H](O)C[C@@](O[C@H](CO)[C@@H](O)[C@@H]2O[C@@](C[C@H](O)[C@H]2NC(C)=O)(O[C@@H]2[C@@H](O)[C@H](O[C@H]3[C@H](O)[C@@H](O)[C@H](OC[C@H](NC([*])=O)[C@H](O)[*])O[C@@H]3CO)O[C@H](CO)[C@@H]2O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@]4(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O4)[C@H](O)[C@H](O)CO)C([O-])=O)[C@H]3O)[C@H]2NC(C)=O)C([O-])=O)(O[C@H]1[C@H](O)[C@H](O)CO)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 8 double "
               "bonds'), "
               "('N1(C([C@H](C1)NC(/C(/C=2C=CC(OCC[C@@H](C(=O)[O-])[NH3+])=CC2)=N\\\\O)=O)=O)[C@@H](C(O)=O)C3=CC=C(C=C3)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('[C@H]1(CCCC([O-])=O)[C@H](/C=C/C=C/C=C\\\\C/C=C\\\\C=C\\\\C(CC)O)O1', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('C([C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(CO)=O)O)C([O-])=O)O)O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('C[C@H](NC(=O)[C@@H](C)O[C@H]1[C@H](O)[C@@H](CO)OC(OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@@H]1NC(C)=O)C(=O)N[C@H](CCC(=O)N[C@@H](CCC[C@@H]([NH3+])C([O-])=O)C([O-])=O)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 11 double "
               "bonds'), "
               "('[H+].[H+].[O-]C(=O)\\\\C=C/C([O-])=O.CCCCCNC(=N)N\\\\N=C\\\\c1c[nH]c2ccc(OC)cc12', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('C1=CC(=NC(N1[C@@H]2O[C@H](COP(O[C@]3(C[C@H](O)[C@@H](O)[C@@](O3)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])(=O)[O-])[C@H]([C@H]2O)O)=O)N', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@H]1(O[C@@H](O[C@@H]2[C@@H](NC(C)=O)[C@@H](O[C@H](CO)[C@H]2O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O[C@]4(O[C@@]([C@@H]([C@H](C4)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C([O-])=O)[C@H]3O)O*)[C@H]([C@@H]([C@@H]1O)O)O)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), ('C\\\\C=C(/C)C(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('C(C([O-])=O)C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC1C(CC)O1', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('C(CCCCCC/C=C/[C@@H](CC1C(C/C=C\\\\CC)O1)O)(=O)[O-]', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('O1/C(/C[C@]2([C@@]1(C[C@H]([C@@H]2/C=C/[C@H](CCCC(C)O)O)O)[H])[H])=C\\\\CCCC([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 3 double "
               "bonds'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)NC(C)=O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 5 double "
               "bonds'), "
               "('C([C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(C)=O)O)C([O-])=O)O)O)O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('[Na+].[H][C@]12SCC(COC(C)=O)=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\\\c1csc(N)n1)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds'), "
               "('OC[C@H]1C(OC[C@@H](C([O-])=O)NC(=O)C2=C3C(=CC(=C2)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O[Fe-]5(OC6=C(C=C(C=C6O5)[C@H]7[C@@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O)C(=O)N1)O3)=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 4 double "
               "bonds'), "
               "('CCCC[C@@H](C)[C@@H](OC(=O)C[C@@H](CC([O-])=O)C([O-])=O)[C@H](C[C@@H](C)C[C@H](O)CCCC[C@@H](O)C[C@H](O)[C@H](C)[NH3+])OC(=O)C[C@@H](CC([O-])=O)C([O-])=O', "
               "'Contains carboxylate anion, hydroperoxy group, and 6 double "
               "bonds')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 21,
    'num_true_negatives': 183829,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.27586206896551724,
    'recall': 1.0,
    'f1': 0.4324324324324324,
    'accuracy': 0.9998857814182684}