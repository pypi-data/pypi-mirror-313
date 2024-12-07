"""
Classifies: CHEBI:25978 phenylacetic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phenylacetic_acids(smiles: str):
    """
    Determines if a molecule is a phenylacetic acid or substituted derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phenylacetic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for phenylacetic acid core structure
    phenylacetic_pattern = Chem.MolFromSmarts('c1ccccc1CC(=O)O')
    if not mol.HasSubstructMatch(phenylacetic_pattern):
        return False, "No phenylacetic acid core structure found"
        
    # Get the aromatic ring
    ring_info = mol.GetRingInfo()
    aromatic_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
                
    if not aromatic_rings:
        return False, "No aromatic ring found"
        
    # Check substituents on the aromatic ring
    ring_atoms = set(aromatic_rings[0])
    substituents = []
    
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                if neighbor.GetSymbol() not in ['C', 'H']:  # Exclude the -CH2COOH chain
                    substituents.append(neighbor.GetSymbol())
                    
    if len(substituents) > 0:
        return True, f"Substituted phenylacetic acid with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted phenylacetic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25978',
                          'name': 'phenylacetic acids',
                          'definition': 'Any monocarboxylic acid that is '
                                        'phenylacetic acid or its substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:22712', 'CHEBI:25384']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 37225,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9973209740938195}