"""
Classifies: CHEBI:26255 prenylquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_prenylquinone(smiles: str):
    """
    Determines if a molecule is a prenylquinone (quinone with polyprenyl side chain).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a prenylquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for quinone core
    # Look for pattern C(=O)-C=C-C(=O)
    quinone_pattern = Chem.MolFromSmarts('[C;$(C=O)]-[C;$(C=C)]-[C;$(C=C)]-[C;$(C=O)]')
    if not mol.HasSubstructMatch(quinone_pattern):
        return False, "No quinone core found"
        
    # Check for prenyl/polyprenyl side chain
    # Look for repeating isoprene units (C5H8)
    prenyl_pattern = Chem.MolFromSmarts('CC(=C)CC|CC(C)=CC')
    if not mol.HasSubstructMatch(prenyl_pattern):
        return False, "No prenyl/polyprenyl side chain found"
        
    # Count number of prenyl units
    prenyl_matches = len(mol.GetSubstructMatches(prenyl_pattern))
    
    # Additional checks for specific prenylquinone classes
    menaquinone_pattern = Chem.MolFromSmarts('c1ccccc1C(=O)C=CC(=O)')
    ubiquinone_pattern = Chem.MolFromSmarts('COC1=CC(=O)C(=C(OC)C1=O)')
    plastoquinone_pattern = Chem.MolFromSmarts('COC1=CC(=O)C(C)=C(C1=O)')
    
    prenylquinone_class = []
    if mol.HasSubstructMatch(menaquinone_pattern):
        prenylquinone_class.append("menaquinone")
    if mol.HasSubstructMatch(ubiquinone_pattern):
        prenylquinone_class.append("ubiquinone")  
    if mol.HasSubstructMatch(plastoquinone_pattern):
        prenylquinone_class.append("plastoquinone")
        
    if prenyl_matches > 0:
        class_str = f" (Possible {', '.join(prenylquinone_class)})" if prenylquinone_class else ""
        return True, f"Prenylquinone with {prenyl_matches} prenyl units{class_str}"
    
    return False, "Structure does not match prenylquinone characteristics"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26255',
                          'name': 'prenylquinone',
                          'definition': 'A quinone substituted by a '
                                        'polyprenyl-derived side-chain. '
                                        'Prenylquinones occur in all living '
                                        'cells. Due to their amphiphilic '
                                        'character, they are mainly located in '
                                        'biological membranes where they '
                                        'function as electron and proton '
                                        'carriers in the photosynthetic and '
                                        'respiratory electron transport '
                                        'chains. Some prenylquinones also '
                                        'perform more specialised roles sucy '
                                        'as antioxidants and enzyme cofactors. '
                                        'Prenylquinones are classified '
                                        'according to ring structure: the main '
                                        'classes are menaquinones, '
                                        'phylloquinones, ubiquinones and '
                                        'plastoquinones.',
                          'parents': ['CHEBI:25830']},
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
    'error': 'Python argument types in\n'
             '    Mol.HasSubstructMatch(Mol, NoneType)\n'
             'did not match C++ signature:\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle query, '
             'RDKit::SubstructMatchParameters params=True)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
             'RDKit::SubstructMatchParameters params)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle query, '
             'bool recursionPossible=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
             'bool recursionPossible=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False)',
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