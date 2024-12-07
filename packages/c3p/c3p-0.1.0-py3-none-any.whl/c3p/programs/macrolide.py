"""
Classifies: CHEBI:25106 macrolide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_macrolide(smiles: str):
    """
    Determines if a molecule is a macrolide (macrocyclic lactone with 12+ membered ring derived from polyketide).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a macrolide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for lactone group (cyclic ester)
    lactone_pattern = Chem.MolFromSmarts('[C,c](=[O,o])[O,o][C,c]')
    if not mol.HasSubstructMatch(lactone_pattern):
        return False, "No lactone group found"
        
    # Get ring information
    rings = mol.GetRingInfo()
    ring_sizes = [len(ring) for ring in rings.AtomRings()]
    
    # Check for macrocycle (12+ membered ring)
    if not any(size >= 12 for size in ring_sizes):
        return False, "No macrocycle (12+ membered ring) found"
        
    # Check for polyketide-like features (alternating C-C and C=O bonds)
    polyketide_pattern = Chem.MolFromSmarts('[C,c]-[C,c](=[O,o])')
    if not mol.HasSubstructMatch(polyketide_pattern):
        return False, "No polyketide-like pattern found"
        
    # Find largest ring containing lactone
    largest_lactone_ring = 0
    for ring in rings.AtomRings():
        ring_mol = Chem.PathToSubmol(mol, list(ring))
        if ring_mol.HasSubstructMatch(lactone_pattern):
            largest_lactone_ring = max(largest_lactone_ring, len(ring))
            
    if largest_lactone_ring < 12:
        return False, "Lactone ring is smaller than 12 members"
        
    return True, f"Macrolide with {largest_lactone_ring}-membered lactone ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25106',
                          'name': 'macrolide',
                          'definition': 'A macrocyclic lactone with a ring of '
                                        'twelve or more members derived from a '
                                        'polyketide.',
                          'parents': ['CHEBI:26188', 'CHEBI:63944']},
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
    'num_true_positives': 26,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.20634920634920634,
    'f1': 0.34210526315789475,
    'accuracy': 0.20634920634920634}