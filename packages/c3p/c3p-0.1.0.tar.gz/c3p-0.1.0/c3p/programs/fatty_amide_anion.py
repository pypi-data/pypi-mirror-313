"""
Classifies: CHEBI:229684 fatty amide anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem.AllChem import GetMolFrags

def is_fatty_amide_anion(smiles: str):
    """
    Determines if a molecule is a fatty amide anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a fatty amide anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate anion group
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"

    # Check for amide group
    amide_pattern = Chem.MolFromSmarts('NC(=O)')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide group found"

    # Get the carbon chain length attached to the amide
    fatty_chain_pattern = Chem.MolFromSmarts('NC(=O)C*')
    matches = mol.GetSubstructMatches(fatty_chain_pattern)
    
    if not matches:
        return False, "No carbon chain attached to amide group"

    # Count carbons in longest chain attached to amide
    def count_chain_carbons(mol, start_idx):
        visited = set()
        stack = [(start_idx, 0)]
        max_length = 0
        
        while stack:
            current, length = stack.pop()
            if current in visited:
                continue
                
            visited.add(current)
            atom = mol.GetAtomWithIdx(current)
            
            if atom.GetSymbol() == 'C':
                max_length = max(max_length, length)
                
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
                    stack.append((neighbor.GetIdx(), length + 1))
                    
        return max_length

    # Get length of carbon chain from amide
    max_chain_length = 0
    for match in matches:
        chain_length = count_chain_carbons(mol, match[2])  # Start from carbon after amide
        max_chain_length = max(max_chain_length, chain_length)

    if max_chain_length < 2:
        return False, "Carbon chain too short to be considered fatty"

    # Check for double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    if double_bonds > 0:
        return True, f"Unsaturated fatty amide anion with {max_chain_length} carbons in longest chain and {double_bonds} double bonds"
    else:
        return True, f"Saturated fatty amide anion with {max_chain_length} carbons in longest chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:229684',
                          'name': 'fatty amide anion',
                          'definition': 'The conjugate base of a fatty amide, '
                                        'arising from deprotonation of the '
                                        'carboxylic acid group of the '
                                        'corresponding fatty amide.',
                          'parents': ['CHEBI:29067']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 12719,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.8,
    'f1': 0.07339449541284404,
    'accuracy': 0.9921241422333126}