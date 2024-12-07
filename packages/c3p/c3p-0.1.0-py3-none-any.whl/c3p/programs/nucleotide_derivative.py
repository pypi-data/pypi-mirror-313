"""
Classifies: CHEBI:231540 nucleotide derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_nucleotide_derivative(smiles: str):
    """
    Determines if a molecule is a nucleotide derivative, defined as a nucleoside phosphate 
    that is derived from a nucleotide.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nucleotide derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Check for nucleobase (purine or pyrimidine)
    purine_pattern = Chem.MolFromSmarts('c1ncnc2[nH]cnc12')  # Purine core
    pyrimidine_pattern = Chem.MolFromSmarts('c1[nH]c(=O)[nH]c(=O)c1')  # Pyrimidine core
    
    has_purine = mol.HasSubstructMatch(purine_pattern)
    has_pyrimidine = mol.HasSubstructMatch(pyrimidine_pattern)
    
    if not (has_purine or has_pyrimidine):
        return False, "No nucleobase (purine/pyrimidine) found"

    # Check for ribose/deoxyribose sugar
    sugar_pattern = Chem.MolFromSmarts('C1OC(CO)C(O)C1')
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "No ribose/deoxyribose sugar found"

    # Check if molecule has modifications/derivatizations
    base_nucleotide_size = 25  # Approximate size of basic nucleotide
    if rdMolDescriptors.CalcNumAtoms(mol) > base_nucleotide_size:
        if has_purine:
            base_type = "purine"
        else:
            base_type = "pyrimidine"
            
        return True, f"Nucleotide derivative with {base_type} base and additional modifications"
    else:
        return False, "Molecule appears to be unmodified nucleotide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:231540',
                          'name': 'nucleotide derivative',
                          'definition': 'A nucleoside phosphate that is '
                                        'derived from a nucleotide.',
                          'parents': ['CHEBI:25608']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.0}