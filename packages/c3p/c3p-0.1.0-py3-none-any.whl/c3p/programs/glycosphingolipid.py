"""
Classifies: CHEBI:24402 glycosphingolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glycosphingolipid(smiles: str):
    """
    Determines if a molecule is a glycosphingolipid - a glycolipid that is a carbohydrate-containing 
    derivative of a sphingoid or ceramide, with the carbohydrate residue attached by a glycosidic linkage 
    to O-1 of the sphingoid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycosphingolipid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of sphingoid/ceramide core
    # Look for characteristic NH-C(=O) amide group and long alkyl chains
    has_amide = False
    has_long_chain = False
    
    # Find amide group
    amide_pattern = Chem.MolFromSmarts('[NH]-C(=O)')
    if mol.HasSubstructMatch(amide_pattern):
        has_amide = True
        
    # Check for long carbon chains by counting connected carbons
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            visited = set()
            chain_length = count_carbon_chain(atom, visited)
            if chain_length >= 10:
                has_long_chain = True
                break
                
    if not (has_amide and has_long_chain):
        return False, "Missing sphingoid/ceramide core structure"

    # Check for carbohydrate residue
    # Look for multiple OH groups and cyclic structures containing O
    rings = mol.GetRingInfo()
    has_sugar = False
    
    for ring in rings.AtomRings():
        if len(ring) >= 5:  # Sugar rings are typically 5 or 6-membered
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            o_count = sum(1 for a in ring_atoms if a.GetSymbol() == 'O')
            oh_count = sum(1 for a in ring_atoms if a.GetSymbol() == 'C' 
                         and any(n.GetSymbol() == 'O' and n.GetTotalNumHs() > 0 
                               for n in a.GetNeighbors()))
            if o_count >= 1 and oh_count >= 2:
                has_sugar = True
                break
                
    if not has_sugar:
        return False, "Missing carbohydrate residue"

    # Check for glycosidic linkage
    # Look for C-O-C connection between sugar and sphingoid
    glycosidic_pattern = Chem.MolFromSmarts('[C]-O-[C]')
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "Missing glycosidic linkage"

    return True, "Contains sphingoid core, carbohydrate residue, and glycosidic linkage"

def count_carbon_chain(atom, visited):
    """Helper function to count length of connected carbon chains"""
    if atom.GetIdx() in visited or atom.GetSymbol() != 'C':
        return 0
    
    visited.add(atom.GetIdx())
    max_length = 1
    
    for neighbor in atom.GetNeighbors():
        if neighbor.GetSymbol() == 'C':
            length = count_carbon_chain(neighbor, visited)
            max_length = max(max_length, length + 1)
            
    return max_length


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24402',
                          'name': 'glycosphingolipid',
                          'definition': 'A glycosphingolipid is a glycolipid '
                                        'that is a carbohydrate-containing '
                                        'derivative of a sphingoid or '
                                        'ceramide. It is understood that the '
                                        'carbohydrate residue is attached by a '
                                        'glycosidic linkage to O-1 of the '
                                        'sphingoid.',
                          'parents': ['CHEBI:26739', 'CHEBI:33563']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 100,
    'num_false_positives': 100,
    'num_true_negatives': 10845,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 0.8264462809917356,
    'f1': 0.6230529595015577,
    'accuracy': 0.989065606361829}