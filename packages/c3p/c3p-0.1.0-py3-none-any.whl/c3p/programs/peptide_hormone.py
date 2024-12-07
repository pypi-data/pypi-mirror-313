"""
Classifies: CHEBI:25905 peptide hormone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_peptide_hormone(smiles: str):
    """
    Determines if a molecule is a peptide hormone based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is likely a peptide hormone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check molecular weight - peptide hormones are typically >500 Da
    mol_weight = Descriptors.ExactMolWt(mol)
    if mol_weight < 500:
        return False, "Molecular weight too low for peptide hormone"

    # Count peptide bonds (-C(=O)-N-)
    peptide_bond_pattern = Chem.MolFromSmarts('[C](=O)-[NH]')
    peptide_bonds = len(mol.GetSubstructMatches(peptide_bond_pattern))
    if peptide_bonds < 3:  # Minimum 3 peptide bonds (tetrapeptide)
        return False, "Too few peptide bonds"

    # Check for presence of amino acids
    amino_acids = 0
    
    # Common amino acid side chains patterns
    aa_patterns = [
        '[NH2]-[CH]-C(=O)',  # Basic amino acid structure
        'CC(C)C[CH]',  # Leu
        'CC[CH](C)',  # Ile
        'CC[CH]',  # Val
        'C1=CC=C(C=C1)C[CH]',  # Phe
        'C1=CC=C(O)C=C1C[CH]',  # Tyr
        'C1=CNC=N1C[CH]',  # His
        'NCCCCC[CH]',  # Lys
        'NC(=N)NCCC[CH]',  # Arg
        'SCC[CH]',  # Met
        'OCC[CH]',  # Ser
        'O[CH](C)C[CH]',  # Thr
        'NCC(=O)',  # Gly
        'CC[CH]',  # Ala
        'N[CH]CC(=O)',  # Asn
        'N[CH]CCC(=O)',  # Gln
        'OC(=O)CC[CH]',  # Glu
        'OC(=O)C[CH]',  # Asp
        'C1=CNc2c1cccc2C[CH]',  # Trp
        'SCC[CH]'  # Cys
    ]

    for pattern in aa_patterns:
        substructure = Chem.MolFromSmarts(pattern)
        if substructure:
            matches = mol.GetSubstructMatches(substructure)
            amino_acids += len(matches)

    if amino_acids < 3:  # Minimum 3 amino acid residues
        return False, "Too few amino acid residues detected"

    # Check for basic characteristics that suggest bioactivity
    # - Presence of basic residues (Lys, Arg) often important for receptor binding
    basic_residues = Chem.MolFromSmarts('NC(=N)N') # Arg guanidino group
    lys_pattern = Chem.MolFromSmarts('NCCCCC')
    
    has_basic = False
    if basic_residues and mol.HasSubstructMatch(basic_residues):
        has_basic = True
    if lys_pattern and mol.HasSubstructMatch(lys_pattern):
        has_basic = True

    # Calculate rotatable bonds - peptide hormones typically flexible
    rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    
    if peptide_bonds >= 3 and amino_acids >= 3 and has_basic and rot_bonds >= 10:
        return True, f"Likely peptide hormone: contains {peptide_bonds} peptide bonds, {amino_acids} amino acid residues, basic residues, and appropriate flexibility"
    elif peptide_bonds >= 3 and amino_acids >= 3:
        return True, f"Possible peptide hormone: contains {peptide_bonds} peptide bonds and {amino_acids} amino acid residues but lacks typical basic residues"
    else:
        return False, "Structure lacks characteristics of peptide hormones"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25905',
                          'name': 'peptide hormone',
                          'definition': 'Any peptide with hormonal activity in '
                                        'animals, whether endocrine, '
                                        'neuroendocrine, or paracrine.',
                          'parents': ['CHEBI:16670']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 1406,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9336870026525199}