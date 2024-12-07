"""
Classifies: CHEBI:146306 partially-defined glycan
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_partially_defined_glycan(smiles: str):
    """
    Determines if a molecule is a partially defined glycan.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a partially defined glycan, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of wildcard atoms (*) indicating undefined parts
    has_wildcards = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == '*':
            has_wildcards = True
            break
            
    # Check for typical glycan features
    # - Multiple cyclic sugars (rings with 5-6 atoms containing O)
    # - Multiple OH groups
    # - Glycosidic linkages (C-O-C between rings)
    
    rings = mol.GetRingInfo()
    sugar_rings = []
    
    for ring in rings.AtomRings():
        if len(ring) in [5,6]:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            has_o = False
            has_multiple_oh = 0
            for atom in ring_atoms:
                if atom.GetSymbol() == 'O':
                    has_o = True
                if atom.GetSymbol() == 'O' and atom.GetTotalDegree() == 2:
                    has_multiple_oh += 1
            if has_o and has_multiple_oh >= 1:
                sugar_rings.append(ring)
                
    if len(sugar_rings) < 2:
        return False, "Not enough sugar rings detected"
        
    # Check for glycosidic linkages between rings
    glycosidic_linkages = 0
    for bond in mol.GetBonds():
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        if a1.GetSymbol() == 'O' and a2.GetSymbol() == 'C':
            if a1.IsInRing() != a2.IsInRing():
                glycosidic_linkages += 1
        elif a1.GetSymbol() == 'C' and a2.GetSymbol() == 'O':
            if a1.IsInRing() != a2.IsInRing():
                glycosidic_linkages += 1
                
    if glycosidic_linkages < 1:
        return False, "No glycosidic linkages detected"

    # Classify based on findings
    if has_wildcards:
        return True, "Partially defined glycan with undefined substituents/linkages"
    elif '?' in smiles:
        return True, "Partially defined glycan with undefined stereochemistry"
    elif any(x in smiles for x in ['alpha', 'beta']):
        return True, "Fully defined glycan"
    else:
        return True, "Partially defined glycan with undefined anomeric configuration"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:146306',
                          'name': 'partially-defined glycan',
                          'definition': 'A member of the class of '
                                        'carbohydrates and carbohydrate '
                                        'derivatives that is any '
                                        'oligosaccharide or polysaccharide in '
                                        'which the identity of one or more of '
                                        'the individual monosaccharide units, '
                                        'their connectivity (position of '
                                        'attachment) or the stereochemistry '
                                        '(alpha- or beta-) of one or more of '
                                        'the glycosidic linkages is not known.',
                          'parents': ['CHEBI:78616']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}