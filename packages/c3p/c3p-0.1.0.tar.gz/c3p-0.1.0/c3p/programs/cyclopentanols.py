"""
Classifies: CHEBI:23495 cyclopentanols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyclopentanols(smiles: str):
    """
    Determines if a molecule is a cyclopentanol (alcohol with OH group attached to cyclopentane).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclopentanol, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    
    # Find 5-membered rings
    five_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 5:
            # Check if ring is cyclopentane (all carbons, all single bonds)
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            bonds = []
            is_cyclopentane = True
            
            for i in range(len(ring)):
                # Check atoms are carbons
                if atoms[i].GetSymbol() != 'C':
                    is_cyclopentane = False
                    break
                    
                # Get bonds in ring
                next_idx = (i + 1) % 5
                bond = mol.GetBondBetweenAtoms(ring[i], ring[next_idx])
                bonds.append(bond)
                
                # Check bonds are single
                if bond.GetBondType() != Chem.BondType.SINGLE:
                    is_cyclopentane = False
                    break
            
            if is_cyclopentane:
                five_rings.append(ring)

    if not five_rings:
        return False, "No cyclopentane rings found"

    # Check for OH groups attached to cyclopentane
    oh_count = 0
    attachment_positions = []
    
    for ring in five_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            
            # Check neighbors for OH groups
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                    # Verify it's a single bond
                    bond = mol.GetBondBetweenAtoms(atom_idx, neighbor.GetIdx())
                    if bond.GetBondType() == Chem.BondType.SINGLE:
                        oh_count += 1
                        attachment_positions.append(atom_idx)

    if oh_count == 0:
        return False, "No hydroxyl groups attached to cyclopentane ring"
        
    return True, f"Found {oh_count} hydroxyl group(s) attached to cyclopentane ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23495',
                          'name': 'cyclopentanols',
                          'definition': 'An alcohol in which one or more '
                                        'hydroxy groups are attached to a '
                                        'cyclopentane skeleton.',
                          'parents': ['CHEBI:23493', 'CHEBI:30879']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 4985,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9803420483585611}