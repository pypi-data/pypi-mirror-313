"""
Classifies: CHEBI:131903 pyranopyrazole
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSymmSSSR

def is_pyranopyrazole(smiles: str):
    """
    Determines if a molecule contains a pyranopyrazole scaffold (pyran ring ortho-fused to pyrazole).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains pyranopyrazole, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for pyranopyrazole core
    # Matches a 6-membered oxygen-containing ring (pyran) fused to a 5-membered ring with 2 nitrogens (pyrazole)
    pyranopyrazole_pattern = Chem.MolFromSmarts('[O]1[C]=[C]2[N]=[N][C]([C]2[C]=[C]1)')
    
    if mol.HasSubstructMatch(pyranopyrazole_pattern):
        # Get all rings
        rings = GetSymmSSSR(mol)
        
        # Find the pyran and pyrazole rings
        pyran_ring = None
        pyrazole_ring = None
        
        for ring in rings:
            ring_atoms = list(ring)
            if len(ring_atoms) == 6:  # Potential pyran
                atoms = [mol.GetAtomWithIdx(i) for i in ring_atoms]
                if any(atom.GetSymbol() == 'O' for atom in atoms):
                    pyran_ring = ring
            elif len(ring_atoms) == 5:  # Potential pyrazole
                atoms = [mol.GetAtomWithIdx(i) for i in ring_atoms]
                n_count = sum(1 for atom in atoms if atom.GetSymbol() == 'N')
                if n_count == 2:
                    pyrazole_ring = ring
        
        if pyran_ring and pyrazole_ring:
            # Check if rings share exactly 2 atoms (ortho-fused)
            shared_atoms = set(pyran_ring).intersection(set(pyrazole_ring))
            if len(shared_atoms) == 2:
                # Get substituents
                all_ring_atoms = set(pyran_ring).union(set(pyrazole_ring))
                substituents = []
                
                for atom_idx in all_ring_atoms:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in all_ring_atoms:
                            substituents.append(neighbor.GetSymbol())
                
                if substituents:
                    return True, f"Pyranopyrazole with substituents: {', '.join(set(substituents))}"
                else:
                    return True, "Unsubstituted pyranopyrazole"
                    
        return False, "Contains pyran and pyrazole rings but not properly fused"
        
    return False, "No pyranopyrazole pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131903',
                          'name': 'pyranopyrazole',
                          'definition': 'An organic heterobicyclic compound '
                                        'whose skeleton consists of a pyran '
                                        'ring which is ortho-fused to a '
                                        'pyrazole ring.',
                          'parents': ['CHEBI:27171', 'CHEBI:38101']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183903,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836873185214}