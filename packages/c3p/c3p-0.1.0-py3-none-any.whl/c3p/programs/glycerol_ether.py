"""
Classifies: CHEBI:24353 glycerol ether
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glycerol_ether(smiles: str):
    """
    Determines if a molecule is a glycerol ether (has glyceryl as at least one O-substituent)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycerol ether, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for glycerol backbone pattern:
    # -O-CH2-CH(O)-CH2-O- or -O-CH2-CH(O)-CH2-OH
    glycerol_patterns = [
        "[OX2]-[CH2]-[CH1](-[OX2])-[CH2]-[OX2]", # Fully substituted glycerol
        "[OX2]-[CH2]-[CH1](-[OX2])-[CH2]-[OH]",  # Terminal OH
        "[OH]-[CH2]-[CH1](-[OX2])-[CH2]-[OX2]",  # Terminal OH
        "[OH]-[CH2]-[CH1](-[OX2])-[CH2]-[OH]"    # Two terminal OHs
    ]
    
    for pattern in glycerol_patterns:
        substructure = Chem.MolFromSmarts(pattern)
        if mol.HasSubstructMatch(substructure):
            matches = mol.GetSubstructMatches(substructure)
            
            # Verify at least one O is an ether oxygen (not part of ester/phosphate)
            for match in matches:
                oxygens = [i for i in match if mol.GetAtomWithIdx(i).GetSymbol() == 'O']
                for o_idx in oxygens:
                    o_atom = mol.GetAtomWithIdx(o_idx)
                    neighbors = [n for n in o_atom.GetNeighbors()]
                    
                    # Check if oxygen is part of an ether
                    is_ether = True
                    for n in neighbors:
                        if n.GetSymbol() == 'C':
                            if any(b.GetBondType() == Chem.BondType.DOUBLE for b in n.GetBonds()):
                                is_ether = False
                        elif n.GetSymbol() == 'P':
                            is_ether = False
                            
                    if is_ether:
                        return True, "Contains glyceryl ether moiety"
                        
    return False, "No glyceryl ether moiety found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24353',
                          'name': 'glycerol ether',
                          'definition': 'Any ether having glyceryl as at least '
                                        'one of the O-substituents.',
                          'parents': ['CHEBI:25698']},
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
    'num_true_positives': 46,
    'num_false_positives': 100,
    'num_true_negatives': 5786,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.3150684931506849,
    'recall': 0.7931034482758621,
    'f1': 0.45098039215686275,
    'accuracy': 0.9811574697173621}