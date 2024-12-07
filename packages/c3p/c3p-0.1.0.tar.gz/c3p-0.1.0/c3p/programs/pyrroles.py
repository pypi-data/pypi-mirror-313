"""
Classifies: CHEBI:26455 pyrroles
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_pyrroles(smiles: str):
    """
    Determines if a molecule contains a pyrrole ring (5-membered aromatic ring with one nitrogen).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains a pyrrole ring, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find all 5-membered rings
    rings = mol.GetRingInfo()
    five_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 5:
            five_rings.append(ring)
            
    if not five_rings:
        return False, "No 5-membered rings found"
        
    # Check each 5-membered ring
    for ring in five_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Count aromatic atoms and nitrogens in ring
        aromatic_count = sum(1 for atom in ring_atoms if atom.GetIsAromatic())
        n_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'N' and atom.GetIsAromatic())
        other_hetero = sum(1 for atom in ring_atoms if atom.GetSymbol() not in ['C','N'] and atom.GetIsAromatic())
        
        # Ring must be aromatic (all 5 atoms aromatic)
        if aromatic_count == 5:
            # Must have exactly one nitrogen
            if n_count == 1:
                # Must not have other heteroatoms
                if other_hetero == 0:
                    return True, "Contains pyrrole ring"
                    
    return False, "No pyrrole ring found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26455',
                          'name': 'pyrroles',
                          'definition': 'An azole that includes only one N '
                                        'atom and no other heteroatom as a '
                                        'part of the aromatic skeleton.',
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
    'num_true_positives': 26,
    'num_false_positives': 100,
    'num_true_negatives': 2192,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.20634920634920634,
    'recall': 0.896551724137931,
    'f1': 0.3354838709677419,
    'accuracy': 0.9556225764756571}