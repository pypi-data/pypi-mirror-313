"""
Classifies: CHEBI:25704 organic sulfate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organic_sulfate(smiles: str):
    """
    Determines if a molecule is an organic sulfate (compounds of formula SO3HOR where R is an organyl group).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an organic sulfate, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find sulfur atoms
    sulfur_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']
    if not sulfur_atoms:
        return False, "No sulfur atoms found"
        
    # Check each sulfur atom for sulfate pattern
    for sulfur in sulfur_atoms:
        # Get neighbors of sulfur
        neighbors = sulfur.GetNeighbors()
        
        # Count oxygen neighbors
        oxygen_neighbors = [n for n in neighbors if n.GetSymbol() == 'O']
        if len(oxygen_neighbors) != 4:
            continue
            
        # Check if one oxygen is bonded to carbon (R group)
        has_c_o_bond = False
        for oxygen in oxygen_neighbors:
            o_neighbors = oxygen.GetNeighbors()
            for n in o_neighbors:
                if n.GetSymbol() == 'C':
                    has_c_o_bond = True
                    break
            if has_c_o_bond:
                break
                
        # Check if remaining oxygens are double-bonded or have H
        double_bonds = 0
        hydroxy = 0
        for oxygen in oxygen_neighbors:
            if oxygen.GetTotalNumHs() > 0:
                hydroxy += 1
            for bond in oxygen.GetBonds():
                if bond.GetBondType() == Chem.BondType.DOUBLE:
                    double_bonds += 1
                    
        # Pattern match: 1 R-O-, 2 O=S, 1 -OH
        if has_c_o_bond and double_bonds == 2 and hydroxy == 1:
            return True, "Contains SO3HOR pattern where R is organic"
            
    return False, "No sulfate group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25704',
                          'name': 'organic sulfate',
                          'definition': 'Compounds of the general formula '
                                        'SO3HOR where R is an organyl group',
                          'parents': ['CHEBI:26820', 'CHEBI:37826']},
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
    'num_true_positives': 75,
    'num_false_positives': 100,
    'num_true_negatives': 19055,
    'num_false_negatives': 39,
    'num_negatives': None,
    'precision': 0.42857142857142855,
    'recall': 0.6578947368421053,
    'f1': 0.5190311418685121,
    'accuracy': 0.9927863407545799}