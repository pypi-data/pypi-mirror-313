"""
Classifies: CHEBI:140310 phenyl acetates
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phenyl_acetates(smiles: str):
    """
    Determines if a molecule is a phenyl acetate - an acetate ester formed by condensation 
    of acetic acid with a phenol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phenyl acetate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of phenol acetate substructure
    phenyl_acetate_pattern = Chem.MolFromSmarts('c-OC(=O)C')
    if not mol.HasSubstructMatch(phenyl_acetate_pattern):
        return False, "No phenyl acetate group found"

    # Find all phenyl rings
    aromatic_rings = mol.GetAromaticAtoms()
    if not aromatic_rings:
        return False, "No aromatic rings found"

    # Get all matches of phenyl acetate pattern
    matches = mol.GetSubstructMatches(phenyl_acetate_pattern)
    
    # For each match, verify it's connected to a phenyl ring
    valid_matches = []
    for match in matches:
        phenoxy_oxygen = mol.GetAtomWithIdx(match[1])  # O atom in O-C(=O)C
        phenyl_carbon = mol.GetAtomWithIdx(match[0])   # aromatic C
        
        # Verify the carbon is part of aromatic ring
        if phenyl_carbon.GetIsAromatic():
            # Verify the oxygen is connected to aromatic carbon and acetyl group
            if (phenoxy_oxygen.GetDegree() == 2 and 
                any(n.GetIsAromatic() for n in phenoxy_oxygen.GetNeighbors())):
                valid_matches.append(match)

    if not valid_matches:
        return False, "No valid phenyl acetate groups found"

    # Count number of phenyl acetate groups
    num_acetates = len(valid_matches)
    
    # Get other substituents on the aromatic ring(s)
    other_substituents = []
    for atom in mol.GetAtoms():
        if atom.GetIsAromatic():
            for neighbor in atom.GetNeighbors():
                if not neighbor.GetIsAromatic() and neighbor.GetIdx() not in [m[1] for m in valid_matches]:
                    other_substituents.append(neighbor.GetSymbol())

    substituent_info = ""
    if other_substituents:
        substituent_info = f" with additional substituents: {', '.join(set(other_substituents))}"
    
    return True, f"Phenyl acetate with {num_acetates} acetate group(s){substituent_info}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140310',
                          'name': 'phenyl acetates',
                          'definition': 'An acetate ester obtained by formal '
                                        'condensation of the carboxy group of '
                                        'acetic acid with the hydroxy group of '
                                        'any phenol.',
                          'parents': ['CHEBI:22712', 'CHEBI:47622']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 33160,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9969936566154586}