"""
Classifies: CHEBI:149433 mannotetraose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_mannotetraose(smiles: str):
    """
    Determines if a molecule is a mannotetraose (tetrasaccharide composed of 4 mannose units)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a mannotetraose, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Count number of pyranose rings (6-membered rings containing oxygen)
    rings = mol.GetRingInfo()
    pyranose_rings = []
    
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring contains exactly one oxygen
            if sum(1 for atom in atoms if atom.GetSymbol() == 'O') == 1:
                pyranose_rings.append(ring)
                
    if len(pyranose_rings) != 4:
        return False, f"Found {len(pyranose_rings)} pyranose rings, expected 4"
        
    # For each pyranose ring, check if it matches mannose pattern:
    # - One oxygen in ring
    # - 4 carbons with OH groups (or glycosidic linkages)
    # - One carbon with CH2OH group
    for ring in pyranose_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Count oxygens
        ring_oxygens = sum(1 for atom in atoms if atom.GetSymbol() == 'O')
        if ring_oxygens != 1:
            return False, f"Ring contains {ring_oxygens} oxygens, expected 1"
            
        # Check carbons
        carbons = [atom for atom in atoms if atom.GetSymbol() == 'C']
        if len(carbons) != 5:
            return False, f"Ring contains {len(carbons)} carbons, expected 5"
            
        # Check for OH groups or glycosidic linkages on carbons
        for carbon in carbons:
            oxygen_count = sum(1 for neighbor in carbon.GetNeighbors() 
                             if neighbor.GetSymbol() == 'O')
            if oxygen_count == 0:
                return False, "Missing OH groups or glycosidic linkages"
                
    # Check for glycosidic linkages between rings
    linkage_count = 0
    for bond in mol.GetBonds():
        if (bond.GetBeginAtom().GetSymbol() == 'O' and 
            bond.GetEndAtom().GetSymbol() == 'C'):
            linkage_count += 1
        elif (bond.GetBeginAtom().GetSymbol() == 'C' and 
              bond.GetEndAtom().GetSymbol() == 'O'):
            linkage_count += 1
            
    if linkage_count < 3:
        return False, f"Found only {linkage_count} glycosidic linkages, expected at least 3"
        
    return True, "Molecule contains 4 mannose units connected by glycosidic linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:149433',
                          'name': 'mannotetraose',
                          'definition': 'Any tetrasaccharide composed of 4 '
                                        'mannose moieties.',
                          'parents': ['CHEBI:25174', 'CHEBI:50126']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_negatives': 44983,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9977819673949208}