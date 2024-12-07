"""
Classifies: CHEBI:25230 methionine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_methionine_derivative(smiles: str):
    """
    Determines if a molecule is a methionine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a methionine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of sulfur
    if not any(atom.GetSymbol() == 'S' for atom in mol.GetAtoms()):
        return False, "No sulfur atom found"
        
    # Check for presence of amino group or modified amino group
    has_amino = False
    has_modified_amino = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            # Count number of hydrogens on N
            n_hydrogens = atom.GetTotalNumHs()
            if n_hydrogens == 2:  # NH2 group
                has_amino = True
            elif n_hydrogens < 2 and atom.GetDegree() > 1:  # Modified NH2
                has_modified_amino = True
                
    if not (has_amino or has_modified_amino):
        return False, "No amino or modified amino group found"

    # Check for presence of carboxyl group or modified carboxyl
    has_carboxyl = False
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if mol.HasSubstructMatch(carboxyl_pattern):
        has_carboxyl = True
    
    has_modified_carboxyl = False
    modified_carboxyl_pattern = Chem.MolFromSmarts('C(=O)[!H]')
    if mol.HasSubstructMatch(modified_carboxyl_pattern):
        has_modified_carboxyl = True
        
    if not (has_carboxyl or has_modified_carboxyl):
        return False, "No carboxyl or modified carboxyl group found"

    # Check for methionine core structure (S-CH3 group connected to carbon chain)
    methionine_core = Chem.MolFromSmarts('SC[CH2][CH2]C')
    if not mol.HasSubstructMatch(methionine_core):
        return False, "No methionine core structure found"

    # Check if it's a simple peptide
    peptide_pattern = Chem.MolFromSmarts('[NH]C(=O)[CH]([CH2])[NH]')
    if mol.HasSubstructMatch(peptide_pattern):
        # Count peptide bonds
        matches = mol.GetSubstructMatches(peptide_pattern)
        if len(matches) > 1:
            return False, "Appears to be a peptide"

    # Determine type of modification
    modification = []
    if has_modified_amino and not has_amino:
        modification.append("N-modified")
    if has_modified_carboxyl and not has_carboxyl:
        modification.append("C-modified")
    if has_carboxyl and has_amino:
        sulfone_pattern = Chem.MolFromSmarts('S(=O)(=O)C')
        if mol.HasSubstructMatch(sulfone_pattern):
            modification.append("sulfone")
            
    if not modification:
        return True, "Unmodified methionine core structure"
    else:
        return True, f"Methionine derivative with modifications: {', '.join(modification)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25230',
                          'name': 'methionine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of methionine at the '
                                        'amino group or the carboxy group, or '
                                        'from the replacement of any hydrogen '
                                        'of methionine  by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing methionine residues.',
                          'parents': ['CHEBI:33261', 'CHEBI:83821']},
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
    'num_true_negatives': 19941,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9947620472912302}