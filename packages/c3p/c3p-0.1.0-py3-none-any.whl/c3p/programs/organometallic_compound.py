"""
Classifies: CHEBI:25707 organometallic compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organometallic_compound(smiles: str):
    """
    Determines if a molecule is an organometallic compound, defined as having bonds 
    between one or more metal atoms and one or more carbon atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organometallic compound, False otherwise
        str: Reason for classification
    """
    # Define list of metals (main group metals and transition metals)
    metals = ['Li','Na','K','Rb','Cs','Fr',
              'Be','Mg','Ca','Sr','Ba','Ra',
              'Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
              'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd',
              'La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg',
              'Al','Ga','In','Sn','Tl','Pb','Bi','Po']

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find metal atoms in molecule
    metal_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() in metals:
            metal_atoms.append(atom)

    if not metal_atoms:
        return False, "No metal atoms found"

    # Check if any metal atom is bonded to carbon
    metal_carbon_bonds = []
    for metal in metal_atoms:
        for neighbor in metal.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                metal_carbon_bonds.append((metal.GetSymbol(), neighbor.GetIdx()))

    if not metal_carbon_bonds:
        return False, "No metal-carbon bonds found"

    # Get details about metal-carbon bonds
    bond_details = []
    for metal_symbol, carbon_idx in metal_carbon_bonds:
        carbon = mol.GetAtomWithIdx(carbon_idx)
        # Check if carbon is part of an organyl group
        if any(n.GetSymbol() in ['C','H'] for n in carbon.GetNeighbors()):
            bond_details.append(f"{metal_symbol}-C")

    if not bond_details:
        return False, "No metal-organyl bonds found"

    unique_metals = set(metal.GetSymbol() for metal in metal_atoms)
    return True, f"Organometallic compound with {', '.join(unique_metals)}-C bond(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25707',
                          'name': 'organometallic compound',
                          'definition': 'A compound having bonds between one '
                                        'or more metal atoms and one or more '
                                        'carbon atoms of an organyl group.',
                          'parents': ['CHEBI:50860']},
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
    'num_false_positives': 54,
    'num_true_negatives': 183795,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.06896551724137931,
    'recall': 0.5,
    'f1': 0.1212121212121212,
    'accuracy': 0.999684537439423}