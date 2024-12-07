"""
Classifies: CHEBI:22693 barbiturates
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_barbiturates(smiles: str):
    """
    Determines if a molecule is a barbiturate (derivative of barbituric acid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a barbiturate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # SMARTS pattern for barbituric acid core (pyrimidine-2,4,6-trione)
    # Matches both O=C and S=C for thio-barbiturates
    barbiturate_pattern = Chem.MolFromSmarts('[#7]1-[#6](=[#8,#16])-[#7]-[#6](=[#8])-[#6]-[#6](=[#8])-1')
    
    if not mol.HasSubstructMatch(barbiturate_pattern):
        return False, "No barbituric acid core structure found"
        
    # Get the atoms in the barbituric acid core
    core_match = mol.GetSubstructMatch(barbiturate_pattern)
    if not core_match:
        return False, "Could not map barbituric acid core atoms"
        
    # Check if the core has proper substitution pattern
    core_atoms = set(core_match)
    
    # Count number of thio (=S) groups
    thio_count = 0
    for atom_idx in core_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'S' and atom.GetTotalNumHs() == 0:
            thio_count += 1
            
    # Get substituents on the ring
    substituents = []
    for atom_idx in core_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in core_atoms:
                if neighbor.GetSymbol() != 'H':
                    substituents.append(neighbor.GetSymbol())
                    
    if thio_count > 0:
        return True, f"Thiobarbiturate with {len(substituents)} substituents"
    else:
        return True, f"Barbiturate with {len(substituents)} substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22693',
                          'name': 'barbiturates',
                          'definition': 'Members of the class of pyrimidones '
                                        'consisting of '
                                        'pyrimidine-2,4,6(1H,3H,5H)-trione '
                                        '(barbituric acid) and its '
                                        'derivatives. Largest group of the '
                                        'synthetic sedative/hypnotics, sharing '
                                        'a characteristic six-membered ring '
                                        'structure.',
                          'parents': ['CHEBI:38337']},
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
    'num_true_positives': 10,
    'num_false_positives': 63,
    'num_true_negatives': 183766,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.136986301369863,
    'recall': 1.0,
    'f1': 0.24096385542168672,
    'accuracy': 0.999657308840888}