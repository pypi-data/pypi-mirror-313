"""
Classifies: CHEBI:23042 carotene
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_carotene(smiles: str):
    """
    Determines if a molecule is a carotene (hydrocarbon carotenoid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a carotene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check if molecule contains only C and H atoms
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if not all(atom in ['C', 'H'] for atom in set(atoms)):
        return False, "Contains non-hydrocarbon atoms"
        
    # Count number of conjugated double bonds
    # Carotenes typically have 9-11 conjugated double bonds
    conjugated_db = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            conjugated_db += 1
            
    if conjugated_db < 7:
        return False, "Too few conjugated double bonds for a carotene"
        
    # Check molecular formula - carotenes are C40Hx
    formula = rdMolDescriptors.CalcMolFormula(mol)
    num_carbons = sum(1 for c in formula if c == 'C')
    if num_carbons != 40:
        return False, f"Not C40 hydrocarbon (has {num_carbons} carbons)"
        
    # Check for presence of methyl branching
    methyl_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            # Count number of single-bonded carbons
            neighbors = [n for n in atom.GetNeighbors() if n.GetSymbol() == 'C']
            single_bonded = sum(1 for n in neighbors if mol.GetBondBetweenAtoms(atom.GetIdx(), n.GetIdx()).GetBondType() == Chem.BondType.SINGLE)
            if single_bonded == 1 and atom.GetTotalNumHs() == 3:
                methyl_count += 1
                
    if methyl_count < 8:
        return False, "Insufficient methyl branching for a carotene"
        
    return True, f"Carotene with {conjugated_db} conjugated double bonds and {methyl_count} methyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23042',
                          'name': 'carotene',
                          'definition': 'Hydrocarbon carotenoids.',
                          'parents': ['CHEBI:35193']},
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
    'num_true_negatives': 183899,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999983686963709}