"""
Classifies: CHEBI:131864 docosanoid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_docosanoid_anion(smiles: str):
    """
    Determines if a molecule is a docosanoid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a docosanoid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of carboxylate anion
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion present"
        
    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 22:
        return False, f"Not a C22 structure (found {carbon_count} carbons)"
        
    # Check for unsaturation (double bonds)
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    if double_bonds < 2:
        return False, "Insufficient unsaturation (needs multiple double bonds)"
        
    # Count oxygen atoms (should have at least 2 - one from carboxylate)
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if oxygen_count < 2:
        return False, "Insufficient oxygen atoms"
        
    # Verify chain structure (should be largely aliphatic)
    aromatic_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetIsAromatic())
    if aromatic_atoms > 0:
        return False, "Contains aromatic systems"
        
    return True, "Docosanoid anion with carboxylate group and unsaturated chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131864',
                          'name': 'docosanoid anion',
                          'definition': 'A polyunsaturated fatty acid anion '
                                        'obtained by the deprotonation of the '
                                        'carboxy group of any docosanoid.',
                          'parents': ['CHEBI:57560']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 21,
    'num_true_negatives': 183820,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.2222222222222222,
    'recall': 0.6666666666666666,
    'f1': 0.3333333333333333,
    'accuracy': 0.9998694587979331}