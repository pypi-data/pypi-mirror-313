"""
Classifies: CHEBI:23437 cyanohydrin
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyanohydrin(smiles: str):
    """
    Determines if a molecule is a cyanohydrin (alpha-hydroxynitrile).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cyanohydrin, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find carbons with both OH and CN groups
    cyanohydrin_carbons = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != 'C':
            continue
            
        # Check for CN group
        has_cn = False
        has_oh = False
        
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'N':
                # Check if N is part of CN triple bond
                if neighbor.GetDegree() == 1 and len([b for b in neighbor.GetBonds() if b.GetBondType() == Chem.BondType.TRIPLE]) == 1:
                    has_cn = True
            elif neighbor.GetSymbol() == 'O':
                # Check if O is part of OH group
                if neighbor.GetDegree() == 1:
                    has_oh = True
                    
        if has_cn and has_oh:
            cyanohydrin_carbons.append(atom.GetIdx())
            
    if not cyanohydrin_carbons:
        return False, "No carbon with both OH and CN groups found"
        
    # For each potential cyanohydrin carbon, check if it was derived from aldehyde/ketone
    for c_idx in cyanohydrin_carbons:
        c_atom = mol.GetAtomWithIdx(c_idx)
        
        # Count number of carbon neighbors (excluding CN)
        carbon_neighbors = 0
        for neighbor in c_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                # Don't count the CN carbon
                if not any(n.GetSymbol() == 'N' and n.GetDegree() == 1 for n in neighbor.GetNeighbors()):
                    carbon_neighbors += 1
                    
        # Must have 0-2 carbon neighbors (excluding CN)
        # 0 = formaldehyde-derived
        # 1 = aldehyde-derived  
        # 2 = ketone-derived
        if carbon_neighbors <= 2:
            if carbon_neighbors == 0:
                return True, "Formaldehyde-derived cyanohydrin"
            elif carbon_neighbors == 1:
                return True, "Aldehyde-derived cyanohydrin"
            else:
                return True, "Ketone-derived cyanohydrin"
                
    return False, "Structure does not match cyanohydrin pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23437',
                          'name': 'cyanohydrin',
                          'definition': 'An alpha-hydroxynitrile resulting '
                                        'from the formal addition of hydrogen '
                                        'cyanide to the C=O bond of an '
                                        'aldehyde or ketone.',
                          'parents': ['CHEBI:22455']},
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
    'num_false_positives': 3,
    'num_true_negatives': 183895,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673737500068}