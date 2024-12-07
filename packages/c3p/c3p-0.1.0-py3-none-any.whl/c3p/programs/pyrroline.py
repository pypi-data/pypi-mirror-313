"""
Classifies: CHEBI:23763 pyrroline
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_pyrroline(smiles: str):
    """
    Determines if a molecule contains a pyrroline (dihydropyrrole) structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains pyrroline, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Get ring info
    rings = mol.GetRingInfo()
    
    # Look for 5-membered rings
    five_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 5:
            five_rings.append(ring)
            
    if not five_rings:
        return False, "No 5-membered rings found"
        
    # Check each 5-membered ring for pyrroline pattern
    for ring in five_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Need exactly one nitrogen in ring
        nitrogens = [a for a in ring_atoms if a.GetSymbol() == 'N']
        if len(nitrogens) != 1:
            continue
            
        # Count double bonds in ring
        double_bonds = 0
        for bond in mol.GetBonds():
            if bond.GetBeginAtomIdx() in ring and bond.GetEndAtomIdx() in ring:
                if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                    double_bonds += 1
                    
        # Pyrroline should have exactly one double bond
        if double_bonds == 1:
            return True, "Contains pyrroline (5-membered ring with 1 N and 1 double bond)"
            
    return False, "No pyrroline pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23763',
                          'name': 'pyrroline',
                          'definition': 'Any organic heteromonocyclic compound '
                                        'with a structure based on a '
                                        'dihydropyrrole.',
                          'parents': ['CHEBI:25693', 'CHEBI:38101']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 9840,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.5,
    'f1': 0.1016949152542373,
    'accuracy': 0.9893488745980707}