"""
Classifies: CHEBI:25676 oligopeptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_oligopeptide(smiles: str):
    """
    Determines if a molecule is an oligopeptide (a peptide containing a relatively small number of amino acids).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an oligopeptide, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count amide bonds (peptide bonds)
    amide_pattern = Chem.MolFromSmarts('[NX3H1,NX3H0][CX3](=[OX1])[#6]')
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    num_amide_bonds = len(amide_matches)
    
    if num_amide_bonds == 0:
        return False, "No peptide bonds found"
    
    # Look for amino acid characteristics
    amine_pattern = Chem.MolFromSmarts('[NX3;H2,H1;!$(NC=O)]')
    carboxyl_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1,OX1-]')
    
    has_amine = len(mol.GetSubstructMatches(amine_pattern)) > 0
    has_carboxyl = len(mol.GetSubstructMatches(carboxyl_pattern)) > 0
    
    if not (has_amine and has_carboxyl):
        return False, "Missing characteristic amino acid groups"

    # Estimate number of amino acid residues based on peptide bonds
    estimated_residues = num_amide_bonds + 1
    
    # Define size limits for oligopeptides (typically 2-20 amino acids)
    MIN_RESIDUES = 2
    MAX_RESIDUES = 20
    
    if estimated_residues < MIN_RESIDUES:
        return False, f"Too few amino acid residues ({estimated_residues})"
    elif estimated_residues > MAX_RESIDUES:
        return False, f"Too many amino acid residues ({estimated_residues})"
        
    return True, f"Oligopeptide with approximately {estimated_residues} amino acid residues"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25676',
                          'name': 'oligopeptide',
                          'definition': 'A peptide containing a relatively '
                                        'small number of amino acids.',
                          'parents': ['CHEBI:16670']},
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
    'num_true_positives': 331,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.7679814385150812,
    'f1': 0.868766404199475,
    'accuracy': 0.7679814385150812}