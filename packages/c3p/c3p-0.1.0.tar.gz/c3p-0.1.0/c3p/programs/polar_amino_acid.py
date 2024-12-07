"""
Classifies: CHEBI:26167 polar amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polar_amino_acid(smiles: str):
    """
    Determines if a molecule is a polar amino acid.
    A polar amino acid has:
    1. An amino group (-NH2)
    2. A carboxylic acid group (-COOH) 
    3. A side chain capable of hydrogen bonding (contains O, N, or S with H-bond capability)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polar amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for amino group
    amino_pattern = Chem.MolFromSmarts('[NH2]C')
    if not mol.HasSubstructMatch(amino_pattern):
        return False, "No amino group (-NH2) found"

    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxylic acid group (-COOH) found"

    # Get the alpha carbon (connected to both NH2 and COOH)
    alpha_c_pattern = Chem.MolFromSmarts('[NH2]C([*])C(=O)[OH]')
    matches = mol.GetSubstructMatches(alpha_c_pattern)
    if not matches:
        return False, "No alpha carbon found with correct connectivity"

    # Get the side chain atoms by excluding the backbone
    backbone_atoms = set(matches[0][:2] + matches[0][-2:])  # NH2, alpha-C, C, OH
    side_chain_atoms = set(range(mol.GetNumAtoms())) - backbone_atoms

    # Check for polar groups in side chain
    polar_patterns = [
        ('[OH]', 'hydroxyl'),
        ('[NH,NH2,NH3]', 'amino'),
        ('[SH]', 'thiol'),
        ('C(=O)[NH2]', 'amide'),
        ('C(=O)[OH]', 'carboxylic acid'),
        ('[NH]C(=[NH])[NH2]', 'guanidino')
    ]

    polar_groups_found = []
    for pattern, group_name in polar_patterns:
        pattern_mol = Chem.MolFromSmarts(pattern)
        matches = mol.GetSubstructMatches(pattern_mol)
        for match in matches:
            # Check if the match involves side chain atoms
            if any(idx in side_chain_atoms for idx in match):
                polar_groups_found.append(group_name)

    if not polar_groups_found:
        return False, "No polar groups found in side chain"

    return True, f"Polar amino acid with side chain containing: {', '.join(set(polar_groups_found))}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26167',
                          'name': 'polar amino acid',
                          'definition': 'Any amino acid whose side chain is '
                                        'capable of forming one or more '
                                        'hydrogen bonds.',
                          'parents': ['CHEBI:33709']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 8767,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9887273137188592}