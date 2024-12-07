"""
Classifies: CHEBI:25497 neolignan
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdDecomposition

def is_neolignan(smiles: str):
    """
    Determines if a molecule is a neolignan based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a neolignan, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for minimum size - neolignans should have at least 2 phenylpropanoid units
    num_atoms = mol.GetNumAtoms()
    if num_atoms < 18:  # Minimum size for 2 phenylpropanoid units
        return False, "Molecule too small to be a neolignan"

    # Look for aromatic rings
    aromatic_rings = []
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if len(aromatic_rings) < 2:
        return False, "Insufficient number of aromatic rings"

    # Check for typical neolignan features
    has_methoxy = False
    has_hydroxy = False
    has_propyl = False
    
    # Look for methoxy groups (-OCH3)
    pattern_methoxy = Chem.MolFromSmarts('cOC')
    if mol.HasSubstructMatch(pattern_methoxy):
        has_methoxy = True
        
    # Look for hydroxy groups (-OH)
    pattern_hydroxy = Chem.MolFromSmarts('cO[H]')
    if mol.HasSubstructMatch(pattern_hydroxy):
        has_hydroxy = True
        
    # Look for propyl chain connections
    pattern_propyl = Chem.MolFromSmarts('ccC[C@H]')
    if mol.HasSubstructMatch(pattern_propyl):
        has_propyl = True

    # Check for ether linkages between units (typical in neolignans)
    pattern_ether = Chem.MolFromSmarts('cOc')
    has_ether = mol.HasSubstructMatch(pattern_ether)

    # Check for beta-carbon coupling (should not be present in neolignans)
    pattern_beta = Chem.MolFromSmarts('ccCC(C)CC')
    beta_coupled = mol.HasSubstructMatch(pattern_beta)

    if beta_coupled:
        return False, "Contains beta-carbon coupling typical of lignans"

    # Evaluate overall structure
    if has_methoxy and has_hydroxy and has_propyl and has_ether:
        features = []
        if has_methoxy:
            features.append("methoxy groups")
        if has_hydroxy:
            features.append("hydroxy groups")
        if has_propyl:
            features.append("propyl chains")
        if has_ether:
            features.append("ether linkages")
            
        return True, f"Neolignan structure confirmed with: {', '.join(features)}"
    else:
        missing = []
        if not has_methoxy:
            missing.append("methoxy groups")
        if not has_hydroxy:
            missing.append("hydroxy groups")
        if not has_propyl:
            missing.append("propyl chains")
        if not has_ether:
            missing.append("ether linkages")
            
        return False, f"Missing key neolignan features: {', '.join(missing)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25497',
                          'name': 'neolignan',
                          'definition': 'A phenylpropanoid that includes plant '
                                        'products formed primarily from '
                                        'oxidative coupling of two '
                                        'para-propylphenol moities. Unlike '
                                        'lignan, the units are coupled at  '
                                        'positions other than their '
                                        'beta-carbon atoms.',
                          'parents': ['CHEBI:26004']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}