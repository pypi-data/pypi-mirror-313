"""
Classifies: CHEBI:18254 ribonucleoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

def is_ribonucleoside(smiles: str):
    """
    Determines if a molecule is a ribonucleoside (nucleoside containing D-ribose).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a ribonucleoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for ribose substructure
    ribose_smarts = "[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O"
    ribose_alt_smarts = "[C@@H]1O[C@H](CO)[C@H](O)[C@H]1O"
    ribose_pattern = Chem.MolFromSmarts(ribose_smarts)
    ribose_alt_pattern = Chem.MolFromSmarts(ribose_alt_smarts)
    
    has_ribose = mol.HasSubstructMatch(ribose_pattern) or mol.HasSubstructMatch(ribose_alt_pattern)
    
    if not has_ribose:
        # Check for 3'-deoxy or 2'-O-methyl variants
        deoxy_smarts = "[C@@H]1O[C@H](CO)C[C@H]1O"
        methoxy_smarts = "[C@@H]1O[C@H](CO)[C@@H](OC)[C@H]1O"
        
        deoxy_pattern = Chem.MolFromSmarts(deoxy_smarts)
        methoxy_pattern = Chem.MolFromSmarts(methoxy_smarts)
        
        if not (mol.HasSubstructMatch(deoxy_pattern) or mol.HasSubstructMatch(methoxy_pattern)):
            return False, "No ribose sugar moiety found"

    # Check for nucleobase
    purine_smarts = "c1ncnc2[nH]cnc12" # Adenine/Guanine core
    pyrimidine_smarts = "c1cn([C,H])c(=O)nc1" # Cytosine/Uracil core
    
    purine_pattern = Chem.MolFromSmarts(purine_smarts)
    pyrimidine_pattern = Chem.MolFromSmarts(pyrimidine_smarts)

    has_base = mol.HasSubstructMatch(purine_pattern) or mol.HasSubstructMatch(pyrimidine_pattern)

    if not has_base:
        # Check for modified bases
        mod_purine_smarts = "c1nc2c([nH]1)ncnc2"  # Alternative purine pattern
        mod_pyrimidine_smarts = "c1cnc(=O)[nH]c1"  # Alternative pyrimidine pattern
        
        mod_purine_pattern = Chem.MolFromSmarts(mod_purine_smarts)
        mod_pyrimidine_pattern = Chem.MolFromSmarts(mod_pyrimidine_smarts)
        
        has_base = mol.HasSubstructMatch(mod_purine_pattern) or mol.HasSubstructMatch(mod_pyrimidine_pattern)
        
        if not has_base:
            return False, "No nucleobase moiety found"

    # Check glycosidic linkage
    if mol.HasSubstructMatch(purine_pattern):
        return True, "Purine ribonucleoside"
    else:
        return True, "Pyrimidine ribonucleoside"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18254',
                          'name': 'ribonucleoside',
                          'definition': 'Any nucleoside where the sugar '
                                        'component is D-ribose.',
                          'parents': ['CHEBI:33838', 'CHEBI:47019']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 24902,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.2857142857142857,
    'f1': 0.06779661016949154,
    'accuracy': 0.9956028141989127}