"""
Classifies: CHEBI:21524 N-acetyl-D-glucosaminyl groups
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_N_acetyl_D_glucosaminyl_groups(smiles: str):
    """
    Determines if a molecule contains N-acetyl-D-glucosaminyl groups.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains N-acetyl-D-glucosaminyl groups, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for N-acetyl-D-glucosaminyl core
    # Matches pyranose ring with N-acetyl group and correct stereochemistry
    pattern = "[C@H]1[C@H]([C@H](O)[C@H]([CH]O1)NC(C)=O)O"
    
    substructure = Chem.MolFromSmarts(pattern)
    if substructure is None:
        return None, "Invalid SMARTS pattern"
        
    # Find matches
    matches = mol.GetSubstructMatches(substructure)
    
    if not matches:
        return False, "No N-acetyl-D-glucosaminyl groups found"
        
    # Check for pyranose ring
    rings = mol.GetRingInfo()
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered pyranose ring found"
        
    # Verify key structural features
    for match in matches:
        # Get atoms in match
        atoms = [mol.GetAtomWithIdx(i) for i in match]
        
        # Check for required functional groups
        has_n_acetyl = False
        has_hydroxyls = False
        
        for atom in atoms:
            # Check for N-acetyl group
            if atom.GetSymbol() == 'N':
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'C':
                        for n2 in neighbor.GetNeighbors():
                            if n2.GetSymbol() == 'O' and n2.GetIsAromatic() == False:
                                has_n_acetyl = True
                                
            # Check for hydroxyl groups
            if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() > 0:
                has_hydroxyls = True
                
        if not (has_n_acetyl and has_hydroxyls):
            continue
            
        return True, "Contains N-acetyl-D-glucosaminyl group(s)"
        
    return False, "Structure does not match N-acetyl-D-glucosaminyl group requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21524',
                          'name': 'N-acetyl-D-glucosaminyl groups',
                          'definition': 'A glucosaminyl group having '
                                        'D-configuration and an N-acetyl '
                                        'substituent (and derivatives '
                                        'thereof).',
                          'parents': ['CHEBI:24272']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1474,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9366687777074097}