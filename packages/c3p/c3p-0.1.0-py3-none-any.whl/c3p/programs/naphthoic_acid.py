"""
Classifies: CHEBI:25483 naphthoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_naphthoic_acid(smiles: str):
    """
    Determines if a molecule is a naphthoic acid (naphthalene with one or more carboxyl groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a naphthoic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES and check validity
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Split into fragments in case of salts
    fragments = Chem.GetMolFrags(mol, asMols=True)
    
    for fragment in fragments:
        # Check for naphthalene core
        rings = fragment.GetRingInfo()
        
        # Find fused aromatic rings
        aromatic_rings = []
        for ring in rings.AtomRings():
            if len(ring) == 6:
                atoms = [fragment.GetAtomWithIdx(i) for i in ring]
                if all(atom.GetIsAromatic() for atom in atoms):
                    aromatic_rings.append(set(ring))
        
        # Check for fused rings (naphthalene)
        has_naphthalene = False
        for i in range(len(aromatic_rings)):
            for j in range(i+1, len(aromatic_rings)):
                if len(aromatic_rings[i].intersection(aromatic_rings[j])) == 2:
                    # Verify the fused rings are made of carbon atoms
                    fused_atoms = list(aromatic_rings[i].union(aromatic_rings[j]))
                    if all(fragment.GetAtomWithIdx(idx).GetSymbol() == 'C' for idx in fused_atoms):
                        has_naphthalene = True
                        break
            if has_naphthalene:
                break
                
        if not has_naphthalene:
            continue
            
        # Check for carboxyl group(s)
        carboxyl_pattern = Chem.MolFromSmarts('C(=O)O')
        if fragment.HasSubstructMatch(carboxyl_pattern):
            num_carboxyl = len(fragment.GetSubstructMatches(carboxyl_pattern))
            return True, f"Naphthoic acid with {num_carboxyl} carboxyl group(s)"
            
    return False, "No naphthalene core with carboxyl group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25483',
                          'name': 'naphthoic acid',
                          'definition': 'An aromatic carboxylic acid that '
                                        'consists of a naphthalene skeleton '
                                        'substituted by one or more carboxy '
                                        'groups.',
                          'parents': ['CHEBI:25477', 'CHEBI:33859']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 29445,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9966160197624446}