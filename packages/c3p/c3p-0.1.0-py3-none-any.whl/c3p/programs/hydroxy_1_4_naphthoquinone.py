"""
Classifies: CHEBI:132157 hydroxy-1,4-naphthoquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxy_1_4_naphthoquinone(smiles: str):
    """
    Determines if a molecule is a hydroxy-1,4-naphthoquinone.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy-1,4-naphthoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for 1,4-naphthoquinone core
    # Two carbonyl groups in para position on a naphthalene ring
    naphthoquinone_pattern = Chem.MolFromSmarts('O=C1C=CC(=O)c2ccccc12')
    
    # SMARTS pattern for hydroxy group
    hydroxy_pattern = Chem.MolFromSmarts('[OH]')

    if naphthoquinone_pattern is None or hydroxy_pattern is None:
        return None, "Invalid SMARTS pattern"

    # Check for 1,4-naphthoquinone core
    if not mol.HasSubstructMatch(naphthoquinone_pattern):
        return False, "No 1,4-naphthoquinone core structure found"

    # Check for at least one hydroxy group
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxy group found"

    # Count hydroxy groups and determine their positions
    hydroxy_matches = len(mol.GetSubstructMatches(hydroxy_pattern))
    
    # Get the positions of hydroxy groups
    atom_indices = mol.GetSubstructMatches(hydroxy_pattern)
    positions = []
    for match in atom_indices:
        oh_atom = mol.GetAtomWithIdx(match[0])
        for neighbor in oh_atom.GetNeighbors():
            if neighbor.GetIsAromatic():
                positions.append("aromatic ring")
            else:
                positions.append("aliphatic")

    position_str = ", ".join(set(positions))
    return True, f"Hydroxy-1,4-naphthoquinone with {hydroxy_matches} hydroxy group(s) on {position_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132157',
                          'name': 'hydroxy-1,4-naphthoquinone',
                          'definition': 'Any member of the class of '
                                        '1,4-naphthoquinones in which the '
                                        'naphthoquinone moiety is substituted '
                                        'by at least one hydroxy group.',
                          'parents': ['CHEBI:132142', 'CHEBI:132155']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 38660,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9974202203131852}