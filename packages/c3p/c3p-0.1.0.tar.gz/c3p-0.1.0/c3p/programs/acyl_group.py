"""
Classifies: CHEBI:22221 acyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_acyl_group(smiles: str):
    """
    Determines if a molecule is an acyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an acyl group, False otherwise
        str: Reason for classification
    """
    # Replace * with dummy atom [X] for better handling
    smiles = smiles.replace('*','[X]') 
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for C(=O)[X] pattern where [X] is the attachment point
    acyl_pattern = Chem.MolFromSmarts('[C](=O)[X]')
    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "No acyl group (C(=O)[X]) pattern found"
        
    # Get matches
    matches = mol.GetSubstructMatches(acyl_pattern)
    
    # For each match, verify:
    # 1. The carbon is attached to something else besides O and X
    # 2. The oxygen has double bond to carbon
    for match in matches:
        c_idx = match[0] 
        o_idx = match[1]
        x_idx = match[2]
        
        c_atom = mol.GetAtomWithIdx(c_idx)
        o_atom = mol.GetAtomWithIdx(o_idx)
        
        # Check carbon has other substituents
        other_neighbors = False
        for neighbor in c_atom.GetNeighbors():
            if neighbor.GetIdx() not in [o_idx, x_idx]:
                other_neighbors = True
                break
                
        if not other_neighbors:
            continue
            
        # Check oxygen has double bond
        bond = mol.GetBondBetweenAtoms(c_idx, o_idx)
        if bond.GetBondType() != Chem.rdchem.BondType.DOUBLE:
            continue
            
        # If we get here, we found a valid acyl group
        return True, "Contains acyl group R-C(=O)-X"
        
    return False, "No valid acyl group pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22221',
                          'name': 'acyl group',
                          'definition': 'An organic group formed by removing '
                                        'one or more hydroxy groups from an '
                                        'oxoacid that has the general '
                                        'structure RkE(=O)l(OH)m (l =/= 0). '
                                        'Although the term is almost always '
                                        'applied to organic compounds, with '
                                        'carboxylic acid as the oxoacid, acyl '
                                        'groups can in principle be derived '
                                        'from other types of acids such as '
                                        'sulfonic acids or phosphonic acids.',
                          'parents': ['CHEBI:33247']},
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
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 2826,
    'num_false_negatives': 34,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9547297297297297}