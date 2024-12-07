"""
Classifies: CHEBI:24164 galactosyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def is_galactosyl_group(smiles: str):
    """
    Determines if a molecule contains a galactosyl group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains a galactosyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of sugar ring
    ring_info = mol.GetRingInfo()
    if not any(len(ring) == 6 for ring in ring_info.AtomRings()):
        return False, "No 6-membered rings found"

    # Find pyranose rings (6-membered rings with 5 carbons and 1 oxygen)
    pyranose_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            symbols = [atom.GetSymbol() for atom in atoms]
            if symbols.count('C') == 5 and symbols.count('O') == 1:
                pyranose_rings.append(ring)

    if not pyranose_rings:
        return False, "No pyranose rings found"

    # Check for galactose configuration
    for ring in pyranose_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Find oxygen atom in ring
        ring_O_idx = next(i for i, atom in enumerate(atoms) if atom.GetSymbol() == 'O')
        
        # Check for characteristic galactose hydroxyl group orientations
        # Note: This is a simplified check and may not catch all cases
        hydroxyls = 0
        for atom in atoms:
            if atom.GetSymbol() == 'C':
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'O' and neighbor.GetIdx() not in ring:
                        hydroxyls += 1

        if hydroxyls >= 3:  # Galactose typically has 4 hydroxyl groups, but some may be modified
            # Check for hemiacetal/acetal linkage
            ring_O = atoms[ring_O_idx]
            for neighbor in ring_O.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    for n2 in neighbor.GetNeighbors():
                        if n2.GetSymbol() == 'O' and n2.GetIdx() not in ring:
                            return True, "Contains galactosyl group with characteristic pyranose ring and glycosidic linkage"

    return False, "No galactosyl group configuration found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24164',
                          'name': 'galactosyl group',
                          'definition': 'A glycosyl group obtained by removing '
                                        'the hydroxy group from the hemiacetal '
                                        'function of a galactose and, by '
                                        'extension, of a lower oligosaccharide '
                                        'having galactose at the reducing end.',
                          'parents': ['CHEBI:24403']},
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
    'num_true_negatives': 705,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 0.6666666666666666,
    'f1': 0.03809523809523809,
    'accuracy': 0.875}