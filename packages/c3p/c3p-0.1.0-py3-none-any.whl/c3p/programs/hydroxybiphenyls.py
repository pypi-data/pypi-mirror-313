"""
Classifies: CHEBI:24681 hydroxybiphenyls
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroxybiphenyls(smiles: str):
    """
    Determines if a molecule is a hydroxybiphenyl (biphenyl with one or more hydroxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxybiphenyl, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # First check if the molecule contains biphenyl structure
    biphenyl_pattern = Chem.MolFromSmarts('c1ccccc1-c1ccccc1')
    if not mol.HasSubstructMatch(biphenyl_pattern):
        return False, "No biphenyl core structure found"

    # Check for hydroxy groups attached to aromatic carbons
    hydroxy_pattern = Chem.MolFromSmarts('cO')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    if not hydroxy_matches:
        return False, "No hydroxy groups attached to aromatic rings"

    # Find all hydroxy groups attached to the biphenyl system
    biphenyl_matches = mol.GetSubstructMatches(biphenyl_pattern)
    biphenyl_atoms = set()
    for match in biphenyl_matches:
        biphenyl_atoms.update(match)

    hydroxy_on_biphenyl = 0
    hydroxy_positions = []
    
    for match in hydroxy_matches:
        aromatic_c = match[0]
        if aromatic_c in biphenyl_atoms:
            hydroxy_on_biphenyl += 1
            # Get position of hydroxy group
            for atom in mol.GetAtomWithIdx(aromatic_c).GetNeighbors():
                if atom.GetAtomicNum() == 8:  # Oxygen
                    hydroxy_positions.append(str(aromatic_c + 1))

    if hydroxy_on_biphenyl == 0:
        return False, "No hydroxy groups attached to biphenyl system"

    position_str = ", ".join(hydroxy_positions)
    return True, f"Hydroxybiphenyl with {hydroxy_on_biphenyl} hydroxy group(s) at position(s): {position_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24681',
                          'name': 'hydroxybiphenyls',
                          'definition': 'Any member of the class of biphenyls '
                                        'that has one or more hydroxy groups '
                                        'attached to the benzenoid ring '
                                        'system.',
                          'parents': ['CHEBI:22888', 'CHEBI:33853']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 8727,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9886762541048579}