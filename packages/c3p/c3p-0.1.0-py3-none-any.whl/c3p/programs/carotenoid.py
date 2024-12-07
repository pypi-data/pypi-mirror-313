"""
Classifies: CHEBI:23044 carotenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_carotenoid(smiles: str):
    """
    Determines if a molecule is a carotenoid based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a carotenoid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check carbon count - should be around 40 (C40) for carotenoids
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 35 or carbon_count > 45:
        return False, f"Carbon count ({carbon_count}) outside typical carotenoid range (35-45)"

    # Check for long conjugated system with alternating single/double bonds
    conjugated_length = 0
    max_conjugated = 0
    
    # Find conjugated systems
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            bonds = atom.GetBonds()
            double_bonds = sum(1 for b in bonds if b.GetBondType() == Chem.BondType.DOUBLE)
            if double_bonds == 1:
                conjugated_length += 1
            else:
                max_conjugated = max(max_conjugated, conjugated_length)
                conjugated_length = 0
                
    max_conjugated = max(max_conjugated, conjugated_length)
    
    if max_conjugated < 8:
        return False, "Insufficient conjugated system length"

    # Check for common carotenoid end groups
    patterns = [
        # Beta ring
        Chem.MolFromSmarts('CC1=C(C)CCCC1(C)C'),
        # Epsilon ring
        Chem.MolFromSmarts('CC1C(C)=CCCC1(C)C'),
        # Acyclic end
        Chem.MolFromSmarts('CC(C)=CCC'),
        # Keto group
        Chem.MolFromSmarts('C(=O)C'),
        # Hydroxy group
        Chem.MolFromSmarts('CC(O)C'),
    ]
    
    end_groups = []
    for p in patterns:
        if p is not None and mol.HasSubstructMatch(p):
            if 'C1=C(C)CCCC1' in Chem.MolToSmarts(p):
                end_groups.append('beta ring')
            elif 'C1C(C)=CCCC1' in Chem.MolToSmarts(p):
                end_groups.append('epsilon ring')
            elif 'CC(C)=CCC' in Chem.MolToSmarts(p):
                end_groups.append('acyclic')
            elif 'C(=O)C' in Chem.MolToSmarts(p):
                end_groups.append('keto')
            elif 'CC(O)C' in Chem.MolToSmarts(p):
                end_groups.append('hydroxy')

    if not end_groups:
        return False, "No characteristic carotenoid end groups found"

    # Check for presence of retinoid structure (which would exclude it)
    retinoid_pattern = Chem.MolFromSmarts('CC1=C(C(=CC=C1)C=CC(=O))C')
    if retinoid_pattern is not None and mol.HasSubstructMatch(retinoid_pattern):
        return False, "Structure contains retinoid motif"

    return True, f"Carotenoid with {', '.join(set(end_groups))} groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23044',
                          'name': 'carotenoid',
                          'definition': 'One of a class of tetraterpenoids '
                                        '(C40), formally derived from the '
                                        'acyclic parent, psi,psi-carotene by '
                                        'hydrogenation, dehydrogenation, '
                                        'cyclization, oxidation, or '
                                        'combination of these processes. This '
                                        'class includes carotenes, '
                                        'xanthophylls and certain compounds '
                                        'that arise from rearrangement of the '
                                        'skeleton of psi,psi-carotene or by '
                                        'loss of part of this structure. '
                                        'Retinoids are excluded.',
                          'parents': ['CHEBI:26935']},
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
    'num_true_positives': 13,
    'num_false_positives': 100,
    'num_true_negatives': 101465,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.11504424778761062,
    'recall': 0.52,
    'f1': 0.1884057971014493,
    'accuracy': 0.9988975292843784}