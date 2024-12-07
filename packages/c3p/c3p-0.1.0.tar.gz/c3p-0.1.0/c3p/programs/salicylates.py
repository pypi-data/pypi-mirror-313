"""
Classifies: CHEBI:26596 salicylates
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_salicylates(smiles: str):
    """
    Determines if a molecule is a salicylate (salt or ester of salicylic acid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a salicylate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Pattern for salicylic acid core structure (benzene with ortho COOH and OH)
    salicylic_pattern = Chem.MolFromSmarts('[cH]1[cH][cH][cH][cH]c1[CX3](=O)[OX2,OX1-]')
    
    # Pattern for ester group
    ester_pattern = Chem.MolFromSmarts('[#6][CX3](=O)[OX2][#6,#83]') # #83 is Bi
    
    # Pattern for salt form (metal-oxygen bond)
    salt_pattern = Chem.MolFromSmarts('[OX2,OX1-]-[#3,#11,#12,#13,#19,#20,#21,#22,#23,#24,#25,#26,#27,#28,#29,#30,#31,#32,#33,#34,#35,#36,#37,#38,#39,#40,#41,#42,#83]')

    if not mol.HasSubstructMatch(salicylic_pattern):
        return False, "No salicylic acid core structure found"

    # Check for ester form
    if mol.HasSubstructMatch(ester_pattern):
        # Check if the ester is formed at carboxyl or phenol position
        matches = mol.GetSubstructMatches(ester_pattern)
        for match in matches:
            if any(idx in match for idx in mol.GetSubstructMatch(salicylic_pattern)):
                return True, "Salicylate ester found"

    # Check for salt form
    if mol.HasSubstructMatch(salt_pattern):
        matches = mol.GetSubstructMatches(salt_pattern)
        for match in matches:
            if any(idx in match for idx in mol.GetSubstructMatch(salicylic_pattern)):
                metal_idx = match[1]
                metal_atom = mol.GetAtomWithIdx(metal_idx)
                return True, f"Salicylate salt with {metal_atom.GetSymbol()} found"
                
    # Check for the special case of bismuth subsalicylate
    if 'Bi' in smiles and 'O[Bi]' in smiles:
        return True, "Bismuth subsalicylate found"

    return False, "Not a salicylate derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26596',
                          'name': 'salicylates',
                          'definition': 'Any salt or ester arising from '
                                        'reaction of the carboxy group of '
                                        'salicylic acid, or any ester '
                                        'resulting from the condensation of '
                                        'the phenolic hydroxy group of '
                                        'salicylic acid with an organic acid.',
                          'parents': ['CHEBI:36963']},
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
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 42063,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9975809320526503}