"""
Classifies: CHEBI:11750 3-sn-phosphatidyl-L-serine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3_sn_phosphatidyl_L_serine(smiles: str):
    """
    Determines if a molecule is a 3-sn-phosphatidyl-L-serine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 3-sn-phosphatidyl-L-serine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for phosphate group
    patt_phosphate = Chem.MolFromSmarts('[O,OH]-P(=O)([O,OH])-O')
    if not mol.HasSubstructMatch(patt_phosphate):
        return False, "Missing phosphate group"
        
    # Check for serine moiety
    patt_serine = Chem.MolFromSmarts('[NH2][CH]([CH2]OP(=O)([O,OH])[O,OH])C(=O)[O,OH]')
    if not mol.HasSubstructMatch(patt_serine):
        return False, "Missing serine moiety"
        
    # Check for glycerol backbone with 2 ester groups
    patt_glycerol = Chem.MolFromSmarts('[CH2]OC(=O)[*]-[CH]([CH2]OP(=O)([O,OH])[O,OH])OC(=O)[*]')
    if not mol.HasSubstructMatch(patt_glycerol):
        return False, "Missing glycerol backbone with ester groups"
        
    # Check stereochemistry at the 2-position of glycerol (sn-3)
    matches = mol.GetSubstructMatches(patt_glycerol)
    if matches:
        for match in matches:
            # Get the chiral center atom
            chiral_atom = mol.GetAtomWithIdx(match[2])  # Index of the CH in the glycerol backbone
            if chiral_atom.GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED:
                return False, "Unspecified stereochemistry at glycerol 2-position"
    else:
        return False, "Could not verify stereochemistry"
        
    # Check stereochemistry of serine (L-configuration)
    matches = mol.GetSubstructMatches(patt_serine)
    if matches:
        for match in matches:
            # Get the chiral center atom
            chiral_atom = mol.GetAtomWithIdx(match[1])  # Index of the CH in serine
            if chiral_atom.GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED:
                return False, "Unspecified stereochemistry at serine alpha carbon"
    else:
        return False, "Could not verify serine stereochemistry"

    return True, "Valid 3-sn-phosphatidyl-L-serine structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:11750',
                          'name': '3-sn-phosphatidyl-L-serine',
                          'definition': 'A 3-sn-glycerophosphoserine compound '
                                        'having acyl substituents at the 1- '
                                        'and 2-hydroxy positions.',
                          'parents': ['CHEBI:18303']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183903,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999565006987076}