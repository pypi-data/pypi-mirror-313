"""
Classifies: CHEBI:26820 sulfates
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_sulfates(smiles: str):
    """
    Determines if a molecule is a sulfate (salt or ester of sulfuric acid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sulfate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Look for sulfate group patterns
    sulfate_patterns = [
        'OS(=O)(=O)O',     # Sulfuric acid pattern
        'OS(=O)(=O)[O-]',  # Sulfate anion pattern
        '[O-]S(=O)(=O)[O-]', # Sulfate dianion pattern
        'OS(=O)(=O)OC',    # Sulfate ester pattern
        'OS(=O)(=O)O[C,c]' # Aromatic/aliphatic sulfate ester pattern
    ]
    
    for pattern in sulfate_patterns:
        substructure = Chem.MolFromSmarts(pattern)
        if mol.HasSubstructMatch(substructure):
            # Check if it's an ester
            if 'C' in pattern or 'c' in pattern:
                return True, "Sulfate ester found"
            
            # Check for metal ions indicating salt
            for atom in mol.GetAtoms():
                if atom.GetSymbol() in ['Na', 'K', 'Li', 'Al', 'Cu']:
                    return True, "Sulfate salt found"
                if atom.GetFormalCharge() > 0 and atom.GetAtomicNum() not in [1, 6, 7, 8, 15, 16]:
                    return True, "Sulfate salt found (metal cation present)"
                    
            # Check if sulfate is part of organic molecule
            matches = mol.GetSubstructMatches(substructure)
            for match in matches:
                sulfur_idx = [i for i, idx in enumerate(match) 
                            if mol.GetAtomWithIdx(idx).GetSymbol() == 'S'][0]
                sulfur = mol.GetAtomWithIdx(match[sulfur_idx])
                
                # Look at neighbors of oxygens bonded to sulfur
                for neighbor in sulfur.GetNeighbors():
                    if neighbor.GetSymbol() == 'O':
                        for o_neighbor in neighbor.GetNeighbors():
                            if o_neighbor.GetSymbol() not in ['S', 'H']:
                                return True, "Sulfate ester found"
            
            return True, "Sulfate group found"
            
    return False, "No sulfate group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26820',
                          'name': 'sulfates',
                          'definition': 'Salts and esters of sulfuric acid',
                          'parents': ['CHEBI:37826']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 99,
    'num_false_positives': 100,
    'num_true_negatives': 11960,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.49748743718592964,
    'recall': 0.8048780487804879,
    'f1': 0.6149068322981367,
    'accuracy': 0.989821882951654}