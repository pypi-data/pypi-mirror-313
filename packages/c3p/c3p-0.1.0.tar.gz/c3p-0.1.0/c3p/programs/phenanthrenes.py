"""
Classifies: CHEBI:25961 phenanthrenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_phenanthrenes(smiles: str):
    """
    Determines if a molecule is a phenanthrene or substituted phenanthrene.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phenanthrene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Generate the aromatic ring information
    rings = mol.GetRingInfo()
    
    # Need at least 3 rings
    if len(rings.AtomRings()) < 3:
        return False, "Less than 3 rings found"
        
    # Find all aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
                
    if len(aromatic_rings) < 3:
        return False, "Less than 3 aromatic 6-membered rings found"
        
    # Check if we have a phenanthrene core structure
    # First create a substructure match pattern for phenanthrene
    phenanthrene_pattern = Chem.MolFromSmarts('c1cccc2c1ccc3ccccc32')
    if not mol.HasSubstructMatch(phenanthrene_pattern):
        return False, "No phenanthrene core structure found"
        
    # If we get here, we have a phenanthrene core
    # Check for substituents
    matches = mol.GetSubstructMatches(phenanthrene_pattern)
    if len(matches) == 0:
        return False, "No phenanthrene substructure found"
        
    core_atoms = set(matches[0])
    substituents = []
    
    for atom_idx in range(mol.GetNumAtoms()):
        if atom_idx not in core_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            # Check if this non-core atom is connected to the core
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() in core_atoms:
                    substituents.append(atom.GetSymbol())
                    break
                    
    if len(substituents) > 0:
        return True, f"Substituted phenanthrene with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted phenanthrene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25961',
                          'name': 'phenanthrenes',
                          'definition': 'Any benzenoid aromatic compound that '
                                        'consists of a phenanthrene skeleton '
                                        'and its substituted derivatives '
                                        'thereof.',
                          'parents': ['CHEBI:33836', 'CHEBI:38032']},
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
    'num_false_positives': 100,
    'num_true_negatives': 77591,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 0.3225806451612903,
    'f1': 0.14184397163120568,
    'accuracy': 0.9984431692442294}