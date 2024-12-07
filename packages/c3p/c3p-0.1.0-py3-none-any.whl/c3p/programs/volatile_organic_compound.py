"""
Classifies: CHEBI:134179 volatile organic compound
"""
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem

def is_volatile_organic_compound(smiles: str):
    """
    Determines if a molecule is a volatile organic compound (VOC), defined as
    having boiling point <= 250°C at standard pressure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a VOC, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check if organic (contains carbon)
    if not any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms()):
        return False, "Not an organic compound (no carbon atoms)"
    
    # Estimate boiling point using group contribution method
    try:
        # Calculate molecular descriptors that correlate with boiling point
        mw = Descriptors.ExactMolWt(mol)
        rotatable_bonds = Descriptors.NumRotatableBonds(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        tpsa = Descriptors.TPSA(mol)
        logp = Descriptors.MolLogP(mol)
        
        # Simple empirical formula for estimating boiling point in Celsius
        # Based on correlation of these descriptors with experimental boiling points
        est_bp = (0.45 * mw) + (2.0 * rotatable_bonds) + (15 * hbd) + \
                 (8.0 * hba) + (0.2 * tpsa) + (12.0 * logp) - 80
                 
        if est_bp <= 250:
            return True, f"Estimated boiling point {est_bp:.1f}°C is <= 250°C"
        else:
            return False, f"Estimated boiling point {est_bp:.1f}°C is > 250°C"
            
    except:
        return None, "Could not estimate boiling point"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134179',
                          'name': 'volatile organic compound',
                          'definition': 'Any organic compound having an '
                                        'initial boiling point less than or '
                                        'equal to 250 degreeC (482 degreeF) '
                                        'measured at a standard atmospheric '
                                        'pressure of 101.3 kPa.',
                          'parents': ['CHEBI:72695']},
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
    'num_true_positives': 36,
    'num_false_positives': 100,
    'num_true_negatives': 95,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2647058823529412,
    'recall': 1.0,
    'f1': 0.4186046511627907,
    'accuracy': 0.5670995670995671}