"""
Classifies: CHEBI:18390 N-acyl-beta-D-galactosylsphingosine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_N_acyl_beta_D_galactosylsphingosine(smiles: str):
    """
    Determines if a molecule is an N-acyl-beta-D-galactosylsphingosine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-acyl-beta-D-galactosylsphingosine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of galactose moiety
    galactose_pattern = Chem.MolFromSmarts('[CH2]O[CH]1O[CH](CO)[CH](O)[CH](O)[CH]1O')
    if not mol.HasSubstructMatch(galactose_pattern):
        return False, "Missing beta-D-galactosyl group"

    # Check for sphingosine backbone with N-acyl group
    sphingosine_pattern = Chem.MolFromSmarts('[CH2]O[CH]([CH](O)/C=C/CCCCC)[NH]C(=O)CCCCC')
    if not mol.HasSubstructMatch(sphingosine_pattern):
        return False, "Missing sphingosine backbone with N-acyl group"

    # Check stereochemistry of key carbons
    # Get matches for the galactose and sphingosine patterns
    gal_matches = mol.GetSubstructMatches(galactose_pattern)
    sph_matches = mol.GetSubstructMatches(sphingosine_pattern)
    
    if not gal_matches or not sph_matches:
        return False, "Could not verify stereochemistry"

    # Check for beta configuration at anomeric carbon
    anomeric_carbon_idx = gal_matches[0][2]  # Index of anomeric carbon in match
    anomeric_carbon = mol.GetAtomWithIdx(anomeric_carbon_idx)
    
    # Check for correct stereochemistry of galactose carbons
    for atom_idx in gal_matches[0]:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED:
            continue
        if atom.GetChiralTag() != Chem.ChiralType.CHI_TETRAHEDRAL_CW and \
           atom.GetChiralTag() != Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
            return False, "Incorrect stereochemistry in galactose moiety"

    # Verify presence of long chain fatty acid in N-acyl group
    acyl_pattern = Chem.MolFromSmarts('C(=O)CCCCCCCCC')
    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "N-acyl group does not contain required long chain fatty acid"

    return True, "Contains beta-D-galactosyl group, sphingosine backbone, and N-acyl group with correct stereochemistry"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18390',
                          'name': 'N-acyl-beta-D-galactosylsphingosine',
                          'definition': 'An N-acyl-D-galactosylsphingosine in '
                                        'which the anomeric configuration of '
                                        'the galactosyl residue is beta; '
                                        'sphingosine substituted at the O-1 '
                                        'position by a beta-D-galactosyl group '
                                        'and at the N-2 position by an acyl '
                                        'group.',
                          'parents': ['CHEBI:143593', 'CHEBI:83866']},
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
    'num_true_negatives': 183906,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836875846206}