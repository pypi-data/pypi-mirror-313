"""
Classifies: CHEBI:22726 benzophenones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzophenones(smiles: str):
    """
    Determines if a molecule is a benzophenone (aromatic ketone with carbonyl group bonded to 2 phenyl groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzophenone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for C(=O)c1ccccc1 pattern (benzophenone core)
    pattern = Chem.MolFromSmarts('[$(C(=O)(c1[c,n]:[c,n]:[c,n]:[c,n]:[c,n]1)c1[c,n]:[c,n]:[c,n]:[c,n]:[c,n]1)]')
    if not mol.HasSubstructMatch(pattern):
        return False, "No benzophenone core structure found"

    # Get matches for the pattern
    matches = mol.GetSubstructMatches(pattern)
    
    for match in matches:
        carbonyl_idx = match[0]
        carbonyl = mol.GetAtomWithIdx(carbonyl_idx)
        
        # Verify carbonyl group
        if carbonyl.GetAtomicNum() != 6 or len([n for n in carbonyl.GetNeighbors() if n.GetAtomicNum() == 8 and n.GetTotalNumHs() == 0]) != 1:
            continue
            
        # Check that the carbonyl carbon is connected to exactly two aromatic rings
        aromatic_ring_atoms = []
        for neighbor in carbonyl.GetNeighbors():
            if neighbor.GetIsAromatic():
                ring_system = []
                for atom in mol.GetAtomWithIdx(neighbor.GetIdx()).GetNeighbors():
                    if atom.GetIsAromatic():
                        ring_system.append(atom.GetIdx())
                if len(ring_system) >= 2:  # At least 2 aromatic neighbors indicates ring
                    aromatic_ring_atoms.append(ring_system)
                    
        if len(aromatic_ring_atoms) == 2:
            # Check for substituents
            substituents = []
            for atom in mol.GetAtoms():
                if atom.GetIsAromatic():
                    for neighbor in atom.GetNeighbors():
                        if not neighbor.GetIsAromatic() and neighbor.GetAtomicNum() != 6:
                            substituents.append(neighbor.GetSymbol())
            
            if len(set(substituents)) > 0:
                return True, f"Benzophenone with substituents: {', '.join(set(substituents))}"
            else:
                return True, "Unsubstituted benzophenone"
                
    return False, "Structure contains C(=O) but not connected to two aromatic rings"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22726',
                          'name': 'benzophenones',
                          'definition': 'Any aromatic ketone in which the '
                                        'carbonyl group is bonded to 2 phenyl '
                                        'groups.',
                          'parents': ['CHEBI:76224']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
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
    'num_true_positives': 19,
    'num_false_positives': 100,
    'num_true_negatives': 14612,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.15966386554621848,
    'recall': 0.95,
    'f1': 0.27338129496402874,
    'accuracy': 0.9931441759435243}