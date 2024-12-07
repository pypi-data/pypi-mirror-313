"""
Classifies: CHEBI:131872 hydroxy saturated fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxy_saturated_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a hydroxy saturated fatty acid anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy saturated fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for carboxylate anion group
    carboxylate_pattern = Chem.MolFromSmarts('[C](=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"
    
    # Check for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[OH1]')
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "No hydroxyl groups found"
        
    # Check if molecule is saturated (no double/triple bonds except carboxylate)
    carboxylate_atoms = mol.GetSubstructMatches(carboxylate_pattern)[0]
    for bond in mol.GetBonds():
        # Skip bonds in carboxylate group
        if bond.GetBeginAtomIdx() in carboxylate_atoms and bond.GetEndAtomIdx() in carboxylate_atoms:
            continue
            
        if bond.GetBondType() != Chem.BondType.SINGLE:
            return False, "Contains unsaturated bonds outside carboxylate group"
            
    # Check carbon chain length (should be at least 2 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 2:
        return False, "Carbon chain too short to be a fatty acid"
        
    # Count number of hydroxyl groups
    hydroxyl_matches = len(mol.GetSubstructMatches(hydroxyl_pattern))
    
    # Success case
    return True, f"Hydroxy saturated fatty acid anion with {hydroxyl_matches} hydroxyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131872',
                          'name': 'hydroxy saturated fatty acid anion',
                          'definition': 'Any saturated fatty acid anion '
                                        'carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:58953', 'CHEBI:59835']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetAtomsMatchingQuery(Mol, Mol)\n'
               'did not match C++ signature:\n'
               '    GetAtomsMatchingQuery(boost::shared_ptr<RDKit::ROMol> '
               'self, RDKit::QueryAtom* qa)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 36877,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9972958355868037}