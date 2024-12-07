"""
Classifies: CHEBI:17792 organohalogen compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organohalogen_compound(smiles: str):
    """
    Determines if a molecule is an organohalogen compound, defined as having at least 
    one carbon-halogen bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organohalogen compound, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES and check for validity
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # List of halogen atomic numbers
    halogens = [9, 17, 35, 53] # F, Cl, Br, I
    
    # Check each bond in the molecule
    for bond in mol.GetBonds():
        # Get atoms in the bond
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()
        
        # Check if bond is between carbon and halogen
        if (atom1.GetAtomicNum() == 6 and atom2.GetAtomicNum() in halogens) or \
           (atom2.GetAtomicNum() == 6 and atom1.GetAtomicNum() in halogens):
            
            # Get halogen symbol
            halogen = atom1.GetSymbol() if atom1.GetAtomicNum() in halogens else atom2.GetSymbol()
            return True, f"Contains carbon-{halogen} bond"
            
    return False, "No carbon-halogen bonds found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17792',
                          'name': 'organohalogen compound',
                          'definition': 'A compound containing at least one '
                                        'carbon-halogen bond (where X is a '
                                        'halogen atom).',
                          'parents': ['CHEBI:33285', 'CHEBI:37578']},
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
    'num_true_positives': 443,
    'num_false_positives': 100,
    'num_true_negatives': 957,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.8158379373848987,
    'recall': 0.9977477477477478,
    'f1': 0.8976697061803446,
    'accuracy': 0.9327115256495669}