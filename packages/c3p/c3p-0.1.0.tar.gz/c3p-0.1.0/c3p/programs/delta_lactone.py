"""
Classifies: CHEBI:18946 delta-lactone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_delta_lactone(smiles: str):
    """
    Determines if a molecule is a delta-lactone (6-membered lactone ring).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a delta-lactone, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate ring info
    rings = mol.GetRingInfo()
    
    # Find all 6-membered rings
    six_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            six_rings.append(ring)
            
    if not six_rings:
        return False, "No 6-membered rings found"
        
    # Check each 6-membered ring for lactone pattern
    for ring in six_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Look for O-C(=O) pattern in ring
        for i, atom in enumerate(ring_atoms):
            if atom.GetSymbol() == 'O':
                # Get next atom in ring
                next_idx = (i + 1) % 6
                next_atom = ring_atoms[next_idx]
                
                if next_atom.GetSymbol() == 'C':
                    # Check if carbon is double bonded to oxygen
                    for bond in next_atom.GetBonds():
                        other_atom = bond.GetOtherAtom(next_atom)
                        if (other_atom.GetSymbol() == 'O' and 
                            bond.GetBondType() == Chem.rdchem.BondType.DOUBLE and
                            other_atom.GetIdx() not in ring):
                            return True, "Contains 6-membered lactone ring"
                            
    return False, "No lactone pattern found in 6-membered rings"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18946',
                          'name': 'delta-lactone',
                          'definition': 'A lactone having a six-membered '
                                        'lactone ring.',
                          'parents': ['CHEBI:25000']},
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
    'num_true_positives': 49,
    'num_false_positives': 100,
    'num_true_negatives': 5446,
    'num_false_negatives': 26,
    'num_negatives': None,
    'precision': 0.3288590604026846,
    'recall': 0.6533333333333333,
    'f1': 0.43749999999999994,
    'accuracy': 0.9775840597758406}