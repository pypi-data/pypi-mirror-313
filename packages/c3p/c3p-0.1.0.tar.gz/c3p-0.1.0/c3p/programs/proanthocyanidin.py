"""
Classifies: CHEBI:26267 proanthocyanidin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_proanthocyanidin(smiles: str):
    """
    Determines if a molecule is a proanthocyanidin (oligomeric flavonoid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a proanthocyanidin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for minimum size - proanthocyanidins are oligomers
    num_atoms = mol.GetNumAtoms()
    if num_atoms < 30:  # Rough minimum size for a dimer
        return False, "Molecule too small to be a proanthocyanidin oligomer"
        
    # Check for presence of multiple hydroxyflavan units
    # Hydroxyflavan core has characteristic O-C-C pattern in ring
    pattern = Chem.MolFromSmarts('[O]-[#6]-[#6]-1-[#6]-[#6]-[#6](-[OH])-[#6]-[#6]-1')
    matches = mol.GetSubstructMatches(pattern)
    
    if len(matches) < 2:
        return False, "Does not contain multiple hydroxyflavan units"
        
    # Check for condensed structure (C-C or C-O-C linkages between units)
    pattern2 = Chem.MolFromSmarts('[#6]-[#6]~[#6]-[O,#6]-[#6]~[#6]-[#6]')
    if not mol.HasSubstructMatch(pattern2):
        return False, "Units are not condensed/linked appropriately"
        
    # Check for characteristic hydroxyl groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    num_oh = len(mol.GetSubstructMatches(oh_pattern))
    
    if num_oh < 4:  # Proanthocyanidins typically have multiple OH groups
        return False, "Insufficient hydroxyl groups"
        
    # Count aromatic rings
    aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    if aromatic_rings < 4:  # At least 2 units with 2 aromatic rings each
        return False, "Insufficient aromatic rings for oligomeric structure"
        
    return True, f"Proanthocyanidin with {len(matches)} hydroxyflavan units"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26267',
                          'name': 'proanthocyanidin',
                          'definition': 'A flavonoid oligomer obtained by the '
                                        'the condensation of two or more units '
                                        'of hydroxyflavans.',
                          'parents': ['CHEBI:26848', 'CHEBI:72720']},
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
    'num_true_positives': 0,
    'num_false_positives': 1,
    'num_true_negatives': 183877,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999673705562776}