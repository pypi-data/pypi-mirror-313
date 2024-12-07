"""
Classifies: CHEBI:25375 monoamine molecular messenger
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_monoamine_molecular_messenger(smiles: str):
    """
    Determines if a molecule is a monoamine molecular messenger.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monoamine molecular messenger, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of exactly one amino group (-NH2 or -NH-)
    amine_pattern = Chem.MolFromSmarts('[NX3;H2,H1;!$(NC=O)]')
    amine_matches = mol.GetSubstructMatches(amine_pattern)
    if len(amine_matches) != 1:
        return False, "Must contain exactly one amino group"
        
    # Check for presence of aromatic ring
    aromatic_pattern = Chem.MolFromSmarts('a1aaaaa1')
    if not mol.HasSubstructMatch(aromatic_pattern):
        return False, "Must contain an aromatic ring"
        
    # Check for ethylene linker (-CH2-CH2-) between amine and aromatic ring
    ethylene_amine_arom_pattern = Chem.MolFromSmarts('a-[CH2][CH2][NH2,NH]')
    if not mol.HasSubstructMatch(ethylene_amine_arom_pattern):
        return False, "Must have ethylene linker (-CH2-CH2-) between amine and aromatic ring"
        
    # Check for characteristic substituents of monoamine neurotransmitters
    hydroxy_pattern = Chem.MolFromSmarts('aO')
    methoxy_pattern = Chem.MolFromSmarts('aOC')
    
    substituents = []
    if mol.HasSubstructMatch(hydroxy_pattern):
        substituents.append("hydroxy")
    if mol.HasSubstructMatch(methoxy_pattern):
        substituents.append("methoxy")
        
    # Additional check for beta-hydroxyl group common in some monoamines
    beta_hydroxy_pattern = Chem.MolFromSmarts('[NH2,NH][CH2][CH](O)[CH3,H]')
    if mol.HasSubstructMatch(beta_hydroxy_pattern):
        substituents.append("beta-hydroxy")
        
    # Check molecular weight is in reasonable range for monoamine messengers
    mol_weight = Descriptors.ExactMolWt(mol)
    if mol_weight > 300:
        return False, "Molecular weight too high for typical monoamine messenger"
        
    substituents_str = ", ".join(substituents) if substituents else "no additional"
    return True, f"Monoamine molecular messenger with {substituents_str} substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25375',
                          'name': 'monoamine molecular messenger',
                          'definition': 'A group of neurotransmitters and '
                                        'neuromodulators that contain one '
                                        'amino group that is connected to an '
                                        'aromatic ring by ethylene group  '
                                        '(-CH2-CH2-). Monoamines are derived '
                                        'from the aromatic amino acids '
                                        'phenylalanine, tyrosine, histidine '
                                        'and tryptophan.',
                          'parents': ['CHEBI:63534']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 127400,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 0.6666666666666666,
    'f1': 0.03809523809523809,
    'accuracy': 0.9992078617758013}