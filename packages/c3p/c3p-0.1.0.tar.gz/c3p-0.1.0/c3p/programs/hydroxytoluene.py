"""
Classifies: CHEBI:24751 hydroxytoluene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxytoluene(smiles: str):
    """
    Determines if a molecule is a hydroxytoluene (toluene with one or more OH groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxytoluene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find aromatic rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check for benzene ring with all carbons
    has_valid_ring = False
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if all(atom.GetSymbol() == 'C' for atom in atoms):
            has_valid_ring = True
            ring_atoms = set(ring)
            break

    if not has_valid_ring:
        return False, "No benzene ring found"

    # Look for methyl group attached to ring
    has_methyl = False
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                if neighbor.GetSymbol() == 'C':
                    # Check if it's a methyl group by counting hydrogens
                    if neighbor.GetTotalNumHs() == 3:
                        has_methyl = True
                        break
    
    if not has_methyl:
        return False, "No methyl group found attached to ring"

    # Look for hydroxyl groups attached to ring
    hydroxy_count = 0
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                    hydroxy_count += 1

    if hydroxy_count == 0:
        return False, "No hydroxyl groups found"

    return True, f"Found toluene with {hydroxy_count} hydroxyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24751',
                          'name': 'hydroxytoluene',
                          'definition': 'Any member of the class of  toluenes '
                                        'carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:27024', 'CHEBI:33853']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Atom' object has no attribute 'GetIsImplicit'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 5959,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9835092348284961}