"""
Classifies: CHEBI:26605 saponin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_saponin(smiles: str):
    """
    Determines if a molecule is a saponin based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a saponin, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # Check for minimum size - saponins are large molecules
        num_atoms = mol.GetNumAtoms()
        if num_atoms < 40:
            return False, "Molecule too small to be a saponin"
            
        # Check for presence of sugar moiety (glycoside)
        sugar_pattern = Chem.MolFromSmarts('[CH]1[CH][CH][CH][CH]O1') # Basic pyranose ring
        if not mol.HasSubstructMatch(sugar_pattern):
            return False, "No sugar/glycoside moiety found"
            
        # Check for steroid/triterpenoid core
        # Look for multiple 6-membered rings characteristic of steroid/triterpenoid skeleton
        rings = mol.GetRingInfo()
        six_mem_rings = sum(1 for ring in rings.AtomRings() if len(ring) == 6)
        if six_mem_rings < 4:
            return False, "No steroid/triterpenoid core structure found"
            
        # Check for characteristic O-glycosidic linkage
        glycosidic_pattern = Chem.MolFromSmarts('[CH]O[CH]1[CH][CH][CH][CH]O1')
        if not mol.HasSubstructMatch(glycosidic_pattern):
            return False, "No O-glycosidic linkage found"
            
        # Calculate lipophilicity using logP
        logp = Descriptors.MolLogP(mol)
        if logp < 0:
            return False, "Molecule not sufficiently lipophilic"
            
        # Molecule has passed all saponin criteria
        sugar_count = len(mol.GetSubstructMatches(sugar_pattern))
        return True, f"Saponin with {sugar_count} sugar moieties detected"
        
    except:
        return None, None


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26605',
                          'name': 'saponin',
                          'definition': 'A glycoside that is a compound '
                                        'containing one or more hydrophilic '
                                        'glycoside moieties combined with a '
                                        'lipophilic triterpenoid or steroid '
                                        'derivative. Found in particular '
                                        'abundance in plant species.',
                          'parents': ['CHEBI:24400']},
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
    'num_true_positives': 39,
    'num_false_positives': 100,
    'num_true_negatives': 39917,
    'num_false_negatives': 43,
    'num_negatives': None,
    'precision': 0.2805755395683453,
    'recall': 0.47560975609756095,
    'f1': 0.35294117647058815,
    'accuracy': 0.9964338262799571}