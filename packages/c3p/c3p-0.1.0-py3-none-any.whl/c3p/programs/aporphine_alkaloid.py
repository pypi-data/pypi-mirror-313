"""
Classifies: CHEBI:134209 aporphine alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aporphine_alkaloid(smiles: str):
    """
    Determines if a molecule is an aporphine alkaloid based on the 4H-dibenzo[de,g]quinoline core.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aporphine alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of nitrogen
    if sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'N') == 0:
        return False, "No nitrogen atoms found - required for alkaloid"

    # Generate ring info
    rings = mol.GetRingInfo()
    
    # Need at least 4 rings for the tetracyclic core
    if rings.NumRings() < 4:
        return False, "Less than 4 rings found - aporphine alkaloids require tetracyclic core"

    # Check for presence of 4H-dibenzo[de,g]quinoline core
    # This requires:
    # - A 6,6,6,6 tetracyclic system
    # - One nitrogen in a 6-membered ring
    # - Two benzene rings fused together
    # - A bridging carbon connecting the rings
    
    ring_sizes = [len(ring) for ring in rings.AtomRings()]
    if ring_sizes.count(6) < 4:
        return False, "Does not contain required tetracyclic 6,6,6,6 ring system"

    # Find nitrogen-containing 6-membered rings
    n_ring = False
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'N' for atom in atoms):
                n_ring = True
                break
                
    if not n_ring:
        return False, "No nitrogen-containing 6-membered ring found"

    # Check for aromatic rings
    aromatic_rings = 0
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings += 1

    if aromatic_rings < 2:
        return False, "Less than 2 aromatic rings found"

    # Check for bridging carbon
    bridge_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            if len(list(atom.GetNeighbors())) == 3:
                bridge_found = True
                break
    
    if not bridge_found:
        return False, "No bridging carbon found"

    # If we get here, the molecule has the core aporphine alkaloid structure
    substituents = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'N', 'H']:
            substituents.append(atom.GetSymbol())
            
    if len(substituents) > 0:
        return True, f"Aporphine alkaloid with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted aporphine alkaloid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134209',
                          'name': 'aporphine alkaloid',
                          'definition': 'Any benzylisoquinoline alkaloid that '
                                        'has a structure based on '
                                        '4H-dibenzo[de,g]quinoline or its '
                                        '3-methyl derivative.',
                          'parents': ['CHEBI:22750']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 3015,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.967948717948718}