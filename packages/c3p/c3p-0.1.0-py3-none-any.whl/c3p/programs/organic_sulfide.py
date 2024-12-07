"""
Classifies: CHEBI:16385 organic sulfide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organic_sulfide(smiles: str):
    """
    Determines if a molecule is an organic sulfide (thioether) with structure R-S-R where R ≠ H.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an organic sulfide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Find sulfur atoms
    sulfur_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']
    if not sulfur_atoms:
        return False, "No sulfur atoms found"
        
    # Check each sulfur atom
    for sulfur in sulfur_atoms:
        # Get neighbors
        neighbors = sulfur.GetNeighbors()
        
        # Check oxidation state - exclude sulfoxides, sulfones etc
        if sulfur.GetTotalNumHs() + sulfur.GetExplicitValence() > 2:
            continue
            
        # Check number of neighbors
        if len(neighbors) != 2:
            continue
            
        # Check that both neighbors are carbon or other non-hydrogen atoms
        if all(n.GetSymbol() != 'H' for n in neighbors):
            # Check bond types - should be single bonds
            bonds = [mol.GetBondBetweenAtoms(sulfur.GetIdx(), n.GetIdx()) for n in neighbors]
            if all(bond.GetBondType() == Chem.BondType.SINGLE for bond in bonds):
                # Check that neighbors are not part of C=S or similar groups
                valid = True
                for n in neighbors:
                    for bond in n.GetBonds():
                        if bond.GetBondType() != Chem.BondType.SINGLE and \
                           bond.GetOtherAtomIdx(n.GetIdx()) == sulfur.GetIdx():
                            valid = False
                            break
                if valid:
                    neighbor_symbols = [n.GetSymbol() for n in neighbors]
                    return True, f"Contains R-S-R structure where R is {' and '.join(neighbor_symbols)}"
                
    return False, "No sulfur atom with appropriate R-S-R structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16385',
                          'name': 'organic sulfide',
                          'definition': 'Compounds having the structure RSR (R '
                                        '=/= H). Such compounds were once '
                                        'called thioethers.',
                          'parents': ['CHEBI:26822', 'CHEBI:33261']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.5702479338842975 is too low.\n'
               'True positives: '
               "[('Cc1c(O)cccc1C(=O)N[C@@H](CSc1ccccc1)[C@H](O)CN1C[C@H]2CCCC[C@H]2C[C@H]1C(=O)NC(C)(C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C[C@H](CSC(=O)c1ccccc1)C(=O)N1C[C@H](C[C@H]1C(O)=O)Sc1ccccc1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=C(C(=CC=C1)C)NC(=O)CSC2=[NH+]C=NC3=C2NC=N3', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('OC([C@H](CSCCNC(C)=O)N)=O', 'Contains R-S-R structure where "
               "R is carbon'), "
               "('CC(C)(C)C(=O)CSC1=NC2=C(CCC2)C(=C1C#N)C3=CC=CS3', 'Contains "
               "R-S-R structure where R is carbon'), ('CSc1c(C)cc(O)cc1C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('NCCCCCCSc1nc2c(nc(N)[nH]c2=O)n1[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('Nc1ncnc2n([C@@H]3O[C@@H]4COP(O)(=O)O[C@H]4[C@H]3O)c(Sc3ccc(Cl)cc3)nc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C1=CC=CC=C1)CCC2C(=O)N(C3=CC=CC=C3)N(C2=O)C4=CC=CC=C4', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CN1C2=CC=CC=C2C(=C1SC3=CC=C(C=C3)Cl)C=O', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('S([C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)CO)C(=NO)CCCCCSC', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CNC(=O)C1=CC=CC=C1SC2=CC3=C(C=C2)C(=NN3)C=CC4=CC=CC=N4', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCOC(=O)CC(=O)CSC1=NC2=C(CCC2)C=C1C#N', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('OC([C@H](CCC(N[C@H](C(NCC(O)=O)=O)CSC)=O)N)=O', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('S(C=1C=C2OC(=O)C(=C2C=CC1)C3=CC=CC=C3)C4=CC=C(O)C=C4', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCNc1nc(NC(C)(C)C)nc(SC)n1', 'Contains R-S-R structure where "
               "R is carbon'), ('CSCCC(=O)C(\\\\O)=C\\\\O', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('ClC=1C(S(=O)(=O)C(C)C)=C(SC1)SC', 'Contains R-S-R structure "
               "where R is carbon'), ('ClC1NC(NCC1C(=O)OCC)SC', 'Contains "
               "R-S-R structure where R is carbon'), ('CSCCO', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CN1C(=NN=N1)SC2=NC=NC3=C2C(=CS3)C4=CC(=CC=C4)C(F)(F)F', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1CCC2=C(C1)SC3=C2C(=NC(=N3)CN4CCOCC4)SC5=CC=CC=C5', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C=1N=CC=CC1C(O)=O)C2=CC=CC=C2', 'Contains R-S-R structure "
               "where R is carbon'), ('S(C1=CC=C(O)C=C1)C=2C3=C(C=CC=C3)NC2', "
               "'Contains R-S-R structure where R is carbon'), "
               "('ClC1=CC=CC(Cl)=C1CSC1=NN=C(S1)C1=NC=CN=C1', 'Contains R-S-R "
               "structure where R is carbon'), ('S(CCCC)C', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CCOP(=S)(OCC)SCSc1ccc(Cl)cc1', 'Contains R-S-R structure "
               "where R is carbon'), "
               "('C1=CNC(=C1)C(=O)CSC2=NN=C(O2)C3=CC=CO3', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C)(C)C1=NN2C(=NN=C2SC1)C3CCCCC3', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('C1=CC=NC(=C1)C=NNC2=NC(=O)C(S2)CC3=CC(=CC=C3)SC(F)F', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CSc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCC(=O)N(C)C=C1C(=O)C2=CC=CC=C2S1', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('[H]C(Cl)=C(Cl)SC[C@H](N)C(O)=O', 'Contains R-S-R structure "
               "where R is carbon'), "
               "('S(C=1N=C(NN1)C(F)(F)F)C2=NC=C([N+]([O-])=O)C=C2', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('O=C(O)[C@@H](N(O)O)CCCCSC', 'Contains R-S-R structure where "
               "R is carbon'), ('CC(C)=CCSC[C@H](N)C(O)=O', 'Contains R-S-R "
               "structure where R is carbon'), ('CSC', 'Contains R-S-R "
               "structure where R is carbon'), ('O=C(O)[C@@H](N)CCCCCSC', "
               "'Contains R-S-R structure where R is carbon'), "
               "('N[C@@H](CSc1ccc(Br)cc1)C(O)=O', 'Contains R-S-R structure "
               "where R is carbon'), "
               "('C1=CC=C(C=C1)CSC2=CC=C(O2)C=C3C(=N)N4C(=NC3=O)SC=N4', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C1=CC=CC=C1)CC(OC)=O', 'Contains R-S-R structure where R "
               "is carbon'), ('CSc1ccc(O)cc1', 'Contains R-S-R structure where "
               "R is carbon'), ('CC(C)Sc1ncnc2nc[nH]c12', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('S(C[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)C(=NO)CCCCCSC', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC(C)(Sc1ccc(CCN(CCCCC2CCCCC2)C(=O)NC2CCCCC2)cc1)C(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CN1C(=NN=N1)SC2=NC=NC3=C2C(=CS3)Br', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('COC(=O)CCSCCO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCN(CC)C(=O)CSC1=NC=NC2=C1SN=C2C3=CC=CS3', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('COC(=O)CCSCCO[C@@H]1O[C@H](CO)[C@H](O[C@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC(=O)N[C@@H](CSC1=CC=CC=C1)C(O)=O', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('C=1(C=CC=CC1N)S/C(=C(/C(/C#N)=C(/SC=2C(=CC=CC2)N)\\\\N)\\\\C#N)/N', "
               "'Contains R-S-R structure where R is carbon'), "
               "('O1[C@@H]([C@H]([C@@H]([C@H]([C@@H]1SC(CCCS(=O)C)=NO)O)O)O)CO', "
               "'Contains R-S-R structure where R is carbon'), "
               "('OC(=O)C1CSC(=N1)c1ccccc1O', 'Contains R-S-R structure where "
               "R is carbon'), ('C(CCO)SCCO', 'Contains R-S-R structure where "
               "R is carbon'), ('CCOC(=O)CSC1=NC(=C(C=C1C#N)C(=O)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSCC(O)=O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=C(NC(=C1C(=O)OC)C)C(=O)CSC2=CC=C(C=C2)Cl', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('C=1C=NC=CC1CCSC=2C=CC(=CC2)OC', 'Contains R-S-R structure "
               "where R is carbon'), ('C(\\\\CCCCCCCSC)=N/O', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CNCC1=CC=CC=C1SC2=C(C=C(C=C2)[N+]#[C-])N', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CSC[C@H](N)C(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC=C(C=C1)C2=NN=C(O2)SCC3=CC=CC=C3F', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('N[C@@H](CCC(=O)N[C@@H](CS[C@H]1[C@@H]([C@H](C(C1)=O)/C=C/[C@H](CCCCC)O)C/C=C\\\\CCCC(=O)O)C(=O)NCC(=O)O)C(=O)O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('NC(CSCC(N)C(O)=O)C(O)=O', 'Contains R-S-R structure where R "
               "is carbon'), ('CC(C)(C)C(=O)NC(C(Cl)(Cl)Cl)SC1=NC=CC=N1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCN1C(=NN=C1SCC2=C(C=CC=C2Cl)F)C3=CC=CO3', 'Contains R-S-R "
               "structure where R is carbon'), ('CSc1nc(N)nc(N)n1', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('CN(C)CCCSC1=NC(=NC2=C1CCC2)C3=CC=CC=C3', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('NCCCSC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon')]\n"
               'False positives: '
               "[('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC=C(C=C1)OCC(=O)NNC(=O)CSC2=NC=C(C(=N2)N)C#N', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C(CCN(C)C)N1C2=C(SC=3C1=NC=CC3)C=CC=C2', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C[C@H](CCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C[C@H](CCCCCCCCC/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C(NC(CCNC(=O)[C@@H](C(COP(OC[C@@H](C(*)=O)N*)(=O)[O-])(C)C)O)=O)CSC(=O)C[C@@H](C/C=C\\\\CCCCCCCCCCCCCC/C=C\\\\CCCCCCCCCCCCCCCCCC)O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C\\\\C(=C\\\\C1=CSC(C)=N1)\\\\C2CC(C(C)(CCCC(C)(C(C(C)C(C(C)(C)C(CC(=N2)O)O)=O)O)O)SCC(/C(=N/CC(=O)O)/O)/N=C(\\\\CCC(C(=O)O)N)/O)O', "
               "'Contains R-S-R structure where R is carbon'), ('C(CCCCSC)#N', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)CO)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C(NC(CCNC(=O)[C@@H](C(COP(O)(=O)O)(C)C)O)=O)CSC(=O)CCCCC', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@@H]1NC(=O)[C@H]([C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)C(N(C(CC[C@@H](NC([C@H]([C@@H](NC1=O)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)C)=O)C(=O)O)=O)C)=C)C)CC(C)C)C(=O)O)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)N[C@@H](CC=2C=3C(NC2)=CC=CC3)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C1=C2C(=C3C(=O)C=4C=CC(=C(C4C(C3=C1)=O)O)[C@@H]5O[C@H]([C@@H](N(C)C)CC5)C)C(=O)C[C@@](C2)(O)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('ClC1=C(OC)C(OC)=C2N(C)[C@H]3[C@](C2=C1)(O)[C@@H](O)[C@@]4(SC)C(=O)N(C)[C@@](C(N34)=O)(SC)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC(=O)N(O)CCC[C@H](N)C(=O)N[C@@H](CCCN(O)C(C)=O)C(=O)N[C@@H](CCCN(O)C(C)=O)C(=O)N[C@@H](CO)C(=O)N[C@H]([C@H](O)[C@H]1S[C@H]([C@H](O)[C@H]1O)n1ccc(=N)n(C)c1=O)C(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C1=CC=C(C=C1)C2=C(C3=CC=CC=C3N2)SCCNC(=O)C4=CC5=CC=CC=C5OC4=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CS)C(=O)NCC(O)=O)C', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('CC1=CC=C(S1)C(=O)CSC2=NC3=CC=CC=C3C(=O)N2C4=CC=CC=C4', "
               "'Contains R-S-R structure where R is carbon'), "
               "('OC[C@H]1O[C@@H](SC(Cc2ccc(O)cc2)=NOS(O)(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C(=O)([C@@H](NC(=O)C)CCSC)N[C@H](C(=O)*)CC1=CC=CC=C1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)CNC(=O)[C@@H](N)CCC(O)=O)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C(=O)\\\\C=C\\\\C/C=C\\\\CCCCCCCC)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\\\C/C=C\\\\CCCCC)C[C@H](N)C(O[C@H](COC(=O)CCCCCCCCC)CO)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CCSC)C(=O)N[C@@H](C(C)C)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=C(C(=CC=C1)NC(=O)CSC2=C(C(C(=C(N2)C)C(=O)NC3=CC=CC=C3)C4=CC=CO4)C#N)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)NCC(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC(O)=O)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCC(=O)SC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)C(=O)NCC(O)=O)C(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CS)C(=O)N[C@@H](CC(=O)N)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C\\\\C=C\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CN1C(=NN=C1SCC#N)CCC2=NC3=CC=CC=C3N2', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CN(C)CCCN1c2ccccc2Sc2ccc(Cl)cc12', 'Contains R-S-R structure "
               "where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CC=1NC=NC1)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C(CCC)CCOC(=O)C)C', 'Contains R-S-R structure where R is "
               "carbon'), "
               "('S1[C@H]([C@H]2NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@H]3NC(=O)[C@@H](NC(=O)[C@H]([C@H](CC)C)NC([C@H]4[C@@H](SC[C@H](NC([C@H](NC([C@@H](NC([C@@H](NC([C@H](C1)NC(=O)[C@@H]([N+](C)(C)C)CCC(=O)O)=O)C)=O)CO)=O)[C@@H](SC3)C)=O)C(N[C@@H](CNCCCC[C@H](NC2=O)C(=O)O)C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(N4)=O)C(C)C)[C@H](CC)C)CC5=CC=CC=C5)=O)C)=O)C(C)C)[C@@H](O)C(=O)O)[C@H](O)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CSCCC(C(=O)O)NC1=NC=NC2=C1C=C(C=C2)Br', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CC([O-])=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H]([C@H](CC)C)C(O)=O)CC(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)CN)C(=O)N[C@@H](CCCCN)C(O)=O)C', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('S(C[C@@H](NC(=O)C)C(O)=O)C/C=C/CO', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CC3=CC=CC=C3)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC=C(C=C1)CSC2=NN=C(N2CC3=CC=CS3)C4=CC=CC=N4', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('O=C([O-])[C@@H](NO)CCCCCCCSC', 'Contains R-S-R structure "
               "where R is carbon'), "
               "('C(=O)([C@@H](N)CCSC)N[C@H](C(=O)N[C@H](C(=O)O)CC(O)=O)CC1=CNC2=C1C=CC=C2', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC2=C(C=C1)N=C(N2)SCC(=O)NC3=C(N(N(C3=O)C4=CC=CC=C4)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('O[N+]([O-])=O.Clc1ccc(C(Cn2ccnc2)OCc2ccc(Sc3ccccc3)cc2)c(Cl)c1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S1C=2C(=NC(C)(C)C(C2CCC3=C4SC5=C(C(=O)C(C)(C)N[C@]5(C)CC4=NC(C3=O)(C)C)C)=O)C[C@@]6(C1=C(C(=O)C(C)(C)N6)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](N)C(=O)N1[C@@H](CCC1)C(=O)N[C@@H](CC(C)C)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC=1NC=NC1)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCN1C(=O)C2=CC=CC=C2N=C1SCC(=O)OC3CCCCC3', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C=Cc1ccc(O)cc1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C(CC)C(OC)=O)C', 'Contains R-S-R structure where R is "
               "carbon'), "
               "('S(C(=O)CCCCCCCCCCCCCCC)CCOP(OCC[N+](C)(C)C)([O-])=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C1(C2=C(CSC3=C1C=CC=C3)C=CC=C2)NC(=O)CCCN4CCN(CC4)C5=CC=C(C=C5)F.C(/C=C\\\\C(O)=O)(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C(NC(CCNC(=O)[C@@H](C(COP(OC[C@@H](C(*)=O)N*)(=O)[O-])(C)C)O)=O)CSC(=O)C[C@@H](CCC/C=C\\\\CCCCCCCCCCCCCC/C=C\\\\CCCCCCCCCCCCCCCCCC)O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC=1NC=NC1)C(=O)N[C@@H](C(C)C)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('[Na+].[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(C)onc1-c1ccccc1)C([O-])=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)C)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@H]1N(CCC1)C(=O)[C@@H](N)CCC(O)=O)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C1[C@H]2[C@@H]([C@@H]([C@H](O2)N3C4=C(C(=NC=N4)N)N=C3SC5=CC=C(C=C5)Cl)O)OP(=O)(O1)O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('COc1cc(\\\\C=C\\\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)n2cnc3c(N)ncnc23)ccc1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C(CC(=O)C)C)CC=1OC=CC1', 'Contains R-S-R structure where R "
               "is carbon'), "
               "('S(CCC1NC(=O)C(NC(=O)NC(C(=O)O)C(CC)C)CCCCNC(=O)C(NC(C(N(C(C(NC1=O)CCC2=CC=CC=C2)=O)C)CCC3=CC=CC=C3)=O)CCSC)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC=C(C=C1)C2=NN=C(O2)SCC(=O)N3C4=C(C=C(C=C4)OC)C(=CC3(C)C)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CCCN1C=C(/C=C/C(=O)NC2=C(O)CCC2=O)C=C1)C', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('C1CC2=C(C1)C=C(C=C2)NC(=O)CSC3=NC(=CC(=O)N3)O', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('[Zn+2].S1C2N(C(C(=O)[O-])=C(C1)CC(=O)C)C(=O)C2NC(=O)CCCC(N)C(=O)[O-]', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC(=O)CC[C@H](CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(C)=C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC2=C(C=C1)C=C(C(=O)N2)C=C3C(=O)N(C(=N)S3)C(=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('[H][N+]([H])(CC[N+]([H])([H])Cc1ccccc1)Cc1ccccc1.[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)COc1ccccc1)C([O-])=O.[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)COc1ccccc1)C([O-])=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCOC1=CC=C(C=C1)C=C2C(=O)N(C(=S)S2)CCC(=O)O', 'Contains "
               "R-S-R structure where R is carbon'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC(C)CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C1=C(OC)C=C(C2=NC=CC=C2)N=C1/C=N\\\\O)C', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)=C1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(C1=C2C(N3C(=O)C=CC=4C3=C2C=CN4)=CC=C1)C', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('[H][C@]12CC[C@@]3(C)[C@@]([H])(CC[C@@]33CCC(=O)O3)[C@]1([H])[C@@H](CC1=CC(=O)CC[C@]21C)SC(C)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OC[C@H](N-*)C(-*)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CSC[C@@H](O)[C@@H](O)[C@@H](O)C=O', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\C=C\\\\c1ccc2OCOc2c1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCCC\\\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OC[C@H](N-*)C(-*)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C[C@@H]1CC2(SCC=N2)[C@]2(O)O[C@@H]3C[C@@]4(C)[C@@H](C[C@@H]5O[C@]55[C@@H]4[C@H](O)C(=O)[C@]4(C)[C@H](CC[C@]54O)C4=CC(=O)OC4)C[C@H]3O[C@@H]2O1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)C)C(=O)N[C@@H](C)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C1C(=O)NC2=C(O1)C=CC(=C2)C(=O)CSC3=NN=C(N3CC4=CC=CC=C4)C5=CC=CS5', "
               "'Contains R-S-R structure where R is carbon'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCC(=O)c1ccc(cc1)N=[N+]=[N-])C(=O)NCC(O)=O)C(O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('[NH2+]([C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(C[C@H](C([O-])=O)[C@H](CC)C)=O)CCCC[NH3+])=O)[C@@H](C)CC)=O)CCCNC(N)=[NH2+])=O)CCCC[NH3+])=O)C(C)C)=O)CC(C)C)=O)C)=O)CC(C)C)=O)CCCNC(N)=[NH2+])=O)CC(C)C)=O)CCCC[NH3+])=O)CCCC[NH3+])=O)C)=O)CCCC[NH3+])=O)CO)=O)CCCC[NH3+])=O)C(C)C)=O)C(C)C)=O)[C@@H](C)CC)CCCC[NH3+])=O)[C@H](CC)C)=O)CCCC[NH3+])=O)CO)=O)CCCC[NH3+])=O)C(C)O)C(=O)CCCC[C@@H]1[C@]2([C@@](CS1)(NC(N2)=O)[H])[H]', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CS)C(=O)N[C@@H](CC(C)C)C(O)=O)C', "
               "'Contains R-S-R structure where R is carbon'), "
               "('S1C=2OC3=C(C(O)=CC=C3)C(C2[C@](O)(C(=O)OC)[C@@H]([C@@H]1C)O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)[C@@H](CC([O-])=O)Cc1ccccc1', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OC[C@H](N-*)C(-*)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CC1=CC=CC=C1CSCCNC(=S)NC2=CC=CC=C2', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('CC(C)OC(=O)C(C(=O)OC(C)C)=C1SCCS1', 'Contains R-S-R "
               "structure where R is carbon'), "
               "('C(NC(CCNC(=O)[C@@H](C(COP(OC[C@@H](C(*)=O)N*)(=O)[O-])(C)C)O)=O)CSC(CC(N)=O)=O', "
               "'Contains R-S-R structure where R is carbon'), "
               "('CCOC(=O)OC(C)OC(=O)[C@H]1C(S[C@@H]2N1C(=O)[C@H]2NC(=O)[C@@H](C3=CC=CC=C3)N)(C)C', "
               "'Contains R-S-R structure where R is carbon')]\n"
               "False negatives: [('[*]S\\\\C([*])=N/[*]', 'No sulfur atom "
               "with appropriate R-S-R structure found'), "
               "('COC(=O)Nc1nc2cc(ccc2[nH]1)S(=O)(=O)CC(C)O', 'No sulfur atom "
               "with appropriate R-S-R structure found'), "
               "('C1COCCN1C2=NC3=C(C(=N2)NCC4=NC5=CC6=CC=CC=C6C=C5N4)N=CN3C7=CSC=C7', "
               "'No sulfur atom with appropriate R-S-R structure found'), "
               "('OC/C(=C\\\\[C@@H](NC1=NC=NC2=C1NC=N2)C)/C', 'No sulfur atoms "
               "found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 70,
    'num_false_positives': 100,
    'num_true_negatives': 1732,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.4117647058823529,
    'recall': 0.958904109589041,
    'f1': 0.5761316872427983,
    'accuracy': 0.9459317585301837}