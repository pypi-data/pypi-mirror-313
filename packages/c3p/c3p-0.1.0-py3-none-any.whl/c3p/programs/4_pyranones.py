"""
Classifies: CHEBI:131906 4-pyranones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4_pyranones(smiles: str):
    """
    Determines if a molecule is a 4-pyranone (contains 4H-pyran-4-one core).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains 4-pyranone core, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for 4H-pyran-4-one core
    # [O;R1]-1-[#6;R1]=[#6;R1]-[#6;R1](=O)-[#6;R1]=[#6;R1]-1
    pyranone_pattern = Chem.MolFromSmarts('[O;R1]1[#6;R1]=[#6;R1][#6;R1](=O)[#6;R1]=[#6;R1]1')
    
    if mol.HasSubstructMatch(pyranone_pattern):
        # Count number of pyranone cores
        matches = mol.GetSubstructMatches(pyranone_pattern)
        num_cores = len(matches)
        
        # Get substituents
        substituents = []
        for match in matches:
            core_atoms = set(match)
            for atom_idx in match:
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() not in core_atoms:
                        if neighbor.GetSymbol() != 'H':  # Ignore hydrogens
                            substituents.append(neighbor.GetSymbol())
        
        if len(substituents) > 0:
            return True, f"Contains {num_cores} 4-pyranone core(s) with substituents: {', '.join(set(substituents))}"
        else:
            return True, f"Contains {num_cores} unsubstituted 4-pyranone core(s)"
    
    return False, "No 4-pyranone core found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131906',
                          'name': '4-pyranones',
                          'definition': 'A pyranone based on the structure of '
                                        '4H-pyran-4-one and its substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:37963', 'CHEBI:3992']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183911,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891252929374}