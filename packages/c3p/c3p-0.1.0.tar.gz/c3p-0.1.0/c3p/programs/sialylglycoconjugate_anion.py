"""
Classifies: CHEBI:231691 sialylglycoconjugate anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sialylglycoconjugate_anion(smiles: str):
    """
    Determines if a molecule is a sialylglycoconjugate anion.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sialylglycoconjugate anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for sialic acid (neuraminic acid) core structure
    sialic_acid_pattern = Chem.MolFromSmarts('[C@]1([C@@H]([C@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O')
    if not mol.HasSubstructMatch(sialic_acid_pattern):
        return False, "No sialic acid core structure found"

    # Check for glycosidic linkages
    glycosidic_pattern = Chem.MolFromSmarts('O[CH1]1[CH1][CH1][CH1][CH1]O[CH1]')
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "No glycosidic linkages found"
        
    # Check for carboxylate anion
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion found"

    # Check for ceramide or other glycoconjugate portion
    ceramide_pattern = Chem.MolFromSmarts('CCCCCCCCC')  # Simplified pattern for long alkyl chain
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "No ceramide/glycoconjugate portion found"

    # Count number of sialic acid residues
    sialic_acid_count = len(mol.GetSubstructMatches(sialic_acid_pattern))
    
    # Count number of glycosidic linkages
    glycosidic_count = len(mol.GetSubstructMatches(glycosidic_pattern))

    return True, f"Sialylglycoconjugate anion with {sialic_acid_count} sialic acid residues and {glycosidic_count} glycosidic linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:231691',
                          'name': 'sialylglycoconjugate anion',
                          'definition': 'A sialylglycoconjugate where the '
                                        'composition of the glycoconjugate '
                                        'represented with an R is not defined, '
                                        'can be an oligosaccharide, a '
                                        'glycoprotein or a glycolipid.',
                          'parents': ['CHEBI:78616']},
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
    'num_true_negatives': 183643,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998421098479899}