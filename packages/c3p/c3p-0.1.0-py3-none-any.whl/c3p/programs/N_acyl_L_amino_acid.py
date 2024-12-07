"""
Classifies: CHEBI:21644 N-acyl-L-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def is_N_acyl_L_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-acyl-L-amino acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-acyl-L-amino acid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for N-acyl group (amide)
    amide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No N-acyl (amide) group found"
        
    # Check for alpha carbon with correct stereochemistry
    alpha_carbon_pattern = Chem.MolFromSmarts('[C@H,@]([NH])(C(=O)[OH])')
    matches = mol.GetSubstructMatches(alpha_carbon_pattern)
    
    if not matches:
        return False, "No alpha carbon with correct stereochemistry found"
        
    # Verify L configuration by checking the @ stereochemistry marker
    for match in matches:
        alpha_carbon = mol.GetAtomWithIdx(match[0])
        if '@H' in Chem.MolToSmiles(mol) or '@' in Chem.MolToSmiles(mol):
            chiral_tag = alpha_carbon.GetChiralTag()
            if str(chiral_tag) == 'CHI_TETRAHEDRAL_CCW':
                return True, "Found N-acyl-L-amino acid structure with correct stereochemistry"
    
    return False, "Incorrect stereochemistry for L-amino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21644',
                          'name': 'N-acyl-L-amino acid',
                          'definition': 'Any N-acylamino acid having '
                                        'L-configuration.',
                          'parents': ['CHEBI:51569']},
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
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 7487,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 0.45,
    'f1': 0.13953488372093023,
    'accuracy': 0.9854081766793743}