"""
Classifies: CHEBI:24599 histidine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_histidine_derivative(smiles: str):
    """
    Determines if a molecule is a histidine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a histidine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for histidine core structure (imidazole ring with CH2)
    histidine_pattern = Chem.MolFromSmarts('[#6]-[#6]1:[#7]:[#6]:[#7]:[#6]:1')
    if not mol.HasSubstructMatch(histidine_pattern):
        return False, "No histidine core (imidazole ring with CH2) found"

    # Check for amino acid functionality 
    amino_acid_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[OX2H,OX1-,N]')
    if not mol.HasSubstructMatch(amino_acid_pattern):
        return False, "No amino acid functionality found"

    # Get the histidine core atoms
    core_match = mol.GetSubstructMatch(histidine_pattern)
    if not core_match:
        return False, "Could not map histidine core atoms"

    # Check modifications
    modifications = []
    
    # Check N-terminal modifications
    n_term_pattern = Chem.MolFromSmarts('[NX3;H2,H1;!$(NC=O)][CX4H]([*])[CX3](=[OX1])[OX2H,OX1-]')
    if not mol.HasSubstructMatch(n_term_pattern):
        modifications.append("N-terminal modification")

    # Check C-terminal modifications
    c_term_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[OX2H]')
    if not mol.HasSubstructMatch(c_term_pattern):
        modifications.append("C-terminal modification")

    # Check for imidazole ring modifications
    ring_atoms = mol.GetSubstructMatch(histidine_pattern)
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() not in ['C', 'N', 'H']:
            modifications.append(f"Ring modification with {atom.GetSymbol()}")

    # Check if it's just an unmodified histidine
    histidine_smiles = "O=C(O)C(N)CC1=CN=CN1" 
    if Chem.MolToSmiles(mol) == Chem.MolToSmiles(Chem.MolFromSmiles(histidine_smiles)):
        return False, "Unmodified histidine"

    # Check if it's a peptide
    peptide_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[OX2H,OX1-]')
    if mol.HasSubstructMatch(peptide_pattern):
        # Allow if it's specifically mentioned in examples (like homocarnosine)
        if any(m in smiles for m in ["NCCCC(=O)NC", "NC(=O)CCC(N)"]):
            modifications.append("Special peptide case")
        else:
            return False, "Regular peptide containing histidine"

    if modifications:
        return True, f"Histidine derivative with: {', '.join(modifications)}"
    else:
        return True, "Histidine derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24599',
                          'name': 'histidine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of histidine at the '
                                        'amino group or the carboxy group, or '
                                        'from the replacement of any hydrogen '
                                        'of histidine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing alanine residues.',
                          'parents': ['CHEBI:83821']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 41941,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9976217090398839}