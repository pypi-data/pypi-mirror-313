"""
Classifies: CHEBI:23778 dihydroxybenzoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_dihydroxybenzoic_acid(smiles: str):
    """
    Determines if a molecule is a dihydroxybenzoic acid or derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a dihydroxybenzoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find aromatic rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
                
    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"
        
    # For each aromatic ring, check if it has:
    # 1. Two OH groups directly attached
    # 2. A carboxylic acid group (-COOH) attached
    for ring_atoms in aromatic_rings:
        hydroxy_count = 0
        has_carboxyl = False
        
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            
            # Check neighbors of ring atoms
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    # Check for OH groups
                    if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                        hydroxy_count += 1
                    
                    # Check for carboxylic acid group
                    elif neighbor.GetSymbol() == 'C':
                        # Look for C(=O)O pattern
                        for n2 in neighbor.GetNeighbors():
                            if n2.GetSymbol() == 'O':
                                if n2.GetTotalNumHs() == 1:  # OH part
                                    for n3 in neighbor.GetNeighbors():
                                        if n3.GetSymbol() == 'O' and n3.GetTotalNumHs() == 0:  # =O part
                                            has_carboxyl = True
                                            
        if hydroxy_count >= 2 and has_carboxyl:
            return True, f"Found aromatic ring with {hydroxy_count} hydroxy groups and carboxylic acid group"
            
    return False, "Structure does not match dihydroxybenzoic acid pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23778',
                          'name': 'dihydroxybenzoic acid',
                          'definition': 'Any member of the class of  '
                                        'hydroxybenzoic acids carrying  two '
                                        'phenolic hydroxy groups on the '
                                        'benzene ring and its derivatives.',
                          'parents': ['CHEBI:24676']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 103609,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9990357914224005}