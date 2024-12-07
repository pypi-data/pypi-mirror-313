"""
Classifies: CHEBI:24780 imidazoles
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_imidazoles(smiles: str):
    """
    Determines if a molecule contains an imidazole ring.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains imidazole ring, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # SMARTS patterns for imidazole ring and its variations
    imidazole_patterns = [
        "[nH,n]1c[nH,n]cc1",  # Basic imidazole pattern
        "N1C=NC=C1",  # Alternative representation
        "N1C=CN=C1",  # Alternative representation
        "[nH]1cncc1",  # Another representation
        "n1cncc1",     # N-substituted version
        "N1=CN=CC1",   # Another tautomer
        "N1=CN=C[CH]1", # Another form
        "[nH]1c(*)ncc1", # Substituted version
        "N1=C(*)N=CC1",  # Another substituted form
        "[nH]1cnc(*)c1", # 4-substituted form
        "N1=CNC(*)=C1",  # Another 4-substituted form
        "C1=CN=CN1",     # Another representation
        "[n]1c[n]cc1",   # Aromatic form
        "N1=C([*,H])N=C([*,H])C1([*,H])", # General substituted form
    ]
    
    # Check for presence of imidazole ring
    found = False
    matching_pattern = None
    for pattern in imidazole_patterns:
        pattern_mol = Chem.MolFromSmarts(pattern)
        if pattern_mol and mol.HasSubstructMatch(pattern_mol):
            found = True
            matching_pattern = pattern
            break
            
    if not found:
        return False, "No imidazole ring found"
    
    # Get atoms involved in the imidazole ring
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts(matching_pattern))
    if not matches:
        return False, "No imidazole ring found"
        
    ring_atoms = set(matches[0])
    
    # Check for substituents and their types
    substituents = set()
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                symbol = neighbor.GetSymbol()
                if symbol != 'H':  # Ignore hydrogens
                    substituents.add(symbol)
    
    # Additional check for fused ring systems
    ring_info = mol.GetRingInfo()
    ring_atoms_list = list(ring_atoms)
    is_fused = False
    for ring in ring_info.AtomRings():
        if any(atom_idx in ring_atoms_list for atom_idx in ring) and \
           not all(atom_idx in ring_atoms_list for atom_idx in ring):
            is_fused = True
            break
    
    if is_fused:
        return True, "Fused imidazole ring system"
    elif substituents:
        return True, f"Imidazole with substituents: {', '.join(sorted(substituents))}"
    else:
        return True, "Unsubstituted imidazole"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24780',
                          'name': 'imidazoles',
                          'definition': 'A five-membered organic heterocycle '
                                        'containing two nitrogen atoms at '
                                        'positions 1 and 3, or any of its '
                                        'derivatives; compounds containing an '
                                        'imidazole skeleton.',
                          'parents': ['CHEBI:23677']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.4421052631578947 is too low.\n'
               "True positives: [('N=1C(=C(NC1)C)C(=O)O', 'Imidazole with "
               "substituents: O'), ('OC(=O)C(=O)Cc1c[nH]cn1', 'Imidazole with "
               "substituents: C'), ('OCc1c[nH]cn1', 'Imidazole with "
               "substituents: O'), "
               "('C1=CC=C(C=C1)C2=C(N3C(=O)C(=CC4=CC(=CC=C4)O)SC3=N2)C5=CC=CC=C5', "
               "'Imidazole with substituents: C'), ('ClCc1nccn1Cc1ccccc1', "
               "'Imidazole with substituents: C, Cl'), "
               "('Clc1ccc([C@@H](Cn2ccnc2)OCc2csc3c(Cl)cccc23)c(Cl)c1', "
               "'Imidazole with substituents: C'), "
               "('C(=C(/C(OCC)=O)\\\\C(C)=O)\\\\C=1N(C)C(=CN1)[N+]([O-])=O', "
               "'Imidazole with substituents: C, O'), "
               "('O[N+]([O-])=O.Clc1ccc([C@H](Cn2ccnc2)OCc2csc3c(Cl)cccc23)c(Cl)c1', "
               "'Imidazole with substituents: C'), ('OCCC=1NC=NC1', 'Imidazole "
               "with substituents: C'), "
               "('CN1C=C(N=C1)S(=O)(=O)N2C[C@@H](COC[C@@H]3[C@@H]2CC[C@@H](O3)CC(=O)OC)O', "
               "'Imidazole with substituents: N, C, O'), "
               "('O1[C@@H](N2C=C(N=C2)CC(=O)O)[C@H](O)[C@H](O)[C@H]1CO', "
               "'Imidazole with substituents: C'), "
               "('OC=1C(C=2N(CC3=CC=CC=C3)C=NC2)=CC=CC1', 'Imidazole with "
               "substituents: C'), ('NC(=N)Nc1nc2ccccc2[nH]1', 'Imidazole with "
               "substituents: C'), "
               "('CC1=CN(C=N1)C1=CCC2C3CC=C4C[C@H](CC[C@]4(C)C3CC[C@]12C)NC(=O)C1=CC=C(F)C=C1', "
               "'Imidazole with substituents: C'), "
               "('C/1CC2=C(\\\\C1=N/O)C=CC(=C2)C=3N=C(NC3C=4C=CN=CC4)C5=CC=C(C=C5)OCCN(C)C', "
               "'Imidazole with substituents: C'), "
               "('O1[C@@H]([C@H]([C@H]([C@@H]1N2C(=CN=C2)N)O)O)COP(=O)(O)O', "
               "'Imidazole with substituents: C'), ('O=C(O)C=1NC(C)=NC1', "
               "'Imidazole with substituents: O'), "
               "('C1=CN2C=C(N=C2N=C1)C3=CC(=C(C=C3)Cl)Cl', 'Imidazole with "
               "substituents: C'), ('Cn1cnc(c1)C(O)=O', 'Imidazole with "
               "substituents: C, O'), "
               "('COC1=C(C=CC(=C1)SC)C2=NC3=C(N2)C=NC=C3', 'Imidazole with "
               "substituents: N, C'), "
               "('CC[C@H](N(Cc1ccco1)C(=O)n1ccnc1)C(=O)OCCCC=C', 'Imidazole "
               "with substituents: C'), "
               "('CC(=O)N1CCN(CC1)c1ccc(OC[C@H]2CO[C@](Cn3ccnc3)(O2)c2ccc(Cl)cc2Cl)cc1', "
               "'Imidazole with substituents: C'), "
               "('CC(=O)N1CCN(CC1)c1ccc(OCC2COC(Cn3ccnc3)(O2)c2ccc(Cl)cc2Cl)cc1', "
               "'Imidazole with substituents: C'), ('S1C=2N(C=C(N2)CO)C=C1', "
               "'Imidazole with substituents: C, O'), "
               "('O1[C@@H](N2C(N)=C(N=C2)NC(O)=O)[C@H](O)[C@H](O)[C@H]1CO', "
               "'Imidazole with substituents: C'), "
               "('Clc1ccc(C(Cn2ccnc2)OCC=C)c(Cl)c1', 'Imidazole with "
               "substituents: C'), ('Clc1ccc(CNC(=N)SCCCc2c[nH]cn2)cc1', "
               "'Imidazole with substituents: C'), "
               "('Nc1nccc(n1)-c1c(ncn1C1CCNCC1)-c1ccc(F)cc1', 'Imidazole with "
               "substituents: N, C'), "
               "('COC1=CC=C(C=C1)C2=CN(C3=[N+]2CCCCC3)C4=CC=C(C=C4)Cl', "
               "'Imidazole with substituents: C'), ('CN1C(=NC=C1)C(O)=O', "
               "'Imidazole with substituents: C, O'), "
               "('O=C(OC)/C=C/C=1N=CN(C1CC=C(C)C)C', 'Imidazole with "
               "substituents: C'), ('CC(c1c[nH]cn1)c1cccc(C)c1C', 'Imidazole "
               "with substituents: C'), ('C[C@H](N)c1nc(C)c(O)n1CC(O)=O', "
               "'Imidazole with substituents: N, C'), "
               "('CC1=CC=CC2=NC(=C(N12)NCC3CCCO3)C4=CC(=C(C=C4)O)OC', "
               "'Imidazole with substituents: C'), "
               "('COc1ccc(CN([C@@H](C)c2nc(c[nH]2)-c2ccccc2)C(=O)[C@@H](N)Cc2c(C)cc(cc2C)C(N)=O)cc1C(O)=O', "
               "'Imidazole with substituents: C, N'), "
               "('NCCCC(=O)N[C@@H](Cc1c[nH]cn1)C(O)=O', 'Imidazole with "
               "substituents: C'), "
               "('C(C(=O)C(N1C=CN=C1)OC2=CC=C(C=C2)Cl)(C)(C)C', 'Imidazole "
               "with substituents: C'), ('C=1(N(C(=NC1)C)CC(C)O)[N+]([O-])=O', "
               "'Imidazole with substituents: C, O'), "
               "('CC1=CC(=NO1)NC(=O)CSC2=NC=CN2C3=CC(=CC=C3)OC', 'Imidazole "
               "with substituents: C'), ('Cc1ccc2[nH]cnc2c1', 'Imidazole with "
               "substituents: C'), "
               "('CN1C(=CN=C1NCC2=C(C=CC(=C2)Cl)O)C3=CC=CC=C3', 'Imidazole "
               "with substituents: C'), "
               "('N(=N/[N+]=1C(=C(N2C1C=CC=C2)C)C3=CC=CC=C3)\\\\[N+]=4C(=C(N5C4C=CC=C5)C)C6=CC=CC=C6', "
               "'Imidazole with substituents: C, N')]\n"
               'False positives: '
               "[('C1=CC=C2C(=C1)N=C(S2)NC(=O)COC(=O)CC3=CN4C=CSC4=N3', "
               "'Imidazole with substituents: C'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=3NC=NC3)CC(O)=O', "
               "'Imidazole with substituents: C'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(C)C', "
               "'Imidazole with substituents: C'), "
               "('C1=CC=C2C(=C1)N=C(N2CC(=O)NC3=CC=CC=C3F)C4=CSC=N4', "
               "'Imidazole with substituents: N, C'), "
               "('CCCCC\\\\C=C/CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('CCCCCCN1C2=C(N=C1N3CCN(CC3)C4=CC=CC=C4)N(C(=O)NC2=O)C', "
               "'Imidazole with substituents: N, C, O'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)/C=C/C/C=C/CCCCCCCC)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Imidazole with substituents: N, C'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)C(C)C)C(C)C', "
               "'Imidazole with substituents: C'), "
               "('C[C@@H]1O[C@@H](OCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'Imidazole with substituents: N, C'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1O*)O)*)COP(O[C@@H]2[C@H](O[C@@H](N3C=4N=C(NC(=O)C4N=C3)N)[C@@H]2O)COP(=O)([O-])[O-])(=O)[O-]', "
               "'Imidazole with substituents: N, C, O'), "
               "('SC[C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)NCC(O)=O', 'Imidazole "
               "with substituents: C'), "
               "('S(CC[C@H](NC(=O)[C@H]1NCCC1)C(=O)N[C@@H](CC=2NC=NC2)C(O)=O)C', "
               "'Imidazole with substituents: C'), "
               "('CC(=O)N[C@@H](Cc1cnc[nH]1)C([O-])=O', 'Imidazole with "
               "substituents: C'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC=3NC=NC3', "
               "'Imidazole with substituents: C'), "
               "('P(OP(OP(OC[C@H]1O[C@@H](N2C=3N=CN=C(N)C3N=C2)[C@@H]([C@@H]1O)OP(=O)(OC[C@H]4O[C@H]([C@@H]([C@@H]4O)O)N5C=6N=CN=C(N)C6N=C5)O)(=O)O)(=O)O)(=O)(O)O', "
               "'Imidazole with substituents: N, C'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\CCCCCCCCCCC(O)=O', "
               "'Imidazole with substituents: N, C'), "
               "('C(=C/C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O)=O)\\\\CCCC[C@H](O[C@@H]4O[C@@H](C)[C@@H](C[C@H]4O)OC(C=5C=6C=CC=CC6NC5)=O)C', "
               "'Imidazole with substituents: N, C'), "
               "('C1=CC=C(C=C1)COC(=O)CC2=CN3C=CSC3=N2', 'Imidazole with "
               "substituents: C'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O[C@@H]2O[C@H](COP([O-])([O-])=O)[C@@H](O)[C@H]2O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('S=C1N(C2OC(C(O)C2O)CO)C3=NC=NC(N)=C3N1', 'Imidazole with "
               "substituents: N, C, S'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC=2C=3C(NC2)=CC=CC3', "
               "'Imidazole with substituents: C'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCC([O-])=O', "
               "'Imidazole with substituents: N, C'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OP(O)(O)=O)[C@@H](O)[C@H]1O', "
               "'Imidazole with substituents: C, N'), "
               "('C[C@H](CCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Imidazole with substituents: N, C'), "
               "('C[C@H](CCCCCCCCCCCCCC/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Imidazole with substituents: N, C'), "
               "('Cn1cnc2n(cnc2c1=O)[C@@H]1O[C@H](COP(O)(=O)O[C@@H]2[C@@H](COP(O)(=O)O[C@@H]3[C@@H](COP(O)(=O)O[C@@H]4[C@@H](CO)O[C@H]([C@@H]4O)n4cnc5c(O)ncnc45)O[C@H]([C@@H]3O)n3cnc4c3nc(N)[nH]c4=O)O[C@H]([C@@H]2O)n2ccc(N)nc2=O)[C@@H](OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)n2ccc(=O)[nH]c2=O)[C@H]1O', "
               "'Imidazole with substituents: N, C, O'), "
               "('O1C(O)[C@H](O)[C@H](OC(C)=O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-]', "
               "'Imidazole with substituents: N, C'), "
               "('O=C(O)C(NC(=O)C(N)CCCN=C(N)N)C1OC(N2C3=NC(=NC=C3N=C2)N)C4OCC(C4(C1O)O)O', "
               "'Imidazole with substituents: N, C'), "
               "('O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC=2NC=NC2', "
               "'Imidazole with substituents: C'), ('OC(=O)c1nc2ccccc2[nH]1', "
               "'Imidazole with substituents: C, O'), "
               "('CN(C)S(=O)(=O)C1=CC=C(C=C1)C(=O)NC2=NC3=CC=CC=C3N2', "
               "'Imidazole with substituents: C'), "
               "('SCC(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C1N(C(=O)C(NC(=O)C(N)CCC=O)CC(=O)N)CCC1)CCCCN)C(C)C)C)CC=2NC=NC2)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N)CCC(=O)N)CO)C', "
               "'Imidazole with substituents: C'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CC2=CC=CC=C2', "
               "'Imidazole with substituents: C'), "
               "('CC1=C(C(=O)N(N1C)C2=CC=CC=C2)NCC3=NC4=CC=CC=C4N3', "
               "'Imidazole with substituents: C, N'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: C, N'), "
               "('[H][C@]12[C@H](CC(N)=O)[C@@]3(C)CCC(=O)NC[C@@H](C)OP([O-])(=O)O[C@@H]4[C@@H](COP([O-])([O-])=O)O[C@@H]([C@@H]4O)n4c[n+](c5cc(C)c(C)cc45)[Co-3]456(C[C@H]7O[C@H]([C@H](O)[C@@H]7O)n7cnc8c(N)ncnc78)N1C3=C(C)C1=[N+]4C(=CC3=[N+]5C(=C(C)C4=[N+]6[C@]2(C)[C@@](C)(CC(N)=O)[C@@H]4CCC(N)=O)[C@@](C)(CC(N)=O)[C@@H]3CCC(N)=O)C(C)(C)[C@@H]1CCC(N)=O', "
               "'Imidazole with substituents: N, C, Co'), "
               "('OC1CN(CCC1)C=2N(C3=C(N2)N(C(=O)N(C3=O)CC4=NC=5C(C(=N4)C)=CC=CC5)C)CC#CC', "
               "'Imidazole with substituents: N, C, O'), "
               "('NC(=O)c1ccc[n+](c1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](OP([O-])([O-])=O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O', "
               "'Imidazole with substituents: N, C'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC(O)CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('N1(C2=C(C(=NC=N2)N)N=C1)[C@@H]3O[C@H](COP([O-])(OC(CC[NH3+])=O)=O)[C@H]([C@H]3O)O', "
               "'Imidazole with substituents: N, C'), "
               "('O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)CCCN=C(N)N', "
               "'Imidazole with substituents: C'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)CCCCN', "
               "'Imidazole with substituents: C'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)CC(=O)N', "
               "'Imidazole with substituents: C'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)C[N+](C)(C)C', "
               "'Imidazole with substituents: N, C'), "
               "('C\\\\C=C/CCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('O[N+]([O-])=O.Clc1ccc([C@@H](Cn2ccnc2)OCc2c(Cl)cccc2Cl)c(Cl)c1', "
               "'Imidazole with substituents: C'), "
               "('CC(C)[C@H](NC(=O)[C@@H](N)Cc1c[nH]cn1)C(O)=O', 'Imidazole "
               "with substituents: C'), "
               "('NC=1N=CN=C2C1N=CN2[C@@H]3O[C@H](CO)CC3', 'Imidazole with "
               "substituents: C, N'), "
               "('CC1=C(N2C=CC=CC2=N1)C(C3=CC=CC=C3)(C4=CC=CC=C4)O', "
               "'Imidazole with substituents: C, O'), "
               "('CN(C)c1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(NCCCC[C@H](NC(C)=O)C(O)=O)N2CCOCC2)[C@@H](O)[C@H]1O', "
               "'Imidazole with substituents: C, N'), "
               "('CCCCCCCCCCC(C(O)=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('C[C@@H]1O[C@@H](OCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'Imidazole with substituents: N, C'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)CCC/C=C\\\\C[C@@H]4[C@@H](/C=C/[C@@H](O)CCCCC)[C@@H](C[C@@H]4O)O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Imidazole with substituents: N, C'), "
               "('CC1=CC=C(C=C1)C(=O)CSC2=NC=CN2C3=CC=CC=C3', 'Imidazole with "
               "substituents: C'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: C, N'), "
               "('C[C@@H]1O[C@@H](OCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O', "
               "'Imidazole with substituents: N, C'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('OC(=O)[C@@H](NC(=O)CCCN)CC=1N(C=NC1)C', 'Imidazole with "
               "substituents: C'), "
               "('O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC=2NC=NC2', "
               "'Imidazole with substituents: C'), "
               "('O=C(N[C@@H]([C@H](O)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)CCCN=C(N)N', "
               "'Imidazole with substituents: C'), "
               "('C[C@H](CCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O', "
               "'Imidazole with substituents: N, C'), "
               "('C1([C@@H]([C@H]1C=C(C)C)C(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O)(C)C', "
               "'Imidazole with substituents: C, N'), "
               "('C1(=O)NC(=NC2=C1[N+](=CN2[C@@H]3O[C@H](COP(OP(OP(OC[C@H]4O[C@H]([C@@H]([C@@H]4O*)O)N5C6=C(C(=NC=N6)N)N=C5)(=O)[O-])(=O)[O-])(=O)[O-])[C@@H](O)[C@H]3O)C)N(C)C', "
               "'Imidazole with substituents: C, N, O'), "
               "('O=C(NC(CC1=CC=CC=C1)C(O)=O)C(N)CC=2NC=NC2', 'Imidazole with "
               "substituents: C'), "
               "('O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@](CC3)(C(N5C=6C(N=C5)=CC=CC6)=CC4)C)[H])(CC2)[H])[H])(CC1)C', "
               "'Imidazole with substituents: C'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('C[C@@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c2nc(N)[nH]c3=O)[C@@H](O)[C@H](O)C1=O', "
               "'Imidazole with substituents: N, C, O'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)N[C@@H](CC(=O)N)C(O)=O)C', "
               "'Imidazole with substituents: C'), "
               "('C1(=CC=C(C=C1)CN2C3=C(C(=O)[O-])C=CC=C3N=C2OCC)C=4C=CC=CC4C=5N=NN(N5)[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)C([O-])=O)O)O)O', "
               "'Imidazole with substituents: C'), "
               "('CN1C2=C(C(=O)N(C1=O)C)N(C(=N2)NN=CC3=CC=CS3)CC4=CC=CC=C4', "
               "'Imidazole with substituents: N, C, O'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OP(O)(=O)OP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c(N)ncnc23)[C@@H](O)[C@H]1O', "
               "'Imidazole with substituents: C, N'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(C)C)CC=1NC=NC1', "
               "'Imidazole with substituents: C'), "
               "('C1(=O)NC(=NC2=C1[N+](=CN2[C@@H]3O[C@H](COP(OP(OP(OC[C@H]4O[C@H]([C@@H]([C@@H]4OP(OC[C@H]5O[C@H]([C@@H]([C@@H]5O*)OC)*)(=O)[O-])OC)*)(=O)[O-])(=O)[O-])(=O)[O-])[C@@H](O)[C@H]3O)C)N', "
               "'Imidazole with substituents: C, N, O'), "
               "('CC[C@H](C)[C@@H](C(=O)N[C@@]1(CCCC=CCCC[C@](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC1=O)CC(C)C)CS)CCCNC(=N)N)(C)C(=O)N[C@@H](CC2=CNC=N2)C(=O)N[C@@H](CC3=CNC=N3)C(=O)N[C@@H](CO)C(=O)N[C@@H]([C@@H](C)O)C(=O)N)C)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](CC4=CNC5=CC=CC=C54)NC(=O)CCNC(=O)C', "
               "'Imidazole with substituents: C'), "
               "('C(CN(C)C)N1C2=C(N=C1)N(C)C(N(C2=O)C)=O', 'Imidazole with "
               "substituents: N, C, O'), "
               "('SC[C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)N[C@@H](CC(O)=O)C(O)=O', "
               "'Imidazole with substituents: C'), "
               "('[H+].Cc1ncc(n1CCO)[N+]([O-])=O', 'Imidazole with "
               "substituents: C, O'), "
               "('CC=CC1=CN=C2C(=C1)C(=O)N(C[C@H]([C@H](O2)CN(C)S(=O)(=O)C3=CN(C=N3)C)C)[C@@H](C)CO', "
               "'Imidazole with substituents: C, N, O'), "
               "('FC(F)(F)C=1C=CC(N2C=CN=C2)=NC1', 'Imidazole with "
               "substituents: C'), "
               "('CN1C=C(N=C1)S(=O)(=O)N[C@H]2C=C[C@H](O[C@H]2CO)CC(=O)N3CCN(CC3)C4=CC=CC=C4', "
               "'Imidazole with substituents: N, C, O'), "
               "('CN1C2=CC=CC=C2N=C1C(COC)(C3=CC=CC=C3)N', 'Imidazole with "
               "substituents: N, C'), "
               "('CC1=C(C=C(C=C1)N2C(=O)C(=CNC3=CC4=C(C=C3)NC(=O)N4)C(=N2)C)C', "
               "'Imidazole with substituents: C, O'), "
               "('O[C@@H]1[C@@H](COP([O-])([O-])=O)O[C@H]([C@@H]1O)n1cnc2c(NC(CC([O-])=O)C([O-])=O)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('C1(OC(CC1*)*)COP(O)(=O)OC2C(OC(C2)N3C(NC4=C3N=C(NC4=O)N)=O)*', "
               "'Imidazole with substituents: N, C, O'), "
               "('N[C@@H](Cc1nc(I)[nH]c1I)C(O)=O', 'Imidazole with "
               "substituents: C'), "
               "('[H]C(=O)Nc1c(ncn1[C@@H]1O[C@H](COP([O-])([O-])=O)[C@@H](O)[C@H]1O)C(N)=O', "
               "'Imidazole with substituents: N, C, O'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1OP(OC[C@H]2O[C@H]([C@@H]([C@@H]2O*)O)*)(=O)[O-])O)N3C=4N=C(NC(=O)C4N=C3)N)COP(OP(OP(OC)(=O)[O-])(=O)[O-])(=O)[O-]', "
               "'Imidazole with substituents: N, C, O'), "
               "('COC1=C(C=C(C=C1)C(=O)NC(=CC2=CC=CS2)C3=NC4=CC=CC=C4N3)OC', "
               "'Imidazole with substituents: C, N'), "
               "('CCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('CC1=C2N3[C@H]([C@H](CC(N)=O)[C@@]2(C)CCC([O-])=O)[C@]2(C)[N+]4=C([C@@H](CCC(N)=O)[C@]2(C)CC(N)=O)C(C)=C2[N+]5=C(C=C6[N+](=C1[C@@H](CCC(N)=O)C6(C)C)[Co--]345C[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc3c(N)ncnc13)[C@@H](CCC(N)=O)[C@]2(C)CC(N)=O', "
               "'Imidazole with substituents: C, N'), "
               "('C1CCC(CC1)C(=O)NCCC2=NC3=CC=CC=C3N2CCOC4=C(C=CC(=C4)F)F', "
               "'Imidazole with substituents: C'), "
               "('S(=O)(=O)(N1CC[N+]([O-])(CC1)CC)C2=CC(=C(OCC)C=C2)C=3NC(=O)C=4N(N3)C(=NC4C)CCC', "
               "'Imidazole with substituents: N, C, O'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: C, N'), "
               "('C(CC[C@]([C@@]1([C@]2([C@H](C[C@@]3([C@]4(CCC(C=C4C=C[C@]3([C@@]2(CC1)[H])[H])=O)C)[H])O)C)[H])(C)[H])(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O', "
               "'Imidazole with substituents: N, C'), "
               "('S(C1=C2C(N=C(N1)N)=NC=N2)C3=C([N+]([O-])=O)N=CN3C', "
               "'Imidazole with substituents: C, N, O'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Imidazole with substituents: N, C')]\n"
               "False negatives: [('CC1=NC=NC1CSCCNC(=NC)NC#N', 'No imidazole "
               "ring found'), "
               "('C(OC)(C1=C(C=CC(=C1)C)C2=N[C@@](C(N2)=O)(C(C)C)C)=O', 'No "
               "imidazole ring found'), "
               "('C(O)(C1=C(C=CC(=C1)C)C2=N[C@](C(N2)=O)(C(C)C)C)=O', 'No "
               "imidazole ring found'), "
               "('CC(C)NC(=O)N1CC(=O)N(C1=O)c1cc(Cl)cc(Cl)c1', 'No imidazole "
               "ring found'), "
               "('[C@@]1(C(N=C(N1)C2=C(C=CC=N2)C(=O)O)=O)(C)C(C)C', 'No "
               "imidazole ring found'), "
               "('C(OC)(C1=C(C=CC(=C1)C)C2=N[C@](C(N2)=O)(C(C)C)C)=O', 'No "
               "imidazole ring found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 43,
    'num_false_positives': 100,
    'num_true_negatives': 2622,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.3006993006993007,
    'recall': 0.8958333333333334,
    'f1': 0.450261780104712,
    'accuracy': 0.9620938628158845}