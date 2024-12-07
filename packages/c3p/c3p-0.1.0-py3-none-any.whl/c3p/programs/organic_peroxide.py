"""
Classifies: CHEBI:25702 organic peroxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_organic_peroxide(smiles: str):
    """
    Determines if a molecule is an organic peroxide (ROOR' where R,R' are organic groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organic peroxide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find O-O bonds
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[O;!H0,$(O-[#6])]~[O;!H0,$(O-[#6])]'))
    
    if not matches:
        return False, "No O-O bonds found"

    # Check each O-O bond
    for match in matches:
        o1_idx, o2_idx = match
        o1 = mol.GetAtomWithIdx(o1_idx)
        o2 = mol.GetAtomWithIdx(o2_idx)
        
        # Get neighbors of both oxygens
        o1_neighbors = [n for n in o1.GetNeighbors() if n.GetIdx() != o2_idx]
        o2_neighbors = [n for n in o2.GetNeighbors() if n.GetIdx() != o1_idx]

        # Check if both oxygens are connected to carbon (organic groups)
        if (len(o1_neighbors) == 1 and len(o2_neighbors) == 1 and
            all(n.GetSymbol() == 'C' for n in o1_neighbors + o2_neighbors)):
            
            # Get the carbon groups attached to the oxygens
            r1 = o1_neighbors[0].GetSymbol() + ''.join([n.GetSymbol() for n in o1_neighbors[0].GetNeighbors() if n.GetIdx() != o1_idx])
            r2 = o2_neighbors[0].GetSymbol() + ''.join([n.GetSymbol() for n in o2_neighbors[0].GetNeighbors() if n.GetIdx() != o2_idx])
            
            return True, f"Contains organic peroxide group -O-O- with R groups: {r1} and {r2}"

    return False, "O-O bonds found but not part of organic peroxide structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25702',
                          'name': 'organic peroxide',
                          'definition': "Compounds of structure ROOR' in which "
                                        "R and R' are organic groups.",
                          'parents': ['CHEBI:25701', 'CHEBI:25940']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 104268,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9990418886291342}