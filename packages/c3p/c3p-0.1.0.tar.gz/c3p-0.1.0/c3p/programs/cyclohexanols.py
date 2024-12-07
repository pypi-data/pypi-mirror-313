"""
Classifies: CHEBI:23480 cyclohexanols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyclohexanols(smiles: str):
    """
    Determines if a molecule is a cyclohexanol (alcohol with OH group(s) attached to cyclohexane).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclohexanol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Get ring information
    rings = mol.GetRingInfo()
    
    # Find 6-membered rings
    six_mem_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            six_mem_rings.append(ring)
            
    if not six_mem_rings:
        return False, "No 6-membered rings found"
        
    # For each 6-membered ring, check if it's a cyclohexane with OH
    for ring in six_mem_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Check if ring is cyclohexane (all sp3 carbons)
        if not all(atom.GetSymbol() == 'C' and atom.GetHybridization() == Chem.HybridizationType.SP3 
                  for atom in ring_atoms):
            continue
            
        # Look for OH groups attached to ring
        oh_count = 0
        for ring_atom in ring_atoms:
            for neighbor in ring_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O':
                    # Check if oxygen is part of OH (has H)
                    if neighbor.GetTotalNumHs() > 0:
                        oh_count += 1
                        
        if oh_count > 0:
            return True, f"Found cyclohexane ring with {oh_count} OH group(s)"
            
    return False, "No cyclohexane ring with OH groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23480',
                          'name': 'cyclohexanols',
                          'definition': 'An alcohol in which one or more '
                                        'hydroxy groups are attached to a '
                                        'cyclohexane skeleton.',
                          'parents': ['CHEBI:30879']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 2055,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9537251272559001}