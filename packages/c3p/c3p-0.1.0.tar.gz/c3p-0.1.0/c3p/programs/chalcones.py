"""
Classifies: CHEBI:23086 chalcones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_chalcones(smiles: str):
    """
    Determines if a molecule is a chalcone (1,3-diphenylpropenone derivative).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a chalcone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for C(=O)C=C substructure (enone)
    enone_pattern = Chem.MolFromSmarts('[#6](=[O:1])[#6]=[#6]')
    if not mol.HasSubstructMatch(enone_pattern):
        return False, "No enone (C(=O)C=C) group found"
    
    # Look for ArC(=O)C=CAr pattern
    chalcone_pattern = Chem.MolFromSmarts('[a;r6]~[#6](=[O:1])[#6]=[#6]~[a;r6]')
    if not mol.HasSubstructMatch(chalcone_pattern):
        return False, "Missing required ArC(=O)C=CAr pattern"

    # Check that both aromatic rings are 6-membered
    rings = mol.GetRingInfo()
    matches = mol.GetSubstructMatches(chalcone_pattern)
    
    for match in matches:
        # Get the atoms in the aromatic rings
        ar1_idx = match[0] 
        ar2_idx = match[-1]
        
        # Find the rings containing these atoms
        ar1_rings = [ring for ring in rings.AtomRings() if ar1_idx in ring]
        ar2_rings = [ring for ring in rings.AtomRings() if ar2_idx in ring]
        
        if not ar1_rings or not ar2_rings:
            continue
            
        if len(ar1_rings[0]) == 6 and len(ar2_rings[0]) == 6:
            # Get substituents on both rings
            substituents = []
            for ring in [ar1_rings[0], ar2_rings[0]]:
                for atom_idx in ring:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in ring and neighbor.GetSymbol() != 'C':
                            substituents.append(neighbor.GetSymbol())
                            
            if substituents:
                return True, f"Chalcone with substituents: {', '.join(set(substituents))}"
            else:
                return True, "Unsubstituted chalcone"
            
    return False, "Structure does not match chalcone pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23086',
                          'name': 'chalcones',
                          'definition': 'A ketone that is '
                                        '1,3-diphenylpropenone '
                                        '(benzylideneacetophenone), '
                                        'ArCH=CH(=O)Ar, and its derivatives '
                                        'formed by substitution.',
                          'parents': [   'CHEBI:51689',
                                         'CHEBI:72544',
                                         'CHEBI:76224']},
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
    'num_true_positives': 22,
    'num_false_positives': 100,
    'num_true_negatives': 61533,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.18032786885245902,
    'recall': 0.8148148148148148,
    'f1': 0.2953020134228188,
    'accuracy': 0.9982971132014272}