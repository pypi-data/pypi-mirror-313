"""
Classifies: CHEBI:145555 macropolylide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_macropolylide(smiles: str):
    """
    Determines if a molecule is a macropolylide (macrocyclic ring with multiple ester linkages).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a macropolylide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"

    # Find macrocyclic rings (size >= 12)
    macro_rings = [ring for ring in rings.AtomRings() if len(ring) >= 12]
    if not macro_rings:
        return False, "No macrocyclic rings (size >= 12) found"

    # Check for ester linkages in macrocyclic rings
    ester_count = 0
    for ring in macro_rings:
        ring_atoms = set(ring)
        
        # Find ester groups (-O-C(=O)-)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'O':
                neighbors = [n for n in atom.GetNeighbors()]
                if len(neighbors) == 2:
                    for n in neighbors:
                        if n.GetSymbol() == 'C':
                            for nn in n.GetNeighbors():
                                if nn.GetSymbol() == 'O' and nn.GetIsAromatic() == False and nn.GetDegree() == 1:
                                    # Found ester group where both O and C are in the ring
                                    if n.GetIdx() in ring_atoms:
                                        ester_count += 1

    if ester_count == 0:
        return False, "No ester linkages found in macrocyclic ring"
    elif ester_count == 1:
        return False, "Only one ester linkage found (macrolide but not macropolylide)"
    
    # Classify based on number of ester linkages
    if ester_count == 2:
        return True, "Macrodiolide (2 ester linkages)"
    elif ester_count == 3:
        return True, "Macrotriolide (3 ester linkages)" 
    elif ester_count == 4:
        return True, "Macrotetrolide (4 ester linkages)"
    elif ester_count == 5:
        return True, "Macropentolide (5 ester linkages)"
    else:
        return True, f"Macropolylide with {ester_count} ester linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145555',
                          'name': 'macropolylide',
                          'definition': 'Macrolides (macrocyclic lactones) in '
                                        'which the macrocyclic ring contains '
                                        'more than one ester linkage. '
                                        'Macropolylides include macrodiolides, '
                                        'macrotriolides, macrotetrolides and '
                                        'macropentolides, each containing di-, '
                                        'tri-, tetra-, and penta- ester '
                                        'linkages, respectively, in one '
                                        'macrocyclic ring. Macrocyclic '
                                        'lactones containing nitrogen in their '
                                        'skeletons (azamacrolides and '
                                        'macrolide lactams) and also '
                                        'containing oxazole or thiazole in '
                                        'their skeletons are known in nature.',
                          'parents': ['CHEBI:25106']},
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
    'num_true_negatives': 19221,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9948248201625006}