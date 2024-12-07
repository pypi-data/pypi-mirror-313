"""
Classifies: CHEBI:26214 porphyrins
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdqueries

def is_porphyrins(smiles: str):
    """
    Determines if a molecule is a porphyrin based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a porphyrin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Check for presence of 4 pyrrole rings
    pyrrole_pattern = Chem.MolFromSmarts('[nH]1cccc1')
    pyrrole_matches = mol.GetSubstructMatches(pyrrole_pattern)
    
    n_pattern = Chem.MolFromSmarts('[n]')
    n_matches = mol.GetSubstructMatches(n_pattern)
    
    if len(pyrrole_matches) + len(n_matches) < 4:
        return False, "Does not contain 4 pyrrole/pyrrole-like rings"

    # Check for macrocyclic structure (at least one ring of size >= 16)
    ri = mol.GetRingInfo()
    ring_sizes = [len(ring) for ring in ri.AtomRings()]
    if not any(size >= 16 for size in ring_sizes):
        return False, "Does not contain macrocyclic structure"
        
    # Check for conjugated system connecting pyrroles
    conjugated_pattern = Chem.MolFromSmarts('c:c')
    if not mol.HasSubstructMatch(conjugated_pattern):
        return False, "Does not have conjugated system"
        
    # Check for metal coordination (optional)
    metal_pattern = Chem.MolFromSmarts('[Mg,Fe,Zn,Cu,Co,Ni,Pd]')
    has_metal = mol.HasSubstructMatch(metal_pattern)
    
    # Check for substituents
    substituents = []
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)O')):
        substituents.append('carboxyl')
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C=C')):
        substituents.append('vinyl')
    if mol.HasSubstructMatch(Chem.MolFromSmarts('CO')):
        substituents.append('methoxy')
    if mol.HasSubstructMatch(Chem.MolFromSmarts('CC')):
        substituents.append('alkyl')
        
    reason = "Contains 4 pyrrole rings in macrocyclic structure"
    if has_metal:
        reason += f" with metal coordination"
    if substituents:
        reason += f" and substituents: {', '.join(substituents)}"
        
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26214',
                          'name': 'porphyrins',
                          'definition': 'Natural pigments containing a '
                                        'fundamental skeleton of four pyrrole '
                                        'nuclei united through the '
                                        'alpha-positions by four methine '
                                        'groups to form a macrocyclic '
                                        'structure.',
                          'parents': ['CHEBI:36309']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 62527,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.5,
    'f1': 0.12903225806451613,
    'accuracy': 0.9982759446386668}