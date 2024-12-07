"""
Classifies: CHEBI:134043 phenylureas
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_phenylureas(smiles: str):
    """
    Determines if a molecule is a phenylurea (urea with at least one N substituted by phenyl/substituted phenyl).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phenylurea, False otherwise
        str: Reason for classification
    """
    # Check valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Standardize the molecule
    clean_mol = rdMolStandardize.Cleanup(mol)
    
    # SMARTS pattern for urea group with at least one N connected to aromatic ring
    # [NH,NH2]-C(=O)-[NH,NH2] is the urea core
    # One N must be connected to a phenyl ring
    urea_phenyl_pattern = Chem.MolFromSmarts('[cR1]1[cR1][cR1][cR1][cR1][cR1]1-[NH]-C(=O)-[NH][#0,#6]')
    urea_phenyl_pattern2 = Chem.MolFromSmarts('[cR1]1[cR1][cR1][cR1][cR1][cR1]1-[NH]-C(=O)-[N]([#0,#6])[#0,#6]')
    
    # Find matches
    matches1 = clean_mol.GetSubstructMatches(urea_phenyl_pattern)
    matches2 = clean_mol.GetSubstructMatches(urea_phenyl_pattern2)
    
    if not (matches1 or matches2):
        return False, "No phenylurea structure found"
        
    # Get number of phenyl rings attached to urea
    phenyl_count = len(matches1) + len(matches2)
    
    # Check substituents on phenyl rings
    substituents = set()
    for match in matches1 + matches2:
        for atom_idx in match[:6]:  # First 6 atoms are phenyl ring
            atom = clean_mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in match:
                    substituents.add(neighbor.GetSymbol())
    
    if substituents:
        return True, f"Phenylurea with {phenyl_count} phenyl ring(s) substituted with: {', '.join(sorted(substituents))}"
    else:
        return True, f"Unsubstituted phenylurea with {phenyl_count} phenyl ring(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134043',
                          'name': 'phenylureas',
                          'definition': 'Any member of the class of ureas in '
                                        'which at least one of the nitrogens '
                                        'of the urea moiety is substituted by '
                                        'a phenyl or substituted phenyl group.',
                          'parents': ['CHEBI:22712', 'CHEBI:47857']},
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
    'num_true_negatives': 4515,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9783643444396365}