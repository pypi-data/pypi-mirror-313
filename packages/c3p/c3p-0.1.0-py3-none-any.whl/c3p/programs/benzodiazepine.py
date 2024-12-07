"""
Classifies: CHEBI:22720 benzodiazepine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzodiazepine(smiles: str):
    """
    Determines if a molecule is a benzodiazepine (contains a benzene ring fused to a diazepine ring).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a benzodiazepine, False otherwise
        str: Reason for classification
    """
    # Generate molecule from SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate ring information
    rings = mol.GetRingInfo()
    
    # Find all rings of size 6 (benzene) and 7 (diazepine)
    six_membered_rings = []
    seven_membered_rings = []
    
    for ring in rings.AtomRings():
        if len(ring) == 6:
            six_membered_rings.append(ring)
        elif len(ring) == 7:
            seven_membered_rings.append(ring)
            
    if not six_membered_rings:
        return False, "No 6-membered rings found"
    if not seven_membered_rings:
        return False, "No 7-membered rings found"
    
    # Check for benzene rings (6-membered aromatic rings with all carbons)
    benzene_rings = []
    for ring in six_membered_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if all(atom.GetIsAromatic() for atom in atoms) and \
           all(atom.GetSymbol() == 'C' for atom in atoms):
            benzene_rings.append(ring)
            
    if not benzene_rings:
        return False, "No benzene rings found"
        
    # Check for diazepine rings (7-membered rings with exactly 2 nitrogens)
    diazepine_rings = []
    for ring in seven_membered_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        n_count = sum(1 for atom in atoms if atom.GetSymbol() == 'N')
        if n_count == 2:
            diazepine_rings.append(ring)
            
    if not diazepine_rings:
        return False, "No diazepine rings found"
    
    # Check if benzene and diazepine rings are fused
    for benz_ring in benzene_rings:
        for diaz_ring in diazepine_rings:
            # Two rings are fused if they share exactly 2 adjacent atoms
            shared_atoms = set(benz_ring).intersection(set(diaz_ring))
            if len(shared_atoms) == 2:
                # Check if shared atoms are adjacent
                shared_list = list(shared_atoms)
                bond = mol.GetBondBetweenAtoms(shared_list[0], shared_list[1])
                if bond is not None:
                    return True, "Contains benzene ring fused to diazepine ring"
                
    return False, "Benzene and diazepine rings are not fused"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22720',
                          'name': 'benzodiazepine',
                          'definition': 'A group of heterocyclic compounds '
                                        'with a core structure containing a '
                                        'benzene ring fused to a diazepine '
                                        'ring.',
                          'parents': ['CHEBI:38101', 'CHEBI:38166']},
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
    'num_true_positives': 17,
    'num_false_positives': 100,
    'num_true_negatives': 95670,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.1452991452991453,
    'recall': 1.0,
    'f1': 0.2537313432835821,
    'accuracy': 0.9989560169960433}