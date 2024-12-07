"""
Classifies: CHEBI:17102 phosphoramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phosphoramide(smiles: str):
    """
    Determines if a molecule is a phosphoramide - a compound where one or more OH groups
    of phosphoric acid have been replaced with amino or substituted amino groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphoramide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define SMARTS patterns for phosphoramide groups
    # P(=O) with at least one N attached and other substituents
    phosphoramide_patterns = [
        "[P;X4](=[O;X1])([N;X3])(~[*])(~[*])",  # General phosphoramide pattern
        "[P;X4](=[O;X1])([N;X3])([N;X3])(~[*])", # Two N atoms
        "[P;X4](=[O;X1])([N;X3])([N;X3])([N;X3])" # Three N atoms (phosphoric triamide)
    ]

    # Check for any matching patterns
    for pattern in phosphoramide_patterns:
        matches = mol.GetSubstructMatches(Chem.MolFromSmarts(pattern))
        if matches:
            # Count N atoms connected to P
            p_atom = mol.GetAtomWithIdx(matches[0][0])
            n_count = sum(1 for neighbor in p_atom.GetNeighbors() if neighbor.GetAtomicNum() == 7)
            
            if n_count == 3:
                return True, "Phosphoric triamide P(=O)(NR2)3"
            else:
                return True, f"Phosphoramide with {n_count} N atoms"

    # Check if molecule contains P but no phosphoramide group
    phosphorus_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15]
    if phosphorus_atoms:
        return False, "Contains phosphorus but no phosphoramide group"
    
    return False, "No phosphorus atoms found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17102',
                          'name': 'phosphoramide',
                          'definition': 'A compound in which one or more of '
                                        'the OH groups of phosphoric acid have '
                                        'been replaced with an amino or '
                                        'substituted amino group. The term is '
                                        'commonly confined to the phosphoric '
                                        'triamides, P(=O)(NR2)3, since '
                                        'replacement of one or two OH groups '
                                        'produces phosphoramidic acids: '
                                        'P(=O)(OH)(NR2)2 , P(=O)(OH)2(NR2).',
                          'parents': ['CHEBI:33256']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.09009009009009009 is too low.\n'
               "True positives: [('OS(=O)CCNC(=N)NP(O)(O)=O', 'Phosphoramide "
               "with 1 N atoms and 0 OH groups'), "
               "('N(CCCl)(CCCl)P1(=O)N(CCCl)CCCO1', 'Phosphoramide with 2 N "
               "atoms and 0 OH groups'), ('OC(=O)CCOP(=O)(NCCCl)NCCCl', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('CN(C)P(F)(=O)N(C)C', 'Phosphoramide with 2 N atoms and 0 OH "
               "groups'), ('NC(=N)NCCCCNP(O)(O)=O', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups')]\n"
               'False positives: '
               "[('C1(=CN(C(NC1=O)=O)C/C=C/CP(N[C@H](C(OCC2=CC=CC=C2)=O)C)(=O)OC3=CC=CC=C3)Cl', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)NP(O)(O)=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[C@H]1(O)[C@H](N2C(N=C(C=C2)N)=O)O[C@H](COP(OP(=O)(N)[O-])(=O)[O-])[C@H]1OP(=O)([O-])[O-]', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('COP([O-])(=O)OCCNC(=[NH2+])NP([O-])([O-])=O', 'Phosphoramide "
               "with 1 N atoms and 0 OH groups'), "
               "('NCCCOP(=O)(NC(=O)[C@@H](N)CC([O-])=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(OC1=CC=CC=C1)(OC2=CC=CC=C2)(=O)/N=C(\\\\OC)/N', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(OC[C@H]1O[C@@H](N2C(=O)NC=3C2=NC=NC3N)[C@@H]([C@@H]1O)O)(OC)N', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('N[C@@H](CCCNC(=N)NP(O)(O)=O)C(O)=O', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), "
               "('P(=O)(N1CC1)(N2CC2)NC(OCC3=CC=CC=C3)=O', 'Phosphoric "
               "triamide P(=O)(NR2)3'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)CCOP(=O)(N1CCOCC1)N1CCOCC1', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('P(O)(O)(=O)N\\\\C(=N\\\\CCCCN)\\\\N', 'Phosphoramide with 1 "
               "N atoms and 0 OH groups'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(N)O)[C@@H](O)[C@H]3O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(O)(O)(=O)N\\\\C(=N\\\\CCCC(N)C(O)=O)\\\\N', 'Phosphoramide "
               "with 1 N atoms and 0 OH groups'), "
               "('CN1C=C(C=C1P(=S)(N2CCOCC2)N3CCOCC3)P(=O)(N4CCOCC4)N5CCOCC5', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(N4CCOCC4)O)[C@@H](O)[C@H]3O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(O)(O)N[C@H]1[C@H](O[C@H](CO)[C@H]([C@@H]1O)O)O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[NH3+][C@@H](CCCNC(=[NH2+])NP([O-])([O-])=O)C([O-])=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CN1C(C=C(CC1=NP(=O)(OC2=CC=CC=C2)OC3=CC=CC=C3)C4=CC=C(C=C4)CO)C5CC5', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCCNC(=[NH2+])NP([O-])([O-])=O)C([O-])=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(N)([O-])=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('N1(P(OC[C@H]2O[C@@H](N3C=4N=C(NC(=O)C4N=C3)N)[C@@H]([C@@H]2O)O)(=O)[O-])C=C(N=C1)C[C@@H](C(*)=O)N*', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('NP(=O)(OCCC(O)=O)N(CCCl)CCCl', 'Phosphoramide with 2 N atoms "
               "and 0 OH groups'), ('CCOP(=O)(SC(C)CC)N1CCSC1=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[C@H]1(O)[C@H](N2C(N=C(C=C2)N)=O)O[C@H](COP(OP(=O)(N)[O-])(=O)[O-])[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[O-]P([O-])(=O)NC(=[NH2+])NCCS([O-])(=O)=O', 'Phosphoramide "
               "with 1 N atoms and 0 OH groups'), "
               "('CN(CC([O-])=O)C(=[NH2+])NP([O-])([O-])=O', 'Phosphoramide "
               "with 1 N atoms and 0 OH groups'), "
               "('CC(O)=O.[H][C@]12SCC(Sc3nc(cs3)-c3cc[n+](C)cc3)=C(N1C(=O)[C@H]2NC(=O)C(=N/OCC)\\\\c1nsc(NP(O)(O)=O)n1)C([O-])=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(O)(N(NC(=O)[C@@H](N)CCCN=C(N)N)C)C(O)C(=O)OC', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[O-]P([O-])(=O)n1cnc(C[C@H](N-*)C(-*)=O)c1', 'Phosphoramide "
               "with 1 N atoms and 0 OH groups'), "
               "('P(O)(O)(=O)/N=C\\\\1/N(CC(=O)N1)C', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), "
               "('[O-]S(=O)CCNC(=[NH2+])NP([O-])([O-])=O', 'Phosphoramide with "
               "1 N atoms and 0 OH groups'), "
               "('CCOP(=O)(OCC)\\\\N=C1/SCC(C)S1', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), "
               "('NCCCOP(=O)(NC(=O)[C@@H](N)CC(O)=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1O)O)N2C=3N=C(NC(=O)C3[N+](=C2)C)N)COP([O-])(=O)N4C=C(N=C4)C[C@@H](C(=O)*)N*', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('S(=O)(=NP(=O)(O)O)(CCC(N)C(=O)NC(C(=O)NC(C(=O)O)C)C)C', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('O.ClCCN(CCCl)P1(=O)NCCCO1', 'Phosphoramide with 2 N atoms "
               "and 0 OH groups'), "
               "('NCCCCCCCCNP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CN1C(=CN=C1[N+](=O)[O-])COP(=O)(NCCBr)NCCBr', 'Phosphoramide "
               "with 2 N atoms and 0 OH groups'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)CCCCCCCCCCCOP(=O)(N1CCOCC1)N1CCOCC1', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('COP(O)(=O)OCCNC(=N)NP(O)(O)=O', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), ('P(=O)(N=C(N(CC)CC)C)(OCC)F', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1O)O)(NC4=C(C=CC=C4)C(O)=O)(=O)O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(N=C(N(CC)CC)C)(C)F', 'Phosphoramide with 1 N atoms and "
               "0 OH groups'), "
               "('CN(C)c1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(NCCCC[C@H](NC(C)=O)C(O)=O)N2CCOCC2)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('N1(P(=O)([O-])OC[C@H]2O[C@@H](N3C=4N=CN=C(N)C4N=C3)[C@@H]([C@@H]2OP(OC[C@H]5O[C@@H](N6C=7N=CN=C(N)C7N=C6)[C@@H]([C@@H]5OP(OC[C@H]8O[C@@H](N9C(NC(=O)C(=C9)C)=O)[C@@H]([C@@H]8OP(OC[C@H]%10O[C@@H](N%11C=%12N=CN=C(N)C%12N=C%11)[C@@H]([C@@H]%10*)O)(=O)[O-])O)(=O)[O-])O)(=O)[O-])O)C=C(N=C1)C[C@@H](C(=O)*)N*', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CCOP(=O)(OCC)N=C1SCCS1', 'Phosphoramide with 1 N atoms and 0 "
               "OH groups'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)CCCCCCCCCCCOP(=O)(N1CCOCC1)N1CCOCC1', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('P(=O)(ONCCCCCCCCCCCC(C)C)(O)N(P(=O)(OC1C(OCC2OC(N3C(=O)N=C(N)C=C3)C(C2O)O)=C(CO)C(C1O)O)O)CC(=O)N', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('ClCCN(CCCl)P1(=O)NC(=O)CCO1', 'Phosphoramide with 2 N atoms "
               "and 0 OH groups'), ('CCCSP(=O)(OCC)N1CCN(CC)\\\\C1=N/C#N', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('N[C@@H](Cc1cncn1P(O)(O)=O)C(O)=O', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), "
               "('COC(=O)[C@H](CCCCNP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)NC(C)=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(N=C(N(CC)CC)C)(OC)F', 'Phosphoramide with 1 N atoms "
               "and 0 OH groups'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(=O)Nc2ccccc2C([O-])=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('NC(=[NH2+])NCCCCNP([O-])([O-])=O', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), "
               "('OC(=O)CCCC(=O)Nc1ccc(CP(O)(=O)Nc2ccc(cc2)[N+]([O-])=O)cc1', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('S(=O)(=O)(O)NP(=O)(N1C(=O)[C@H](N)CCC1)N', 'Phosphoric "
               "triamide P(=O)(NR2)3'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1O*)O)*)COP([O-])(=O)N2C=C(N=C2)C[C@@H](C(=O)*)N*', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('S(=O)(=O)(O)N[P@](=O)(N1C(=O)[C@@H](N)CCC1)N', 'Phosphoric "
               "triamide P(=O)(NR2)3'), "
               "('[C@H]1(O)[C@H](N2C(N=C(C=C2)N)=O)O[C@H](COP(OP(=O)(NC(CC[C@@H](C(=O)[O-])[NH3+])=O)[O-])(=O)[O-])[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('NP1(=O)OCCCN1CCCl', 'Phosphoramide with 2 N atoms and 0 OH "
               "groups'), ('[P@](=O)(OC1=CC=C(/C=C/C(=O)OC)C=C1)(OC)N', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(OC[C@H]1O[C@@H](N2C(=O)NC=3C2=NC=NC3N)[C@@H]([C@@H]1O)O)(O)NC(=O)[C@H]4NCCC4', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('C1(=O)NC(=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(NCCCC[C@@H](C(*)=O)N*)[O-])[C@@H](O)[C@H]3O)N', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('C(C(=O)NP([O-])(=O)[O-])C[C@@H](C(=O)[O-])[NH3+]', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(OC)(O)N(NC(=O)[C@@H](N)CC(C)C)C', 'Phosphoramide with "
               "1 N atoms and 0 OH groups'), "
               "('[O-]P([O-])(=O)NC(=[NH2+])NCCC[C@H](N-*)C(-*)=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CNC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO.CNC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO.C[C@@H](O[C@H]1OCCN(Cc2nn(c(=O)[nH]2)P(O)(O)=O)[C@H]1c1ccc(F)cc1)c1cc(cc(c1)C(F)(F)F)C(F)(F)F', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('C(C(=O)NP(O)(=O)O)C[C@@H](C(=O)O)N', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), ('NP(O)(O)=O', 'Phosphoramide with 1 "
               "N atoms and 0 OH groups'), "
               "('P(N(CCCl)CCCl)(N(CCCl)CCCl)(OCCS(C[C@@H](C(N[C@@H](C(O)=O)C1=CC=CC=C1)=O)NC(CC[C@@H](C(O)=O)N)=O)(=O)=O)=O', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('C1[C@H]([C@@H]1C(=O)NC2=CC3=CC=CC=C3C=C2)[C@H](C4=CC=CC=C4)NP(=O)(C5=CC=CC=C5)C6=CC=CC=C6', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CN(CC(O)=O)C(=N)NP(O)(O)=O', 'Phosphoramide with 1 N atoms "
               "and 0 OH groups'), "
               "('CC1=C(C=C(C=C1)NP(=O)(OC2=CC=CC=C2F)OC3=CC=CC=C3F)C', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(=O)(OC[C@H]1O[C@@H](N2C(=O)NC=3C2=NC=NC3N)[C@@H]([C@@H]1O)O)(OC)NC(=O)[C@H]4NCCC4', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CN(C)P(=O)(N(C)C)n1nc(nc1N)-c1ccccc1', 'Phosphoric triamide "
               "P(=O)(NR2)3'), "
               "('P(=O)(OCC1OC(OC2C(O)C(O)C(OCC(OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)OC2CO)C(O)C(C1O)O)(O)N[C@H](C(=O)N[C@H](C(=O)O)CC3=CC=CC=C3)CC4=CC=CC=C4', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('P(Cl)(*)(N)=O', 'Phosphoramide with 1 N atoms and 0 OH "
               "groups'), ('S(=O)(=O)(C1=C(C=C(OP(OCC)(=O)NC(C)C)C=C1)C)C', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('NP(=O)(OCCC=O)N(CCCl)CCCl', 'Phosphoramide with 2 N atoms "
               "and 0 OH groups'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)NP([O-])([O-])=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[O-]C(=O)CNC(=[NH2+])NP([O-])([O-])=O', 'Phosphoramide with "
               "1 N atoms and 0 OH groups'), "
               "('CSCC[C@H](NC=O)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@@H]([C@@H](C)O)C(=O)NCC(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H](C)C(=O)N[C@@H](CC(O)=O)C(=O)NP(=O)(OCCCN)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CNP(=O)(OC)Oc1ccc(cc1Cl)C(C)(C)C', 'Phosphoramide with 1 N "
               "atoms and 0 OH groups'), "
               "('P(=O)(O[C@H]1O[C@H]([C@@H](O)[C@H]([C@H]1O)O)C)(O)N[C@H](C(=O)N[C@H](C(=O)O)CC=2C3=C(C=CC=C3)NC2)CC(C)C', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('COC(=O)[C@H](CCCCNP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)NC(C)=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(=O)N[C@@H](Cc2ccccc2)C([O-])=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('C[C@@H](O[C@H]1OCCN(Cc2nn(c(=O)[nH]2)P([O-])([O-])=O)[C@H]1c1ccc(F)cc1)c1cc(cc(c1)C(F)(F)F)C(F)(F)F', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('NP(=O)(OCCCO)N(CCCl)CCCl', 'Phosphoramide with 2 N atoms and "
               "0 OH groups'), "
               "('O.CC(O)=O.[H][C@]12SCC(Sc3nc(cs3)-c3cc[n+](C)cc3)=C(N1C(=O)[C@H]2NC(=O)C(=N/OCC)\\\\c1nsc(NP(O)(O)=O)n1)C([O-])=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('[C@H](NC([C@@H](NC([C@H](CCCNP(NS(O)(=O)=O)(=O)N)N)=O)C)=O)(CCCNC(N)=N)C(O)=O', "
               "'Phosphoric triamide P(=O)(NR2)3'), "
               "('NC(CCC(=O)NC(CSC1CCOP(=O)(N1)N(CCCl)CCCl)C(=O)NCC(O)=O)C(O)=O', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)N[C@@H](Cc2ccccc2)C(O)=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('N(CCCl)(CCCl)[P@@]1(=O)N[C@H](OO)CCO1', 'Phosphoramide with "
               "2 N atoms and 0 OH groups'), ('NP([O-])([O-])=O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)CCOP(=O)(N1CCOCC1)N1CCOCC1', "
               "'Phosphoramide with 2 N atoms and 0 OH groups'), "
               "('CCOP(=O)(OCC)N=C1SCS1', 'Phosphoramide with 1 N atoms and 0 "
               "OH groups'), "
               "('[H+].[Na+].[Na+].[Na+].Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)NP([O-])([O-])=O)[C@@H](O)[C@H]1O', "
               "'Phosphoramide with 1 N atoms and 0 OH groups'), "
               "('CN(C1=CC=CC=C1)P(=O)(N(C)C2=CC=CC=C2)N(C)C3=CC=CC=C3', "
               "'Phosphoric triamide P(=O)(NR2)3'), "
               "('P(OC1OC(C(O)C1O)C(O)CO)(O)(=O)NC=2N=CN=C3N(C4OC(CC4O)COP(O)(=O)NC(=O)C(O)C(O)C(C)C)C=NC32', "
               "'Phosphoramide with 1 N atoms and 0 OH groups')]\n"
               'False negatives: '
               "[('S1C(=NC(=C1)C2=NC(=C(O)C(=C2OC)OC)C(=O)N)[C@@H](O)CCCC', "
               "'No phosphorus atoms found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 91,
    'num_true_negatives': 183780,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.052083333333333336,
    'recall': 0.8333333333333334,
    'f1': 0.09803921568627451,
    'accuracy': 0.9994996655372885}