"""
Classifies: CHEBI:139051 phytoceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phytoceramide(smiles: str):
    """
    Determines if a molecule is a phytoceramide based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phytoceramide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for amide group (R-C(=O)-N-R)
    amide_pattern = Chem.MolFromSmarts('[CX3](=O)[NX3]')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide group found"

    # Check for phytosphingoid base core structure
    # Looking for -CH(OH)-CH(OH)-CH(NH-)-CH2OH or similar pattern
    sphingoid_pattern = Chem.MolFromSmarts('[CH1,CH2]([OH1])[CH1]([OH1])[CH1]([NH1])[CH2][OH1]')
    if not mol.HasSubstructMatch(sphingoid_pattern):
        return False, "No phytosphingoid base core structure found"

    # Check for long alkyl chain (fatty acid part)
    # Count carbons in longest chain from amide
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if amide_matches:
        amide_carbon = amide_matches[0][0]  # Get carbon atom index of first amide match
        fatty_acid_carbons = 0
        visited = set()
        
        def count_chain_carbons(atom_idx, current_chain=0):
            nonlocal fatty_acid_carbons
            if atom_idx in visited:
                return
            visited.add(atom_idx)
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'C':
                current_chain += 1
                fatty_acid_carbons = max(fatty_acid_carbons, current_chain)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'C':
                        count_chain_carbons(neighbor.GetIdx(), current_chain)
                        
        count_chain_carbons(amide_carbon)
        
        if fatty_acid_carbons < 12:  # Typical fatty acids have 12+ carbons
            return False, "Fatty acid chain too short"

    # Optional: Check for sugar moiety (common in phytoceramides but not required)
    sugar_pattern = Chem.MolFromSmarts('[CH1]1[OH1,OR][CH1][CH1][CH1][CH1]([CH2][OH1,OR])O1')
    has_sugar = mol.HasSubstructMatch(sugar_pattern)

    if has_sugar:
        return True, "Phytoceramide with sugar moiety"
    else:
        return True, "Phytoceramide without sugar moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139051',
                          'name': 'phytoceramide',
                          'definition': 'A class of phytoceramides obtained by '
                                        'formal condensation of the carboxy '
                                        'group of any fatty acid with the '
                                        'amino group of any phytosphingoid '
                                        'base.',
                          'parents': ['CHEBI:83273', 'CHEBI:84403']},
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
    'num_true_positives': 6,
    'num_false_positives': 7,
    'num_true_negatives': 183762,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.46153846153846156,
    'recall': 0.375,
    'f1': 0.41379310344827586,
    'accuracy': 0.9999075006121283}