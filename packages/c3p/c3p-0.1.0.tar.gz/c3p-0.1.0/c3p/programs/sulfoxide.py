"""
Classifies: CHEBI:22063 sulfoxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_sulfoxide(smiles: str):
    """
    Determines if a molecule is a sulfoxide (R2S=O or R2C=S=O where R =/= H).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sulfoxide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for sulfur atoms
    sulfur_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']
    if not sulfur_atoms:
        return False, "No sulfur atoms found"

    for s_atom in sulfur_atoms:
        # Get neighbors of sulfur
        neighbors = s_atom.GetNeighbors()
        
        # Count number of double bonds to oxygen
        s_o_double_bonds = 0
        non_h_neighbors = 0
        
        for neighbor in neighbors:
            # Check bonds between S and neighbor
            bond = mol.GetBondBetweenAtoms(s_atom.GetIdx(), neighbor.GetIdx())
            
            # Count double bonds to oxygen
            if neighbor.GetSymbol() == 'O' and bond.GetBondType() == Chem.BondType.DOUBLE:
                s_o_double_bonds += 1
            
            # Count non-hydrogen neighbors
            if neighbor.GetSymbol() != 'H':
                non_h_neighbors += 1

        # Sulfoxide should have exactly:
        # - One double bond to oxygen
        # - Two other non-H neighbors (the R groups)
        if s_o_double_bonds == 1 and non_h_neighbors == 3:
            return True, "Contains R2S=O group"
            
        # Check for R2C=S=O pattern
        if s_o_double_bonds == 1 and non_h_neighbors == 2:
            for neighbor in neighbors:
                if neighbor.GetSymbol() == 'C':
                    bond = mol.GetBondBetweenAtoms(s_atom.GetIdx(), neighbor.GetIdx())
                    if bond.GetBondType() == Chem.BondType.DOUBLE:
                        return True, "Contains R2C=S=O group"

    return False, "No sulfoxide group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22063',
                          'name': 'sulfoxide',
                          'definition': 'An organosulfur compound having the '
                                        'structure R2S=O or R2C=S=O (R =/= H).',
                          'parents': ['CHEBI:33261']},
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
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 36021,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 0.9333333333333333,
    'f1': 0.21705426356589147,
    'accuracy': 0.9972050033207881}