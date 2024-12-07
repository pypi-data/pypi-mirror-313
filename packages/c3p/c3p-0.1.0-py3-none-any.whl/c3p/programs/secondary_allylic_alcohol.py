"""
Classifies: CHEBI:134396 secondary allylic alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_secondary_allylic_alcohol(smiles: str):
    """
    Determines if a molecule is a secondary allylic alcohol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a secondary allylic alcohol, False otherwise
        str: Reason for classification
    """
    # Create RDKit mol object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Add explicit hydrogens
    mol = Chem.AddHs(mol)
    
    # SMARTS pattern for secondary allylic alcohol:
    # [C]=[C]-[C@H]([*])([OH1])
    # This pattern looks for:
    # - A carbon-carbon double bond
    # - Connected to a carbon
    # - That carbon has exactly one hydrogen
    # - That carbon has a hydroxyl group
    # - That carbon has one other non-H substituent
    pattern = Chem.MolFromSmarts('[C]=[C][C@H]([*])[OH1]')
    
    if mol.HasSubstructMatch(pattern):
        matches = mol.GetSubstructMatches(pattern)
        
        for match in matches:
            central_c = mol.GetAtomWithIdx(match[2])  # The carbon attached to OH
            
            # Count the number of heavy atoms (non-H) attached
            heavy_neighbors = [n for n in central_c.GetNeighbors() if n.GetSymbol() != 'H']
            
            # For a secondary carbon, should have exactly 2 heavy atom neighbors (not counting OH)
            if len(heavy_neighbors) == 3:  # 3 because we're counting the OH group
                # Verify one neighbor is part of C=C double bond
                double_bond_found = False
                for neighbor in heavy_neighbors:
                    if neighbor.GetSymbol() == 'C':
                        for bond in neighbor.GetBonds():
                            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                                other_atom = bond.GetOtherAtom(neighbor)
                                if other_atom.GetSymbol() == 'C':
                                    double_bond_found = True
                                    break
                
                if double_bond_found:
                    return True, "Secondary allylic alcohol found"
    
    return False, "No secondary allylic alcohol pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134396',
                          'name': 'secondary allylic alcohol',
                          'definition': 'An allylic alcohol in which the '
                                        'carbon atom that links the double '
                                        'bond to the hydroxy group is also '
                                        'attached to one other carbon and one '
                                        'hydrogen.',
                          'parents': ['CHEBI:134361', 'CHEBI:35681']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.1746031746031746 is too low.\n'
               'True positives: '
               "[('C=1(C(CC[C@@H](C1C)O)(C)C)/C=C/C(=C/C=C/C(=C/C(O)=O)/C)/C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(\\\\CCO)=C\\\\C/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/C(CCCC(=O)O)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C=1(C(C[C@H](O)C1C)=O)C/C=C\\\\CC', 'Secondary carbon with "
               "OH group adjacent to C=C double bond'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\[C@@H](C/C=C\\\\C/C=C\\\\CCO)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CC(/C=C/C=C\\\\C/C=C\\\\CC)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(CCC[C@@H](/C=C/C=C\\\\C/C=C\\\\C=C\\\\[C@H](CCCCC)OO)O)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CCC(C)C1OC(=O)\\\\C=C\\\\C=C\\\\C=C\\\\C=C\\\\C=C\\\\CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)\\\\C=C\\\\C1C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\[C@H](CCCC)O)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\C/C=C\\\\CCO)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C1[C@H]2[C@@H]([C@H](O[C@@H]1C2)/C=C/[C@H](CCC(CC)O)O)C/C=C\\\\CCCC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(CC/C=C\\\\C[C@@H]([C@@H](/C=C/C=C/C=C\\\\C=C\\\\[C@@H](C/C=C\\\\CC)O)O)O)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double "
               "bond')]\n"
               'False positives: '
               "[('O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/[C@H](O)C(O[C@@H]2O[C@@H]([C@@H](O)[C@@H]([C@H]2O)O)CO)(C)C)\\\\C)\\\\C)\\\\C)/C)/C)C(C)(C)CC1)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1OC(C(C=CC=C(C(O)CC(O)CC(O)CC(OC(=O)CC(=O)O)CC2OC(CC(C(CCC(C(C(CC(C(C=CC=C1C)C)O)O)C)O)C)O)(O)C(O)C(C2)O)C)C)C(CCC/C=C/CCCN=C(N)N)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CC\\\\C=C/C[C@H](O)\\\\C=C\\\\[C@@H]1[C@@H](C\\\\C=C/CCCC(O)=O)[C@@H](O)CC1=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('[H][C@@]12C[C@H](OC(C)=O)[C@@]3([H])[C@]45CCCC(C)(C)[C@@]4([H])[C@H](O)[C@](O)(O[C@@H]5OC)[C@@]3([C@H](O)C1=C)[C@@H]2O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCC(O)C(C)=C)C)[H])[H])C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@@]2([C@@H](O)C[C@@H]3C([C@@H]2[C@H]1[C@H](O)/C(=C/CCC)/C)=CO[C@@]4([C@]56OC5(CC=C[C@@H]6O)C)[C@@H]3O4)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1[C@@H]([C@@H](C/C=C\\\\CCCC(O[C@H](COC(=O)CCCCCCC)CO)=O)C=C1)/C=C/[C@@H](O)CCCCC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('ClC1=C(OC)C=C2CC(=CC=C[C@@H](OC)C(=O)C[C@@H]([C@H](C=C([C@H](CC(NC1=C2)=O)O)C)C)O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C1[C@H]2[C@@H]([C@H]([C@@H]1OO2)/C=C/[C@H](CCCCC)O)CCCCCCC([O-])=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@H]2[C@@H](C)C([C@@]1([C@H](NC(=O)C(O)C)C=C(C=C[C@@H](O)CC=C(C=C[C@H](C2)OC(=O)C)C)C)C)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)[C@@H](CCC(=O)OCCCC)C)C)[C@@H](O)C[C@@H]4[C@@]2(CCC(C4(C)C)=O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CCCCC[C@H](O)\\\\C=C\\\\[C@H]1[C@H](O)CC(=O)[C@@H]1C\\\\C=C/CC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@H]1[C@@H]([C@@H](CCCCCCC(O)=O)C(=O)C1)/C=C/[C@H](O)CCCCC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O1C=2C(CC(O)C(C)=C)=C(OC)C=CC2C=CC1=O', 'Secondary carbon "
               "with OH group adjacent to C=C double bond'), "
               "('O[C@H]1[C@@H]([C@@H](CCCCC(OC)CC(O)=O)C(=O)C1)/C=C/[C@@H](O)C[C@H](CCCC)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@H](CCCCCCCC(OC)=O)/C=C/C=C/CCCCC', 'Secondary carbon "
               "with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@@H](CC=CC(=O)CC=C[C@@H](C1)O)C', 'Secondary carbon "
               "with OH group adjacent to C=C double bond'), "
               "('CC(C)=CC(O)CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@@H](CC[C@@H](O)C=CC(=O)O[C@H](C[C@@H](CC[C@H](C=C1)O)O)C)C[C@@H](O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('OC(CC(C1CCC(=CC1)C)=C)C=C(C)C', 'Secondary carbon with OH "
               "group adjacent to C=C double bond'), "
               "('O1C(C1CCCC(O)=O)C[C@H]2[C@@H]([C@@H](O)CC2=O)/C=C/[C@@H](O)CCCCC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O1[C@@]([C@@H](O)CC[C@H]([C@@]2([C@@]3([C@@](CC2)(/C(/CCC3)=C/C=C\\\\4/C[C@@H](O)C[C@H](O)C4=C)[H])C)[H])C)(C1)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4([C@@H](O)C=C([C@]4(C1)C)[C@@H](CC(=O)CC(C(=O)O)C)C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CC(=C)[C@@H](O)CC[C@](C)(O)[C@H]1CC[C@]2(C)[C@@H]1CC[C@@H]1[C@@]3(C)CCC(=O)C(C)(C)[C@@H]3CC[C@@]21C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@H]1CC[C@@]2([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H](CCCC(C)C)C)[H])(CC3)C)[H])(C=CC2=C1)[H])[H])C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1OC(C=CC(O)CC(O)CCCC(O)C(C(O)CCC(C(O)CC(O)CC(O)CCCC(C(C=C(C(CC(CCCC(C(C(CC=CC=C(C(C(C2OC(C1)(O)C(C(O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)N(C)C)C)C2)C)C)O)C)O)C)O)O)O)C)CCCCC(C)C)O)C)C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O1C(C2C(C=3C1=CC(=CC3O)CCCCC)C=C(C(O)C2)C)(C)C', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/C(O)CCCCCCCC([O-])=O', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H]1C=2[C@]3([C@@]([C@](CC3=O)([C@@H](CC(=O)C[C@@H](C)C(O)=O)C)[H])(CC(=O)C2[C@@]4([C@](C([C@@H](O)CC4)(C)C)(C1)[H])C)C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C=C/C(O)CCC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C1[C@H]2[C@@H]([C@H](O[C@@H]1C2)/C=C/[C@H](CCCC(C)O)O)C/C=C\\\\CCCC(=O)[O-]', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC(C)C)COC(=O)CCC/C=C\\\\C[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@]([C@@]2(CC=C(C)[C@H](C2)O)C)(C)CC1', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('CC(C)C1=C(C(=C(C(=N1)C(C)C)C=C[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)COC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('[C@@H]1(C[C@@H](C/C(/C1=C)=C/C=C\\\\2/[C@]3([C@](CCC2)([C@](CC3)([C@@H](/C=C/[C@@H](O)C4CC4)C)[H])C)[H])O)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('OCCCCC\\\\C=C/C[C@@H](O)C(O)\\\\C=C\\\\C(O)C\\\\C=C/CCCC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C[C@@H]1[C@H](C(=O)C=C1)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('ClC1=C(O)C=C(O)C2=C1CC(=O)C[C@@H](O)C=CCCC=CC[C@H](OC2=O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CCCCC[C@@H](C=C[C@H]1[C@@H]([C@H](CC1=O)O)CC=CCCCC(=O)O)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@](\\\\C=C\\\\[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C)(C(O)(C)C)CO', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H](C[C@H](O)C(C(C)C)=C)C)[H])(CC3)C)[H])(CC2)[H])[H])(CC1)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1OC2C3(C4(C5C(C(O)(C)CC4)CC3(O)C(C2)O5)COC(=O)C6C7(C(C(=CCC=C1)OCC7)O)O6)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](NC(=O)C/C=C\\\\C[C@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(OCC[N+](C)(C)C)([O-])=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](NC(=O)CCC(O)\\\\C=C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)[C@H](O)CCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC(CC)C)(OC[C@@H](O)CO)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@H]1[C@@H]([C@@H]([C@@H](O)C1)/C=C/[C@@H](O)CC)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H](COc1cccc(c1)C(F)(F)F)\\\\C=C\\\\[C@H]1[C@H](O)C[C@H](O)[C@@H]1C\\\\C=C/CCCC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1N[C@@H]([C@H](O)C)C([C@@]12C(=O)[C@]3([C@H]4[C@@H](C[C@H](C)CC4)C=C[C@H]3[C@@H]2/C=C/[C@H](O)C)C)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C(O[C@@H](CCC(=O)/C=C/C(=O)O)C)/C=C/[C@@H](O)CC[C@H](OC(=O)C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(O)C=C(C(=O)O)C)C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('OC(/C=C\\\\CCCCCCC)C#CC#CC(=O)C=C', 'Secondary carbon with "
               "OH group adjacent to C=C double bond'), "
               "('OC1C23C(C4(C(C2C(O)=O)C(CCC4)(C)C(O)=O)C)CCC(O)(C3)C1=C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1OC(C2=CC=CC=C2)C(C1NC(=O)C(NC(=O)C(C(OC)CC(O)/C(=C/CC3OC(/C=C/C=C/CC(OC)CC(=O)/C=C/C(=C/C=C/C4C(O)C(O)(C(C)OC4)C)/C)C(C)C(C3CC)O)/C)C)C(C)C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1OC(C=CC(O)CC(O)CCCC(O)C(C(O)CCC(C(O)CC(O)CC(O)CCCC(C(C=C(C(CC(CCCC(C(C(CC=CC=C(C(C(C2OC(C1)(O)C(C(O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)N(C)C)C)C2)C)C)O)C)O)C)O)O)O)C)CCCC(CC)C)O)C)C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(C(CC/C=C/C=C\\\\[C@H](CCCC([O-])=O)O)=O)/C=C\\\\CCCCC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O1[C@H](/C=C/C=C/[C@H](O)C)[C@H]2C[C@@H](O)[C@@H]([C@@H]([C@@H]2C1)O)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@H](CCCC=CC=C[C@H](O)C[C@@H](O)CC=CC=C[C@H](CC=CC=C1)OC(=O)/C=C/C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCC(O)/C=C/C=C/C/C=C/CC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)([O-])=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('[H][C@@]1(CC[C@]2(C)[C@]1([H])[C@H](O)C[C@]1([H])[C@@]3(C)CC[C@H](O)C(C)(C)[C@]3([H])[C@@H](O)C[C@@]21C)[C@@](C)(O)C(O)C[C@H](O)C(C)=C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C(=C(C=CC(O)(C)C)[C@@H](O)CC1)CC=C(C)C', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC(C)C)COC(=O)CCCC(O)\\\\C=C\\\\C=C\\\\C\\\\C=C\\\\CCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@H]2C(C)(C)C([C@@]1([C@@]2(/C=C/C=C/C=C(\\\\C=C(\\\\[C@@H](O)/C(=C/C)/C)/C)/C)C)C)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('C(=C/[C@@H](C#N)O)\\\\C', 'Secondary carbon with OH group "
               "adjacent to C=C double bond'), "
               "('FC(F)(F)C(O)(C#CC[C@@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])CCCC(O)(C)C)C(F)(F)F', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H]1[C@H]([C@H]([C@H](O)C1)/C=C/[C@H](O)CCCCC)C/C=C\\\\CC(O[C@H](COC(=O)CCCCCCCCCCCCCCCCCCCC)CO)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O([C@@H]1CC=2[C@@]([C@@H]3[C@H]([C@H]4[C@@]([C@H](CC4)[C@@H](CCCC(C)C)C)(CC3)C)CC2)(CC1)C)C(=O)CCCCC(=O)C[C@@H]5[C@H]([C@H](O)C[C@@H]5O)/C=C/[C@@H](O)CCCCC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('CC1OC(OC2C\\\\C=C(CCC=C)/CC\\\\C=C\\\\C(O)C(C)C(O)C(C)\\\\C=C\\\\C=C\\\\C=C\\\\C=C\\\\C=C\\\\CCC(=O)OC(CC(O)CC(O)CC(O)C\\\\C=C\\\\C(O)CC(O)CC(O)CC(=O)C2C)\\\\C=C\\\\CC(O)\\\\C=C\\\\CC(O)CCCN)C(O)C(O)C1O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@@H](C[C@H](O)C[C@@H](O)CCCCCCCCCCCC[C@@H](C[C@@H](C=C1)O)O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1O[C@H]([C@H](C=C[C@H](O)C[C@H](O)C[C@@H](O)C[C@H](O)C[C@@H](O)C[C@H](C[C@H]([C@H]([C@H]2O[C@H](C=CC=CC=CC=C1)[C@H](O)C2)C)O)O)C)C(CC)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('S1S[C@@]23N4[C@@H]5[C@@H](OC(=O)C=6C=CC(=C(OC=7C=C(C[C@]1(N(C)C2=O)C4=O)C=CC7OC)C6)OC)C=COC=C5[C@H]3O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P1(O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@H]([C@@H](O)CC(O[C@@H]([C@@H](O)[C@H]2OP(O)(O)=O)C=C[C@@H](O)CCCCC)O)CC=CCCCC(O[C@@H](CO1)COC(=O)CCCCCCC/C=C\\\\CCCCCC)=O)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C([C@@]3(O)CCCC(C3=C1)(C)C)CC[C@@]([C@H]2O)(C=C)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@H](CCCC(O)=O)/C=C\\\\C=C\\\\C=C\\\\[C@@H](O)C/C=C\\\\CCC(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H]1C\\\\C(=C\\\\C=C/2\\\\[C@]3([C@@]([C@](CC3)([C@H](C)/C=C/C=C/C=C/CO)[H])(CCC2)C)[H])\\\\C([C@@H](O)C1)=C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCC(O)/C=C/C=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1/C(=C/[C@@H](O)C)/C[C@H](O)[C@@]23[C@@]1(OC(C)(C)[C@@H]2C3)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@H]1C/C(=C\\\\C=C/2\\\\[C@H]3[C@@]([C@H](CC3)[C@H](CC)C)(CCC2)C)/C[C@@H](O)C1=C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C(O[C@@H](C2)/C=C/CCCCCC)[C@H](O)CC1', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('[C@]1([C@H](C(=C(C(C1)=O)O)[O-])O)(CO)O', 'Secondary carbon "
               "with OH group adjacent to C=C double bond'), "
               "('OC1C(C(C(=O)C1)C/C=C/CCC(OC(C[N+](C)(C)C)CC([O-])=O)=O)/C=C/C(O)C/C=C\\\\C/C=C/CC', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P1(O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@H]([C@@H](O)CC(O[C@@H]([C@@H](O)[C@H]2OP(O)(O)=O)/C=C/[C@@H](O)CCCCC)O)CC=CCCCC(OC[C@@H](OC(=O)CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCC)CO1)=O)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@@]12[C@@](C=3C([C@H]4[C@]([C@@H]([C@@H](/C=C/[C@@H](C(C)C)C)C)CC4)(C)CC3)=C[C@H]1O)(CC[C@@H](C2)O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O1C(C(NC2=CC=C(C=C2)C=O)CC1=O)C=CC(O)C', 'Secondary carbon "
               "with OH group adjacent to C=C double bond'), "
               "('C[C@H]1[C@H]2[C@H](Cc3c[nH]c4ccccc34)NC(=O)[C@@]22[C@H](C=C1C)\\\\C=C\\\\C[C@H](C)\\\\C=C(C)\\\\[C@@H](O)C(=O)\\\\C=C\\\\C2=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('COc1cc2c(CN3CC[C@@]22C=C[C@@H](O)C[C@H]32)cc1O', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('O=C1[C@@]23C(=O)N[C@H]([C@@H]2C(C)=C([C@H]([C@@H]3C=CC[C@H](C)C=C([C@H](C(CC1)=O)O)C)OC)C)CC=4C5=C(C=CC=C5)NC4', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O1[C@@H](OC[C@]2([C@@H](O)[C@H](O)C[C@]3([C@H]2C[C@@H](O)C4=C3CC[C@@](C4)(C=C)C)C)C)[C@@H](O)[C@H](O)[C@@H]([C@H]1CO)O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C([C@H](O)/C(/C=O)=C\\\\C=C\\\\C)C', 'Secondary carbon "
               "with OH group adjacent to C=C double bond'), "
               "('O=C1C(=C(C)C)C[C@@]2([C@H](CCC(C2=C1)O)C)C', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C(C(O)=C(C)C=C2C(=O)C=3C1=C(O)C=C(O)C3)C4=C5C(=O)C6=C([C@@H](OC)[C@@H](O)[C@]([C@H]6O)(O)C)C(C5=C(O)C=C4OC)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](NC(=O)CCC/C=C\\\\C[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)[C@H](O)/C=C/CCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('OC(C(O)CC(O)/C(=C/CC/C(=C\\\\CO)/C)/C)(C)C', 'Secondary "
               "carbon with OH group adjacent to C=C double bond'), "
               "('CCCCCC(O)C=CC(O)=O', 'Secondary carbon with OH group "
               "adjacent to C=C double bond'), "
               "('O=C1O[C@@H](CC=C[C@H](CCC1)O)C', 'Secondary carbon with OH "
               "group adjacent to C=C double bond'), "
               "('O=C1NC=C(C2=CC=CC=C2)C3=C1[C@](/C=C(/C(O)C)\\\\C)([C@H](O)O3)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('P(OC[C@H](OC(=O)CCC[C@@H](O)[C@H](O)/C=C\\\\C=C/C=C/C=C/[C@@H](O)C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCCCCCC(C)C)(OC[C@@H](O)CO)(O)=O', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O[C@H](\\\\C=C\\\\CCCCCCCCC\\\\C=C/CCCCCCCCC\\\\C=C\\\\[C@@H](O)C#C)C#C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1C2=C([C@@]3(CC[C@@H]([C@]3(C1)C)[C@@H](CC/C=C(/C(=O)O)\\\\C)C)C)[C@@H](O)C[C@@H]4[C@@]2(CCC([C@]4(CO)C)=O)C', "
               "'Secondary carbon with OH group adjacent to C=C double bond'), "
               "('O=C1[C@@]2(O[C@@H]2[C@H](C(=O)OC)O[C@H]1O)[C@H](O)/C=C(/[C@@H]3OC(C)(C)[C@@H]4[C@H]3C=C(CC4)C)\\\\C', "
               "'Secondary carbon with OH group adjacent to C=C double "
               "bond')]\n"
               'False negatives: '
               "[('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C(C1C(CCCCC)O1)O)O', 'No "
               "secondary allylic alcohol pattern found'), "
               "('CCCCCC(O)C(O)C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(O)=O', 'No "
               "secondary allylic alcohol pattern found'), "
               "('C1=CC=C(C(=C1/C=C/C=C/[C@H]([C@H](C)O)O)C([H])=O)O', 'No "
               "secondary allylic alcohol pattern found'), "
               "('CC1C(O)C=C2C1(C)C=CCC2(C)C', 'No secondary allylic alcohol "
               "pattern found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 1962,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 0.9333333333333333,
    'f1': 0.21705426356589147,
    'accuracy': 0.9513721714010592}