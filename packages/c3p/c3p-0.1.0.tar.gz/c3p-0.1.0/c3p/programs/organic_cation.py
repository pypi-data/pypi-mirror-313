"""
Classifies: CHEBI:25697 organic cation
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_organic_cation(smiles: str):
    """
    Determines if a molecule is an organic cation (organic ion with net positive charge).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organic cation, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check if molecule contains carbon (organic)
    has_carbon = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            has_carbon = True
            break
            
    if not has_carbon:
        return False, "Not organic - contains no carbon atoms"

    # Calculate formal charge
    total_charge = 0
    for atom in mol.GetAtoms():
        total_charge += atom.GetFormalCharge()
        
    if total_charge <= 0:
        return False, f"Not a cation - net charge is {total_charge}"

    # Get count of positive and negative charges
    pos_charges = 0
    neg_charges = 0
    charge_atoms = []
    
    for atom in mol.GetAtoms():
        charge = atom.GetFormalCharge()
        if charge > 0:
            pos_charges += charge
            charge_atoms.append(f"{atom.GetSymbol()}{charge}+")
        elif charge < 0:
            neg_charges += abs(charge)
            charge_atoms.append(f"{atom.GetSymbol()}{charge}-")
            
    return True, f"Organic cation with net charge +{total_charge} ({', '.join(charge_atoms)})"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25697',
                          'name': 'organic cation',
                          'definition': 'Any organic ion with a net positive '
                                        'charge.',
                          'parents': ['CHEBI:25699', 'CHEBI:36916']},
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
    'num_true_positives': 76,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.4318181818181818,
    'f1': 0.6031746031746031,
    'accuracy': 0.4318181818181818}