"""
Classifies: CHEBI:23424 cyanides
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyanides(smiles: str):
    """
    Determines if a molecule contains a cyanide group (C#N).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains cyanide group, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # SMARTS pattern for cyanide group (C#N)
    cyanide_pattern = Chem.MolFromSmarts('C#N')
    
    # Find matches
    matches = mol.GetSubstructMatches(cyanide_pattern)
    
    if not matches:
        return False, "No cyanide (C#N) group found"
        
    # Get all cyanide carbons
    cyanide_carbons = [match[0] for match in matches]
    
    # Get all cyanide nitrogens 
    cyanide_nitrogens = [match[1] for match in matches]
    
    # Verify triple bond between C and N
    for c, n in zip(cyanide_carbons, cyanide_nitrogens):
        bond = mol.GetBondBetweenAtoms(c, n)
        if bond.GetBondType() != Chem.BondType.TRIPLE:
            return False, "C-N bond is not a triple bond"
            
    # Count number of cyanide groups
    num_cyanides = len(matches)
    
    # Get all atoms connected to cyanide carbons
    substituents = []
    for c in cyanide_carbons:
        atom = mol.GetAtomWithIdx(c)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in cyanide_nitrogens:
                substituents.append(neighbor.GetSymbol())
                
    return True, f"Contains {num_cyanides} cyanide group(s) with substituents: {', '.join(set(substituents))}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23424',
                          'name': 'cyanides',
                          'definition': 'Salts and C-organyl derivatives of '
                                        'hydrogen cyanide, HC#N.',
                          'parents': ['CHEBI:35352']},
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
    'num_true_positives': 66,
    'num_false_positives': 100,
    'num_true_negatives': 7178,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.39759036144578314,
    'recall': 1.0,
    'f1': 0.5689655172413793,
    'accuracy': 0.9863834422657952}