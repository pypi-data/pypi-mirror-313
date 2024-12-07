"""
Classifies: CHEBI:132130 hydroxyquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMolFrags

def is_hydroxyquinone(smiles: str):
    """
    Determines if a molecule is a hydroxyquinone (quinone with one or more hydroxy substituents
    on the quinone ring system).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxyquinone, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find quinone patterns
    # Pattern 1: para-quinone
    patt1 = Chem.MolFromSmarts('[#6]=O.[#6]=O.[$([#6]1=,:[#6][#6]=,:[#6][#6]=,:[#6]1),$([#6]1=,:[#6][#6]=,:[#6][#6]=,:[#6][#6]1)]')
    # Pattern 2: ortho-quinone
    patt2 = Chem.MolFromSmarts('[#6](=O)-[#6]=,:[#6]-[#6](=O)')
    
    matches1 = mol.GetSubstructMatches(patt1)
    matches2 = mol.GetSubstructMatches(patt2)
    
    if not (matches1 or matches2):
        return False, "No quinone moiety found"

    # Find hydroxy groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    
    if not oh_matches:
        return False, "No hydroxy groups found"

    # For each quinone pattern found, check if any hydroxy groups are attached to the quinone ring
    quinone_atoms = set()
    for match in matches1:
        quinone_atoms.update(match)
    for match in matches2:
        quinone_atoms.update(match)

    # Check if any OH groups are connected to quinone ring atoms
    for oh_match in oh_matches:
        oh_atom = mol.GetAtomWithIdx(oh_match[0])
        for neighbor in oh_atom.GetNeighbors():
            if neighbor.GetIdx() in quinone_atoms:
                num_oh = len([m for m in oh_matches if mol.GetAtomWithIdx(m[0]).GetNeighbors()[0].GetIdx() in quinone_atoms])
                return True, f"Found hydroxyquinone with {num_oh} hydroxy group(s) on quinone ring"

    return False, "No hydroxy groups attached to quinone ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132130',
                          'name': 'hydroxyquinone',
                          'definition': 'Any quinone in which one or more of '
                                        'the carbons making up the quinone '
                                        'moiety is substituted by a hydroxy '
                                        'group.',
                          'parents': ['CHEBI:33822', 'CHEBI:36141']},
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 814,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.8914223669923995}