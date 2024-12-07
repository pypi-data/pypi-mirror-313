"""
Classifies: CHEBI:23117 chlorine molecular entity
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chlorine_molecular_entity(smiles: str):
    """
    Determines if a molecule contains one or more chlorine atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains chlorine, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"

        # Check for chlorine atoms
        chlorine_atoms = []
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'Cl':
                chlorine_atoms.append(atom.GetIdx())
                
        if len(chlorine_atoms) > 0:
            return True, f"Contains {len(chlorine_atoms)} chlorine atom(s)"
        else:
            return False, "No chlorine atoms found"
            
    except Exception as e:
        return False, f"Error processing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23117',
                          'name': 'chlorine molecular entity',
                          'definition': 'A halogen molecular entity containing '
                                        'one or more atoms of chlorine.',
                          'parents': ['CHEBI:24471']},
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
    'num_true_positives': 279,
    'num_false_positives': 100,
    'num_true_negatives': 2009,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.7361477572559367,
    'recall': 1.0,
    'f1': 0.8480243161094225,
    'accuracy': 0.9581239530988275}