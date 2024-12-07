"""
Classifies: CHEBI:24433 group
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_group(smiles: str):
    """
    Determines if a molecule is a group, defined as 'A defined linked collection of atoms 
    or a single atom within a molecular entity.'

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a group, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of attachment point(s) marked with *
    attachment_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == '*':
            attachment_atoms.append(atom.GetIdx())
            
    if not attachment_atoms:
        return False, "No attachment points (*) found - not a group"

    # Count number of atoms (excluding attachment points)
    num_real_atoms = len([a for a in mol.GetAtoms() if a.GetSymbol() != '*'])
    
    # Single atom groups
    if num_real_atoms == 1:
        return True, "Single atom group"
        
    # Check connectivity using BFS
    def bfs_connected(mol, start_idx, exclude_atoms):
        visited = set([start_idx])
        queue = [start_idx]
        while queue:
            current = queue.pop(0)
            for neighbor in mol.GetAtomWithIdx(current).GetNeighbors():
                n_idx = neighbor.GetIdx()
                if n_idx not in visited and n_idx not in exclude_atoms:
                    visited.add(n_idx)
                    queue.append(n_idx)
        return visited

    # Start BFS from first non-attachment atom
    start_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != '*':
            start_atom = atom.GetIdx()
            break
    
    if start_atom is None:
        return False, "No non-attachment atoms found"
        
    # Check if all non-attachment atoms are connected
    connected_atoms = bfs_connected(mol, start_atom, set(attachment_atoms))
    all_non_attachment_atoms = set([a.GetIdx() for a in mol.GetAtoms() if a.GetSymbol() != '*'])
    
    if connected_atoms != all_non_attachment_atoms:
        return False, "Multiple disconnected fragments found"
        
    # Must be a connected collection of multiple atoms with attachment point(s)
    return True, f"Connected group of {num_real_atoms} atoms with {len(attachment_atoms)} attachment point(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24433',
                          'name': 'group',
                          'definition': 'A defined linked collection of atoms '
                                        'or a single atom within a molecular '
                                        'entity.',
                          'parents': ['CHEBI:24431']},
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
    'num_true_positives': 274,
    'num_false_positives': 100,
    'num_true_negatives': 5049,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.732620320855615,
    'recall': 0.9647887323943662,
    'f1': 0.8328267477203648,
    'accuracy': 0.9797533591017854}