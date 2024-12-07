"""
Classifies: CHEBI:197504 very long-chain fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_very_long_chain_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a very long-chain fatty alcohol (C23-C27).
    Must be a secondary alcohol with linear carbon chain.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a very long-chain fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of exactly one OH group
    oh_pattern = Chem.MolFromSmarts('[OH1]')
    if len(mol.GetSubstructMatches(oh_pattern)) != 1:
        return False, "Must contain exactly one OH group"
    
    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 23 or carbon_count > 27:
        return False, f"Carbon count {carbon_count} outside C23-C27 range"
        
    # Check if linear
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        return False, "Contains rings - must be linear"
        
    # Check if saturated (no double/triple bonds)
    if any(bond.GetBondTypeAsDouble() > 1 for bond in mol.GetBonds()):
        return False, "Contains unsaturated bonds"
        
    # Check if it's a secondary alcohol
    oh_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            oh_atom = atom
            break
            
    if oh_atom:
        carbon_neighbors = [n for n in oh_atom.GetNeighbors() if n.GetSymbol() == 'C']
        if len(carbon_neighbors) != 1:
            return False, "Oxygen must be bonded to exactly one carbon"
            
        c_atom = carbon_neighbors[0]
        c_neighbors = len([n for n in c_atom.GetNeighbors() if n.GetSymbol() == 'C'])
        
        # Must be secondary alcohol (carbon bonded to OH has exactly 2 other carbons)
        if c_neighbors != 2:
            return False, "Must be a secondary alcohol"
            
        # Check if branched
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'C':
                carbon_neighbors = len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'C'])
                if carbon_neighbors > 2:
                    return False, "Must be unbranched"
                    
        return True, f"C{carbon_count} secondary fatty alcohol"
        
    return False, "Invalid alcohol structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197504',
                          'name': 'very long-chain fatty alcohol',
                          'definition': 'A fatty alcohol which has a chain '
                                        'length between C23 and C27.',
                          'parents': ['CHEBI:24026']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.5882352941176471 is too low.\n'
               "True positives: [('CCCCCCCCCCCCCCCC(O)CCCCCCC', 'C23 secondary "
               "fatty alcohol'), ('CCCCCCCCCCCCC(O)CCCCCCCCCCC', 'C24 "
               "secondary fatty alcohol'), ('CCCCCCCCCCCCCCCCC(O)CCCCCCC', "
               "'C24 secondary fatty alcohol'), ('CCCCCCCCCCCCCCC(O)CCCCCCCC', "
               "'C23 secondary fatty alcohol'), ('CCCCCCCCCCCCCCCCCC(O)CCCCC', "
               "'C23 secondary fatty alcohol')]\n"
               "False positives: [('CC(C)CCCCCCCCCCCCCCCCCCCCCO', 'C24 primary "
               "fatty alcohol'), ('CCC(C)CCCCCCCCCCCCCCCCCCCCCCCO', 'C27 "
               "primary fatty alcohol'), ('CCC(C)CCCCCCCCCCCCCCCCCCCO', 'C23 "
               "primary fatty alcohol'), ('CCC(C)CCCCCCCCCCCCCCCCCCCCCO', 'C25 "
               "primary fatty alcohol'), ('CC(C)CCCCCCCCCCCCCCCCCCCCCCCO', "
               "'C26 primary fatty alcohol'), "
               "('OC(CCCCCCCCCCCCCCCCCCCC)(CCCC)C', 'C26 tertiary fatty "
               "alcohol'), ('C(CCCCCCCCCCCCCCCCO)CCCCCCCCCC', 'C27 primary "
               "fatty alcohol')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 0,
    'num_true_negatives': 183884,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0}