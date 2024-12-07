"""
Classifies: CHEBI:140920 triazolothiadiazole
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_triazolothiadiazole(smiles: str):
    """
    Determines if a molecule is a triazolothiadiazole (contains fused triazole and thiadiazole rings).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a triazolothiadiazole, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for fused triazole-thiadiazole core
    # Matches both [1,2,4]triazolo[3,4-b][1,3,4]thiadiazole and [1,2,4]triazolo[3,4-c][1,3,4]thiadiazole
    triazolothiadiazole_pattern = Chem.MolFromSmarts('[#6,#7,#8,#16]1[#6,#7]=,:[#7][#6,#7]=,:[#7]2[#7]=,:[#6][#16][#6,#7]=,:[#7]12')
    
    if mol.HasSubstructMatch(triazolothiadiazole_pattern):
        # Get the atoms involved in the core structure
        match = mol.GetSubstructMatch(triazolothiadiazole_pattern)
        
        # Check if we have the required atoms
        core_atoms = [mol.GetAtomWithIdx(i) for i in match]
        
        # Count atoms of each type in core
        atom_counts = {}
        for atom in core_atoms:
            symbol = atom.GetSymbol()
            atom_counts[symbol] = atom_counts.get(symbol, 0) + 1
            
        # Verify we have the correct number of atoms for triazolothiadiazole core
        if atom_counts.get('N', 0) >= 4 and atom_counts.get('S', 0) == 1:
            # Check for aromaticity
            if all(atom.GetIsAromatic() for atom in core_atoms):
                return True, "Contains fused aromatic triazole-thiadiazole ring system"
            else:
                return False, "Contains triazole-thiadiazole structure but not fully aromatic"
    
    return False, "No triazolothiadiazole core structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140920',
                          'name': 'triazolothiadiazole',
                          'definition': 'Any organic heterobicyclic compound '
                                        'containing ortho-fused triazole and '
                                        'thiadiazole rings.',
                          'parents': [   'CHEBI:27171',
                                         'CHEBI:38101',
                                         'CHEBI:38106']},
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
    'num_true_negatives': 183914,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891254703234}