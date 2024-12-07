"""
Classifies: CHEBI:26004 phenylpropanoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_phenylpropanoid(smiles: str):
    """
    Determines if a molecule is a phenylpropanoid based on its structure.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phenylpropanoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for aromatic ring
    rings = mol.GetRingInfo()
    has_aromatic_ring = False
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                has_aromatic_ring = True
                break
    
    if not has_aromatic_ring:
        return False, "No aromatic ring found"

    # Look for phenylpropane skeleton (C6-C3)
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('c1ccccc1CCC'))
    if not matches:
        # Also check for modified phenylpropane structures common in phenylpropanoids
        patterns = [
            'c1ccccc1CC=C',  # Propenyl chain
            'c1ccccc1C(=O)CC', # Ketone
            'c1ccccc1COC', # Methoxy
            'c1ccccc1C1OCC1', # Cyclic ether
            'c1ccccc1C=CC=O', # Cinnamaldehyde
            'c1ccccc1C=CC(=O)O', # Cinnamic acid
            'c1ccccc1CC(=O)O', # Phenylacetic acid
        ]
        
        found_pattern = False
        for pattern in patterns:
            if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
                found_pattern = True
                break
                
        if not found_pattern:
            return False, "No phenylpropane or related skeleton found"

    # Check for common phenylpropanoid functionalities
    functionalities = []
    if mol.HasSubstructMatch(Chem.MolFromSmarts('cO')):
        functionalities.append("phenolic hydroxyl")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('cOC')):
        functionalities.append("methoxy")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)O')):
        functionalities.append("carboxylic acid")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C=O')):
        functionalities.append("carbonyl")
    
    if functionalities:
        return True, f"Phenylpropanoid with {', '.join(functionalities)} groups"
    else:
        return True, "Basic phenylpropanoid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26004',
                          'name': 'phenylpropanoid',
                          'definition': 'Any organic aromatic compound with a '
                                        'structure based on a phenylpropane '
                                        'skeleton. The class includes '
                                        'naturally occurring phenylpropanoid '
                                        'esters, flavonoids, anthocyanins, '
                                        'coumarins and many small phenolic '
                                        'molecules as well as their '
                                        'semi-synthetic and synthetic '
                                        'analogues. Phenylpropanoids are also '
                                        'precursors of lignin.',
                          'parents': ['CHEBI:33659']},
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
    'num_true_positives': 217,
    'num_false_positives': 100,
    'num_true_negatives': 423,
    'num_false_negatives': 96,
    'num_negatives': None,
    'precision': 0.6845425867507886,
    'recall': 0.6932907348242812,
    'f1': 0.6888888888888889,
    'accuracy': 0.7655502392344498}