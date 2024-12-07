"""
Classifies: CHEBI:143129 primary fatty amide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_primary_fatty_amide(smiles: str):
    """
    Determines if a molecule is a primary fatty amide (RC(=O)NH2).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a primary fatty amide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of primary amide group
    primary_amide_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[NX3H2]")
    if not mol.HasSubstructMatch(primary_amide_pattern):
        return False, "No primary amide group (C(=O)NH2) found"

    # Get all primary amide groups
    amide_matches = mol.GetSubstructMatches(primary_amide_pattern)
    
    # Count number of primary amides
    if len(amide_matches) > 1:
        return False, "Multiple primary amide groups found"

    # Get the amide carbon
    amide_carbon_idx = amide_matches[0][0]
    amide_carbon = mol.GetAtomWithIdx(amide_carbon_idx)

    # Check if there is only one carbon chain attached to the amide carbon
    carbon_neighbors = [n for n in amide_carbon.GetNeighbors() if n.GetSymbol() == 'C']
    if len(carbon_neighbors) != 1:
        return False, "Amide carbon must have exactly one carbon neighbor"

    # Get all carbons in the longest chain
    chain_carbons = []
    visited = set()

    def dfs_carbon_chain(atom, visited):
        if atom.GetIdx() in visited:
            return
        visited.add(atom.GetIdx())
        if atom.GetSymbol() == 'C':
            chain_carbons.append(atom)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in visited:
                    dfs_carbon_chain(neighbor, visited)

    # Start DFS from the carbon attached to amide
    dfs_carbon_chain(carbon_neighbors[0], visited)

    # Check chain characteristics
    if len(chain_carbons) < 1:
        return False, "No carbon chain attached to amide group"

    # Check for aromatic atoms in the chain
    if any(atom.GetIsAromatic() for atom in chain_carbons):
        return False, "Contains aromatic carbons"

    # Check if the carbon chain is linear/branched aliphatic
    for carbon in chain_carbons:
        # Skip checking amide carbon
        if carbon.GetIdx() == amide_carbon_idx:
            continue
            
        # Check for non-carbon/hydrogen atoms attached to chain
        for neighbor in carbon.GetNeighbors():
            if neighbor.GetSymbol() not in ['C', 'H'] and neighbor.GetIdx() != amide_carbon_idx:
                return False, "Carbon chain contains non-carbon/hydrogen substituents"

    # Count total carbons including amide carbon
    total_carbons = len(chain_carbons) + 1

    return True, f"Primary fatty amide with {total_carbons} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143129',
                          'name': 'primary fatty amide',
                          'definition': 'A primary carboxamide RC(=O)NH2 '
                                        'resultng from the formal condensation '
                                        'of the carboxy group of a fatty acid '
                                        'with ammonia.',
                          'parents': ['CHEBI:140324', 'CHEBI:29348']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.038461538461538464 is too low.\n'
               "True positives: [('CCCCCCCCCCCC(N)=O', 'Primary fatty amide "
               "with 13 carbons'), "
               "('C(=C\\\\C/C=C\\\\CCCC(N)=O)\\\\C/C=C\\\\C/C=C\\\\CCCCC', "
               "'Primary fatty amide with 21 carbons')]\n"
               "False positives: [('O=C(N)/C=C/C(=C/[C@@H](CCCC)C)/C', "
               "'Primary fatty amide with 13 carbons'), "
               "('O=C(N([C@H](C(=O)N)C(C)C)C)[C@@H](N(C(=O)[C@@H](O)CC1=CC=C(OC)C=C1)C)C(C)C', "
               "'Primary fatty amide with 6 carbons'), ('NCC(N)=O', 'Primary "
               "fatty amide with 3 carbons'), "
               "('O=C(N)/C(=C/C(=O)CC12C3[C@@H](C(CO)(CC1C3)OC2)C)/C', "
               "'Primary fatty amide with 17 carbons'), "
               "('C1CN(CCC1C(=O)N)C2CC(=O)N(C2=O)C3=CC(=C(C=C3)F)Cl', 'Primary "
               "fatty amide with 7 carbons'), "
               "('P(=O)(ONCCCCCCCCCCCC(C)C)(O)N(P(=O)(OC1C(OCC2OC(N3C(=O)N=C(N)C=C3)C(C2O)O)=C(CO)C(C1O)O)O)CC(=O)N', "
               "'Primary fatty amide with 3 carbons'), ('CSCC[C@H](N)C(N)=O', "
               "'Primary fatty amide with 5 carbons'), "
               "('C(CCN1CCC(CC1)(C(N)=O)N2CCCCC2)(C#N)(C3=CC=CC=C3)C4=CC=CC=C4', "
               "'Primary fatty amide with 7 carbons'), ('O=C(N)[C@@H]1CCCN1*', "
               "'Primary fatty amide with 6 carbons'), "
               "('[Na+].NC(=O)[C@@H]1CC[C@@H]2CN1C(=O)N2OS([O-])(=O)=O', "
               "'Primary fatty amide with 7 carbons'), "
               "('C1(CC(N(C1)CC(N)=O)=O)O', 'Primary fatty amide with 3 "
               "carbons'), "
               "('C1CN(CCC1C(=O)N)C2=NC(=CS2)C3=CC=C(C=C3)OCC4=CC=CC=C4', "
               "'Primary fatty amide with 7 carbons'), "
               "('C1CN(CCC1C(=O)N)C2=NC(=CS2)C3=CC=C(C=C3)N', 'Primary fatty "
               "amide with 7 carbons'), ('NC(=O)C([O-])=O', 'Primary fatty "
               "amide with 3 carbons'), "
               "('O=C1O/C(=C\\\\[C@@H](C(=O)N)C)/C=C1C2CCC(O)(CO)CC2', "
               "'Primary fatty amide with 16 carbons'), "
               "('C1CCC2=C(C1)C3=C(S2)N(C(=O)N(C3=O)CCC4=CC=CC=C4)CC(=O)N', "
               "'Primary fatty amide with 3 carbons'), "
               "('NC(=O)C(CCC(O)=O)NC=O', 'Primary fatty amide with 6 "
               "carbons'), "
               "('C=1(C(=C(N=C(C1C#N)N)SCC(=O)N)C#N)C2=CC=C(C=C2)OCC3CC3', "
               "'Primary fatty amide with 3 carbons'), "
               "('N[C@@H](CCCNC(N)=N)C(N)=O', 'Primary fatty amide with 6 "
               "carbons'), ('O=C(OC(C)(C)C)N[C@H](C(=O)N)CC(C)C', 'Primary "
               "fatty amide with 7 carbons'), ('NC(=O)[C@@H]1CCCN1', 'Primary "
               "fatty amide with 6 carbons'), ('O=C(N)C#CC#CCCC', 'Primary "
               "fatty amide with 9 carbons'), "
               "('NC(=O)C1(CC[NH+](CCCC(=O)c2ccc(F)cc2)CC1)[NH+]1CCCCC1', "
               "'Primary fatty amide with 7 carbons'), ('OC[C@H](NC=O)C(=O)N', "
               "'Primary fatty amide with 4 carbons'), ('O=C(N)CNCCCCC', "
               "'Primary fatty amide with 3 carbons'), ('NCCC(N)=O', 'Primary "
               "fatty amide with 4 carbons'), ('O=C(N)CCCCCCCCCCCC(C)C', "
               "'Primary fatty amide with 16 carbons'), ('CCCC(CCC)C(N)=O', "
               "'Primary fatty amide with 9 carbons'), "
               "('C(=O)(N)C[C@]([H])(NC(*)=O)C(=O)[O-]', 'Primary fatty amide "
               "with 5 carbons'), ('CS(CCCCCCCCC(N)=O)=O', 'Primary fatty "
               "amide with 10 carbons'), ('NC(=O)CC[C@H]([NH3+])C(O)=O', "
               "'Primary fatty amide with 6 carbons'), ('CCC(C)C(CC)C(N)=O', "
               "'Primary fatty amide with 9 carbons'), "
               "('NC(=O)[C@@H]1CC[C@@H]2CN1C(=O)N2OS([O-])(=O)=O', 'Primary "
               "fatty amide with 7 carbons'), "
               "('C1CN(CCC1C(=O)N)C2=NC=C(S2)Br', 'Primary fatty amide with 7 "
               "carbons'), ('S(/C(=N\\\\C#N)/N1CCC(C(=O)N)CC1)C', 'Primary "
               "fatty amide with 7 carbons'), ('O=C(N)/C=C/C=C\\\\CCCCC', "
               "'Primary fatty amide with 11 carbons'), "
               "('NC(=O)C1CCN(CCCN2C3=CC=CC=C3SC4=CC=C(Cl)C=C24)CC1', 'Primary "
               "fatty amide with 7 carbons'), ('O=C(N)CCCCCCCCCCCCC(CC)C', "
               "'Primary fatty amide with 18 carbons'), ('CCCC1OC1(CC)C(N)=O', "
               "'Primary fatty amide with 9 carbons'), "
               "('N1(C2=C(C(=NC=N2)N)N=C1)[C@@H]3O[C@H](COP(OP(OC[C@H]4O[C@@H](N5CC(=CC=C5)C(=O)N)[C@@H]([C@@H]4O)O)(=O)[O-])(=O)[O-])[C@H]([C@H]3OP(=O)([O-])[O-])O', "
               "'Primary fatty amide with 7 carbons'), "
               "('NC(=O)CCCC[C@@H]1CCSS1', 'Primary fatty amide with 9 "
               "carbons'), ('O=C(N)C(/C=C/[N+]([O-])=NC(C(O)C)C)CCC', 'Primary "
               "fatty amide with 8 carbons'), ('C(C(C(*)=O)N*)C(N)=O', "
               "'Primary fatty amide with 5 carbons'), "
               "('NC(=O)C1=CN([C@@H](O)CC1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O', "
               "'Primary fatty amide with 7 carbons'), "
               "('O=C(N)C1CCN(CC1)C(=O)C=CC(O)=O', 'Primary fatty amide with 7 "
               "carbons'), ('NCSCCC(S)CCCCC(N)=O', 'Primary fatty amide with 9 "
               "carbons'), ('O=C(*)[C@@H](N)CCC(=O)N', 'Primary fatty amide "
               "with 6 carbons'), "
               "('O=C1N(OC)C(=C(OC(=O)CC(=O)N)N=C1C(C)C)[C@H](CC)C', 'Primary "
               "fatty amide with 4 carbons'), "
               "('N1(C2=C(C(=NC=N2)N)N=C1)[C@@H]3O[C@H](COP(OP(OC[C@H]4O[C@@H](N5C=C(CC=C5)C(=O)N)[C@@H]([C@@H]4O)O)(=O)[O-])(=O)[O-])[C@H]([C@H]3O)O*', "
               "'Primary fatty amide with 7 carbons'), "
               "('C1CN(CCC1C(=O)N)C2=NC=C(C=N2)Br', 'Primary fatty amide with "
               "7 carbons'), ('N=1[NH2+]N=NC1C(=O)N', 'Primary fatty amide "
               "with 3 carbons'), ('OC(=O)[C@@H](NC1=CC(O)=C(O)C=C1)CCC(=O)N', "
               "'Primary fatty amide with 6 carbons'), "
               "('N[C@H](CCC(N)=O)C([O-])=O', 'Primary fatty amide with 6 "
               "carbons'), ('O=C(*)C(N*)CCC(=O)N', 'Primary fatty amide with 6 "
               "carbons'), ('O=C(N)C(CC(C)C(O)=O)CC', 'Primary fatty amide "
               "with 9 carbons'), ('NC(=O)C(CCC([O-])=O)NC=O', 'Primary fatty "
               "amide with 6 carbons'), ('C(N)(=O)[C@@H](N*)CC([O-])=O', "
               "'Primary fatty amide with 5 carbons'), ('NC(=N)NCCCC(N)=O', "
               "'Primary fatty amide with 5 carbons'), "
               "('CCOC1=CC=C(C=C1)C2=CSC(=N2)N3CCC(CC3)C(=O)N', 'Primary fatty "
               "amide with 7 carbons'), "
               "('O=C(N)/C(=C/CC[C@@]12[C@H]3[C@](CC[C@H]1C3)(CO)OC2)/C', "
               "'Primary fatty amide with 16 carbons'), "
               "('[C@@H](CCC(N)=O)(NC(=O)*)C(O)=O', 'Primary fatty amide with "
               "6 carbons'), ('C(N)(=O)[C@@H](N*)C', 'Primary fatty amide with "
               "4 carbons'), ('O(N=C(N)N)CCC(=O)N', 'Primary fatty amide with "
               "4 carbons'), ('NC(=O)CC([NH3+])C(O)=O', 'Primary fatty amide "
               "with 5 carbons'), ('NC(=O)[C@@H]1CCCNC1', 'Primary fatty amide "
               "with 7 carbons'), "
               "('CC1=C(SC(=N1)NC(=O)N2CCC[C@H]2C(=O)N)C3=CC(=NC=C3)C(C)(C)C(F)(F)F', "
               "'Primary fatty amide with 6 carbons'), ('NC(=O)CCC(=O)C(O)=O', "
               "'Primary fatty amide with 6 carbons'), "
               "('NC(=O)C[C@H]([NH3+])C(O)=O', 'Primary fatty amide with 5 "
               "carbons'), ('C[C@H](C(=O)N)NCC1=CC=C(C=C1)OCC2=CC(=CC=C2)F', "
               "'Primary fatty amide with 4 carbons'), "
               "('C1=CC=C(C=C1)CN2C(=NN=C2SCC(=O)N)C3=CC4=CC=CC=C4O3', "
               "'Primary fatty amide with 3 carbons'), "
               "('O=C1N(C=CC(N1)=O)[C@@H]2OC([C@H](O[C@@H]3OC(C(=O)O)=C[C@H]([C@@H]3O)O)C(=O)N)[C@H]([C@H]2O)O', "
               "'Primary fatty amide with 7 carbons'), "
               "('NC(=[NH2+])NCCCC(N)=O', 'Primary fatty amide with 5 "
               "carbons'), "
               "('O=C1N(C=CC(N1)=O)[C@@H]2O[C@H]([C@H](O[C@@H]3OC(C(=O)OC)=C[C@H]([C@@H]3O)O)C(=O)N)[C@H]([C@H]2O)OC', "
               "'Primary fatty amide with 7 carbons'), "
               "('CCCCCC=CCC=CCCCCCCCC(=O)N', 'Primary fatty amide with 19 "
               "carbons'), ('[O-]C([C@H](CC(N)=O)N*)=O', 'Primary fatty amide "
               "with 5 carbons'), ('OC(=O)[C@@H](NO)CC(=O)N', 'Primary fatty "
               "amide with 5 carbons'), ('O=C(N)C(N)CCCC', 'Primary fatty "
               "amide with 7 carbons'), "
               "('NC(=O)C1=CN([C@H](O)CC1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](OP(O)(O)=O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O', "
               "'Primary fatty amide with 7 carbons'), ('NCCCC[C@H](N)C(N)=O', "
               "'Primary fatty amide with 7 carbons'), "
               "('O=C(N)C(C(O)CC/C(=C/C(=C/C)/CO)/C)C', 'Primary fatty amide "
               "with 14 carbons'), "
               "('[H][C@@]12CC(\\\\C=C\\\\C(N)=O)=CN1C(=O)C1=C(N[C@@H]2O)C(O)=C(C)C=C1', "
               "'Primary fatty amide with 9 carbons'), ('CCCCC(N)=O', 'Primary "
               "fatty amide with 6 carbons'), "
               "('NC(=O)CC(=O)CC(=O)CC(=O)CC(=O)CC(O)CC(=O)CC(=O)CC(=O)CC(=O)S[*]', "
               "'Primary fatty amide with 20 carbons'), "
               "('C=1(C=CC([N+](=O)[O-])=CC1)OC([C@@H](NC(OC(C)(C)C)=O)CC(N)=O)=O', "
               "'Primary fatty amide with 5 carbons'), "
               "('O=C(*)[C@@H]([NH3+])CC(N)=O', 'Primary fatty amide with 5 "
               "carbons'), ('CC1=CC(=NC(=N1)N(CC(=O)N2CCC(CC2)C(=O)N)C#N)C', "
               "'Primary fatty amide with 7 carbons'), ('NC(=O)C=C', 'Primary "
               "fatty amide with 4 carbons'), "
               "('COC1=CC(=CC(=C1OC)OC)C2=CSC(=N2)N3CCC(CC3)C(=O)N', 'Primary "
               "fatty amide with 7 carbons'), "
               "('NC(=O)C1=C(N)[C@@H](O)[C@H](O)[C@@H](Nc2cc(ccc2O)-c2nc3c(O)cccc3c(=O)[nH]2)C1=O', "
               "'Primary fatty amide with 8 carbons'), ('NC(=O)CC[NH3+]', "
               "'Primary fatty amide with 4 carbons'), "
               "('O=C(N)/C(=C/CCC12C3[C@@H](C(O)(CC1C3)OC2)C)/C', 'Primary "
               "fatty amide with 16 carbons'), "
               "('NC(=O)CC(=O)CC(=O)CC(=O)CC(=O)CC(=O)CC(=O)CC(=O)CC(=O)CC(=O)S[*]', "
               "'Primary fatty amide with 20 carbons'), "
               "('CSC1=CC=C(C=C1)C2=CN=C(S2)N3CCC(CC3)C(=O)N', 'Primary fatty "
               "amide with 7 carbons'), "
               "('NC(=O)C1=C[NH+]([C@@H](O)CC1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O', "
               "'Primary fatty amide with 7 carbons'), "
               "('O=C(*)[C@H](N*)CCC(=O)N', 'Primary fatty amide with 6 "
               "carbons'), ('O=C(N)CCCCCCC\\\\C=C\\\\CCCCCCCC', 'Primary fatty "
               "amide with 19 carbons'), "
               "('NC(=O)CC[C@@H]1NCC2(OC[C@@H](O)[C@@H](O)[C@@H]2O)OC1=O', "
               "'Primary fatty amide with 6 carbons'), "
               "('[C@H](C)([C@@H]([C@@H]([C@H](\\\\C=C\\\\O[C@]1(OC=2C(C1=O)=C3C(C(C(=CC3=O)[O-])=O)=C(C2C)[O-])C)OC)C)OC(=O)C)[C@H](O)[C@@H]([C@@H](O)[C@@H](C)/C=C/C=C(/C)\\\\C(N)=O)C', "
               "'Primary fatty amide with 21 carbons'), "
               "('CC(C)OC1=CC=C(C=C1)C2=CSC(=N2)N3CCC(CC3)C(=O)N', 'Primary "
               "fatty amide with 7 carbons'), ('O=C(N)C=CCCCCCCCCCCCCC', "
               "'Primary fatty amide with 17 carbons')]\n"
               'False negatives: []',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 37,
    'num_true_negatives': 183871,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05128205128205128,
    'recall': 1.0,
    'f1': 0.09756097560975609,
    'accuracy': 0.9997988146375945}