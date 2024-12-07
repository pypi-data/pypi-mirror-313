"""
Classifies: CHEBI:143212 thienopyrimidine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_thienopyrimidine(smiles: str):
    """
    Determines if a molecule is a thienopyrimidine (pyrimidine ring fused to thiophene).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a thienopyrimidine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate the ring information
    rings = mol.GetRingInfo()
    
    # Find all 6-membered rings (potential pyrimidine)
    six_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring has exactly 2 nitrogens
            n_count = sum(1 for atom in atoms if atom.GetSymbol() == 'N')
            if n_count == 2:
                six_rings.append(ring)
                
    if not six_rings:
        return False, "No pyrimidine ring found"

    # Find all 5-membered rings (potential thiophene)
    five_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring has exactly 1 sulfur
            s_count = sum(1 for atom in atoms if atom.GetSymbol() == 'S')
            if s_count == 1:
                five_rings.append(ring)
                
    if not five_rings:
        return False, "No thiophene ring found"

    # Check for fusion between pyrimidine and thiophene rings
    for six_ring in six_rings:
        for five_ring in five_rings:
            # Find shared atoms between rings
            shared = set(six_ring).intersection(set(five_ring))
            if len(shared) == 2:  # Two shared atoms indicates fusion
                # Verify ring atoms
                six_atoms = [mol.GetAtomWithIdx(i) for i in six_ring]
                five_atoms = [mol.GetAtomWithIdx(i) for i in five_ring]
                
                # Check pyrimidine ring
                n_atoms = [a for a in six_atoms if a.GetSymbol() == 'N']
                if len(n_atoms) != 2:
                    continue
                    
                # Check thiophene ring
                s_atoms = [a for a in five_atoms if a.GetSymbol() == 'S']
                if len(s_atoms) != 1:
                    continue
                    
                return True, "Contains fused thiophene-pyrimidine ring system"
                
    return False, "No fused thiophene-pyrimidine ring system found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143212',
                          'name': 'thienopyrimidine',
                          'definition': 'A class of aromatic heterobicyclic '
                                        'compounds each of which contains a '
                                        'pyrimidine ring ortho fused to a '
                                        '5-membered thiophene ring.',
                          'parents': [   'CHEBI:27171',
                                         'CHEBI:38101',
                                         'CHEBI:38106']},
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 72026,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9986136719670609}