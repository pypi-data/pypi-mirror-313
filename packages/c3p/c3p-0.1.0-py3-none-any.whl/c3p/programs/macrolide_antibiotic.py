"""
Classifies: CHEBI:25105 macrolide antibiotic
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_macrolide_antibiotic(smiles: str):
    """
    Determines if a molecule is a macrolide antibiotic based on structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a macrolide antibiotic, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Get ring information
    ri = mol.GetRingInfo()
    if not ri.NumRings():
        return False, "No rings found"

    # Find macrocyclic lactone rings (12+ membered rings containing -O-C(=O)-)
    macrolactone_rings = []
    
    for ring in ri.AtomRings():
        if len(ring) >= 12:  # Check ring size
            # Get atoms in ring
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            
            # Look for lactone pattern
            has_lactone = False
            for i, atom in enumerate(ring_atoms):
                if atom.GetSymbol() == 'O':  # Find oxygen
                    # Check next atom is C(=O)
                    next_idx = (i + 1) % len(ring)
                    next_atom = ring_atoms[next_idx]
                    if next_atom.GetSymbol() == 'C':
                        # Check for carbonyl
                        for bond in next_atom.GetBonds():
                            other_atom = bond.GetOtherAtom(next_atom)
                            if other_atom.GetSymbol() == 'O' and bond.GetBondType() == Chem.BondType.DOUBLE:
                                has_lactone = True
                                break
                if has_lactone:
                    break
                    
            if has_lactone:
                macrolactone_rings.append(ring)

    if not macrolactone_rings:
        return False, "No macrocyclic lactone rings found"

    # Check for characteristic substitution patterns of macrolide antibiotics
    # Look for sugar moieties (especially desosamine)
    substructure_matches = []
    
    # Desosamine pattern
    desosamine_smarts = 'O[C@H]1[CH2][CH]([CH]([CH](O1)C)O)N(C)C'
    desosamine = Chem.MolFromSmarts(desosamine_smarts)
    if desosamine is not None and mol.HasSubstructMatch(desosamine):
        substructure_matches.append("desosamine")
        
    # Check for hydroxyl groups
    hydroxyl = Chem.MolFromSmarts('[OH]')
    if hydroxyl is not None:
        hydroxyl_count = len(mol.GetSubstructMatches(hydroxyl))
        if hydroxyl_count >= 2:
            substructure_matches.append(f"{hydroxyl_count} hydroxyl groups")
        
    if substructure_matches:
        return True, f"Macrolide antibiotic with {', '.join(substructure_matches)}"
    else:
        return True, "Basic macrolide structure found but lacking characteristic substitution patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25105',
                          'name': 'macrolide antibiotic',
                          'definition': 'A macrocyclic lactone with a ring of '
                                        'twelve or more members which exhibits '
                                        'antibiotic activity.',
                          'parents': ['CHEBI:25106']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
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
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 5844,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 0.375,
    'f1': 0.05405405405405406,
    'accuracy': 0.9823588709677419}