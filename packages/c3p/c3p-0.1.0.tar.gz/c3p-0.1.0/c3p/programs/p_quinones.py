"""
Classifies: CHEBI:25830 p-quinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_p_quinones(smiles: str):
    """
    Determines if a molecule is a p-quinone (para-quinone).
    A p-quinone has two oxo (=O) groups in para positions on a 6-membered quinonoid ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a p-quinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find all rings
    rings = mol.GetRingInfo()
    
    # Look for 6-membered rings
    for ring in rings.AtomRings():
        if len(ring) != 6:
            continue
            
        # Get ring atoms
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Count carbons and oxygens connected to ring
        carbons = []
        oxo_groups = []
        
        for i, atom in enumerate(ring_atoms):
            if atom.GetSymbol() == 'C':
                carbons.append(i)
                # Check for oxo groups (=O) connected to ring carbons
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 0:
                        bond = mol.GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
                        if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                            oxo_groups.append(i)

        # Need at least 4 carbons and exactly 2 oxo groups
        if len(carbons) < 4 or len(oxo_groups) != 2:
            continue

        # Check if oxo groups are para (1,4) to each other
        ring_size = 6
        distance = (oxo_groups[1] - oxo_groups[0]) % ring_size
        if distance == 3 or distance == -3:
            return True, "Found 6-membered ring with para oxo groups"

    return False, "No ring with para oxo groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25830',
                          'name': 'p-quinones',
                          'definition': 'A quinone in which the two oxo groups '
                                        'of the quinone are located para to '
                                        'each other on the 6-membered '
                                        'quinonoid ring.',
                          'parents': ['CHEBI:36141']},
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
    'num_true_positives': 40,
    'num_false_positives': 100,
    'num_true_negatives': 5509,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2857142857142857,
    'recall': 1.0,
    'f1': 0.4444444444444445,
    'accuracy': 0.9822977518144804}