"""
Classifies: CHEBI:177332 carbotetracyclic compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_carbotetracyclic_compound(smiles: str):
    """
    Determines if a molecule is a carbotetracyclic compound (containing exactly 4 carbocyclic rings).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is carbotetracyclic, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Get ring information
    rings = mol.GetRingInfo()
    ring_list = rings.AtomRings()
    
    # Count number of rings
    if len(ring_list) != 4:
        return False, f"Contains {len(ring_list)} rings, not exactly 4 rings"
        
    # Check that all rings are carbocyclic (only carbon atoms)
    for ring in ring_list:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(atom.GetSymbol() == 'C' for atom in atoms):
            return False, "Contains non-carbocyclic ring(s)"
            
    # Check ring sizes
    ring_sizes = [len(ring) for ring in ring_list]
    
    # Success case
    return True, f"Contains 4 carbocyclic rings of sizes: {ring_sizes}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:177332',
                          'name': 'carbotetracyclic compound',
                          'definition': 'A carbopolyclic compound comprising '
                                        'of four carbocyclic rings.',
                          'parents': ['CHEBI:177333', 'CHEBI:35294']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 3282,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9704491725768322}