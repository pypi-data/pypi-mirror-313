"""
Classifies: CHEBI:25903 peptide antibiotic
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

def is_peptide_antibiotic(smiles: str):
    """
    Determines if a molecule is a peptide antibiotic.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a peptide antibiotic, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check molecular weight - peptide antibiotics are typically large molecules
    mw = Descriptors.ExactMolWt(mol)
    if mw < 400:
        return False, "Molecular weight too low for peptide antibiotic"

    # Count peptide bonds (amide bonds)
    amide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])')
    num_amide_bonds = len(mol.GetSubstructMatches(amide_pattern))
    if num_amide_bonds < 3:
        return False, "Too few peptide bonds"

    # Count amino groups
    amino_pattern = Chem.MolFromSmarts('[NX3;H2,H1;!$(NC=O)]')
    num_amino_groups = len(mol.GetSubstructMatches(amino_pattern))
    
    # Look for basic amino acid residues (Lys, Arg, His patterns)
    basic_aa_pattern = Chem.MolFromSmarts('[NX3;H2,H1]CC[CH2]')  # Simplified pattern
    num_basic_aa = len(mol.GetSubstructMatches(basic_aa_pattern))

    # Calculate ratio of heteroatoms
    num_n = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    total_atoms = mol.GetNumAtoms()
    heteroatom_ratio = (num_n + num_o) / total_atoms

    # Combine criteria for classification
    if (num_amide_bonds >= 3 and  # Multiple peptide bonds
        heteroatom_ratio > 0.2 and  # High heteroatom content
        (num_amino_groups >= 2 or num_basic_aa >= 1) and  # Contains amino groups
        mw >= 400):  # Reasonable molecular weight
        
        reasons = []
        reasons.append(f"Contains {num_amide_bonds} peptide bonds")
        reasons.append(f"Molecular weight: {mw:.1f}")
        if num_amino_groups > 0:
            reasons.append(f"Contains {num_amino_groups} amino groups")
        if num_basic_aa > 0:
            reasons.append(f"Contains basic amino acid residues")
        reasons.append(f"Heteroatom ratio: {heteroatom_ratio:.2f}")
        
        return True, "; ".join(reasons)

    return False, "Does not meet structural criteria for peptide antibiotic"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25903',
                          'name': 'peptide antibiotic',
                          'definition': 'A chemically diverse class of '
                                        'peptides that exhibit antimicrobial '
                                        'properties.',
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1373,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.93234100135318}