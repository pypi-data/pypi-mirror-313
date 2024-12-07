"""
Classifies: CHEBI:24151 galactooligosaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_galactooligosaccharide(smiles: str):
    """
    Determines if a molecule is a galactooligosaccharide (oligosaccharide of galactose residues)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a galactooligosaccharide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Count number of oxygen atoms in rings (pyranose/furanose oxygens)
    ring_O_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.IsInRing():
            ring_O_count += 1
            
    if ring_O_count < 2:
        return False, "Less than 2 sugar rings found"
        
    # Count number of carbons and oxygens
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    
    # Check C:O ratio - galactose has C6H12O6 so ratio should be ~1:1
    if num_carbons/num_oxygens < 0.8 or num_carbons/num_oxygens > 1.2:
        return False, "C:O ratio not consistent with galactose units"
        
    # Check for presence of glycosidic bonds (O linking two carbons)
    glycosidic_bonds = 0
    for bond in mol.GetBonds():
        if bond.GetBeginAtom().GetSymbol() == 'O' and bond.GetEndAtom().GetSymbol() == 'C':
            o_atom = bond.GetBeginAtom()
            neighbors = [n for n in o_atom.GetNeighbors()]
            if len(neighbors) == 2 and all(n.GetSymbol() == 'C' for n in neighbors):
                glycosidic_bonds += 1
    
    if glycosidic_bonds < 1:
        return False, "No glycosidic bonds found"
        
    # Check for hydroxyl groups characteristic of sugars
    hydroxyl_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            neighbors = [n for n in atom.GetNeighbors()]
            if len(neighbors) == 1 and neighbors[0].GetSymbol() == 'C':
                hydroxyl_count += 1
                
    if hydroxyl_count < ring_O_count:
        return False, "Insufficient hydroxyl groups for galactose units"
        
    # If all checks pass, this is likely a galactooligosaccharide
    return True, f"Contains {ring_O_count} galactose units linked by {glycosidic_bonds} glycosidic bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24151',
                          'name': 'galactooligosaccharide',
                          'definition': 'An oligosaccharide comprised of '
                                        'galactose residues.',
                          'parents': ['CHEBI:50699']},
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
    'num_true_negatives': 6426,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9846860643185299}