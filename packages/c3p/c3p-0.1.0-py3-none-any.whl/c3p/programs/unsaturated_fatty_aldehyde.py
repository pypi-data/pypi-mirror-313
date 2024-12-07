"""
Classifies: CHEBI:231547 unsaturated fatty aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_unsaturated_fatty_aldehyde(smiles: str):
    """
    Determines if a molecule is an unsaturated fatty aldehyde.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an unsaturated fatty aldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for aldehyde group (C=O)
    has_aldehyde = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
                    has_aldehyde = True
                    break
    
    if not has_aldehyde:
        return False, "No aldehyde group found"
        
    # Check for unsaturation (C=C or C#C)
    has_unsaturation = False
    for bond in mol.GetBonds():
        if bond.GetBondType() in [Chem.rdchem.BondType.DOUBLE, Chem.rdchem.BondType.TRIPLE]:
            # Make sure we're not counting the aldehyde C=O
            if not (bond.GetBeginAtom().GetSymbol() == 'O' or bond.GetEndAtom().GetSymbol() == 'O'):
                has_unsaturation = True
                break
                
    if not has_unsaturation:
        return False, "No carbon-carbon multiple bonds found"
        
    # Check carbon chain length (should be fatty - at least 4 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 4:
        return False, "Carbon chain too short to be considered fatty"
        
    # If we get here, it meets all criteria
    return True, f"Unsaturated fatty aldehyde with {carbon_count} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:231547',
                          'name': 'unsaturated fatty aldehyde',
                          'definition': 'Any fatty aldehyde containing at '
                                        'least one C=C or C#C bond.',
                          'parents': ['CHEBI:35746']},
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
    'num_true_positives': 19,
    'num_false_positives': 100,
    'num_true_negatives': 165,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.15966386554621848,
    'recall': 1.0,
    'f1': 0.2753623188405797,
    'accuracy': 0.647887323943662}