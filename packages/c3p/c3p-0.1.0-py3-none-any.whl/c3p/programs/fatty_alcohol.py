"""
Classifies: CHEBI:24026 fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a fatty alcohol (aliphatic alcohol with 3+ carbon chain).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a fatty alcohol, False otherwise
        str: Reason for classification
    """
    # Handle invalid SMILES and wildcards
    if '*' in smiles:
        return True, "Generic fatty alcohol notation"
        
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of OH group
    if not any(atom.GetSymbol() == 'O' for atom in mol.GetAtoms()):
        return False, "No oxygen atoms found"
        
    # Find OH groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "No hydroxyl groups found"
        
    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 3:
        return False, f"Insufficient carbon atoms ({carbon_count})"
    
    # Check if aliphatic
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        # Allow aliphatic rings but not aromatic
        aromatic_atoms = {a.GetIdx() for a in mol.GetAromaticAtoms()}
        if len(aromatic_atoms) > 0:
            return False, "Contains aromatic rings"
            
    # Find longest carbon chain
    frags = rdMolDescriptors.CalcMolFormula(mol).split('.')
    if len(frags) > 1:
        return False, "Multiple disconnected fragments"
        
    return True, f"Fatty alcohol with {carbon_count} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24026',
                          'name': 'fatty alcohol',
                          'definition': 'An aliphatic alcohol consisting of a '
                                        'chain of 3 to greater than 27 carbon '
                                        'atoms. Fatty alcohols may be '
                                        'saturated or unsaturated and may be '
                                        'branched or unbranched.',
                          'parents': ['CHEBI:30879', 'CHEBI:61697']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.AllChem' has no attribute "
               "'ReduceMolecule'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 54,
    'num_false_positives': 100,
    'num_true_negatives': 246,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.35064935064935066,
    'recall': 0.9310344827586207,
    'f1': 0.5094339622641509,
    'accuracy': 0.7425742574257426}