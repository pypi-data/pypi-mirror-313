"""
Classifies: CHEBI:22331 alkylamines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alkylamines(smiles: str):
    """
    Determines if a molecule is an alkylamine (amine with alkyl substituents).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alkylamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Find all nitrogen atoms
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]
    if not n_atoms:
        return False, "No nitrogen atoms found"
        
    # Check each nitrogen atom
    alkylamine_n = []
    for n_atom in n_atoms:
        # Skip if nitrogen is in ring or aromatic
        if n_atom.IsInRing() or n_atom.GetIsAromatic():
            continue
            
        # Get neighbors
        neighbors = n_atom.GetNeighbors()
        
        # Count carbon neighbors that are sp3 hybridized (alkyl groups)
        alkyl_count = sum(1 for neigh in neighbors 
                         if neigh.GetAtomicNum() == 6 and 
                         neigh.GetHybridization() == Chem.HybridizationType.SP3)
        
        # Must have at least one alkyl group
        if alkyl_count > 0:
            alkylamine_n.append((n_atom.GetIdx(), alkyl_count))
            
    if not alkylamine_n:
        return False, "No nitrogen atoms with alkyl substituents found"
        
    # Format reason string
    reasons = []
    for n_idx, alkyl_count in alkylamine_n:
        reasons.append(f"N{n_idx} has {alkyl_count} alkyl substituent(s)")
        
    return True, "; ".join(reasons)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22331',
                          'name': 'alkylamines',
                          'definition': 'Any amine formally derived from '
                                        'ammonia by replacing one, two or '
                                        'three hydrogen atoms by alkyl groups.',
                          'parents': ['CHEBI:32952']},
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
    'num_true_positives': 28,
    'num_false_positives': 100,
    'num_true_negatives': 123,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.21875,
    'recall': 0.7368421052631579,
    'f1': 0.3373493975903615,
    'accuracy': 0.578544061302682}