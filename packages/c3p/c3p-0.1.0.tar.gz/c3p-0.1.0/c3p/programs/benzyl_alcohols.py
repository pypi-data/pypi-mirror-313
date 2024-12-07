"""
Classifies: CHEBI:22743 benzyl alcohols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzyl_alcohols(smiles: str):
    """
    Determines if a molecule is a benzyl alcohol (contains phenylmethanol skeleton).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzyl alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Create SMARTS pattern for benzyl alcohol
    # [cH,c]:1:[cH,c]:[cH,c]:[cH,c]:[cH,c]:[cH,c]:1[CH2]O
    # This matches a benzene ring (aromatic carbons) connected to a CH2OH group
    benzyl_alcohol_pattern = Chem.MolFromSmarts('[cH,c]1[cH,c][cH,c][cH,c][cH,c][cH,c]1[CH2]O')
    
    if mol.HasSubstructMatch(benzyl_alcohol_pattern):
        # Get the matches
        matches = mol.GetSubstructMatches(benzyl_alcohol_pattern)
        
        # For each match, verify the carbon of CH2OH is sp3 hybridized
        for match in matches:
            ch2_idx = match[-2]  # Second to last atom in match is the CH2
            ch2_atom = mol.GetAtomWithIdx(ch2_idx)
            
            if ch2_atom.GetHybridization() == Chem.HybridizationType.SP3:
                # Count number of substituents on benzene ring
                ring_atoms = match[0:6]
                substituents = []
                
                for atom_idx in ring_atoms:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in ring_atoms and neighbor.GetIdx() != ch2_idx:
                            substituents.append(neighbor.GetSymbol())
                
                if len(substituents) > 0:
                    return True, f"Benzyl alcohol with substituents: {', '.join(set(substituents))}"
                else:
                    return True, "Unsubstituted benzyl alcohol"
                    
    return False, "No benzyl alcohol substructure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22743',
                          'name': 'benzyl alcohols',
                          'definition': 'Compounds containing a phenylmethanol '
                                        'skeleton.',
                          'parents': ['CHEBI:33854']},
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
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 6056,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 0.8181818181818182,
    'f1': 0.15000000000000002,
    'accuracy': 0.9834603534944057}