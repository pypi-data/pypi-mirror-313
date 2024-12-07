"""
Classifies: CHEBI:24586 hexosamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_hexosamine(smiles: str):
    """
    Determines if a molecule is a hexosamine (6-carbon amino monosaccharide with at least one 
    alcoholic hydroxy group replaced by an amino group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hexosamine, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"

        # Find cyclic sugar rings
        ri = mol.GetRingInfo()
        rings = ri.AtomRings()
        
        # Look for 6-membered or 5-membered rings that could be sugar rings
        sugar_rings = []
        for ring in rings:
            if len(ring) in [5,6]:
                # Check if ring contains oxygen and carbons
                atoms = [mol.GetAtomWithIdx(i) for i in ring]
                if any(atom.GetSymbol() == 'O' for atom in atoms):
                    carbons = sum(1 for atom in atoms if atom.GetSymbol() == 'C')
                    if carbons >= 4: # Need at least 4 carbons for a sugar ring
                        sugar_rings.append(ring)
        
        if not sugar_rings:
            return False, "No sugar rings found"

        # For each potential sugar ring, look for:
        # 1. At least one NH2/NH group
        # 2. Multiple OH groups
        # 3. Total of 6 carbons in/attached to ring
        for ring in sugar_rings:
            ring_atoms = set(ring)
            ring_and_neighbors = set()
            
            # Get ring atoms and their immediate neighbors
            for atom_idx in ring:
                ring_and_neighbors.add(atom_idx)
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    ring_and_neighbors.add(neighbor.GetIdx())
            
            # Count carbons, nitrogens with H, and oxygens with H
            carbon_count = 0
            amino_groups = 0
            hydroxy_groups = 0
            
            for atom_idx in ring_and_neighbors:
                atom = mol.GetAtomWithIdx(atom_idx)
                if atom.GetSymbol() == 'C':
                    carbon_count += 1
                elif atom.GetSymbol() == 'N':
                    # Check if nitrogen has hydrogens
                    if atom.GetTotalNumHs() > 0:
                        amino_groups += 1
                elif atom.GetSymbol() == 'O':
                    # Check if oxygen has a hydrogen (hydroxy group)
                    if atom.GetTotalNumHs() > 0:
                        hydroxy_groups += 1
            
            if carbon_count >= 6 and amino_groups >= 1 and hydroxy_groups >= 1:
                return True, f"Found hexosamine structure with {carbon_count} carbons, {amino_groups} amino groups, and {hydroxy_groups} hydroxy groups"
                
        return False, "Structure does not meet hexosamine criteria"

    except Exception as e:
        return None, f"Error analyzing structure: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24586',
                          'name': 'hexosamine',
                          'definition': 'Any 6-carbon amino monosaccharide '
                                        'with at least one alcoholic hydroxy '
                                        'group replaced by an amino group.',
                          'parents': ['CHEBI:60926']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 25,
    'num_false_positives': 100,
    'num_true_negatives': 1369,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2,
    'recall': 1.0,
    'f1': 0.33333333333333337,
    'accuracy': 0.9330655957161981}