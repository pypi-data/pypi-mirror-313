"""
Classifies: CHEBI:26513 quinolines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors


def is_quinolines(smiles: str):
    """
    Determines if a molecule is a quinoline (contains a benzene ring ortho fused to carbons 2 and 3 of a pyridine ring).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a quinoline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all rings
    rings = mol.GetRingInfo()
    
    # Get all aromatic rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if len(aromatic_rings) < 2:
        return False, "Does not contain at least 2 aromatic rings"

    # Find pyridine ring (6-membered aromatic ring with 1 nitrogen)
    pyridine_rings = []
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        n_count = sum(1 for atom in atoms if atom.GetSymbol() == 'N')
        if n_count == 1:
            pyridine_rings.append(ring)

    if not pyridine_rings:
        return False, "No pyridine ring found"

    # Find benzene ring (6-membered aromatic ring with all carbons)
    benzene_rings = []
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if all(atom.GetSymbol() == 'C' for atom in atoms):
            benzene_rings.append(ring)

    if not benzene_rings:
        return False, "No benzene ring found"

    # Check if benzene and pyridine rings share exactly 2 atoms
    for pyridine_ring in pyridine_rings:
        for benzene_ring in benzene_rings:
            shared_atoms = set(pyridine_ring).intersection(set(benzene_ring))
            if len(shared_atoms) == 2:
                # Check if shared atoms are carbons 2 and 3 of pyridine ring
                pyridine_atoms = [mol.GetAtomWithIdx(i) for i in pyridine_ring]
                nitrogen_idx = next(i for i, atom in enumerate(pyridine_atoms) if atom.GetSymbol() == 'N')
                shared_positions = [(i-nitrogen_idx)%6 for i, atom in enumerate(pyridine_atoms) 
                                 if atom.GetIdx() in shared_atoms]
                if set(shared_positions) == {2,3}:
                    return True, "Contains benzene ring ortho fused to carbons 2 and 3 of pyridine ring"

    return False, "Benzene ring not properly fused to pyridine ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26513',
                          'name': 'quinolines',
                          'definition': 'A class of aromatic heterocyclic '
                                        'compounds each of which contains a '
                                        'benzene ring ortho fused to carbons 2 '
                                        'and 3 of a pyridine ring.',
                          'parents': ['CHEBI:33659', 'CHEBI:38101']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.0}