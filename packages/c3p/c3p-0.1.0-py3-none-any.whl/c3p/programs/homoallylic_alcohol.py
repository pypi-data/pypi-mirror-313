"""
Classifies: CHEBI:134362 homoallylic alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_homoallylic_alcohol(smiles: str):
    """
    Determines if a molecule contains a homoallylic alcohol group.
    A homoallylic alcohol has a hydroxy group beta to a double bond.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains homoallylic alcohol, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Add explicit hydrogens
    mol = Chem.AddHs(mol)
    
    # SMARTS pattern for homoallylic alcohol:
    # [OH]-[CH2]-[CH2]-C=C
    # The pattern looks for:
    # - An OH group
    # - Connected to a carbon (beta carbon)
    # - Connected to another carbon (alpha carbon) 
    # - Connected to a carbon involved in a double bond
    pattern = Chem.MolFromSmarts('[OH]-[#6]-[#6]-[#6]=[#6]')
    
    if mol.HasSubstructMatch(pattern):
        # Find all matches
        matches = mol.GetSubstructMatches(pattern)
        
        # For each match, verify it's an aliphatic alcohol
        for match in matches:
            oh_atom = mol.GetAtomWithIdx(match[0])
            beta_carbon = mol.GetAtomWithIdx(match[1])
            alpha_carbon = mol.GetAtomWithIdx(match[2])
            double_bond_carbon = mol.GetAtomWithIdx(match[3])
            
            # Check if carbons are aliphatic (not aromatic)
            if not any(atom.GetIsAromatic() for atom in [beta_carbon, alpha_carbon, double_bond_carbon]):
                return True, "Contains homoallylic alcohol group: OH beta to double bond"
                
    return False, "No homoallylic alcohol group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134362',
                          'name': 'homoallylic alcohol',
                          'definition': 'An aliphatic alcohol where the '
                                        'hydroxy carbon is beta to a double '
                                        'bond.',
                          'parents': ['CHEBI:2571', 'CHEBI:78840']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1707,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9448123620309051}