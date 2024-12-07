"""
Classifies: CHEBI:23677 diazole
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_diazole(smiles: str):
    """
    Determines if a molecule contains a diazole ring (5-membered ring with 2 nitrogens and 3 carbons).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains a diazole ring, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all 5-membered rings
    ri = mol.GetRingInfo()
    rings = ri.AtomRings()
    
    # Check each 5-membered ring
    for ring in rings:
        if len(ring) != 5:
            continue
            
        # Count nitrogens and carbons in the ring
        n_count = 0
        c_count = 0
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'N':
                n_count += 1
            elif atom.GetSymbol() == 'C':
                c_count += 1
                
        # Check if ring has exactly 2 nitrogens and 3 carbons
        if n_count == 2 and c_count == 3:
            # Check if atoms in ring are aromatic
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                return True, "Contains diazole ring (5-membered aromatic ring with 2 N and 3 C atoms)"
                
    return False, "No diazole ring found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23677',
                          'name': 'diazole',
                          'definition': 'An azole that is either one of a pair '
                                        'of heterocyclic organic compounds '
                                        'comprising three carbon atoms and two '
                                        'nitrogen atoms arranged in a ring.',
                          'parents': ['CHEBI:68452']},
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
    'num_true_positives': 103,
    'num_false_positives': 100,
    'num_true_negatives': 2280,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.5073891625615764,
    'recall': 0.8956521739130435,
    'f1': 0.6477987421383649,
    'accuracy': 0.9551102204408818}