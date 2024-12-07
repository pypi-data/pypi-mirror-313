"""
Classifies: CHEBI:22562 anilines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_anilines(smiles: str):
    """
    Determines if a molecule is an aniline (aromatic amine with at least one amino substituent on benzene).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aniline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find all aromatic rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms) and all(atom.GetSymbol() == 'C' for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic benzene rings found"

    # Check for amino substituents on benzene rings
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    # Check if neighbor is NH2 or substituted NH
                    if neighbor.GetSymbol() == 'N':
                        # Count non-H neighbors of N
                        non_h_neighbors = len([n for n in neighbor.GetNeighbors() if n.GetSymbol() != 'H'])
                        total_neighbors = neighbor.GetDegree()
                        h_count = total_neighbors - non_h_neighbors
                        
                        if h_count >= 1 or neighbor.GetNumExplicitHs() >= 1:
                            substituents = []
                            for n in neighbor.GetNeighbors():
                                if n.GetIdx() not in ring_atoms:
                                    substituents.append(n.GetSymbol())
                            
                            if substituents:
                                return True, f"Aniline with substituted amino group. Substituents: {', '.join(set(substituents))}"
                            else:
                                return True, "Primary aniline (unsubstituted amino group)"

    return False, "No amino substituents found on benzene ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22562',
                          'name': 'anilines',
                          'definition': 'Any  aromatic amine that is benzene '
                                        'carrying at least one amino '
                                        'substituent and its substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:22712', 'CHEBI:33860']},
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
    'num_false_positives': 100,
    'num_true_negatives': 2311,
    'num_false_negatives': 39,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.943265306122449}