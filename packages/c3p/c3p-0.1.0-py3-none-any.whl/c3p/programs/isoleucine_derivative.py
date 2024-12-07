"""
Classifies: CHEBI:24899 isoleucine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_isoleucine_derivative(smiles: str):
    """
    Determines if a molecule is an isoleucine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an isoleucine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Define isoleucine substructure pattern
    isoleucine_pattern = Chem.MolFromSmarts('[CH3][CH2][CH]([CH3])[CH]([NH2,NH,N])[C](=O)[O,N]')
    
    # Define patterns that would indicate derivatives
    modified_patterns = [
        # N-substituted/acylated isoleucine
        Chem.MolFromSmarts('[CH3][CH2][CH]([CH3])[CH]([NX3])C(=O)[O,N]'),
        # O-substituted isoleucine
        Chem.MolFromSmarts('[CH3][CH2][CH]([CH3])[CH]([NX3])C(=O)[OX2][!H]'),
    ]

    # Check if molecule contains isoleucine core structure
    has_isoleucine_core = False
    if isoleucine_pattern is not None and mol.HasSubstructMatch(isoleucine_pattern):
        has_isoleucine_core = True
    else:
        for pattern in modified_patterns:
            if pattern is not None and mol.HasSubstructMatch(pattern):
                has_isoleucine_core = True
                break

    if not has_isoleucine_core:
        return False, "No isoleucine core structure found"

    # Analyze modifications
    modifications = []
    
    # Check for N-substitution/acylation
    n_subst_pattern = Chem.MolFromSmarts('[CH3][CH2][CH]([CH3])[CH]([NX3][!H])[C](=O)')
    if n_subst_pattern and mol.HasSubstructMatch(n_subst_pattern):
        if mol.HasSubstructMatch(Chem.MolFromSmarts('[CH3][CH2][CH]([CH3])[CH]([NH]C(=O))')):
            modifications.append("N-acylated")
        else:
            modifications.append("N-substituted")
        
    # Check for O-substitution
    o_subst_pattern = Chem.MolFromSmarts('[CH3][CH2][CH]([CH3])[CH]([NX3])C(=O)[OX2][!H]')
    if o_subst_pattern and mol.HasSubstructMatch(o_subst_pattern):
        modifications.append("O-substituted")

    # Count peptide bonds
    peptide_pattern = Chem.MolFromSmarts('[NX3][CX3](=O)[CX4][NX3][CX3](=O)[CX4][NX3][CX3](=O)')
    peptide_matches = len(mol.GetSubstructMatches(peptide_pattern)) if peptide_pattern else 0

    # Count isoleucine fragments
    ile_fragment_count = len(mol.GetSubstructMatches(isoleucine_pattern)) if isoleucine_pattern else 0

    # If there are multiple peptide bonds and multiple isoleucine fragments, it's likely a peptide
    if peptide_matches >= 1 and ile_fragment_count >= 2:
        return False, "Appears to be a peptide containing isoleucine rather than an isoleucine derivative"

    if modifications:
        return True, f"Isoleucine derivative with modifications: {', '.join(modifications)}"
    else:
        return True, "Unmodified isoleucine derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24899',
                          'name': 'isoleucine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of isoleucine at the '
                                        'amino group or the carboxy group, or '
                                        'from the replacement of any hydrogen '
                                        'of isoleucine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing isoleucine residues.',
                          'parents': ['CHEBI:83821']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.07207207207207209 is too low.\n'
               'True positives: '
               "[('O=C(N[C@H](C(=O)OC[C@@H](NC(=O)C1=CC=CC=C1)C(C)C)[C@@H](CC)C)C2=CC=CC=C2', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C(OC)[C@H]1N(C(=O)[C@@H](N(C(=O)[C@H]2N(C(=O)[C@@H](NC(=O)[C@H](N(C(=O)[C@@H](NC(=O)[C@@H](N(C(=O)CCCCCCCCNC(=O)CCCC3=CC=C(O)C=C3)C)CC(C)C)[C@H](CC)C)C)C(C)C)CCC(=O)N)CCC2)C)CC4=CC=CC=C4)CCC1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('ClC1=C(O)C(Cl)=CC(=C1)C[C@H](O)C(=O)N[C@@H](C(=O)N2[C@@H]3[C@@H](CC[C@H](C3)O)C[C@H]2C(=O)NCCCCN=C(N)N)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(O)[C@H](NC(=O)C)[C@@H](CC)C', 'Isoleucine derivative "
               "with modifications: N-acylated')]\n"
               'False positives: '
               "[('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)CC(O)CCCCCCC)CC(C)C)CC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](C(N[C@@H](C(N[C@H](C(N[C@H](C(N[C@H]1CC(=O)O)=O)[C@H](CC)C)=O)[C@H](CC)C)=O)CO)=O)CC(C)C)CO)CC(C)C)CC(C)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H](CO)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(C)C)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)C(=O)N[C@@H]([C@H](CC)C)C(O)=O)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N[C@H](C(=O)N([C@H](C(=O)N([C@H](C(=O)N([C@H](C(=O)O[C@@H](C(C)C)C(N2[C@H](C(N3[C@H](C(N[C@H](C(O[C@@H](C1(C)C)CCCCC)=O)C(C)C)=O)CCC3)=O)CCC2)=O)C(C)C)C)C(C)C)C)C)C)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1OC(C(=O)N[C@H](C(=O)N[C@H](C(=O)O)[C@H](CC)C)C(C)C)C1C(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CCCCCCCCC)CC=2C3=C(C=CC=C3)NC2)CCC(=O)O)[C@@H](O)C(=O)N)C(=O)N(CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](CCCCN)C(N[C@H](C(NCC(N[C@@H](C(N[C@H](C(N[C@H]1[C@H](CC)C)=O)CCC(=O)O)=O)CC(=O)N)=O)=O)[C@@H](OC)C(=O)O)=O)CC(=O)O)C)C)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C1O[C@H](C(=O)N2[C@H](C(=O)N[C@H](C(=O)O[C@@H]([C@@H](C(N[C@H](C(N([C@H]1C(C)C)C)=O)C(C)C)=O)C)CCCCC)[C@H](CC)C)CCC2)CC3=CC=CC=C3', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('S(CCC(N)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N1C(C(=O)NC(C(=O)N2C(C(=O)NCC(=O)N3C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)O)C(CC)C)CCC(=O)O)C)C)C)CCC3)CCC2)C(CC)C)CCC1)C)CC(C)C)CCC(=O)O)CCCNC(=N)N)CC4=CC=C(O)C=C4)CC(C)C)CC(=O)N)CC(=O)N)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('SC[C@H](N)C(=O)N[C@@H]([C@H](CC)C)C(=O)N[C@@H](CCC(=O)N)C(O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1NC(C(=O)NCCCCC(C(NC1C(CC)C)=O)NC(=O)NC(C(=O)O)C(C)C)CCC2=CC=CC=C2', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC2=CC=CC=C2)CCC(=O)N)CCC(=O)N)(C)C)(C)C)C(C)C)CCC1)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)(C)C)C)(C)C)C)(C)C)C)CCC(=O)N)(C)C)C(CC)C)(C)C)(C)C)(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N([C@H](C(=O)NCCC(=O)O[C@H](CC(CO)C)C(N2[C@H](C(N[C@H](C(N[C@H]1C(C)C)=O)C(CC)C)=O)CCC2)=O)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1OC([C@H](NC(=O)C(NC(=O)C(NC(=O)[C@H](NC(=O)C(NC(=O)C(NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@H](NC(=O)C(NC(=O)C(O)CO)CC(C)C)C)CC(C)C)CC(C)C)C(CC)C)CCCNC(=N)N)CC(C)C)CC(C)C)C(C)C)CCCCN)CC(C)C)C(=O)NC(C(=O)N[C@@H](C(NC(C(NC1CCCCN)=O)CCCCN)=O)C)CC(C)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('ClC1=CC=2NC(Cl)=C(C2C=C1)C[C@H]3NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](CO)NC([C@H](NC([C@@H](NC3=O)[C@@H](CC)C)=O)CCC(=O)O)=O)C(C)C)CC=4C5=C(C=CC=C5)NC4', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(=O)N[C@@H](CCCCN)C(O)=O)[C@H]1NCCC1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)N[C@H](Cc1ccccc1)C(=O)N(C)[C@@H](C(C)C)C(=O)N[C@@H](C(C)CC)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](C)C(=O)OC', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)CN)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CC[C@H](C)[C@@H](C(=O)N1CCC[C@H]1C(=O)N[C@@H]([C@@H](C)CC)C(=O)O)N', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(O)CCCCCCCCCCCCN=C(N)N)C(=O)N[C@@H](C(=O)N[C@@H]([C@H](CC)C)C(N[C@@H](C(N[C@@H](C(N[C@@H]1C)=O)CCC(=O)N)=O)[C@H](O)C)=O)C(C)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N(C(C(=O)NC(C(=O)NCCCCC(C(NC(C(NC1CCC2=CC=CC=C2)=O)C(C)C)=O)NC(=O)NC(C(=O)O)C(CC)C)CC3=CC=CC=C3)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N([C@H](C(=O)N([C@H](C(=O)N([C@H](C(=O)N2[C@H](C(=O)N([C@H](C(=O)N3[C@@H](CCC3)C(O[C@@H](CCC[C@H]([C@H](C(O[C@@H]([C@H](CC=C(C(=C1)OC)C)C)C)=O)C)O)CC)=O)C(C)C)C)CCC2)COC)C)C(C)C)C)[C@H](CC)C)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C1NC(C(C)C)C(=O)NC(C(C)C)C(=O)N(C(C(=O)NC(CC(C)C)C(=O)N(C(C(=O)N(C(C(=O)NC1C(CC)C)CC=2C=COC2)C)C)C)CC=3C=COC3)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('SC[C@H](NC(=O)CN)C(=O)N[C@@H]([C@H](CC)C)C(O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CC[C@H](C)[C@H](NC(=O)[C@@H](NC(=O)[C@H](C)NC(=O)[C@H](CCCCNC(=O)c1cc(ccc1C(F)(F)F)C(F)(F)F)NC(=O)[C@H](CC(O)=O)NC(C)=O)[C@@H](C)O)C(=O)NCC(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S1SC(N)C(=O)N[C@H](C(=O)N[C@@]([C@@H](CC)C)(C(=O)N[C@H](C(=O)NC(C(=O)N[C@@H](C(=O)N2[C@H](CCC2)C(=O)N[C@H](CC(C)C)C(O)=O)C1)CC(=O)N)CCC(=O)N)[H])CC3=CC=C(O)C=C3', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(NC(C(=O)NC(CNCCO)C)(C)C)C(NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C(NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H]1N(C(=O)C(CCCCCC)C)CCC1)CC(CC(O)CC(=O)CC)C)C)(C)C)[C@H](CC)C)[C@H](CC)C)(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N([C@H](C(=O)NCCC(=O)O[C@H](CC(O)CO)C(N2C(C(N[C@H](C(N([C@H]1C(C)C)C)=O)[C@H](CC)C)=O)CCC2)=O)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](O)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(C)C)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N(C(C(=O)NC(C(=O)NCCCCC(C(NC(C(NC1CC=2C3=C(C=CC=C3)NC2)=O)C(CC)C)=O)NC(=O)NC(C(=O)O)C(C)C)CC4=CC=CC=C4)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(C)C)CC=1NC=NC1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CC[C@H](C)[C@@H](C(=O)N[C@@]1(CCCC=CCCC[C@](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC1=O)CC(C)C)CS)CCCNC(=N)N)(C)C(=O)N[C@@H](CC2=CNC=N2)C(=O)N[C@@H](CC3=CNC=N3)C(=O)N[C@@H](CO)C(=O)N[C@@H]([C@@H](C)O)C(=O)N)C)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCCNC(=N)N)NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](CC4=CNC5=CC=CC=C54)NC(=O)CCNC(=O)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('BrC1=C(OC)C=CC(=C1)C[C@@H]2N(C(=O)[C@@H](N3C(=O)[C@@H](NC(=O)[C@H](CCCN=C(N)N)NC([C@H]([C@H](OC([C@@H](NC2=O)C(C)C)=O)C)NC(=O)[C@@H](NC(=O)CCC)CCS(=O)C)=O)CC[C@H]3O)[C@H](CC)C)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)[C@H](CC)C)C(O)=O)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('ClC1=C(O)C=CC(=C1)C[C@@H]2N(C(=O)[C@@H](N3C(=O)[C@@H](NC(=O)[C@H](CCCN=C(N)N)NC([C@H]([C@@H](OC(C(NC2=O)C(CC)C)=O)C)NC(=O)C(NC(=O)C)CCC(=O)O)=O)CC[C@H]3O)CC4=CC=CC=C4)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CC(O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CC[C@H](C)[C@H](N(C)C)C(=O)N[C@H]1[C@@H](Oc2ccc(cc2)\\\\C=C/NC(=O)[C@H](CC(C)C)NC1=O)C(C)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C1OC([C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@@H](O)CCCCCCCCC)CC(C)C)CCC(=O)O)C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1C(CC)C)=O)CO)=O)CC(C)C)=O)CO)CC(C)C)C(C)C)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C1O[C@@H](CC(=O)N[C@@H](C(=O)N[C@H](CO)C(N[C@@H](C(N[C@H](C(N[C@H]1C(CC)C)=O)CC2=CC=CC=C2)=O)[C@@H](O)C)=O)CC(C)C)CCCCCCC', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC1=CC=C(O)C=C1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@H](CO)C(N[C@@H](C(N[C@H](C(NC(CC(O[C@@H]([C@@H]1NC(=O)C(NC(=O)[C@H](NC(=O)CC(O)CCCCCCC)CC(C)C)CC(=O)O)C)=O)C(=O)O)=O)[C@H](CC)C)=O)CC(C)C)=O)CC(C)C)CO)CC(C)C)CC(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC1=CC=C(O)C=C1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N([C@H](C(=O)N[C@@H](C(=O)N[C@@H](C)CC(O[C@@H]([C@@H](C(N[C@H]1[C@H](CC)C)=O)NC(=O)C(=NNC2=C(C(=O)OCCCCCCCCCC(C)C)C=C(O)C=C2)C)C3=CC=CC=C3)=O)CC=4C5=C(C(OC)=CC=C5)NC4)[C@@H](O)C6=CC=CC=C6)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N1C(CCC1)C(=O)NC(C(CC)C)C(O)=O)C(NC(=O)C(NC(=O)C(NC(=O)C2N(CCC2)C(=O)C(N)CC3=CC=C(O)C=C3)CC4=CC=CC=C4)C(C)C)CCC(O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@H](C(=O)N2[C@H](C(=O)N([C@H](C(=O)O[C@H]([C@H](C(N[C@H](C(N([C@H]1[C@H](CC)C)C)=O)C(C)C)=O)C)CCCC=C)C(C)C)C)CCC2)CC3=CC=CC=C3', "
               "'Isoleucine derivative with modifications: N-substituted, "
               "O-substituted'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(C)C)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1OC(C(CC)C)CC(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CC2=CC=CC=C2)C(NC(C(NC(C(NC(C(NC(C(NC1CO)=O)CC(C)C)=O)C(C)C)=O)CCN)=O)CC(C)C)=O)CCN)C(CC)C)CCN', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)CN)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S1C(=NC(=C1)C(=O)N[C@@H](CC2=CC=C(O)C=C2)C[C@@H](C(=O)O)C)[C@H](OC(=O)C)C[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H]3N(CCCC3)C)[C@H](CC)C)COC(=O)CC)C(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)C(=O)N[C@@H]([C@H](CC)C)C(O)=O)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CCC(C)[C@H](NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CO)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](CCC(O)=O)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CC(O)=O)NC(=O)[C@@H]1CCCN1C(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](CO)NC(=O)[C@@H]1CCCN1C(=O)[C@H](CO)NC(=O)[C@@H](N)CCC(N)=O)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](CCSC)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](Cc1c[nH]cn1)C(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CS)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CCCNC(N)=N)C(=O)N[C@@H](CC(C)C)C(N)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@@H]([C@H](NC(=O)C[C@H](O)CC(C)C)C(=O)N[C@@H](C(=O)N[C@H](C(=O)NCC(=O)N([C@@H](C(=O)N[C@@H](CC(C)C)C(N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@@H](C(N[C@H](C(N[C@H]1[C@H](O)C)=O)[C@H](CC)C)=O)CC=2C3=C(C=CC=C3)NC2)=O)CCC(=O)N)=O)CCC(=O)O)=O)CCCN=C(N)N)=O)CC4=CC=CC=C4)C)CO)CCCN=C(N)N)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1NC(C(=O)NC(C(=O)NC(C(=O)NCCCCC(C(NC1C(CC)C)=O)NC(=O)NC(C(=O)O)C(CC)C)CC2=CC=CC=C2)C)CCC3=CC=CC=C3', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('ClC(Cl)CCCCCC[C@@H](N)[C@@H](O)C(=O)N[C@H](C(=O)N([C@H](C(=O)N1[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC1)CC(C)C)C)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC(=O)N)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(NC(C(=O)O)CC1=CC=C(O)C=C1)C2N(C(=O)C(N(C(=O)C(NC(=O)C(O)C(NC)CCCCCCC)CC3=CC=C(O)C=C3)C)C(CC)C)CCC2', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(=O)N[C@@H]([C@H](CC)C)C(O)=O)[C@H]2NCCC2', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C/1N[C@H](C(=O)N[C@@H](C(=O)N2[C@H](C(=O)NC(C(O)C(=O)N[C@@H](C(=O)NCC(N3[C@H](C(N4[C@H](C(N[C@@H](C(N[C@H](C(N\\\\C1=C\\\\C)=O)CO)=O)[C@H](CC)C)=O)CCC4)=O)CCC3)=O)CCC(=O)N)CC(OC(=O)[C@@H](N(C(=O)C)C)CC(C)C)CC(O)CC5=CC=CC=C5)CCC2)CCC6=CC=C(OC)C=C6)[C@H](O)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S1C(=NC(=C1)C(=O)N[C@@H](CC2=CC=CC=C2)C[C@@H](C(=O)O)C)CC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]3N(CCCC3)C)[C@H](CC)C)C(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC[C@H](NC(=O)[C@@H](NC(=O)CCC)CC(C)C)C(=O)O)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1[C@H](CC)C)=O)CC3=CC=CC=C3)C)=O)C(C)C)C2=O)O)CC4=CC=C(O)C=C4)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C(O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCC(C)C)CC(=O)N)C(C)C)C(C)C)CC(=O)N)CC(=O)N)C[C@H](O)CCN)[C@@H](O)C)CO)CC=1C2=C(C=CC=C2)NC1)[C@@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@H](C(=O)N[C@H](CN)CC(C)C)[C@H](CC)C)C(NC(=O)[C@@H](NC(=O)C(NC(=O)[C@@H](NC(=O)[C@H]1N(C(=O)[C@H]2N(C(=O)CCCCCCCCC)C[C@@H](C2)O)C[C@@H](C1)O)C(C)C)(C)C)CCC(=O)N)(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1NC(C(=O)NC(C(C(=O)OC(C(=O)NCC(=O)N(C(C(CC)C)C(NCC(N(C(C(N(C(C(NC(C(C1(C)C)=O)C)=O)CC2=CC=C(OC)C=C2)C)=O)C(C)C)C)=O)=O)C)C(CC)C)C)CC)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C1NC(C(=O)NCCCCC(C(NC1C(CC)C)=O)NC(=O)NC(C(=O)O)C(CC)C)CCC2=CC=CC=C2', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CC[C@H](C)[C@H](N)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](C)C(=O)N[C@@H]([C@@H](C)CC)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H]([C@@H](C)CC)C(N)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('[H]N1[C@@H](Cc2ccc(OC)cc2)C(=O)N(C)[C@@H](C)C(=O)N(C)[C@@H]([C@@H](C)CC)C(=O)N2CCC[C@H]2C(=O)O[C@@H](C[C@@H](C)C[C@H](O)[C@H](C)C2=N[C@H](CS2)\\\\C=C(C)\\\\C1=O)C(C)(C)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)O)CC=2NC=3C=CC=CC3C2)CCC(=O)NCCCC[C@@H]4NC(=O)C(CCCNC(=N)N)NC([C@@H]([C@H](OC(CC5C(N[C@H](C(N[C@@H]1CCC(=O)OC[C@H](NC(=O)[C@H]6N(C(=O)[C@H](CC7=CC=C(O)C=C7)NC4=O)CCC6)C(=O)N5)=O)CC=8C9=C(C=CC=C9)NC8)=O)=O)C)NC(=O)[C@@H](NC(=O)C(NC(=O)C)C(CC)C)CO)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('[H]N[C@@H](CCCCN)C(N[C@H]1CSSC[C@H](NC([C@H]([C@@H](C)O)NC([C@H](C)NC([C@H]([C@@H](C)O)NC([C@@H](NC1=O)CC(N)=O)=O)=O)=O)=O)C(N[C@@H](C)C(N[C@@H]([C@@H](C)O)C(N[C@@H](CCC(N)=O)C(N[C@@H](CCCNC(N)=N)C(N[C@@H](CC(C)C)C(N[C@@H](C)C(N[C@@H](CC(N)=O)C(N[C@@H](CC2=CC=CC=C2)C(N[C@@H](CC(C)C)C(N[C@@H](C(C)C)C(N[C@@H](CC3=CNC=N3)C(N[C@@H](CO)C(N[C@@H](CO)C(N[C@@H](CC(N)=O)C(N[C@@H](CC(N)=O)C(N[C@@H](CC4=CC=CC=C4)C(NCC(N5CCC[C@H]5C(N[C@@H]([C@H](CC)C)C(N[C@@H](CC(C)C)C(N6CCC[C@H]6C(N7CCC[C@H]7C(N[C@@H]([C@@H](C)O)C(N[C@@H](CC(N)=O)C(N[C@@H](C(C)C)C(NCC(N[C@@H](CO)C(N[C@@H](CC(N)=O)C(N[C@@H]([C@@H](C)O)C(N[C@@H](CC8=CC=C(O)C=C8)C(N)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(C)C)[C@H](CC)C)C)[C@](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC(=O)CCCCCCC)C)CC(C)C)(CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@H]([C@H](NC(=O)CC[C@H](NC(=O)[C@@H](NC(=O)CCC)CC2=CC=C(O)C=C2)C(=O)OC)C(=O)N[C@H](C(=O)N[C@H]3CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1[C@H](CC)C)=O)CC4=CC=CC=C4)C)=O)C(C)C)C3=O)O)CCCN=C(N)N)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(O)CCCCCCCCCCCCN=C(N)N)C(=O)N[C@@H](C(=O)N[C@@H]([C@H](CC)C)C(N[C@@H](C(N[C@@H](C(N[C@@H]1C)=O)CCC(=O)N)=O)[C@H](O)C)=O)[C@@H](CC)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1O[C@@H]([C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCCCC)CC(C)C)CCC(=O)O)C(=O)N[C@@H](C(=O)N[C@@H](C(=O)N[C@@H](C(N[C@H](C(N[C@@H](C(N[C@H]1[C@H](CC)C)=O)CO)=O)CC(C)C)=O)CO)CC(C)C)[C@H](CC)C)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)[C@H](CC)C)C(O)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CCCCN', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S(CC[C@@H]1NC(=O)[C@@H](NC(=O)CN(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@H]2N(CCC2)C(=O)[C@H]3N(CCC3)C(=O)[C@@H](NC1=O)CCC(=O)N)[C@@H](CC)C)[C@@H](O)C)C)CC(C)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(NC(C(=O)NC(CN(CCO)C)C)(C)C)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C1N(C(=O)C(CCCCCCCC)C)CCC1)CC(CC(O)CC(=O)CC)C)C)(C)C)C(C)C)C(CC)C)(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1OC(C(NC(=O)CCCCC(CC)C)C(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C(=O)NC(C(NCC(NC(C(NC(C(NC(C(NC1CC2=CC=CC=C2)=O)CCN)=O)C(CC)C)=O)CC=3NC=4C=CC=CC4C3)=O)=O)CC(=O)O)CC(=O)N)CC(=O)O)CCN)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('ClCCCCCCC[C@@H](N)[C@@H](O)C(=O)N[C@H](C(=O)N([C@H](C(=O)N1[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC1)CC(C)C)C)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S1SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC([C@@H](NC([C@H](C1)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC(=O)[C@H]2N(C(=O)[C@H]3NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)CNC(C(NC(C(NC(CNC(CC3)=O)=O)CO)=O)CCCNC(=N)N)=O)CC=4NC=5C=CC=CC5C4)CC6=CC=CC=C6)CCC2)C(C)C)CCCNC(=N)N)=O)CC(C)C)=O)[C@H](CC)C)CC=7NC=8C=CC=CC8C7)C(=O)N[C@H](C(=O)O)CC(=O)O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CC1=CC=C(O)C=C1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N([C@H](C(=O)N([C@H](C(=O)N[C@H](C(=O)N(C)[C@H](C(N([C@@H](C(N[C@@H](C(N[C@@H]1[C@H](CC)C)=O)[C@H](O)C(C)C)=O)C)C)=O)C)CC(C)C)CC(C)C)C)C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('S1C2=N[C@H](C1)C=C(C(=O)N[C@H](C(=O)N([C@H](C(=O)N(C)[C@H](C(N3[C@H](C(O[C@@H](C[C@H](C[C@@H]([C@@H]2C)O)C)C(C)(C)C)=O)CCCC3)=O)[C@H](CC)C)C)C)CC4=CC=C(OC)C=C4)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C1OC(CC(=O)N[C@@H](C(=O)N[C@@H](CO)C(N[C@H](C(N[C@@H](C(N[C@H]1[C@H](CC)C)=O)CC(C)C)=O)[C@H](O)C)=O)CC(C)C)CCCCCCC', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C(OC)[C@H]1N(C(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C[C@H](O)[C@@H](NC(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](O)C)CC(C)C)C)CCC(=O)N)CC(C)C)[C@H](CC)C)C)CC2=CC=CC=C2)CCC1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC=1C=2C(NC1)=CC=CC2', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(OC)[C@H]1N(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N(C(=O)C(OC(=O)C(O)C(C)C)C(C)C)C)CC(=O)N)[C@H](CC)C)C)CC2=CC=CC=C2)CCC1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H]1C(CC)C)=O)CC(=O)N)CC(C)C)CC(=O)N', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('CC[C@H](C)[C@@H]1N(C)C(=O)[C@H](C)N(C)C(=O)[C@H](Cc2ccc(OC)cc2)NC(=O)\\\\C(C)=C\\\\[C@H]2CSC(=N2)[C@@H](C)[C@@H](O)C[C@H](C)C[C@H](OC(=O)[C@@H]2CCCN2C1=O)[C@@H](C)CC(C)(C)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C1OC2=CC=C(CC(NC(=O)C(NC(=O)C(NC(=O)CCCCCCCCCCCCCC(C)C)CCC(=O)O)CCCN)C(=O)NC(C(=O)NC(C(=O)NC(C(N3C(C(NC(C(NC(C(NC1C(CC)C)=O)CC4=CC=C(O)C=C4)=O)CCC(=O)N)=O)CCC3)=O)C(C)C)CCC(=O)O)C(O)C)C=C2', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('O=C1O[C@H](C(=O)N[C@H](C(=O)N2[C@H](C(=O)N([C@H](C(=O)N(C(C(=O)N([C@H](C(=O)N([C@@H](C(=O)N[C@H](C(N([C@H](C(N[C@H](C(N3[C@H](C(N4[C@H](C(N([C@H](C(NC(C1C)CCCC#C)=O)[C@H](CC)C)C)=O)CCC4)=O)CCC3)=O)CC(C)C)=O)C(C)C)C)=O)C)C)C)CC5=CC=CC=C5)C)COC)C)C(C)C)C)CCC2)C)C(C)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C(N1C(CCC1)C(=O)NC2C(OC3=CC=C(C=C3)C=CNC(=O)C(NC2=O)CC4=CC=CC=C4)C5=CC=CC=C5)C(N(C)C)C(CC)C', "
               "'Isoleucine derivative with modifications: N-substituted'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(=O)NCC(O)=O)[C@@H](N)CC(C)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N1[C@@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)C)CCCN=C(N)N)C(C)C)CC2=CC=C(O)C=C2)[C@H](CC)C)CC=3NC=NC3', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1NCCCCC(NC(=O)C(NC(=O)NC(C(=O)O)C(CC)C)C(C)C)C(NC(C=C1)C(C)C)=O', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C1OC(CC(=O)NC(C(=O)NC(C(=O)NC(CC(C)C)C(NC(C(NC(C(NC(C(NC1C(CC)C)=O)CC(C)C)=O)CC(=O)O)=O)C(C)C)=O)CC(C)C)CCC(=O)N)CCCCCCCCC(CC)C', "
               "'Isoleucine derivative with modifications: O-substituted, "
               "N-acylated'), "
               "('S(CCC1NC(=O)C(N(C(=O)C(NC(=O)C(C(C)C)NC(C(CCCCNC1=O)NC(=O)NC(C(=O)O)C(CC)C)=O)CCC2=CC=CC=C2)C)CCC3=CC=CC=C3)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)[C@H](CC)C', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)CN)CC=1NC=NC1', "
               "'Isoleucine derivative with modifications: N-acylated'), "
               "('O=C(O)[C@H](N(C(=O)[C@@H](NC(=O)C)[C@@H](CC)C)C)CC1=CC=C(O)C=C1', "
               "'Isoleucine derivative with modifications: N-acylated')]\n"
               'False negatives: '
               "[('S(=O)(=O)(NC(=O)[C@@H](N)[C@H](CC)C)CC(=O)N[C@]1(C(=O)O)[C@H]2[C@H](C(C(=O)N)=CN(C2)C)C[C@@H]1OC(=O)[C@@H](N)[C@H](C3=CC=CC=C3)C', "
               "'No isoleucine core structure found'), "
               "('O=C(N([C@H](C(=O)N[C@H](C(=O)N([C@H](C(=O)NCC(=O)N)[C@@H](CC)C)C)[C@@H](CC)C)C(C)C)C)[C@@H](N(C(=O)[C@@H](CCCCC#C)C)C)C(C)C', "
               "'Appears to be a peptide containing isoleucine rather than an "
               "isoleucine derivative'), "
               "('CCC(C)C(C(=O)OC1=CC2=C(C=C1)C3=C(CCC3)C(=O)O2)NS(=O)(=O)C4=CC=C(C=C4)C', "
               "'No isoleucine core structure found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 6331,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.8571428571428571,
    'f1': 0.10619469026548672,
    'accuracy': 0.9843118981050015}