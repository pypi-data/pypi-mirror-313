"""
Classifies: CHEBI:24745 hydroxypyridine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxypyridine(smiles: str):
    """
    Determines if a molecule is a hydroxypyridine (pyridine with at least one hydroxy substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxypyridine, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for pyridine ring with hydroxy substituent
    patterns = [
        # Basic pyridine with OH
        Chem.MolFromSmarts('c1ccncc1[OH]'),
        # Alternative forms of pyridine with OH
        Chem.MolFromSmarts('[nH]1c(O)cccc1'),
        Chem.MolFromSmarts('n1c(O)cccc1'),
        # Keto form
        Chem.MolFromSmarts('O=c1[nH]cccc1'),
        # N-oxide form
        Chem.MolFromSmarts('[O-][n+]1ccccc1'),
        # Various tautomeric forms
        Chem.MolFromSmarts('Oc1[nH]cccc1'),
        Chem.MolFromSmarts('Oc1ccncc1'),
        Chem.MolFromSmarts('O=c1cccc[nH]1'),
    ]

    found = False
    for pattern in patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            found = True
            break

    if not found:
        return False, "No hydroxy substituent found on pyridine ring"

    # Find position of hydroxy group(s)
    positions = []
    for pattern in patterns:
        if pattern is None:
            continue
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            # For each match, find the position relative to nitrogen
            for ring in mol.GetRingInfo().AtomRings():
                if any(idx in match for idx in ring):
                    # Find nitrogen and oxygen indices in the ring
                    n_idx = None
                    o_idx = None
                    for idx in ring:
                        atom = mol.GetAtomWithIdx(idx)
                        if atom.GetSymbol() == 'N':
                            n_idx = idx
                        elif atom.GetSymbol() == 'O':
                            neighbors = [n.GetIdx() for n in atom.GetNeighbors()]
                            if any(nidx in ring for nidx in neighbors):
                                o_idx = idx

                    if n_idx is not None and o_idx is not None:
                        # Calculate position
                        for neighbor in mol.GetAtomWithIdx(o_idx).GetNeighbors():
                            if neighbor.GetIdx() in ring:
                                pos = (ring.index(neighbor.GetIdx()) - ring.index(n_idx)) % 6
                                if pos == 0:
                                    positions.append(1)  # N-hydroxy
                                else:
                                    positions.append(pos)

    positions = list(set(positions))  # Remove duplicates
    positions.sort()

    if len(positions) == 1:
        return True, f"{positions[0]}-hydroxypyridine"
    elif len(positions) > 1:
        return True, f"Multiple hydroxypyridine positions: {','.join(map(str, positions))}"
    else:
        return True, "Hydroxypyridine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24745',
                          'name': 'hydroxypyridine',
                          'definition': 'Any member of the class of pyridines '
                                        'with at least one hydroxy '
                                        'substituent.',
                          'parents': ['CHEBI:26421', 'CHEBI:74818']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.10619469026548672 is too low.\n'
               "True positives: [('NCCCC(=O)C1=CN=C(O)C=C1', "
               "'5-hydroxypyridine'), "
               "('C(C)(O)=O.C=1(N=C(C(O)=CC1)CO)C(CNC(C)(C)C)O', "
               "'4-hydroxypyridine'), ('Cc1ncc(cc1O)C(O)=O', "
               "'2-hydroxypyridine'), ('O/N=C\\\\C1=C(O)C(=NC=C1CO)C', "
               "'2-hydroxypyridine'), ('OC1=C(C(=CN=C1C)CO)C2SCC(N2)C(=O)O', "
               "'4-hydroxypyridine'), "
               "('CC(C)CC(=O)OC(c1ccccc1)c1cc(O)c(C(O)=O)c(=O)[nH]1', "
               "'3-hydroxypyridine')]\n"
               'False positives: '
               "[('O=C1N(C=C([C@]2(O)[C@H](O)CC(=O)CC2)C(=C1[C@H]3O[C@@H](/C(=C/C(CC(CC)C)C)/C)[C@H](C)CC3)O)C', "
               "'3-hydroxypyridine'), "
               "('O=C1N(O)C=C(C2=CC=C(O[C@H]3OC([C@H](OC)[C@@H](C3O)O)CO)C=C2)C(=C1C4OC(CCC4C)C)O', "
               "'Hydroxypyridine'), "
               "('O1C(C2OC3=C(C2O)C=4N(C=5C(C(=O)C4C(O)=C3)=CC=CC5)C)(C1)C', "
               "'Hydroxypyridine'), "
               "('CCCCCN1C2=CC=CC=C2C(=C(C1=O)C(=O)NC(C)C3=CC=CC=C3)O', "
               "'3-hydroxypyridine'), "
               "('O1C(OC2=C(O)C(=[N+]([O-])C=C2)C3=[N+]([O-])C=CC(=C3O)OC4OC(C(O)C(C4O)O)CO)C(O)C(O)C(C1CO)O', "
               "'4-hydroxypyridine'), "
               "('O=C1NC=C(C2=CC=C(O)C=C2)C(=C1C(=O)[C@@H]3C=C([C@H]4CC[C@@H](C[C@@H]4[C@H]3/C=C/CO)C)C)O', "
               "'3-hydroxypyridine'), ('OC(=O)[C@@H](N)CC1=NC=C(O)C=C1', "
               "'4-hydroxypyridine'), "
               "('CC(C)CCn1c2ccccc2c(O)c(C(=O)Nc2ncc(C)s2)c1=O', "
               "'3-hydroxypyridine'), "
               "('C1CCC2=C(C1)C3=C4N2C(=O)C(=C(C4=CC=C3)O)CC5=CC=CC=C5', "
               "'3-hydroxypyridine'), ('CC(=NC1=CC=CC=C1O)CC(=O)C2=CC=NC=C2', "
               "'Hydroxypyridine'), "
               "('O=C1NC=C(C2=CC=C(O)C=C2)C3=C1C(=O)[C@H]4[C@H](C=CC)[C@H]5C[C@@H](C)CC[C@@H]5[C@@]([C@@H]4O3)(O)C', "
               "'Hydroxypyridine'), ('O=C1C(O)=C2N=CC3=C2C(=C1)N(C=C3)CCCO', "
               "'Hydroxypyridine'), "
               "('CC[C@H]1NC(=O)[C@@H](NC(=O)c2ncccc2O)[C@@H](C)OC(=O)[C@@H](NC(=O)C2CC(=O)C(CS[C@@H]3CN4CCC3CC4)CN2C(=O)[C@H](Cc2ccc(cc2)N(C)C)N(C)C(=O)[C@@H]2CCCN2C1=O)c1ccccc1', "
               "'4-hydroxypyridine'), ('CCCOC(=O)CC1=C(C2=CC=CC=C2NC1=O)O', "
               "'3-hydroxypyridine'), "
               "('O=C1NC=C([C@]2(O)[C@@H]3O[C@@H]3[C@H](O)CC2)C(=C1C(=O)[C@H]4[C@H]5[C@H](C=C[C@H]4C)[C@@H](O)[C@H](C)CC5)O', "
               "'3-hydroxypyridine'), ('Oc1cccc2[nH]c(=O)ccc12', "
               "'Hydroxypyridine'), "
               "('COC(=O)\\\\C=C/NC(=O)c1cc2c3cccc(O)c3[nH]c2c(n1)C(C)=O', "
               "'Hydroxypyridine'), "
               "('O1C(CC(C2=C1C(C(C)(C)C=C)=C3OC(=O)C(=CC3=C2O)C(C)(C)C=C)C=4C=5NC6=C(C(=O)C5C(O)=CC4OC)C=CC(O)=C6OC)(C)C', "
               "'Hydroxypyridine'), "
               "('[S@](=O)(C=1C=2NC=C(O)C=3C2N(C4=CC(=O)C=CC34)C(C1)=O)C', "
               "'2-hydroxypyridine'), "
               "('O1C(C1C(O)C=2C=3N(C4=C(C(=O)C3C(O)=CC2OC)C=CC(OC)=C4OC)C)(C)C', "
               "'Hydroxypyridine'), "
               "('C1CN2C3=C(C=CC=C31)C(=C(C2=O)C(=O)NCCC4=CC=CC=C4)O', "
               "'3-hydroxypyridine'), ('CCCCCCCc1cc(O)c2ccccc2[n+]1[O-]', "
               "'3-hydroxypyridine'), "
               "('CN1C(=C(C(=O)NC1=S)C(C2=CC=CC=N2)C3=C(N(C(=S)NC3=O)C)O)O', "
               "'5-hydroxypyridine'), ('OC(=O)c1c(O)[nH]c2ccccc2c1=O', "
               "'1-hydroxypyridine'), "
               "('O=C(O)C1=NC2=C(O)C(O)=C3O[C@]4(CC[C@H]5[C@]([C@@H]4CC3=C2C=C1)(CCCC5(C)C)C)C', "
               "'Hydroxypyridine'), "
               "('O=C1C=2N=CC3=CC(CC)=CC(=C3C2C(=O)C=4C1=C(O)C=CC4)O', "
               "'Hydroxypyridine'), ('O=C1NC(O)=CC2=NN(C(N)=C21)C3=CC=CC=C3', "
               "'5-hydroxypyridine'), "
               "('O=C1N(C=C(C2(O)CCC(=O)CC2)C(=C1[C@H]3O[C@@H](/C(=C/C(CC(CC)C)C)/C)[C@H](C)CC3)O)C', "
               "'3-hydroxypyridine'), "
               "('CCN(C1CCOCC1)C2=CC(=CC(=C2C)/C(=N/CC=3C(C)=CC(C)=NC3O)/O)C4=CC=C(C=C4)CN5CCOCC5', "
               "'1-hydroxypyridine'), "
               "('CCCCn1c2ccccc2c(O)c(C(=O)Nc2nnc(CC)s2)c1=O', "
               "'3-hydroxypyridine'), ('O=C(O)C=1C2=NC=CC=C2C=C(C1)O', "
               "'Hydroxypyridine'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C=3SC=C(N3)C(=O)N[C@H](C=4SC=C(C5=C(C6=NC(C(N[C@H](C(NC2=C(OC)C)=O)[C@H](O)C)=O)=CS6)C=C(O)C(=N5)C=7SC=C(N7)C(=O)NC(C(=O)N)=C)N4)CO)[C@H](O)[C@H](O)C(=O)O', "
               "'4-hydroxypyridine'), "
               "('C[C@H](OP(O)(=O)OC[C@@H](O)[C@@H](O)[C@@H](O)Cn1c2cc(O)ccc2cc2c1nc(=O)[nH]c2=O)C(=O)N[C@@H](CCC(=O)N[C@@H](CCC(=O)N[C@@H](CCC(O)=O)C(O)=O)C(O)=O)C(O)=O', "
               "'Hydroxypyridine'), "
               "('O=C1NC=C(C2=CC=C(O)C=C2)C(=C1C(=O)C3=C(/C=C/C)[C@@H]4[C@H](CC[C@@H](C4)C)C(=C3)C)O', "
               "'3-hydroxypyridine'), "
               "('ClC(C(CC(C(=O)C=1C(=O)NC(OC)=C(C1O)OC)C)C)CCl', "
               "'3-hydroxypyridine'), ('O=C1NC(=CC(=C1C=O)O)CC2=CC=CC=C2', "
               "'3-hydroxypyridine'), "
               "('O=C1N(O)C=C([C@@]2(O)[C@H]3O[C@H]3[C@@H](O)CC2)C(=C1C(=O)[C@@H]4[C@@H]5[C@@H](C=C[C@@H]4C)CC(C)=CC5)O', "
               "'Hydroxypyridine'), "
               "('S1(=O)(=O)N(C(=C(O)C=2C1=CC=CC2)C(=O)NC3=NC=C(O)C=C3)C', "
               "'2-hydroxypyridine'), "
               "('O=C1O[C@@H]([C@H](NC(=O)C2=NC=CC=C2O)C(=O)N[C@@H](C(=O)N3[C@@H](C(=O)N(C)CC(N([C@H](C(N[C@H](C(N([C@H]1C4=CC=CC=C4)C)=O)CO)=O)C(C(C)C)C)C)=O)C[C@H](C3)O)CC(C)C)C', "
               "'4-hydroxypyridine'), "
               "('ClC1=C(OC)C=2OC3=C4OCO[C@H]5C4=C(C=6C(=O)C=7C(=O)NC(C)=CC7C(C6C5)=O)C(=C3C(C2C=C1)=O)O', "
               "'Hydroxypyridine'), "
               "('COc1ccc(cc1O)-c1c2c3cc(OC)c(OS(O)(=O)=O)cc3oc(=O)c2n2ccc3cc(OC)c(OC)cc3c12', "
               "'Hydroxypyridine'), "
               "('O1C(C=CC2=C1C=C(O)C=3C2=NC=4C(C3O)=CC=CC4)(C)C', "
               "'3-hydroxypyridine'), "
               "('CCN1C2=CC=CC=C2C(=C(C1=O)C(=O)NC3=CC=CC=C3F)O', "
               "'3-hydroxypyridine'), "
               "('COc1ccc(cc1O)-c1c2c3cc(OC)c(OS([O-])(=O)=O)cc3oc(=O)c2n2ccc3cc(OC)c(OC)cc3c12', "
               "'Hydroxypyridine'), "
               "('OC(=O)c1cc(C(O)=O)c2c(n1)c(O)c(O)c1cc([nH]c21)C(O)=O', "
               "'Hydroxypyridine'), "
               "('O=C1N(O)CCCC1NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)[C@H]2NC3=[N+](C=4C(=CC(O)=C(C4)O)C=C3NC(=O)CCC(N)C(=O)O)CC2)CC(=O)O)CCCCN)C(O)C)C(O)C(=O)O)C(O)C)C(O)C', "
               "'Hydroxypyridine'), ('Cc1ncc(CO)c(C[NH3+])c1O', "
               "'2-hydroxypyridine'), "
               "('C12=CC(=CC=C1C(=CC=N2)NC3=CC(=C(C=C3)O)C[NH+](CC)CC)Cl', "
               "'Hydroxypyridine'), "
               "('O=C(O)C1=C(C(O)=C(O)C(=C1C)O)C2=NC=CC3=C2N(C=4C=CC=CC34)C', "
               "'Hydroxypyridine'), ('COc1cc2n(C)c3c(O)cccc3c(=O)c2c(O)c1OC', "
               "'Hydroxypyridine'), ('C1(O)=C(C)[NH+]=CC(CO)=C1C[NH3+]', "
               "'2-hydroxypyridine'), "
               "('ClC1=C(O)C2=C(O)C3=C(C(=O)C4(O)C5=C(OC)C=6C(=O)NC(C)=CC6C=C5CCC4C3=O)C(=C2C=C1O)C', "
               "'Hydroxypyridine'), "
               "('S1SCC2N(C(=O)CNC(=O)C(NC(=O)C3=NC=4C(=CC=CC4)C=C3O)CSC(C(N(C(C(C1)N(C(=O)CNC(=O)C(NC(=O)C5=NC=6C(=CC=CC6)C=C5O)CSC(C(N(C2=O)C)=C)=O)C)=O)C)=C)=O)C', "
               "'4-hydroxypyridine'), "
               "('C1=C(C(=C(C=C1C2=NC(=NO2)C=3C(=[N+](C(=C(C3C)Cl)C)[O-])Cl)O)O)[N+](=O)[O-]', "
               "'Hydroxypyridine'), "
               "('O=C1C(O)=C2N=C3C(=CC(=O)C=C3)C4=C2C(=C1)C=CN4', "
               "'Hydroxypyridine'), "
               "('O=C1OC(C(NC(=O)C2=NC=CC=C2O)C(=O)NC(C(=O)N3C(C(=O)N(C)CC(NC(C(NC(C(N(C1C4=CC=CC=C4)C)=O)C)=O)C(C(C)C)C)=O)C[C@H](C3)O)C(CC)C)C', "
               "'4-hydroxypyridine'), ('Oc1ccc2nc(Cl)ccc2c1', "
               "'Hydroxypyridine'), "
               "('S(=O)(=O)(N1CCN(C(=O)C=2C=3C(N=C(O)C2)=CC=CC3)CC1)C=4C(=C(C=C(C4C)C)C)C', "
               "'1-hydroxypyridine'), "
               "('CC(C)Cn1c2ccccc2c(O)c(C(=O)Nc2ncc(C)s2)c1=O', "
               "'3-hydroxypyridine'), "
               "('C(NN=CC1=CC(OC)=C(C=C1)O)(=O)C=2C=CN=CC2', "
               "'Hydroxypyridine'), "
               "('O=C1N2C=3C(O)=C(NC(=O)[C@@H](O)C)C4=CC=C(N=C4C3C=C[C@@]2(C)CC1)C', "
               "'Hydroxypyridine'), ('OC1=C(C(=O)N(C=2C1=CC=CC2)C)CC', "
               "'3-hydroxypyridine'), "
               "('N=1C=CC=C2C1OC=3C2=NC(=NC3N4CCOCC4)C=5C=CC=C(O)C5', "
               "'Hydroxypyridine'), "
               "('O=C1NC(C(=O)NC(C(=O)NCCCCC1NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C2[N+]3=C(NCC2)C(NC(=O)CCC(=O)O)=CC=4C3=CC(O)=C(C4)O)CO)CCCCN)CCCN(O)C=O)CO)CCCN(O)C=O', "
               "'Hydroxypyridine'), "
               "('COC1=C(C=CC(=C1)C=C2C(=O)N=C(S2)NC3=CC=CC=N3)O', "
               "'Hydroxypyridine'), "
               "('CC(C)Cn1c2ccccc2c(O)c(C(=O)Nc2nc(C)cs2)c1=O', "
               "'3-hydroxypyridine'), ('C[NH+]1CCC=C1c1ccc(O)nc1', "
               "'5-hydroxypyridine'), "
               "('COC1=CC=C(C=C1)C(=O)NC(C2=CC(=C(C=C2)OC)OC)C3=CC(=C4C=CC=NC4=C3O)Cl', "
               "'Hydroxypyridine'), "
               "('O[C@@H](CNC1CC=2C(C1)=CC(=C(C2)CC)CC)C3=C4C(NC(=O)C=C4)=C(O)C=C3.OC(=O)/C=C/C(O)=O', "
               "'Hydroxypyridine'), ('Oc1ccc-2c(c1)-c1nccc3ccnc-2c13', "
               "'Hydroxypyridine'), "
               "('CCC(CO)\\\\C=C\\\\C=C\\\\C=C\\\\C(=O)c1c(O)c(c[nH]c1=O)[C@@]1(O)CC[C@H](O)CC1', "
               "'3-hydroxypyridine'), "
               "('O=C1NC=C(C2=CC=C(O)C=C2)C3=C1[C@H]4[C@@H](C[C@H](C)[C@H]([C@@H]4C)O)[C@@H](O3)C', "
               "'Hydroxypyridine'), ('CC1=CC(=O)NC2=C1C=CC(=C2)O', "
               "'Hydroxypyridine'), "
               "('O(C1=C(C(C2=C(OC)C=C3OC(=O)C=CC3=C2)C=C(C)C)C(O)=C4C(N(C5=C(C4=O)C=CC(OC)=C5OC)C)=C1)C', "
               "'Hydroxypyridine'), "
               "('[H+].[H+].O.O.[Cl-].[Cl-].CCN(CC)Cc1cc(Nc2ccnc3cc(Cl)ccc23)ccc1O', "
               "'Hydroxypyridine'), "
               "('CC1CC11N(C)C(=O)C2CSSCC(N(C)C(=O)C(C)NC(=O)C(COC1=O)NC(=O)c1nc3ccccc3cc1O)C(=O)N(C)C1(CC1C)C(=O)OCC(NC(=O)c1nc3ccccc3cc1O)C(=O)NC(C)C(=O)N2C', "
               "'4-hydroxypyridine'), ('O(C(=O)C=1C2=C(NC(=O)C1)C=CC(O)=C2)C', "
               "'Hydroxypyridine'), ('O=C(O)C1=C2C3=NC(=CC=C3COC2=CC(=C1)O)C', "
               "'Hydroxypyridine'), "
               "('O=C1C=2N=CC3=CC(C)=CC(=C3C2C(=O)C=4C1=C(O[C@@H]5O[C@H]([C@H](O)[C@@H](C5)O)C)C=CC4)O', "
               "'Hydroxypyridine'), "
               "('O=C1NC(=C(CCC)C(=C1C)O)C/C=C(/C/C=C/C(O)(C)C)\\\\C', "
               "'3-hydroxypyridine'), "
               "('O=C1N(C=C(C2(O)C(O)CC(=O)CC2)C(=C1C3OC(C(=CC(CC(CC)C)C)C)C(C)CC3)O)C', "
               "'3-hydroxypyridine'), "
               "('COC1=C(C=C(C=C1)C=NNC(=O)C2=C(C=C(C=C2)O)O)CSC3=CC=CC=N3', "
               "'Hydroxypyridine'), "
               "('CCCN1C2=CC=CC=C2C(=C(C1=O)C(=O)NCC3=CC(=C(C=C3)OC)OC)O', "
               "'3-hydroxypyridine'), "
               "('CCCN1C2=CC=CC=C2C(=C(C1=O)C(=O)NCC3=CC=NC=C3)O', "
               "'3-hydroxypyridine'), ('O=C1NC=C(C2=CC=CC=C2)C(=C1C=O)O', "
               "'3-hydroxypyridine'), "
               "('CC1=C(C(=O)OC2=CC(=C(C=C12)Cl)O)CC(=O)N3C[C@H]4C[C@@H](C3)C5=CC=CC(=O)N5C4', "
               "'Hydroxypyridine'), "
               "('O=C1N(OC)C=C(C2=CC=CC=C2)C(=C1[C@@H]3O[C@@H]([C@@H](C)C[C@H]3C)[C@@H](CCOC(=O)C)C)O', "
               "'3-hydroxypyridine'), "
               "('O=C1NC=C(C2=CC=C(O)C=C2)C(=C1C(=O)[C@H]3[C@H]4[C@H](C=C[C@H]3C)CC(C)=CC4)O', "
               "'3-hydroxypyridine'), "
               "('O=C/1C2=C(C=NC(=C2)C(=O)N)C\\\\C1=C/C3=CC=C(O)C=C3', "
               "'Hydroxypyridine'), ('CC1=NC2=C(C=C(C=C2)O)C(=C1)NCCO', "
               "'Hydroxypyridine'), "
               "('CCN1CCN(CC1)C(C2=CN=CC=C2)C3=C(C4=C(C=CC=N4)C=C3)O', "
               "'Hydroxypyridine'), ('[NH3+]CCCC(=O)C1=CN=C(O)C=C1', "
               "'5-hydroxypyridine'), "
               "('O=C(OC)C1=NC(=C2NC3=C(C2=C1)C=C(O)C=C3)[C@@H](O)C', "
               "'Hydroxypyridine'), "
               "('O1C(CC(C2=C1C(C(C)(C)C=C)=C3OC(=O)C(=CC3=C2O)C(C)(C)C=C)C=4C=5NC6=C(C(=O)C5C(O)=CC4OC)C=CC(OC)=C6OC)(C)C', "
               "'Hydroxypyridine'), "
               "('O=C1N(OC)C=C(C2=CC=CC=C2)C(=C1[C@@H]3O[C@@H]([C@@H](C)C[C@H]3C)[C@H](CO)CC)O', "
               "'3-hydroxypyridine'), "
               "('C[C@H]1CCc2c1c[n+](CCc1ccc(O)cc1)cc2C', 'Hydroxypyridine'), "
               "('S1C(=NC(=C1)C2=NC(=C(O)C(=C2OC)OC)C(=O)N)CCCC(=O)C', "
               "'2-hydroxypyridine'), "
               "('CC(C)(C)N1C(=NN=N1)C(C2=CC=NC=C2)N3CCN(CC3)C4=CC=C(C=C4)O', "
               "'Hydroxypyridine'), "
               "('O=C1N(C=C(N1)C=O)[C@@H]2O[C@@H]([C@@H](NC(=O)[C@H](N)C[C@H](O)C3=NC=C(O)C=C3)C(=O)O)[C@@H]([C@@H]2O)O', "
               "'2-hydroxypyridine'), "
               "('O=C1N(O)C=C(C2=CC=C(O)C=C2)C(=C1C(=O)/C=C/C=C/C=C/C(=C/[C@H](CC)C)/C)O', "
               "'Hydroxypyridine')]\n"
               'False negatives: '
               "[('O=C1NC2=C([C@]3(N)/C(/[C@H](C2)C=C(C3)C)=C\\\\C)C=C1', 'No "
               "hydroxy substituent found on pyridine ring')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 6579,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9850433742147772}