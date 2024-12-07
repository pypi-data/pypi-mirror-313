"""
Classifies: CHEBI:22323 alkyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alkyl_group(smiles: str):
    """
    Determines if a molecule is an alkyl group (-CnH2n+1).
    
    Args:
        smiles (str): SMILES string of the molecule, with * representing attachment point
        
    Returns:
        bool: True if molecule is an alkyl group, False otherwise
        str: Reason for classification
    """
    # Check for presence of attachment point (*)
    if '*' not in smiles:
        return False, "No attachment point (*) found"
        
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count atoms
    num_carbons = 0
    num_hydrogens = 0
    num_stars = 0
    num_other = 0
    
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            num_carbons += 1
        elif atom.GetSymbol() == 'H':
            num_hydrogens += 1
        elif atom.GetSymbol() == '*':
            num_stars += 1
        else:
            num_other += 1
            
    # Should only contain C, H and one attachment point
    if num_other > 0:
        return False, "Contains atoms other than C, H and attachment point"
    if num_stars != 1:
        return False, "Must have exactly one attachment point"
        
    # Check for saturation - no double/triple bonds
    for bond in mol.GetBonds():
        if bond.GetBondType() != Chem.BondType.SINGLE:
            return False, "Contains unsaturated bonds"
            
    # Add implicit hydrogens to get total H count
    num_hydrogens += sum(atom.GetNumImplicitHs() for atom in mol.GetAtoms())
    
    # Check formula CnH2n+1
    if num_hydrogens != (2 * num_carbons + 1):
        return False, f"Does not match CnH2n+1 formula. Has C{num_carbons}H{num_hydrogens}"
        
    # Check connectivity - should be one continuous chain
    fragments = Chem.GetMolFrags(mol)
    if len(fragments) > 1:
        return False, "Structure is not a single connected group"
        
    return True, f"Valid alkyl group with {num_carbons} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22323',
                          'name': 'alkyl group',
                          'definition': 'A univalent group -CnH2n+1 derived '
                                        'from an alkane by removal of a '
                                        'hydrogen atom from any carbon atom.',
                          'parents': ['CHEBI:33248']},
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
    'num_false_positives': 4,
    'num_true_negatives': 183891,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 1.0,
    'f1': 0.6666666666666666,
    'accuracy': 0.9999782489301192}