"""
Classifies: CHEBI:24613 homodetic cyclic peptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors


def is_homodetic_cyclic_peptide(smiles: str):
    """
    Determines if a molecule is a homodetic cyclic peptide.
    A homodetic cyclic peptide has a ring consisting solely of amino acid residues 
    connected by peptide bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a homodetic cyclic peptide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate the ring information
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"

    # Look for peptide bonds (-C(=O)-N-) in rings
    peptide_bonds = []
    for bond in mol.GetBonds():
        # Get the atoms connected by this bond
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()
        
        # Check if this is a C-N single bond
        if bond.GetBondType() == Chem.BondType.SINGLE and \
           atom1.GetSymbol() in ['C', 'N'] and atom2.GetSymbol() in ['C', 'N']:
            
            # For C atom, check if it has a double-bonded O
            c_atom = atom1 if atom1.GetSymbol() == 'C' else atom2
            n_atom = atom2 if atom1.GetSymbol() == 'C' else atom1
            
            has_carbonyl = False
            for neighbor in c_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and \
                   mol.GetBondBetweenAtoms(c_atom.GetIdx(), neighbor.GetIdx()).GetBondType() == Chem.BondType.DOUBLE:
                    has_carbonyl = True
                    break
                    
            if has_carbonyl:
                peptide_bonds.append((c_atom.GetIdx(), n_atom.GetIdx()))

    if not peptide_bonds:
        return False, "No peptide bonds found"

    # Check if peptide bonds form a cycle
    bond_atoms = set()
    for c, n in peptide_bonds:
        bond_atoms.add(c)
        bond_atoms.add(n)

    # Get all ring atoms
    ring_atoms = set()
    for ring in rings.AtomRings():
        ring_atoms.update(ring)

    # Check if peptide bonds are part of a ring
    peptide_ring = False
    for ring in rings.AtomRings():
        ring_set = set(ring)
        if any(c in ring_set and n in ring_set for c, n in peptide_bonds):
            peptide_ring = True
            break

    if not peptide_ring:
        return False, "No cyclic peptide structure found"

    # Additional checks for amino acid residues
    for ring in rings.AtomRings():
        ring_set = set(ring)
        peptide_bonds_in_ring = [(c,n) for c,n in peptide_bonds if c in ring_set and n in ring_set]
        if len(peptide_bonds_in_ring) >= 2:  # Need at least 2 peptide bonds for cyclic peptide
            return True, "Homodetic cyclic peptide structure found"

    return False, "Structure does not match homodetic cyclic peptide pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24613',
                          'name': 'homodetic cyclic peptide',
                          'definition': 'A homodetic cyclic peptide is a '
                                        'cyclic peptide in which the ring '
                                        'consists solely of amino-acid '
                                        'residues in peptide linkages.',
                          'parents': ['CHEBI:23449']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 100,
    'num_true_negatives': 779,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.13043478260869565,
    'recall': 0.9375,
    'f1': 0.22900763358778628,
    'accuracy': 0.8871508379888268}