"""
Classifies: CHEBI:25627 octadecadienoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_octadecadienoic_acid(smiles: str):
    """
    Determines if a molecule is an octadecadienoic acid (C18 fatty acid with 2 double bonds).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an octadecadienoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Count carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 18:
        return False, f"Carbon count is {carbon_count}, should be 18"

    # Count double bonds (excluding the carboxylic acid C=O)
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_count = len(mol.GetSubstructMatches(double_bond_pattern))
    
    if double_bond_count != 2:
        return False, f"Number of C=C double bonds is {double_bond_count}, should be 2"

    # Check if it's a straight chain
    # First create a copy without explicit H atoms
    mol_no_h = Chem.RemoveHs(mol)
    
    # Count rings
    if rdMolDescriptors.CalcNumRings(mol_no_h) > 0:
        return False, "Contains rings - not a straight chain"

    # Check for branching by counting number of non-H neighbors for each carbon
    for atom in mol_no_h.GetAtoms():
        if atom.GetSymbol() == 'C':
            non_h_neighbors = len([n for n in atom.GetNeighbors() 
                                 if n.GetSymbol() != 'H'])
            if non_h_neighbors > 4:  # No carbon should have more than 4 non-H neighbors
                return False, "Contains branching - not a straight chain"
            if atom.GetIsAromatic():
                return False, "Contains aromatic carbons"

    return True, "Valid octadecadienoic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25627',
                          'name': 'octadecadienoic acid',
                          'definition': 'Any straight-chain, C18 '
                                        'polyunsaturated fatty acid having two '
                                        'C=C double bonds.',
                          'parents': [   'CHEBI:140949',
                                         'CHEBI:15904',
                                         'CHEBI:26208',
                                         'CHEBI:36326',
                                         'CHEBI:53339',
                                         'CHEBI:59202']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 141641,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9992945176970236}