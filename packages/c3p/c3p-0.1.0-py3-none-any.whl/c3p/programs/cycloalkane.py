"""
Classifies: CHEBI:23453 cycloalkane
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cycloalkane(smiles: str):
    """
    Determines if a molecule is a cycloalkane (saturated monocyclic hydrocarbon).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cycloalkane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains only carbon and hydrogen
    atoms = mol.GetAtoms()
    if not all(atom.GetSymbol() in ['C', 'H'] for atom in atoms):
        return False, "Contains non C/H atoms"

    # Get ring information
    rings = mol.GetRingInfo()
    ring_count = rings.NumRings()
    
    # Must have exactly one ring
    if ring_count != 1:
        return False, f"Has {ring_count} rings, must have exactly 1 ring"

    # Get the ring atoms
    ring = rings.AtomRings()[0]
    ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
    
    # Check if any ring atoms are aromatic or unsaturated
    for atom in ring_atoms:
        if atom.GetIsAromatic():
            return False, "Contains aromatic ring"
        if any(bond.GetBondTypeAsDouble() != 1.0 for bond in atom.GetBonds()):
            return False, "Contains unsaturated bonds"

    # Count carbons in ring and side chains
    ring_size = len(ring)
    total_carbons = sum(1 for atom in atoms if atom.GetSymbol() == 'C')
    side_chain_carbons = total_carbons - ring_size
    
    if side_chain_carbons > 0:
        return True, f"{ring_size}-membered cycloalkane with {side_chain_carbons} carbons in side chains"
    else:
        return True, f"{ring_size}-membered cycloalkane"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23453',
                          'name': 'cycloalkane',
                          'definition': 'Saturated monocyclic hydrocarbons '
                                        '(with or without side chains).',
                          'parents': ['CHEBI:33654', 'CHEBI:33664']},
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
    'num_true_positives': 3,
    'num_false_positives': 15,
    'num_true_negatives': 183881,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.16666666666666666,
    'recall': 1.0,
    'f1': 0.2857142857142857,
    'accuracy': 0.9999184334879472}