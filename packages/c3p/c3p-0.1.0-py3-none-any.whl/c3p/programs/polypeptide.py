"""
Classifies: CHEBI:15841 polypeptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polypeptide(smiles: str):
    """
    Determines if a molecule is a polypeptide (contains 10 or more amino acid residues).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polypeptide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for peptide bonds (-C(=O)-N-)
    peptide_bond_pattern = Chem.MolFromSmarts('[C](=O)[NH]')
    if peptide_bond_pattern is None:
        return False, "Error creating peptide bond pattern"
    
    matches = mol.GetSubstructMatches(peptide_bond_pattern)
    num_peptide_bonds = len(matches)
    
    # A polypeptide with 10+ amino acids should have at least 9 peptide bonds
    if num_peptide_bonds < 8:  # Lowered threshold to catch edge cases
        return False, f"Only {num_peptide_bonds} peptide bonds found - fewer than required for 10+ amino acids"

    # Calculate molecular weight
    mol_weight = sum([atom.GetMass() for atom in mol.GetAtoms()])
    
    # Most polypeptides with 10+ residues will have MW > 800
    if mol_weight < 800:  # Lowered threshold to catch edge cases
        return False, f"Molecular weight ({mol_weight:.1f}) too low for a 10+ residue polypeptide"

    # Look for characteristic amino acid patterns
    aa_patterns = [
        '[NH2][CH]C(=O)',  # N-terminal amino acid
        'C(=O)[OH]',       # C-terminal acid
        'C(=O)N[CH]C(=O)', # Internal amino acid
        'N[CH](C)C(=O)',   # Alanine-like pattern
        'N[CH](CC)C(=O)',  # Larger side chains
        'N[CH](C(C)C)C(=O)' # Branched side chains
    ]

    aa_matches = 0
    for pattern in aa_patterns:
        pat = Chem.MolFromSmarts(pattern)
        if pat is not None:
            aa_matches += len(mol.GetSubstructMatches(pat))

    # If we have enough peptide bonds and amino acid patterns
    if num_peptide_bonds >= 8 and aa_matches >= 5:
        return True, f"Found {num_peptide_bonds} peptide bonds and {aa_matches} amino acid patterns, MW={mol_weight:.1f}"

    # Additional check for cyclic peptides
    if num_peptide_bonds >= 9 and mol_weight >= 1000:
        return True, f"Found {num_peptide_bonds} peptide bonds and MW={mol_weight:.1f}"

    return False, "Does not match polypeptide characteristics"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15841',
                          'name': 'polypeptide',
                          'definition': 'A peptide containing ten or more '
                                        'amino acid residues.',
                          'parents': ['CHEBI:16670', 'CHEBI:33839']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.4301075268817204 is too low.\n'
               'True positives: '
               "[('S1C[C@]2(NC(=O)[C@@H](NC(=O)CNC([C@H](C2)NC(=O)[C@@H](NC(=O)CNC(=O)CNC(=O)CNC(=O)CNC(=O)[C@@H](NC(=O)CN)CC=3NC=NC3)CC(=O)O)=O)CC(C)C)C(=O)N[C@H](C(=O)N[C@@H]([C@H](O)C)C(NCC(N[C@@H](C1)C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@@H]4C(=O)NCC(=O)N[C@H](C(N[C@]5(C4)C(=O)N[C@H](C(=O)N[C@@H](CC(C)C)C(N[C@@H](CSC5)C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(C)C)CC(=O)O)=O)CC(C)C)=O)[C@H](CC)C)CC=6NC=NC6)CC(=O)N)=O)=O)C(C)C', "
               "'Found 26 peptide bonds and MW=2245.4'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC(=O)NCCCC[C@H]3C(=O)N[C@H](C(N4[C@H](C(N[C@H](C(N[C@H](C(N[C@H]1CC=5C6=C(C=CC=C6)NC5)=O)CC(=O)O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@H]7N(C(=O)[C@@H](NC(=O)C)CC8=CC=C(O)C=C8)CCC7)CCC(=O)N)C(=O)N[C@H](C(=O)N3)CC(C)C)C)=O)CO)=O)CCC4)=O)CC9=CC=C(O)C=C9)CCC(=O)OC', "
               "'Found 13 peptide bonds and MW=1723.1'), "
               "('CC[C@H](C)[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@@H](NC(=O)[C@H](C)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCSC)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCCCN)NC(=O)[C@H](CO)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CO)NC(=O)[C@@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](NC(=O)CNC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CO)NC(=O)[C@@H](N)Cc1c[nH]cn1)[C@H](C)O)[C@H](C)O)C(C)C)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CC(N)=O)C(=O)NCC(=O)NCC(=O)N1CCC[C@H]1C(=O)N[C@@H](CO)C(=O)N[C@@H](CO)C(=O)NCC(=O)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(=O)N[C@@H](CO)C(N)=O', "
               "'Found 34 peptide bonds, terminal COOH and NH2 groups, "
               "MW=3918.4'), "
               "('C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N1[C@H](C(=O)O)CCC1)CC(C)C)=O)CCCCN)=O)CC=2C=CC=CC2)=O)CC3=CNC4=C3C=CC=C4)CC(=O)O)=O)CCCNC(=N)N)=O)CC5=CNC6=C5C=CC=C6)=O)C(C)C)([C@H](CCC(=O)N)NC(=O)[C@H]7N(CCC7)C([C@@H](N)C(CC)C)=O)=O', "
               "'Found 9 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1471.0'), "
               "('S1C(C2NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C3NC(=O)C(CC(=O)C(CC4=CC=CC=C4)NC(C5C(SCC(NC(C(NC(C(NC(C(NC(C(C1)N)=O)C)=O)CO)=O)C(SC3)C)=O)C(NC(CNCCCCC(NC2=O)C(=O)O)C(=O)NC(C(=O)NCC(=O)N6C(C(=O)NC(C(N5)=O)CC7=CC=CC=C7)CCC6)C)=O)C)=O)C)C(O)C(=O)O)CO)C', "
               "'Found 16 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1687.2'), "
               "('O=C1N2[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@@H](CCC(=O)OC)C(N[C@@H]([C@@H](C(NCCCC[C@@H](C(N[C@H]1CC3=CC=C(O)C=C3)=O)NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C)[C@H](O)C)C)[C@H](O)C)CCCNC(=N)N)=O)O)C(=O)N[C@H](C(=O)O)CC4=CC=C(O)C=C4)=O)CC=5C6=C(C=CC=C6)NC5)CC(=O)O)CO)CCC2', "
               "'Found 13 peptide bonds and MW=1580.9'), "
               "('CC[C@H](C)[C@H](NC(=O)[C@@H](NC(=O)[C@H](C)NC(=O)[C@H](CCCCNC(=O)c1ccccc1I)NC(=O)[C@H](CC(O)=O)NC(C)=O)[C@@H](C)O)C(=O)NCC(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(O)=O', "
               "'Found 13 peptide bonds and MW=1539.7'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(C)C)CO)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CO)C)(C)C)(C)C)CCC(=O)N)(C)C)CC(C)C)(C)C)CC(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1593.0'), "
               "('O=C(N1C(C(=O)NC(CO)CC(C)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C2N(C(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CCC(=O)N)C(CC)C)CC(C)C)(C)C)CCC2)CC(C)C)C(CC)C)(C)C', "
               "'Found 9 peptide bonds and MW=1084.7'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)(C)C)CCC(=O)N)(CC)C)C(C)C)(C)C)(CC)C)(C)C', "
               "'Found 17 peptide bonds and MW=1589.0'), "
               "('S1CC2NC(=O)/C(/NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(C(NC(C(CSCC(NC2=O)C(=O)NC(C(=O)O)CO)NC(=O)C(NC(=O)C(NC(C(NC(C3NC(C(NC(C(NC(C(C1)NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)CNC(=O)CNC(=O)C(N)CCCCN)CO)C(C)C)C(CC)C)CC=4N=CNC4)C(SC3)C)C(CC)C)=O)CC=5N=CNC5)=O)CCC(=O)O)=O)=O)CC(=O)N)=O)CCSC)CC(=O)N)=O)CC=6C7=C(C=CC=C7)NC6)=O)CCC(=O)N)CC8=CC=CC=C8)C(C)C)CC9=CC=CC=C9)=C/C', "
               "'Found 26 peptide bonds, terminal COOH and NH2 groups, "
               "MW=2717.9'), "
               "('S1CC(NC(=O)C(NC(=O)C2NC(=O)CNC(=O)C3CCCN3C(C(C(SC2)C)NC(=O)C4NC(=O)C(NC(=O)C(NC(=O)C(NC(C(CSC4)NC(=O)/C(/NC(=O)C(N)C(CC)C)=C/C)=O)C(CC)C)=C)CC(C)C)=O)C(O)C)C(=O)NC(C(=O)NCC(=O)NCC(=O)NCC(NC5C(NC(C(NC(C1)C(=O)NC6C(=O)NC(C(=O)NC(CSC5)C(NC=CSC6)=O)CC7=CC=CC=C7)=O)CC(=O)N)=O)=O)C', "
               "'Found 22 peptide bonds and MW=1967.5'), "
               "('O=C1N2C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CC3=CC=C(O)C=C3)C(NC(C(NC(CC(NCC(NC1CC4=CC=C(O)C=C4)=O)=O)C(=O)NC(C(=O)NC(C(=O)NCC(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N5C(C(=O)O)CCC5)CO)C(CC)C)CC6=CC=CC=C6)C(O)C)CC=7N=CNC7)CC8=CC=CC=C8)CC(C)C)=O)CCCNC(=N)N)=O)CC(=O)O)CC=9C%10=C(C=CC=C%10)NC9)CC=%11C%12=C(C=CC=C%12)NC%11)CCC2', "
               "'Found 17 peptide bonds and MW=2153.4'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N2C(C(=O)NC(CO)CC(C)C)CCC2)(C)C)CC(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CC(=O)N)C(C)C)C(C)C)(C)C', "
               "'Found 9 peptide bonds and MW=1048.7'), "
               "('CC[C@H](C)[C@H](NC(=O)[C@@H](NC(=O)[C@H](C)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)[C@H](CC(N)=O)NC(=O)[C@H](CO)NC(=O)CNC(=O)[C@@H](NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](C)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCCN)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@@H](NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)CNC(=O)[C@H](CO)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](C)NC(=O)[C@@H](N)CC(O)=O)C(C)C)C(C)C)C(C)C)[C@@H](C)CC)C(=O)NCC(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CCSC)C(=O)N[C@@H](C(C)C)C(=O)NCC(=O)NCC(=O)N[C@@H](C(C)C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H]([C@@H](C)CC)C(=O)N[C@@H](C)C(O)=O', "
               "'Found 41 peptide bonds, terminal COOH and NH2 groups, "
               "MW=4200.6'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(C)C)CO)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CO)C)CC(C)C)(C)C)CCC(=O)N)(CC)C)C(C)C)(C)C)(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1593.0'), "
               "('O=C1N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](CO)C(N[C@@H](C(N[C@H](C(NC(CC(O[C@@H]([C@@H]1NC(=O)C(NC(=O)[C@H](NC(=O)CC(O)CCCCCCC)CC(C)C)CC(=O)O)C)=O)C(=O)O)=O)[C@H](CC)C)=O)CC(C)C)=O)CC(C)C)CO)CC(C)C)CC(C)C', "
               "'Found 11 peptide bonds and MW=1242.8'), "
               "('S(=O)(=O)(O)O.O=C1NCCC(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CCCCC(CC)C)CCN)C(O)C)CCN)C(=O)NC(C(=O)NC(C(=O)NC(C(NC(C(NC(C(NC1C(O)C)=O)CCN)=O)CCN)=O)CC(C)C)CC2=CC=CC=C2)CCN', "
               "'Found 11 peptide bonds and MW=1200.8'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)(CC)C)CCC(=O)N)(CC)C)C(C)C)(C)C)(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1589.0'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC2=CC=C(O)C=C2)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CO)C)(C)C)(C)C)CCC(=O)N)(C)C)C(C)C)(C)C)CC(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1645.0'), "
               "('CC[C@H](C)[C@H](NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CC1=CC=CC=C1)NC(=O)[C@H](CC(O)=O)NC(=O)CNC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CC(N)=O)NC(=O)[C@H](CC1=CNC=N1)NC(=O)[C@H](CO)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@@H]1CCCN1C(=O)[C@H](CCCCN)NC(=O)[C@@H]1CCCN1C(=O)[C@@H](NC(=O)CNC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]1CSSC[C@@H]2NC(=O)[C@@H](NC(=O)[C@H](CC(N)=O)NC(=O)[C@H](CO)NC(=O)CNC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CSSC[C@H](NC(=O)[C@H](CCCCN)NC(=O)[C@H](CC(N)=O)NC(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)CNC2=O)C(=O)N[C@@H]([C@@H](C)CC)C(=O)N[C@@H](CC(C)C)C(=O)NCC(=O)N[C@@H](CO)C(=O)N[C@@H](CC(O)=O)C(=O)NCC(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H](CCC(N)=O)C(=O)N1)NC(=O)[C@H](CC(C)C)NC(=O)[C@@H]1CSSC[C@H](NC(=O)[C@H](CC(O)=O)NC(=O)[C@@H](NC(=O)[C@H](CC2=CC=C(O)C=C2)NC(=O)[C@@H](NC(=O)[C@@H](N)C(C)C)C(C)C)[C@@H](C)O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CO)C(=O)NCC(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H](CC(C)C)C(=O)N1)C(C)C)C(C)C)[C@@H](C)O)[C@@H](C)O)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CCC(N)=O)C(O)=O', "
               "'Found 61 peptide bonds, terminal COOH and NH2 groups, "
               "MW=6520.0'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC2=CC=CC=C2)CCC(=O)N)CCC(=O)N)(C)C)(C)C)C(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)C)(C)C)C)(C)C)C)CCC(=O)N)(C)C)C(CC)C)(C)C)(C)C)(C)C', "
               "'Found 19 peptide bonds and MW=1775.1'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)(C)C)CCC(=O)N)(CC)C)C(C)C)(C)C)(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1577.0'), "
               "('SCC(NC(=O)C(NC(=O)C(N)C(O)C)C)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C=O)CO)CO)CCC(=O)O)CO)CC(C)C)C(CC)C)CO)C(C)C)CC(C)C)C(O)C)CCCCN)CC1=CC=C(O)C=C1)C)C)C(O)C)CCC(=O)N)CCC(=O)N)C(O)C)C)C(O)C', "
               "'Found 22 peptide bonds, terminal COOH and NH2 groups, "
               "MW=2189.3'), "
               "('S1CC(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)CN)CC(=O)O)CC(C)C)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(NC(C(NC(C(NC(C1)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)C(=O)NC2C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(O)C)C(NC(C(NC(CNC(CSC2)C(=O)CC(C(=O)O)CC(C)C)CC(C)C)=O)CC(C)C)=O)=C)CC3=CC=CC=C3)C)CC4=CC=CC=C4)CCCCN)CC(=O)O)=O)CC(C)C)=O)CC(C)C)=O)CC(C)C)=C)C)=C', "
               "'Found 21 peptide bonds and MW=2213.5'), "
               "('O=C(O)[C@@H](NC(=C)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC[C@H](NC[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)CNC(=O)[C@H](NC(=O)CNC(=O)CCCC[C@H](CC)C)CCN)CO)CC=1C2=C(C=CC=C2)NC1)CC)CCN)CCN)[C@H](CC)C)CCC(=O)O)[C@H](CC)C)[C@H](CC)C)CO', "
               "'Found 10 peptide bonds and MW=1334.9'), "
               "('C([C@@H](N)CC=1C=CC=CC1)(=O)NCC(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CCC(=O)N)CC(=O)N)C)=O)CC(C)C)=O)CCCCN)CCCNC(=N)N)=O)C)CO)CCCCN)CCCNC(=N)N)C)[C@@H](C)O)CC=2C=CC=CC2', "
               "'Found 16 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1679.0'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N2C(C(=O)NC(CO)CC(C)C)CCC2)(C)C)CC(C)C)C(CC)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CC(=O)N)C(CC)C)CC(C)C)(C)C', "
               "'Found 9 peptide bonds and MW=1072.7'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC2=CC=CC=C2)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)CO)C)(CC)C)(CC)C)CCC(=O)N)(C)C)C(C)C)(C)C)CC(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1653.1'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(C)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)CC(C)C)(CC)C)CCC(=O)N)(C)C)CC(C)C)(C)C)(CC)C)(C)C', "
               "'Found 17 peptide bonds and MW=1601.0'), "
               "('S(CCC(N)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NCC(=O)NCC(=O)O)C(C)C)C(C)C)C(C)C)C)CC(C)C)CC(=O)O)CCCCN)CC=1N=CNC1)CO)CC(C)C)CC2=CC=C(O)C=C2)CC(=O)N)CC3=CC=CC=C3)CCC(=O)N)CCCCN)C', "
               "'Found 17 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1861.2'), "
               "('O=C(O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CC(O)CCCCCCC)CC(=O)N)C(C)C)CC1=CC=CC=C1)CC(=O)N)CC(=O)N)CCCCN)C(O)C)CC=2C3=C(C=CC=C3)NC2)C(CC)C', "
               "'Found 10 peptide bonds and MW=1262.8'), "
               "('S1C(NC(=O)[C@H]2N(C(=O)CNC([C@H](C1)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)C)CO)=O)CCC2)(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC3C(=O)NCC(=O)NCC(NC(SC3)C(=O)N[C@H](C(=O)O)CCCN=C(N)N)=O)CO)CC=4NC=NC4)CO', "
               "'Found 12 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1212.8'), "
               "('S1CC(NC(=O)C(NC(=O)C2NC(=O)CNC(=O)C3CC(O)CN3C(C(C(SC2)C)NC(=O)C4NC(=O)C(NC(=O)C(NC(=O)C(NC(C(CSC4)NC(=O)/C(/NC(=O)C(N)C(CC)C)=C/C)=O)C(CC)C)=C)CC(C)C)=O)C(O)C)C(=O)NC(C(=O)NCC(=O)NCC(=O)NCC(NC5C(NC(C(NC(C1)C(=O)NC6C(=O)NC(C(=O)NC(CSC5)C(NC=CSC6)=O)CC7=CC=CC=C7)=O)CC(=O)N)=O)=O)C', "
               "'Found 22 peptide bonds and MW=1983.5'), "
               "('CC[C@H](C)[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@@H](NC(=O)[C@H](C)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCSC)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCCCN)NC(=O)[C@H](CO)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CO)NC(=O)[C@@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](NC(=O)CNC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@@H](N)Cc1c[nH]cn1)[C@@H](C)O)[C@@H](C)O)C(C)C)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CC(N)=O)C(=O)NCC(=O)NCC(=O)N1CCC[C@H]1C(=O)N[C@@H](CO)C(=O)N[C@@H](CO)C(=O)NCC(=O)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(=O)N[C@@H](CO)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(N)=O', "
               "'Found 40 peptide bonds, terminal COOH and NH2 groups, "
               "MW=4508.8'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)NCC(=O)NCC(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)O)CC2=CC=C(O)C=C2)CCNC(=N)N)C(C)C)[C@@H](CC)C)CC3=CC=CC=C3)CC4=CC=C(O)C=C4)CCC(=O)NCC(=O)NCC(N[C@H](C(NCC(NC(C(NC1[C@@H](CC)C)=O)CCCCCN)=O)=O)C(C)C)=O)C(CC)C', "
               "'Found 19 peptide bonds and MW=1747.1'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N2[C@H](C(=O)O)CCC2)CCCCN)[C@H](CC)C)C(C)C)CC(=O)N)CO)CC=3NC=NC3)C(C)C)CC=4C5=C(C=CC=C5)NC4)CCC(=O)NCC(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H]1C(C)C)=O)CC(C)C)=O)CCC(=O)N)=O)CO)=O)CCCNC(=N)N)CC6=CC=C(O)C=C6', "
               "'Found 17 peptide bonds and MW=1907.2'), "
               "('CCCC[C@H](NC(=O)[C@H](CO)NC(=O)[C@H](CC1=CC=C(O)C=C1)NC(=O)[C@H](CO)NC(C)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CC1=CNC=N1)C(=O)N[C@H](CC1=CC=CC=C1)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@@H](CC1=CNC2=C1C=CC=C2)C(=O)NCC(=O)N[C@@H](CCCCN)C(=O)N1CCC[C@H]1C(=O)N[C@@H](C(C)C)C(N)=O', "
               "'Found 12 peptide bonds and MW=1535.0'), "
               "('O=C(O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCC)CC(C)C)CCC(=O)N)[C@H](O)C)C(C)C)CC(C)C)CO)CC(C)C)CO)[C@H](CC)C', "
               "'Found 9 peptide bonds and MW=1044.6'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC(C)C)CCC(=O)N)(CC)C)(C)C)CC(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C)(C)C)C)(C)C)(CC)C)CCC(=O)N)C(C)C)C(C)C)(C)C)CC(C)C)(C)C', "
               "'Found 17 peptide bonds and MW=1601.0')]\n"
               'False positives: '
               "[('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H]8O)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C(=O)N/C(/C=3OC=C(N3)C(=O)NC(C(=O)N[C@@H](C(O)(C)C)C(NC(C4=NC(C(NC(C(NC(C5=NC(C6=C2C=CC(=N6)C(=O)NC(C(=O)N[C@H](C(=O)N)C)=C)=CO5)=C)=O)=C)=O)=C(O4)C)=C)=O)=C)=C\\\\C)[C@H](O)C', "
               "'Found 9 peptide bonds and MW=1082.7'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N2[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N3[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(=O)N)CCC(=O)O)CC(C)C)CCCNC(=N)N)CCCNC(=N)N)CO)CC(C)C)C(C)C)CCC3)CC=4NC=NC4)CCC(=O)O)CCC(=O)O)CO)CC(=O)N)CCC(=O)N)CCC2)CC(NCC(N[C@H]1[C@H](O)C)=O)=O)[C@H](CC)C', "
               "'Found 18 peptide bonds and MW=2119.2'), "
               "('S1[C@H]([C@H]2NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@H]3NC(=O)[C@@H](NC(=O)[C@H]([C@H](CC)C)NC([C@H]4[C@@H](SC[C@H](NC([C@H](NC([C@@H](NC([C@@H](NC([C@H](C1)NC(=O)[C@@H]([N+](C)(C)C)CCC(=O)O)=O)C)=O)CO)=O)[C@@H](SC3)C)=O)C(N[C@@H](CNCCCC[C@H](NC2=O)C(=O)O)C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(N4)=O)C(C)C)[C@H](CC)C)CC5=CC=CC=C5)=O)C)=O)C(C)C)[C@@H](O)C(=O)O)[C@H](O)C)C', "
               "'Found 19 peptide bonds and MW=1883.3'), "
               "('O=NN(O)CCC[C@H]1NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCCCCCCCC)[C@@H](O)C(=O)O)CO)CO)CCCNC(=O)[C@@H](CCCN(O)N=O)NC(CNC([C@@H](NC1=O)CCCCN)=O)=O', "
               "'Found 9 peptide bonds and MW=1024.6'), "
               "('O=C(NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(C)C)CO)CC(C)C)CC1=CC=C(O)C=C1)CCCCN)C(C)C)C(C)C)CCCCN)C(C)C)C(C)C)C(CC)C)CCCN)CC(C)C)/C(/NC(=O)C(O)C(CC)C)=C\\\\C', "
               "'Found 13 peptide bonds and MW=1429.0'), "
               "('O=C1NC(C(=O)NC(C(=O)NCC(=O)NCCC(=O)NC(CCCCCCCC(O)CCCCCC)C(NC(C(NC(C(NC(C(NC(C(NC1C(O)C)=O)CC(O)C(=O)N)=O)C)=O)CC(=O)N)=O)CC(=O)N)=O)CCC(O)CCCCCCCCCC)C(O)C', "
               "'Found 10 peptide bonds and MW=1190.7'), "
               "('O=C1O[C@H]([C@H](NC(=O)/C=C/C2=C(C=CC=C2)[C@@H](O)[C@@H](O)/C=C/C)C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](CO)C(N[C@@H](C(N[C@@H](C(N[C@@H](C(N[C@H](C(N[C@@H]1CC(C)C)=O)C(C)C)=O)C3=CC=C(O)C=C3)=O)CO)=O)[C@H](O)C)=O)CC4=CC=CC=C4)CC(C)C)CO)C', "
               "'Found 10 peptide bonds and MW=1224.8'), "
               "('[NH2+]([C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(C[C@H](C([O-])=O)[C@H](CC)C)=O)CCCC[NH3+])=O)[C@@H](C)CC)=O)CCCNC(N)=[NH2+])=O)CCCC[NH3+])=O)C(C)C)=O)CC(C)C)=O)C)=O)CC(C)C)=O)CCCNC(N)=[NH2+])=O)CC(C)C)=O)CCCC[NH3+])=O)CCCC[NH3+])=O)C)=O)CCCC[NH3+])=O)CO)=O)CCCC[NH3+])=O)C(C)C)=O)C(C)C)=O)[C@@H](C)CC)CCCC[NH3+])=O)[C@H](CC)C)=O)CCCC[NH3+])=O)CO)=O)CCCC[NH3+])=O)C(C)O)C(=O)CCCC[C@@H]1[C@]2([C@@](CS1)(NC(N2)=O)[H])[H]', "
               "'Found 26 peptide bonds and MW=2934.0'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]%14O[C@@H]([C@@H](O)[C@H](O)[C@@H]%14O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO', "
               "'Found 9 peptide bonds and MW=3179.4'), "
               "('O=C1N2C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CC(=O)N)C(NC(C(NC(CC(NCC(NC1CC3=CC=C(O)C=C3)=O)=O)C(=O)NC(C(=O)NC(C(=O)NCC(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NCC(=O)O)C(CC)C)CC4=CC=CC=C4)C(O)C)CC5=CC=C(O)C=C5)CC6=CC=CC=C6)C(CC)C)=O)CCCNC(=N)N)=O)CC(=O)O)CC=7C8=C(C=CC=C8)NC7)CC9=CC=CC=C9)CCC2', "
               "'Found 17 peptide bonds and MW=1975.3'), "
               "('O=C1NCCCC[C@@H]2NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C)[C@H](O)C)C)[C@H](OC(C[C@H]3C(N[C@@H](C(N[C@H](C(N[C@@H]([C@@H]1O)C(=O)N[C@H](C(=O)O)CC4=CC=C(O)C=C4)=O)CCC(=O)OC[C@H](NC([C@H]5N(C([C@@H](NC2=O)CC6=CC=C(O)C=C6)=O)CCC5)=O)C(=O)N3)=O)CC=7C8=C(C=CC=C8)NC7)=O)=O)C)CCCNC(=N)N', "
               "'Found 13 peptide bonds and MW=1536.9'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO)[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3317.4'), "
               "('BrC1=CC=C([C@@H]([C@@H]2NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]3NC(=O)[C@@H](NC(=O)C[C@H](NC(=O)[C@@H](NC([C@@H](NC([C@@H](NC([C@@H](NC(C[C@@H](C[C@H](NC([C@H](CNC2=O)O)=O)C(=O)O)O)=O)CC4=CN(C3)C=[N+]4[C@@H]5O[C@@H]([C@H](O)[C@@H]([C@H]5O)O)CO)=O)[C@@H](O)C)=O)CO)=O)CC6=CC=CC=C6)[C@@H](O)/C=C(/C=C/C7=CC=CC=C7)\\\\C)CO)CC(=O)N)[C@@H](O)C(=O)N)C)C=C1', "
               "'Found 12 peptide bonds and MW=1664.8'), "
               "('ClCC(O)C1NC(=O)C(NC(=O)/C(/NC(=O)C(NC(=O)C(NC(=O)C(NC(C(NC(C(NC(C(COC1=O)NC(=O)CC(O)C(O)CCCCCCCCCC)=O)CCN)=O)CCN)=O)CCO)CCCN)C(O)C)=C/C)C(O)C(=O)O', "
               "'Found 9 peptide bonds and MW=1108.1'), "
               "('[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O)O)NC(C)=O)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO[C@]6(O[C@@]([C@@H]([C@@H](CO)O)O)([C@H](NC(=O)C)[C@@H](O)C6)[H])C([O-])=O)O)O)O)O)NC(C)=O)O[C@@H]7[C@@H]([C@@H](O[C@@H]([C@H]7O)CO[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O[C@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O)O)O)NC(=O)C)O)O)O[C@H]%11[C@@H]([C@H]([C@@H]([C@H](O%11)CO)O[C@H]%12[C@@H]([C@H]([C@H]([C@H](O%12)CO)O)O[C@]%13(O[C@@]([C@@H]([C@@H](CO)O)O)([C@H](NC(=O)C)[C@@H](O)C%13)[H])C([O-])=O)O)O)NC(=O)C)O[C@H]%14[C@@H]([C@H]([C@@H](O[C@@H]%14CO)O[C@H]%15[C@@H]([C@H]([C@@H](O[C@@H]%15CO)NC(C[C@@H](C(=O)*)N*)=O)NC(C)=O)O)NC(C)=O)O)O', "
               "'Found 9 peptide bonds and MW=2861.3'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)O)[C@H]1O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]7NC(=O)C)CO)CO)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O[C@@H]%17O[C@H]([C@@H](O)[C@@H](O)[C@@H]%17O)C)CO[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 9 peptide bonds and MW=3299.5'), "
               "('O=C(N1[C@H](C(=O)N[C@H](C(=O)NC([C@@H](O)C(=O)NCCC(=O)N[C@H](C(=O)NC(C(=O)NCCC(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)N[C@H](C(=O)NCCC(=O)NCCO)CC(C)C)(C)C)(C)C)CC(C)C)(C)C)CC(C)C)(C)C)C)CCC1)[C@](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@@H](NC(=O)[C@H]2N(C(=O)C(NC(=O)C)(C)C)CCC2)C)(C)C)(C)C)CC3=CC=CC=C3)(CC)C', "
               "'Found 18 peptide bonds and MW=1713.1'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H]%10NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O)[C@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H]%13NC(=O)C)CO)CO)[C@@H]%16O[C@@H]([C@@H](O)[C@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('C(N[C@@H]1C(N[C@@H](C(N[C@@H](CCCCN)C(N[C@H](C(N[C@H](C(NCC(N[C@@H](C(N[C@H](C(N2[C@H](C(NC1C)=O)C[C@H](C2)C)=O)C(C)C)=O)C(C)C(=O)O)=O)=O)CC(O)=O)=O)C(C(O)=O)O)=O)=O)C(C)C)=O)([C@@H](NC(/C=C/C=C\\\\CCC(C)C)=O)C(C)C(=O)O)=O', "
               "'Found 10 peptide bonds and MW=1160.7'), "
               "('S1C=CNC(=O)[C@@H](NC([C@@H](NC([C@H](C1)NC(=O)[C@H](NC(=O)/C(/NC(=O)[C@@H](NC(=O)CNC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)/C(/NC(=O)[C@@H]2N(C(=O)/C(/NC(=O)[C@H](NC(=O)[C@@H]3N(C(=O)/C(/NC(=O)[C@@H]([N+]([O-])(C)C)C)=C/C)CCC3)C)=C/C)CCC2)=C/C)C)C)CCC(=O)N)CC4=CC=CC=C4)C(C)C)[C@@H](CC)C)CCC(=O)N)CO)=C/C)[C@@H](CC)C)=O)CC(C)C)=O)C(C)C', "
               "'Found 19 peptide bonds and MW=1933.3'), "
               "('C(C(=O)N)[C@@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@@H](CC(=O)N)C(=O)N[C@H](C(N[C@H](C(N[C@@H](CC(=O)N)C(N[C@H](C(=O)N1[C@@H](CCC1)C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N2[C@H](C(=O)NCC(NCCN(CCNC(CCC(N)=O)=O)C(CCCCS(=O)CCO[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@@H]([C@H]([C@@H](O4)C)O)O)O)O)=O)=O)CCC2)=O)CO)=O)CC5=CC=C(C=C5)O)=O)C)CCCNC(N)=N)=O)=O)CC6=CC=C(C=C6)O)=O)CO)=O)CC=7N=CNC7)C(C)C)=O)C(C)C)=O)CCC(=O)N)=O)CC=8C=CC=CC8)=O)CC(C)C)=O)N', "
               "'Found 17 peptide bonds and MW=2547.6'), "
               "('[O-]S([O-])(=O)=O.[O-]S([O-])(=O)=O.[O-]S([O-])(=O)=O.[O-]S([O-])(=O)=O.[O-]S([O-])(=O)=O.CC(C)CCCCC(=O)N[C@@H](CC[NH3+])C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CC[NH3+])C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CC[NH3+])NC(=O)[C@H](CC[NH3+])NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CC[NH3+])NC1=O)[C@@H](C)O.CC(C)CCCCC(=O)N[C@@H](CC[NH3+])C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](CC[NH3+])C(=O)N[C@H]1CCNC(=O)[C@@H](NC(=O)[C@H](CC[NH3+])NC(=O)[C@H](CC[NH3+])NC(=O)[C@H](CC(C)C)NC(=O)[C@@H](CC(C)C)NC(=O)[C@H](CC[NH3+])NC1=O)[C@@H](C)O', "
               "'Found 22 peptide bonds and MW=2593.7'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O)CO[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3317.4'), "
               "('O=C1N2[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@@H](O)C(=O)N[C@@H](C(=O)N[C@H]([C@@H](O)C(C)C)C(N[C@@H]([C@@H](C(N[C@H](C(N[C@H](C(NCC(N[C@H]1[C@@H](O)C3=CC=CC=C3)=O)=O)CC(=O)O)=O)C)=O)NC(=O)/C=C/C4=NC=CC=C4/C=C\\\\C)C)=O)CC(C)C)CC=5C6=C(C=CC=C6)NC5)[C@@H](O)C7=CC=C(OC)C=C7)CCC2', "
               "'Found 11 peptide bonds and MW=1376.9'), "
               "('S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO)O)[C@H]6O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12NC(=O)C)CO)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16NC(=O)C)CO)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O', "
               "'Found 10 peptide bonds and MW=3309.5'), "
               "('O=C(NC(C(=O)N[C@@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)NCCC(=O)NC(CNCCO)C)CC(C)C)(C)C)CC(C)C)CC(CCCCCC)C)(C)C)C(NC(=O)[C@@H](NC(=O)[C@H]1N(C(=O)CCC)CCC1)CC(CC(O)CC(=O)CC)C)(C)C', "
               "'Found 9 peptide bonds and MW=1118.8'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('O=C/1NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)O[C@H]([C@@H](C(NC(C(NC(C(N\\\\C1=C/C)=O)C)=O)CO)=O)NC(=O)/C(/NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C2N(C(=O)/C(/NC(=O)CC(O)CCCCCCCCC)=C/C)CCC2)C(C)C)CC(C)C)C)C)CC(C)C)C(C)C)C)C)C(C)C)C)C)=C/C)C)CC3=CC=C(O)C=C3)CCN)CCN)C', "
               "'Found 21 peptide bonds and MW=2017.3'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO[C@@H]%18O[C@@H]([C@@H](O[C@@H]%19O[C@@H]([C@H](O)[C@H](O[C@@H]%20O[C@@H]([C@@H](O[C@@H]%21O[C@@H]([C@H](O)[C@H](O[C@]%22(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%22)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%21O)CO)[C@H](O)[C@H]%20NC(=O)C)CO)[C@H]%19O)CO)[C@H](O)[C@H]%18NC(=O)C)CO)CO', "
               "'Found 12 peptide bonds and MW=4137.8'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O)[C@H]%17NC(=O)C)CO[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 11 peptide bonds and MW=3491.5'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O[C@]%19(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%19)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%20O[C@@H]([C@@H](O[C@@H]%21O[C@@H]([C@H](O)[C@H](O[C@]%22(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%22)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%21O)CO)[C@H](O)[C@H]%20NC(=O)C)CO', "
               "'Found 12 peptide bonds and MW=4137.8'), "
               "('C[C@H](O)[C@@H]1NC(=O)[C@@H]2Cc3c[n+](C[C@@H](NC(=O)[C@H](CO)NC(=O)C[C@H](NC(=O)[C@H](Cc4ccccc4)NC(=O)[C@H](CO)NC1=O)[C@@H](O)\\\\C=C(C)\\\\C=C\\\\c1ccccc1)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H]([C@@H](O)C(N)=O)C(=O)N[C@@H]([C@@H](C)c1ccc(Br)cc1)C(=O)NC[C@@H](O)C(=O)N[C@@H](CCCC(=O)N2)C([O-])=O)cn3[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O', "
               "'Found 12 peptide bonds and MW=1648.8'), "
               "('C[C@@H](O)[C@H](NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CC[C@H](CN)O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)[C@H](Cc1cccc(C)c1)NC(=O)CNC(=O)[C@H](C)NC(=O)[C@@H](NC(=O)CN)C1CCCCC1)C(O)=O', "
               "'Found 13 peptide bonds and MW=1576.9'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]%10CO[C@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O[C@H]%19O[C@@H]([C@H](O)[C@H](O)[C@H]%19O)C)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3589.6'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7NC(=O)C)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO', "
               "'Found 9 peptide bonds and MW=2875.3'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H]2N(C(=O)CCC)CCC2)C)C(C)C)CC(C)C)[C@@H](CC)C)C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(NCCC(N3[C@@H](C(N[C@H]1C(C)C)=O)CCC3)=O)=O)C)C(C)C)CC(C)C)C(C)C)C', "
               "'Found 11 peptide bonds and MW=1202.8'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CCCCCCC(CC)C)CC=2C3=C(C=CC=C3)NC2)CCC(=O)O)[C@@H](O)C(=O)N)C(=O)N(CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CCCCN)C(N[C@H](C(NCC(N[C@@H](C(N[C@H](C(N[C@H]1C(C)C)=O)[C@@H](CC(=O)O)C)=O)CC(=O)N)=O)=O)[C@@H](OC)C(=O)O)=O)CC(=O)O)C)C)C', "
               "'Found 12 peptide bonds and MW=1546.9'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC(=O)NCCCC[C@@H]3NC(=O)[C@H](CC4=CC=CC=C4)NC([C@H]([C@H](OC(C[C@H]5C(N[C@H](C(N[C@H]1CCC(=O)OC[C@H](NC(=O)[C@H]6N(C(=O)[C@@H](CC7=CC=C(O)C=C7)NC3=O)CCC6)C(=O)N5)=O)CC=8C9=C(C=CC=C9)NC8)=O)=O)C)NC(=O)CNC(=O)CNC(=O)[C@@H](NC(=O)C)CC%10=CC=C(O)C=C%10)=O', "
               "'Found 14 peptide bonds and MW=1629.0'), "
               "('O=C1OC2=CC=C(CC(NC(=O)C(NC(=O)C(NC(=O)CCCCCCCCCCCCCC(C)C)CCC(=O)O)CCCN)C(=O)NC(C(=O)NC(C(=O)NC(C(N3C(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CCC(=O)N)=O)CCC3)=O)C)CCC(=O)O)C(O)C)C=C2', "
               "'Found 9 peptide bonds and MW=1348.9'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]9[C@H](O)[C@H](O[C@@H](O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%11CO[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)O)[C@H]9O)CO[C@H]%13O[C@@H]([C@@H](O)[C@H](O)[C@@H]%13O[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@@H]%18O[C@@H]([C@@H](O[C@@H]%19O[C@@H]([C@H](O)[C@H](O)[C@H]%19O)CO)[C@H](O)[C@H]%18NC(=O)C)CO)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO)CO[C@@H]%20O[C@@H]([C@@H](O[C@@H]%21O[C@@H]([C@H](O)[C@H](O[C@@H]%22O[C@@H]([C@@H](O[C@@H]%23O[C@@H]([C@H](O)[C@H](O[C@@H]%24O[C@@H]([C@@H](O[C@@H]%25O[C@@H]([C@H](O)[C@H](O[C@]%26(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%26)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%25O)CO)[C@H](O[C@@H]%27O[C@H]([C@@H](O)[C@@H](O)[C@@H]%27O)C)[C@H]%24NC(=O)C)CO)[C@H]%23O)CO)[C@H](O[C@@H]%28O[C@H]([C@@H](O)[C@@H](O)[C@@H]%28O)C)[C@H]%22NC(=O)C)CO)[C@H]%21O)CO)[C@H](O)[C@H]%20NC(=O)C)CO)[C@@H]%29O[C@@H]([C@@H](O[C@@H]%30O[C@@H]([C@H](O)[C@H](O[C@@H]%31O[C@@H]([C@@H](O[C@@H]%32O[C@@H]([C@H](O)[C@H](O[C@@H]%33O[C@@H]([C@@H](O[C@@H]%34O[C@@H]([C@H](O)[C@H](O)[C@H]%34O)CO)[C@H](O[C@@H]%35O[C@H]([C@@H](O)[C@@H](O)[C@@H]%35O)C)[C@H]%33NC(=O)C)CO)[C@H]%32O)CO)[C@H](O[C@@H]%36O[C@H]([C@@H](O)[C@@H](O)[C@@H]%36O)C)[C@H]%31NC(=O)C)CO)[C@H]%30O)CO)[C@H](O[C@@H]%37O[C@H]([C@@H](O)[C@@H](O)[C@@H]%37O)C)[C@H]%29NC(=O)C)CO', "
               "'Found 16 peptide bonds and MW=6322.8'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@@H](O)[C@@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO)[C@@H]5O)CO)[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3317.4'), "
               "('S1C(=NC(=C1)C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)NCCCC[C@@H]2NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC([C@H](NC([C@@H](NC([C@H](NC2=O)CCCN)=O)C(C)C)=O)CC3=CC=CC=C3)=O)CC=4NC=NC4)CC(=O)O)CC(=O)N)C(C)C)CCC(=O)O)CC(C)C)C(=O)[C@H](CC)C', "
               "'Found 11 peptide bonds and MW=1296.9'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('O=C/1O[C@@H](C(NC(=O)[C@@H](NC(=O)C2OC2CCC)CO)C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C3=CC=C(O)C=C3)C(N[C@H](C(NCC(N[C@@H](C(N[C@H](C(N\\\\C1=C\\\\C=4C5=C(C=CC=C5)NC4)=O)C(CC(=O)O)C)=O)C(O)C(=O)N)=O)=O)CC(=O)O)=O)CC(=O)O)CC(=O)O)CC=6C7=C(C=CC=C7)NC6)C', "
               "'Found 11 peptide bonds and MW=1416.8'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CCCCCCC(CC)C)CC=2C3=C(C=CC=C3)NC2)CCC(=O)O)C(O)C(=O)O)C(=O)N(CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CCCCN)C(N[C@H](C(NCC(N[C@@H](C(NC(C(N[C@H]1C(CC)C)=O)CCC(=O)O)=O)CC(=O)N)=O)=O)CC(=O)O)=O)CC(=O)O)C)C)C', "
               "'Found 12 peptide bonds and MW=1520.9'), "
               "('O=C1OCC(O)CC(NC(=O)C(NC(=O)C(NC(=O)[C@H]2NCCC2)CCC(=O)N)CC3=CC=C(O)C=C3)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(NC(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CO)=O)CCCCN)=O)CC5=CC=C(O)C=C5)C(O)C)CCC(=O)O)C', "
               "'Found 11 peptide bonds and MW=1376.8'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@@H](O)[C@@H](O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%10NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)[C@@H]5O)CO)[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('S(=O)(CC[C@@H]1NC(=O)[C@H]2NC(=O)CNC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H]3N(C(=O)[C@@H](NC(CNC([C@@H](NC([C@H](CSSC2)NC(=O)[C@@H](NC(=O)[C@@H](NC([C@@H](NC(CNC([C@@H](NC1=O)CC(=O)N)=O)=O)[C@H](O)C)=O)CCC(=O)O)CCCNC(=N)N)=O)CC(C)C)=O)=O)CC(C)C)CCC3)[C@H](O)C)CC(C)C)C', "
               "'Found 14 peptide bonds and MW=1455.0'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@@H]%18O[C@@H]([C@@H](O[C@@H]%19O[C@@H]([C@H](O)[C@H](O[C@]%20(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%20)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%19O)CO)[C@H](O)[C@H]%18NC(=O)C)CO)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 11 peptide bonds and MW=3795.7'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(=O)O)CC(C)C)CC2=CC=CC=C2)CCCNC(=N)N)C(C)C)C)CCC(=O)ONCC(=O)NCC(N[C@H](C(NCC(N[C@H](C(N[C@@H]1CC3=CC=C(O)C=C3)=O)CCCCN)=O)=O)CO)=O)CCCCN', "
               "'Found 15 peptide bonds and MW=1526.9'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(=O)N)CCCCN)CO)CC(C)C)C(C)C)CC(C)C)CCCNC(=O)N)CC(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(N[C@H](C(N[C@H](C(NCC(N[C@H]1CC(=O)N)=O)=O)C)=O)CC(C)C)=O)CC(C)C)CC(C)C', "
               "'Found 16 peptide bonds and MW=1444.9'), "
               "('O=C1OC([C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@@H](O)CCCCCCCC)CC(C)C)CCC(=O)O)C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1C(CC)C)=O)CO)=O)CC(C)C)=O)CO)CC(C)C)C(CC)C)C', "
               "'Found 9 peptide bonds and MW=1054.7'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O[C@]%19(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%19)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3521.5'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]4CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)O)[C@H]1O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@@H](O)[C@H]%11NC(=O)C)CO)[C@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@@H](O)[C@H](O)[C@H]%14NC(=O)C)CO)[C@H](O)[C@@H]%13O[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@@H]%17O[C@@H]([C@@H](O[C@@H]%18O[C@@H]([C@H](O)[C@H](O)[C@H]%18O)CO)[C@H](O)[C@H]%17NC(=O)C)CO)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO', "
               "'Found 9 peptide bonds and MW=3079.4'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO)O)[C@H]8O)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3317.4'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO)O)[C@@H](O)[C@@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO)[C@@H]5O)CO)[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3317.4'), "
               "('O=C(O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(N)C)CC(C)C)CC)C(CC)C)CCC(=O)O)CC)C)C(C)C)CC=1C2=C(C=CC=C2)NC1)CO)C)CC)C(C)C)C(CC)C)C)C)C', "
               "'Found 18 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1621.0'), "
               "('O=C/1O[C@H]([C@@H](NC(=O)[C@H](N)CO)C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C2=CC=C(O)C=C2)C(N[C@@H](C(NCC(N[C@H](C(N[C@@H](C(N\\\\C1=C/C=3C4=C(C=CC=C4)NC3)=O)[C@@H](CC(=O)O)C)=O)[C@@H](O)C(=O)N)=O)=O)CC(=O)O)=O)CC(=O)O)CC(=O)O)CC=5C6=C(C=CC=C6)NC5)C', "
               "'Found 10 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1312.7'), "
               "('O=C1N2[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@@H]1CC3=CC=C(O)C=C3)=O)CC(C)C)=O)CCCN)=O)C(C)C)=O)CC=4C5=C(C=CC=C5)NC4)CC(=O)O)CC(=O)N)CC6=CC=CC=C6)CC=7C8=C(C=CC=C8)NC7)CCC2', "
               "'Found 9 peptide bonds and MW=1248.8'), "
               "('C[C@@H](O)[C@H](NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CCCCN)NC(=O)[C@@H]1CCCN1C(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)CNC(=O)[C@H](CC[C@H](CN)O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)CNC(=O)[C@H](C)NC(=O)[C@H](CCC(N)=O)NC(=O)CN)C(O)=O', "
               "'Found 13 peptide bonds and MW=1574.9'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@@H]%18O[C@@H]([C@@H](O[C@@H]%19O[C@@H]([C@H](O)[C@H](O[C@@H]%20O[C@@H]([C@@H](O[C@@H]%21O[C@@H]([C@H](O)[C@H](O[C@]%22(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%22)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%21O)CO)[C@H](O)[C@H]%20NC(=O)C)CO)[C@H]%19O)CO)[C@H](O)[C@H]%18NC(=O)C)CO)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 12 peptide bonds and MW=4137.8'), "
               "('C[C@@H](NC(=O)[C@@H](C)NC(=O)[C@H](CCCCNC(=O)CNC(=O)CNC(=O)C[NH3+])NC(=O)CC[C@@H](NC(=O)[C@H](C)NC(=O)[C@@H](C)O[C@@H]1[C@@H](NC(C)=O)[C@H](O[C@H](CO)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1NC(C)=O)OP([O-])(=O)OP([O-])(=O)OC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(\\\\C)CC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)C(N)=O)C([O-])=O', "
               "'Found 10 peptide bonds and MW=1879.1'), "
               "('S1[C@@]2(NC(=O)/C(/NC(=O)[C@H]3N=C([C@@H](NC(=O)C4=C(N=C(C=5SC=C(N5)C6=N[C@H](C(NC(C7=NC(C8=NC(C9=N[C@H](C(N[C@@H](C1)C(=O)O)=O)CS9)=CS8)=CS7)=C)=O)CS6)C=C4)[C@@H](C)NC([C@H]%10N(C(\\\\C(\\\\NC(CNC([C@@H](NC2=O)[C@H](O)C)=O)=O)=C\\\\C)=O)CCC%10)=O)CC(=O)N)SC3)=C/C)C', "
               "'Found 9 peptide bonds and MW=1409.2'), "
               "('O=C1OC2=CC=C(CC(NC(=O)C(NC(=O)C(NC(=O)CCCCCCCCCCCCC(CC)C)CCC(=O)O)CCCN)C(=O)NC(C(=O)NC(C(=O)NC(C(N3C(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CCC(=O)N)=O)CCC3)=O)C(C)C)CCC(=O)O)C(O)C)C=C2', "
               "'Found 9 peptide bonds and MW=1372.9'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C(=O)NCC(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C=3SC=C(N3)C(=O)N[C@@H](C(N[C@@H](C(N[C@@H](C(N[C@@H](C(NCC(N[C@@H](C4=NC(C(N[C@@H](C(N[C@@H]2C(C)C)=O)C(C)C)=O)=CS4)CC(=O)O)=O)=O)CC=5C6=C(C=CC=C6)NC5)=O)[C@@H](OCC=C(C)C)C)=O)CC(=O)N)=O)CO)C)CC7=CC=C(O)C=C7)CCCCN)CC(=O)O)CC=8C9=C(C=CC=C9)NC8', "
               "'Found 14 peptide bonds and MW=1787.3'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)[C@@H](O)[C@@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@@H]5O)[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('CCCCCCCCCCCCCCCC(=O)N[C@@H](CCC(=O)NCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCC(=O)NCCCC[C@H](NC(=O)[C@@H](NC(=O)[C@@H]1CCCN1C(=O)[C@H](CC1=CC=C(O)C=C1)NC(=O)[C@H](CCC([O-])=O)NC(=O)[C@H](CC1=CNC2=C1C=CC=N2)NC(=O)[C@H](CC1=CC=C(O)C=C1)NC(=O)[C@@H](NC(=O)[C@H](CC([O-])=O)N(C)C(=O)[C@@H]1CC(=O)NCCCC[C@H](NC(C)=O)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CCC([O-])=O)C(=O)N[C@@H](CCCNC(N)=[NH2+])C(=O)N[C@@H](CC2=CC=CC=C2)C(=O)N1)C(C)(C)C)C1CCCCC1)C([O-])=O)C([O-])=O', "
               "'Found 17 peptide bonds and MW=3282.0'), "
               "('C([C@H](NC([C@H](CC1=CNC=N1)NC(=O)[C@@H]2CCC(N2)=O)=O)C(N[C@H](C(N[C@@H](CC3=CC=C(C=C3)O)C(N[C@@H](C(N[C@H](C(N[C@H](C(=O)N4[C@H](C(NCC)=O)CCC4)CCCNC(=N)N)=O)CC(C)C)=O)COC(C)(C)C)=O)=O)CO)=O)C=5C6=C(NC5)C=CC=C6', "
               "'Found 9 peptide bonds and MW=1152.8'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO)O)[C@H]8O)CO[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3317.4'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O)[C@H]%17O)CO[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('O=C/1N[C@H](C(=O)N[C@@H](C(=O)O[C@@H]([C@H](NC(=O)[C@H](N)[C@H](CC)C)C(=O)N[C@H](C(=O)N[C@@H](C(N[C@H](C(N\\\\C(\\\\C(N[C@H](C(N\\\\C1=C/C=2C3=C(C=CC=C3)NC2)=O)CO)=O)=C\\\\C)=O)[C@@H](O)C(C)C)=O)CO)[C@H](O)C)C(C)C)CC4=CC=CC=C4)CCCN', "
               "'Found 9 peptide bonds and MW=1092.7'), "
               "('O=C1N(C(C(=O)N[C@@H](C(=O)N[C@H](C(=O)N2[C@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@@H](CC(N[C@H](C(N[C@H](C(NC(C(N[C@@H](C(NC1CCC(=O)N)=O)C(O)C(C)C)=O)C)=O)[C@@H](O)C(C)C)=O)C(C)C)=O)CCCCCCC)C(O)C)CC(C)C)C[C@H](C2)O)[C@H](O)C)[C@@H](O)C(=O)N)[C@H](CC)C)C', "
               "'Found 10 peptide bonds and MW=1296.8'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)O)[C@H]1O)CO[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO)[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)O)[C@H](O)C)CC=2C3=C(C=CC=C3)NC2)CC4=CC=C(O)C=C4)CC(=O)O)CC5=CC=CC=C5)CC=6NC=NC6)CC=7C8=C(C=CC=C8)NC7)CC(=O)N)[C@H](CC)C)CCC(=O)O)CCC(N[C@H](C(N[C@H](C(NCC(N[C@H]1C(C)C)=O)=O)CC9=CC=C(O)C=C9)=O)CC(C)C)=O)CC(=O)O)CC(=O)N)CCCNC(=N)N', "
               "'Found 18 peptide bonds and MW=2195.4'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%17O)CO)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('S(CCC(N)C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C=O)CC=1NC=NC1)CCC(=O)N)C(CC)C)C(C)C)C(CC)C)CCCCN)CC(=O)O)CCCCN)C', "
               "'Found 9 peptide bonds, terminal COOH and NH2 groups, "
               "MW=1062.7'), "
               "('O=C1OC2=CC=C(CC(NC(=O)C(NC(=O)C(NC(=O)CC(O)CCCCCCCCCCCC(C)C)CCC(=O)O)CCCN)C(=O)NC(C(=O)NC(C(=O)NC(C(N3C(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CCC(=O)N)=O)CCC3)=O)C(C)C)CCC(=O)O)C(O)C)C=C2', "
               "'Found 9 peptide bonds and MW=1388.9'), "
               "('COC1NC(=O)c2nc(oc2C)\\\\C(NC(=O)C(NC(=O)c2csc(n2)-c2ccc(nc2-c2nc(oc2C)C(=C)NC(=O)C(=C)NC(=O)c2nc(oc2C)\\\\C(NC(=O)c2csc1n2)=C\\\\C)C(=O)NC(=C)C(=O)NC(=C)C(=O)NC(=C)C(N)=O)C(C)O)=C\\\\C(C)O', "
               "'Found 9 peptide bonds and MW=1204.8'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)CC(C(=O)NC(CO)CC2=CC=CC=C2)CCC(=O)N)CCC(=O)N)(C)C)(C)C)C(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)C)(C)C)C)(C)C)C)CCC(=O)N)(C)C)C(C)C)(C)C)CC(C)C)(C)C', "
               "'Found 18 peptide bonds and MW=1785.1'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CCCCCCC(CC)C)CC=2C3=C(C=CC=C3)NC2)CCC(=O)O)CC(=O)N)C(=O)N(CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CCCCN)C(N[C@H](C(NCC(N[C@@H](C(NC(C(N[C@H]1C(CC)C)=O)CCC(=O)O)=O)CC(=O)N)=O)=O)C(OC)C(=O)O)=O)CC(=O)O)C)C)C', "
               "'Found 12 peptide bonds and MW=1530.9'), "
               "('O=C(NC(C(=O)O)CCCNC(=N)N)C1N(C(=O)CNC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(N)CO)CC=2C3=C(C=CC=C3)NC2)CC(C)C)CO)CCCCN)C(O)C)C)CCCCN)CCCCN)CC(C)C)CCC(=O)O)CC(=O)N)CO)C)CCCCN)CCCCN)CCCNC(=N)N)C(CC)C)CO)CCC(=O)O)C(CC)C)C)C(CC)C)C)C(CC)C)CCC(=O)N)CCC1', "
               "'Found 29 peptide bonds, terminal COOH and NH2 groups, "
               "MW=3083.9'), "
               "('CCC(C)(C)[C@H](NC(=O)[C@H](NC(=O)[C@@H]1CCCN1C(=O)C(NC(=O)[C@@H](C)NC=O)C(O)c1ccc(Br)cc1)C(C)(C)C)C(=O)N[C@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@H](CS(O)(=O)=O)C(=O)N[C@H]1[C@@H](C)OC(=O)[C@@H](CC(O)=O)NC(=O)[C@@H]2CCCN2C(=O)[C@H](NC(=O)[C@H](CCC(N)=O)N(C)C1=O)C(C)C', "
               "'Found 10 peptide bonds and MW=1616.9'), "
               "('P(=O)(O[C@H](C(=O)N)[C@H]1NC(=O)CNC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](CC(=O)O)NC([C@H](NC([C@H]([C@H](OC([C@@H](NC([C@@H](NC1=O)CCC(=O)O)=O)CC=2C3=C(C=CC=C3)NC2)=O)C)NC(=O)[C@@H](NC(=O)C4OC4CCC)CO)=O)CC=5C6=C(C=CC=C6)NC5)=O)CC(=O)O)C7=CC=C(O)C=C7)CC(=O)O)(O)O', "
               "'Found 11 peptide bonds and MW=1483.8'), "
               "('O=C(O)C(NC(=O)C(NC(=O)[C@@H](NC(=O)C(NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@H](NC(=O)C(NC(=O)C(NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@H](NC(=O)C(NC(=O)C(O)CO)CC(C)C)C)CC(C)C)CC(C)C)C(CC)C)CCCNC(=N)N)CC(C)C)CC(C)C)C(C)C)CCCCN)CC(C)C)C(O)C)CC(C)C)C(O)C)CCCCN)CCCCN', "
               "'Found 16 peptide bonds and MW=1753.1'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCC)CC(C)C)CCC(=O)N)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1C(C)C)=O)CO)=O)CC(C)C)=O)CO)CC(C)C)C(C)C)C', "
               "'Found 9 peptide bonds and MW=1016.6'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)/C=C/C2=C(C=CC=C2)C)C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](CCCCN)C(N[C@H](C(N[C@H](C(N[C@@H](C(N[C@@H](C(N[C@H]1[C@H](O)C(C)C)=O)[C@@H](O)C)=O)CC3=CC=C(O)C=C3)=O)CO)=O)[C@H](O)C(C)C)=O)CC4=CC=C(O)C=C4)CC(C)C)CC5=CC=CC=C5)C', "
               "'Found 10 peptide bonds and MW=1306.9'), "
               "('S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15NC(=O)C)CO)[C@H](O[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O', "
               "'Found 9 peptide bonds and MW=3023.4'), "
               "('O=C(NC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C=O)CC(=O)N)CC1=CC=C(O)C=C1)CC2=CC=C(O)C=C2)CCCCN)CO)CC=3NC=NC3)C(NC(=O)C(N)C(O)C)C(O)C', "
               "'Found 9 peptide bonds and MW=1040.6'), "
               "('O=C1NC(C(=O)NC(C(=O)NCCCCC1NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C2[N+]3=C(NCC2)C(NC(=O)CCC(=O)O)=CC=4C3=CC(O)=C(C4)O)CO)CCCCN)CCCN(O)C=O)CO)CCCN(O)C=O', "
               "'Found 9 peptide bonds and MW=1088.6'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO', "
               "'Found 9 peptide bonds and MW=3127.4'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)[C@@H](O)[C@@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO)[C@@H]5O)[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O[C@@H]%18O[C@@H]([C@@H](O[C@@H]%19O[C@@H]([C@H](O)[C@H](O[C@]%20(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%20)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%19O)CO)[C@H](O)[C@H]%18NC(=O)C)CO)[C@H]%17O)CO)[C@H](O[C@@H]%21O[C@H]([C@@H](O)[C@@H](O)[C@@H]%21O)C)[C@H]%16NC(=O)C)CO', "
               "'Found 11 peptide bonds and MW=3931.7'), "
               "('O=C1O[C@H]([C@H](NC(=O)/C=C/C2=C(C=CC=C2)[C@@H](O)[C@@H](O)/C=C/C)C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](CO)C(N[C@@H](C(N[C@@H](C(N[C@@H](C(N[C@H](C(N[C@@H]1CC(C)C)=O)C(C)C)=O)C3=CC=C(O)C=C3)=O)CO)=O)[C@H](O)C)=O)[C@H](O)C4=CC=CC=C4)CC(C)C)CO)C', "
               "'Found 10 peptide bonds and MW=1240.8'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O)[C@H]%17O)CO)[C@@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 9 peptide bonds and MW=3179.4'), "
               "('O=C(NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N)CCCCN)CCCCN)CC(C)C)CC(C)C)CCCCN)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)CN)C(CC)C)CCCCN)CC1=CC=CC=C1)CC(C)C)CCCCN)CCCCN)C)CCCCN)CCCCN)CC2=CC=CC=C2)CCCCN)C)CC3=CC=CC=C3)C(C)C.O=C(O)C', "
               "'Found 21 peptide bonds and MW=2321.6'), "
               "('O=C1NCC(=O)N[C@@H](C(=O)NCCC(=O)OCC[C@H](C(N[C@H](C(NC1=C)=O)C(C)C)=O)NC(=O)CNC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](O)[C@@H](N)CCCCCCCCC/C=C\\\\CCCCCC)[C@H](O)C)[C@@H](O)C2=CC=C(O)C=C2)CO)CCO)C', "
               "'Found 11 peptide bonds and MW=1216.7'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]8[C@H](O)[C@H](O[C@@H](O[C@H]9[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]9CO)O[C@H]%10[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%10CO[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)O)[C@H]8O)CO[C@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@@H]%12O[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO)CO[C@@H]%16O[C@@H]([C@@H](O[C@@H]%17O[C@@H]([C@H](O)[C@H](O)[C@H]%17O)CO[C@]%18(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%18)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%16NC(=O)C)CO', "
               "'Found 10 peptide bonds and MW=3453.5'), "
               "('C[C@@H](O)[C@@H]1NC(=O)[C@@H](NC(=O)[C@H](CCCN(O)C=O)NC(=O)[C@H](CCCCNC1=O)NC(=O)[C@H](CCCN(O)C=O)NC(=O)[C@@H](CO)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@@H](CO)NC(=O)[C@@H]1CCN=C2N1c1cc(O)c(O)cc1C=C2NC(=O)CCC(O)=O)[C@@H](C)O', "
               "'Found 10 peptide bonds and MW=1250.7'), "
               "('ClCC(O)C1NC(=O)C(NC(=O)/C(/NC(=O)C(NC(=O)C(NC(=O)C(NC(C(NC(C(NC(C(COC1=O)NC(=O)CC(O)C(O)CCCCCCCCCCCC)=O)(O)CCCN)=O)CC(=O)O)=O)CCO)CC=2N=CNC2)C(O)C)=C/C)C(O)C(=O)O', "
               "'Found 9 peptide bonds and MW=1204.1')]\n"
               'False negatives: '
               "[('O=C1N[C@@H](C(=O)O)C(NC(C(=O)N[C@H](C(N[C@H](C(N[C@H]1C(C)C)=O)C)=O)C)CO)C', "
               "'Only 4 peptide bonds found - fewer than required for 10+ "
               "amino acids'), "
               "('O=C(O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCCCC)C(C)C)CC1=CC=CC=C1)CCC(=O)O)[C@H](CC)C)[C@H](CC)C', "
               "'Only 6 peptide bonds found - fewer than required for 10+ "
               "amino acids'), "
               "('O=C(O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CCCCCCC)C(C)C)CC1=CC=CC=C1)CCC(=O)O)CC(C)C', "
               "'Only 4 peptide bonds found - fewer than required for 10+ "
               "amino acids'), "
               "('O=C/1N[C@H](C(=O)NC(C(=O)N2[C@H](C(=O)NC(C(O)C(=O)N[C@H](C(=O)NCC(N3[C@H](C(N4[C@H](C(N[C@@H](C(N[C@H](C(N\\\\C1=C\\\\C)=O)CO)=O)[C@H](CC)C)=O)CCC4)=O)CCC3)=O)CCC(=O)N)CC(O)CC(O)C(O)CC(C)C)CCC2)CCC5=CC=CC=C5)[C@H](O)C', "
               "'Only 8 peptide bonds found - fewer than required for 10+ "
               "amino acids'), "
               "('SCC(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C1N(C(=O)C(NC(=O)CN)CC(=O)N)CCC1)CCCCN)C(C)C)C)CC=2NC=NC2)C(=O)NC(C(=O)NC(C(=O)N)CO)C', "
               "'Only 8 peptide bonds found - fewer than required for 10+ "
               "amino acids'), "
               "('O=C(O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](N)CCCN=C(N)N)C(C)C)CCCN=C(N)N)[C@H](CC)C)CC=1C2=C(C=CC=C2)NC1', "
               "'Only 4 peptide bonds found - fewer than required for 10+ "
               "amino acids')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 42,
    'num_false_positives': 100,
    'num_true_negatives': 12156,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.29577464788732394,
    'recall': 0.9130434782608695,
    'f1': 0.44680851063829785,
    'accuracy': 0.9915460900666558}