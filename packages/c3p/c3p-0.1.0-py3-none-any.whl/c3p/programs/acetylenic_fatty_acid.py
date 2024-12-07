"""
Classifies: CHEBI:25380 acetylenic fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import FindMolChiralCenters

def is_acetylenic_fatty_acid(smiles: str):
    """
    Determines if a molecule is an acetylenic fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an acetylenic fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for triple bond
    triple_bond_pattern = Chem.MolFromSmarts('C#C')
    if not mol.HasSubstructMatch(triple_bond_pattern):
        return False, "No triple bond found"
        
    # Check for carbon chain length (minimum 8 carbons for fatty acids)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 8:
        return False, "Carbon chain too short for fatty acid classification"
        
    # Count triple bonds
    triple_bonds = len(mol.GetSubstructMatches(triple_bond_pattern))
    
    # Count double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    # Check if molecule is linear (allowing for small rings)
    ring_info = mol.GetRingInfo()
    has_large_rings = any(len(ring) > 4 for ring in ring_info.AtomRings())
    
    # Get chiral centers if any
    chiral_centers = FindMolChiralCenters(mol)
    chirality_info = f" with {len(chiral_centers)} chiral center(s)" if chiral_centers else ""
    
    # Build classification reason
    unsaturation_info = []
    if triple_bonds > 0:
        unsaturation_info.append(f"{triple_bonds} triple bond(s)")
    if double_bonds > 0:
        unsaturation_info.append(f"{double_bonds} double bond(s)")
        
    structure_type = "cyclic" if has_large_rings else "linear"
    
    reason = f"{structure_type.capitalize()} fatty acid with {' and '.join(unsaturation_info)}" + \
             f"{chirality_info}, containing {carbon_count} carbons"
    
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25380',
                          'name': 'acetylenic fatty acid',
                          'definition': 'Any  unsaturated fatty acid '
                                        'containing at least one triple bond '
                                        'in the carbon chain framework.',
                          'parents': ['CHEBI:27208', 'CHEBI:73474']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 63254,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9984216424388781}