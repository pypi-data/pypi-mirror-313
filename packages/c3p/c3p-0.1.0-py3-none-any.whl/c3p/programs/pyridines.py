"""
Classifies: CHEBI:26421 pyridines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_pyridines(smiles: str):
    """
    Determines if a molecule is a pyridine or substituted pyridine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pyridine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get rings
    rings = mol.GetRingInfo()
    
    # Check for 6-membered rings
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered rings found"
        
    # Find pyridine rings - 6-membered aromatic rings with 1 nitrogen
    pyridine_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if aromatic and contains exactly 1 nitrogen
            if (all(atom.GetIsAromatic() for atom in atoms) and
                sum(1 for atom in atoms if atom.GetSymbol() == 'N') == 1):
                pyridine_rings.append(ring)
                
    if not pyridine_rings:
        return False, "No pyridine rings found"
        
    # Get substituents
    ring_atoms = set(pyridine_rings[0]) 
    substituents = []
    
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                substituents.append(neighbor.GetSymbol())
                
    if len(substituents) > 0:
        return True, f"Substituted pyridine with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted pyridine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26421',
                          'name': 'pyridines',
                          'definition': 'Any organonitrogen heterocyclic '
                                        'compound based on a pyridine skeleton '
                                        'and its substituted derivatives.',
                          'parents': ['CHEBI:25693', 'CHEBI:38101']},
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
    'num_true_positives': 233,
    'num_false_positives': 100,
    'num_true_negatives': 1866,
    'num_false_negatives': 26,
    'num_negatives': None,
    'precision': 0.6996996996996997,
    'recall': 0.8996138996138996,
    'f1': 0.7871621621621622,
    'accuracy': 0.9433707865168539}