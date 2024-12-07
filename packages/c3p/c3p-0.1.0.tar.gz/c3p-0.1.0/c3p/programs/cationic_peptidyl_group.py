"""
Classifies: CHEBI:134400 cationic peptidyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cationic_peptidyl_group(smiles: str):
    """
    Determines if a molecule contains a cationic peptidyl group.
    A cationic peptidyl group is defined as an organic cationic group obtained by protonation 
    of any peptide group; major species at pH 7.3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains a cationic peptidyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of peptide bonds (C(=O)N)
    peptide_pattern = Chem.MolFromSmarts('[C](=O)[NH]')
    if not mol.HasSubstructMatch(peptide_pattern):
        return False, "No peptide bonds found"

    # Check for presence of cationic groups
    cationic_patterns = [
        Chem.MolFromSmarts('[NH3+]'),  # Protonated amine
        Chem.MolFromSmarts('[NH2+]'),  # Protonated imine
        Chem.MolFromSmarts('[N+](C)(C)(C)'), # Quaternary amine
    ]
    
    cationic_groups = []
    for pattern in cationic_patterns:
        if mol.HasSubstructMatch(pattern):
            matches = mol.GetSubstructMatches(pattern)
            cationic_groups.extend(matches)
    
    if not cationic_groups:
        return False, "No cationic groups found"

    # Check for amino acid backbone pattern
    aa_pattern = Chem.MolFromSmarts('[NH2,NH3+,N+0,N+1][CH]C(=O)')
    if not mol.HasSubstructMatch(aa_pattern):
        return False, "No amino acid backbone found"

    # Count formal charges
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if total_charge <= 0:
        return False, "Total molecular charge is not positive"

    # Check for presence of wildcards (*) indicating this is a residue/group
    if '*' not in smiles:
        return False, "Not a residue/group (no wildcards found)"

    return True, f"Cationic peptidyl group with {len(cationic_groups)} cationic centers and total charge of +{total_charge}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134400',
                          'name': 'cationic peptidyl group',
                          'definition': 'An organic cationic group obtained by '
                                        'protonation of any peptide group; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:64769']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 3,
    'num_false_positives': 25,
    'num_true_negatives': 183878,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 1.0,
    'f1': 0.19354838709677416,
    'accuracy': 0.9998640609876784}