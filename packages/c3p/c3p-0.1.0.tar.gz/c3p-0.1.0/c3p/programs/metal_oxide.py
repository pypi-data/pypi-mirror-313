"""
Classifies: CHEBI:133331 metal oxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_metal_oxide(smiles: str):
    """
    Determines if a molecule is a metal oxide (an inorganic oxide of any metal).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a metal oxide, False otherwise
        str: Reason for classification
    """
    # List of metals (includes transition metals, alkali/alkaline earth metals, post-transition metals)
    metals = {'Li','Be','Na','Mg','Al','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
              'Ga','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Cs','Ba',
              'La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta',
              'W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','Fr','Ra','Ac','Th','Pa','U',
              'Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr'}

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get all atoms in molecule
    atoms = [atom for atom in mol.GetAtoms()]
    
    # Check if molecule contains at least one metal
    metal_atoms = [atom for atom in atoms if atom.GetSymbol() in metals]
    if not metal_atoms:
        return False, "No metal atoms found"
        
    # Check if molecule contains oxygen
    oxygen_atoms = [atom for atom in atoms if atom.GetSymbol() == 'O']
    if not oxygen_atoms:
        return False, "No oxygen atoms found"
        
    # Check if oxygen is bonded to metal
    for metal in metal_atoms:
        for neighbor in metal.GetNeighbors():
            if neighbor.GetSymbol() == 'O':
                # Check if there's a metal-oxygen double bond or single bond
                bond = mol.GetBondBetweenAtoms(metal.GetIdx(), neighbor.GetIdx())
                if bond.GetBondType() in [Chem.BondType.SINGLE, Chem.BondType.DOUBLE]:
                    metal_sym = metal.GetSymbol()
                    charge = metal.GetFormalCharge()
                    charge_str = f"({charge:+d})" if charge != 0 else ""
                    return True, f"Metal oxide containing {metal_sym}{charge_str} bonded to oxygen"
    
    return False, "No metal-oxygen bonds found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133331',
                          'name': 'metal oxide',
                          'definition': 'An inorganic oxide that is an oxide '
                                        'of any metal.',
                          'parents': ['CHEBI:24836']},
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
    'num_true_negatives': 64914,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9984619170665683}