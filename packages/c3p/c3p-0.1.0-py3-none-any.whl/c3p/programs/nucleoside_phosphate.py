"""
Classifies: CHEBI:25608 nucleoside phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_nucleoside_phosphate(smiles: str):
    """
    Determines if a molecule is a nucleoside phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a nucleoside phosphate, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of phosphate group
    patt_phosphate = Chem.MolFromSmarts('[P](=[O])([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(patt_phosphate):
        return False, "No phosphate group found"
        
    # Check for nucleoside core structure patterns
    # Purine nucleoside pattern
    patt_purine = Chem.MolFromSmarts('[nX2r5]1[cX3r5][nX2r5][cX3r5]2[cX3r5][nX2r5][cX3r5][nX2r5][c]12')
    
    # Pyrimidine nucleoside pattern  
    patt_pyrimidine = Chem.MolFromSmarts('[nX2r6]1[cX3r6][nX2r6][cX3r6][cX3r6][cX3r6]1')
    
    # Sugar pattern
    patt_sugar = Chem.MolFromSmarts('[C]1[O][C]([C][O])[C]([O,OH])[C]1')
    
    has_purine = mol.HasSubstructMatch(patt_purine)
    has_pyrimidine = mol.HasSubstructMatch(patt_pyrimidine) 
    has_sugar = mol.HasSubstructMatch(patt_sugar)
    
    if not (has_purine or has_pyrimidine):
        return False, "No nucleobase found"
        
    if not has_sugar:
        return False, "No sugar moiety found"
    
    # Check phosphate is attached to sugar
    # Get sugar atoms
    sugar_match = mol.GetSubstructMatch(patt_sugar)
    if not sugar_match:
        return False, "Could not find sugar atoms"
        
    # Get phosphate atoms
    phos_match = mol.GetSubstructMatch(patt_phosphate)
    if not phos_match:
        return False, "Could not find phosphate atoms"
        
    # Check connectivity between sugar and phosphate
    sugar_atoms = set(sugar_match)
    phos_atoms = set(phos_match)
    
    for sugar_atom_idx in sugar_atoms:
        sugar_atom = mol.GetAtomWithIdx(sugar_atom_idx)
        for neighbor in sugar_atom.GetNeighbors():
            if neighbor.GetIdx() in phos_atoms:
                base_type = "purine" if has_purine else "pyrimidine"
                return True, f"Found {base_type} nucleoside with phosphate group attached to sugar"
                
    return False, "Phosphate group not attached to sugar moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25608',
                          'name': 'nucleoside phosphate',
                          'definition': 'A nucleobase-containing molecular '
                                        'entity that is a nucleoside in which '
                                        'one or more of the sugar hydroxy '
                                        'groups has been converted into a '
                                        'mono- or poly-phosphate. The term '
                                        'includes both nucleotides and '
                                        'non-nucleotide nucleoside phosphates.',
                          'parents': [   'CHEBI:25703',
                                         'CHEBI:37734',
                                         'CHEBI:61120']},
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
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.0}