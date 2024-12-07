"""
Classifies: CHEBI:25622 orthoquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_orthoquinones(smiles: str):
    """
    Determines if a molecule is an orthoquinone (quinone with carbonyl groups joined by single bond).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an orthoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for carbonyl groups (C=O)
    carbonyl_patterns = mol.GetSubstructMatches(Chem.MolFromSmarts('[C;!R]=[O;!R]'))
    ring_carbonyl_patterns = mol.GetSubstructMatches(Chem.MolFromSmarts('[C;R]=[O;!R]'))
    
    all_carbonyls = carbonyl_patterns + ring_carbonyl_patterns
    
    if len(all_carbonyls) < 2:
        return False, "Less than 2 carbonyl groups found"
        
    # Check pairs of carbonyls to find adjacent ones
    for i in range(len(all_carbonyls)):
        for j in range(i+1, len(all_carbonyls)):
            c1 = all_carbonyls[i][0]  # Carbon atom index of first carbonyl
            c2 = all_carbonyls[j][0]  # Carbon atom index of second carbonyl
            
            # Check if carbonyls are connected by single bond
            bond = mol.GetBondBetweenAtoms(c1, c2)
            if bond is not None and bond.GetBondType() == Chem.BondType.SINGLE:
                # Verify both carbonyls are part of the same ring system
                if mol.GetAtomWithIdx(c1).IsInRing() and mol.GetAtomWithIdx(c2).IsInRing():
                    # Additional check to ensure carbons are in same ring
                    ring_info = mol.GetRingInfo()
                    rings = ring_info.AtomRings()
                    for ring in rings:
                        if c1 in ring and c2 in ring:
                            return True, "Found adjacent carbonyl groups in ring system connected by single bond"
                
    return False, "No adjacent carbonyl groups found connected by single bond in ring system"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25622',
                          'name': 'orthoquinones',
                          'definition': 'Any quinone in which the carbons of '
                                        'the two carbonyl groups in the '
                                        'quinone system are joined to each '
                                        'other by a single bond.',
                          'parents': ['CHEBI:36141']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 36779,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 0.75,
    'f1': 0.056074766355140186,
    'accuracy': 0.9972616110403166}