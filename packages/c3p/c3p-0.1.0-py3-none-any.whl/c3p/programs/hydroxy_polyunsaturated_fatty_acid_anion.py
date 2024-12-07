"""
Classifies: CHEBI:131871 hydroxy polyunsaturated fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_hydroxy_polyunsaturated_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a hydroxy polyunsaturated fatty acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy polyunsaturated fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for carboxylate anion
    carboxylate = False
    for atom in mol.GetAtoms():
        if atom.GetFormalCharge() == -1 and atom.GetSymbol() == 'O':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    for n2 in neighbor.GetNeighbors():
                        if n2.GetSymbol() == 'O' and n2.GetFormalCharge() == 0:
                            carboxylate = True
                            
    if not carboxylate:
        return False, "No carboxylate anion group found"
        
    # Check for hydroxy groups
    hydroxy_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    hydroxy_count += 1
                    
    if hydroxy_count == 0:
        return False, "No hydroxy groups found"
        
    # Count double bonds
    double_bond_count = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
            # Don't count the carboxylate double bond
            atoms = [bond.GetBeginAtom(), bond.GetEndAtom()]
            if not any(a.GetFormalCharge() == -1 for a in atoms):
                double_bond_count += 1
                
    if double_bond_count < 2:
        return False, "Not polyunsaturated (less than 2 double bonds)"
        
    # Check carbon chain length (should be medium-long chain fatty acid)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 12:
        return False, "Carbon chain too short for fatty acid"
        
    return True, f"Hydroxy polyunsaturated fatty acid anion with {hydroxy_count} OH group(s) and {double_bond_count} double bond(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131871',
                          'name': 'hydroxy polyunsaturated fatty acid anion',
                          'definition': 'Any polyunsaturated fatty acid anion '
                                        'carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:59835', 'CHEBI:76567']},
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
    'num_true_positives': 11,
    'num_false_positives': 100,
    'num_true_negatives': 7229,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0990990990990991,
    'recall': 0.9166666666666666,
    'f1': 0.17886178861788618,
    'accuracy': 0.9862416564500749}