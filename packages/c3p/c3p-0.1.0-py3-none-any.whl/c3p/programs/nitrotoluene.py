"""
Classifies: CHEBI:25566 nitrotoluene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nitrotoluene(smiles: str):
    """
    Determines if a molecule is a nitrotoluene (toluene with one or more nitro groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nitrotoluene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for benzene ring
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check for methyl group attached to benzene ring
    has_methyl = False
    ring_atoms = set(aromatic_rings[0])
    methyl_count = 0
    
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                if neighbor.GetSymbol() == 'C' and len([n for n in neighbor.GetNeighbors()]) == 4:
                    methyl_count += 1
                    has_methyl = True

    if not has_methyl:
        return False, "No methyl group found"
    
    if methyl_count > 1:
        return False, "More than one methyl group found - not a toluene derivative"

    # Check for nitro groups
    nitro_pattern = Chem.MolFromSmarts('[$(N(=O)O-),$(N(=O)=O)]')
    nitro_matches = mol.GetSubstructMatches(nitro_pattern)
    
    if not nitro_matches:
        return False, "No nitro groups found"

    # Check if nitro groups are attached to the benzene ring
    nitro_on_ring = False
    nitro_count = 0
    for match in nitro_matches:
        n_atom = mol.GetAtomWithIdx(match[0])
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetIdx() in ring_atoms:
                nitro_on_ring = True
                nitro_count += 1

    if not nitro_on_ring:
        return False, "Nitro groups not attached to benzene ring"

    return True, f"Nitrotoluene with {nitro_count} nitro group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25566',
                          'name': 'nitrotoluene',
                          'definition': 'Any member of the class of  toluenes '
                                        'bearing one or more nitro '
                                        'substituents on the benzene ring.',
                          'parents': ['CHEBI:27024', 'CHEBI:35716']},
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
    'success': False,
    'best': True,
    'error': 'Python argument types in\n'
             '    Mol.GetSubstructMatches(Mol, NoneType)\n'
             'did not match C++ signature:\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
             'query, RDKit::SubstructMatchParameters params)\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
             'RDKit::SubstructMatchParameters params)\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
             'query, bool uniquify=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
             '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
             'bool uniquify=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False, unsigned int maxMatches=1000)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}