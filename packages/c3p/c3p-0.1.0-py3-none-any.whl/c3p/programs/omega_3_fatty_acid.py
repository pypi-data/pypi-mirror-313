"""
Classifies: CHEBI:25681 omega-3 fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_omega_3_fatty_acid(smiles: str):
    """
    Determines if a molecule is an omega-3 fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an omega-3 fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if len(mol.GetSubstructMatches(carboxylic_pattern)) == 0:
        return False, "No carboxylic acid group found"

    # Find the carbon chain
    # First find the carboxylic carbon
    matches = mol.GetSubstructMatches(carboxylic_pattern)
    if not matches:
        return False, "Could not identify carboxylic carbon"
    carboxylic_carbon = matches[0][0]
    
    # Get all carbons in longest chain from carboxylic end
    def get_carbon_chain(atom_idx, visited=None):
        if visited is None:
            visited = set()
            
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() != 'C':
            return []
            
        visited.add(atom_idx)
        current_chain = [atom_idx]
        
        # Get neighboring carbons
        neighbors = [n for n in atom.GetNeighbors() 
                    if n.GetSymbol() == 'C' and n.GetIdx() not in visited]
        
        # Continue along longest chain
        max_subchain = []
        for n in neighbors:
            subchain = get_carbon_chain(n.GetIdx(), visited.copy())
            if len(subchain) > len(max_subchain):
                max_subchain = subchain
                
        return current_chain + max_subchain
    
    chain = get_carbon_chain(carboxylic_carbon)
    
    if len(chain) < 4:  # Need at least 4 carbons
        return False, "Carbon chain too short"
        
    # Check for double bond at omega-3 position (3rd from methyl end)
    methyl_end = chain[-1]
    omega3_carbon = chain[-3]
    
    # Get bond between omega-3 carbon and next carbon
    for neighbor in mol.GetAtomWithIdx(omega3_carbon).GetNeighbors():
        if neighbor.GetIdx() in chain:
            bond = mol.GetBondBetweenAtoms(omega3_carbon, neighbor.GetIdx())
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                return True, "Found double bond at omega-3 position"
                
    return False, "No double bond at omega-3 position"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25681',
                          'name': 'omega-3 fatty acid',
                          'definition': 'A family of polyunsaturated fatty '
                                        'acids that have in common a final '
                                        'carbon-carbon double bond in the '
                                        'omega-3 position, i.e., the third '
                                        'bond from the methyl end of the fatty '
                                        'acid.',
                          'parents': ['CHEBI:26208', 'CHEBI:59549']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Mol' object has no attribute "
               "'HasSubstructMatches'",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 8422,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9882697947214076}