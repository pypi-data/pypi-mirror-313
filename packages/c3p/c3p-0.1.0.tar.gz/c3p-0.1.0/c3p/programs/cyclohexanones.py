"""
Classifies: CHEBI:23482 cyclohexanones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_cyclohexanones(smiles: str):
    """
    Determines if a molecule is a cyclohexanone (cyclic 6-membered ketone) or derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cyclohexanone, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    
    # Find 6-membered rings
    six_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            six_rings.append(ring)
            
    if not six_rings:
        return False, "No 6-membered rings found"

    # For each 6-membered ring, check if it contains a ketone
    for ring in six_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Check if ring is aliphatic (not aromatic)
        if any(atom.GetIsAromatic() for atom in ring_atoms):
            continue
            
        # Look for ketone pattern (C(=O)C) in ring
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            
            # Check if atom is carbon
            if atom.GetSymbol() != 'C':
                continue
                
            # Check for double-bonded oxygen
            carbonyl_o = False
            ring_carbons = 0
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and \
                   mol.GetBondBetweenAtoms(atom_idx, neighbor.GetIdx()).GetBondType() == Chem.BondType.DOUBLE:
                    carbonyl_o = True
                # Count carbons that are part of the ring
                if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() in ring:
                    ring_carbons += 1
                    
            # Valid ketone pattern found in ring
            if carbonyl_o and ring_carbons == 2:
                # Get substituents
                substituents = []
                for ring_atom in ring_atoms:
                    for neighbor in ring_atom.GetNeighbors():
                        if neighbor.GetIdx() not in ring:
                            substituents.append(neighbor.GetSymbol())
                
                if len(substituents) > 0:
                    return True, f"Substituted cyclohexanone with substituents: {', '.join(set(substituents))}"
                else:
                    return True, "Unsubstituted cyclohexanone"
                    
    return False, "No cyclohexanone pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23482',
                          'name': 'cyclohexanones',
                          'definition': 'Any alicyclic ketone based on a '
                                        'cyclohexane skeleton and its '
                                        'substituted derivatives thereof.',
                          'parents': ['CHEBI:36132']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1924,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9507146377525875}