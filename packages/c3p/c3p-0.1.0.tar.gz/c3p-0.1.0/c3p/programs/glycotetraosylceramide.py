"""
Classifies: CHEBI:23075 glycotetraosylceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_glycotetraosylceramide(smiles: str):
    """
    Determines if a molecule is a glycotetraosylceramide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycotetraosylceramide, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Standardize the molecule
    uncharger = rdMolStandardize.Uncharger()
    mol = uncharger.uncharge(mol)
    
    # Count rings that could be sugars (5-6 membered rings with multiple OH groups)
    rings = mol.GetRingInfo()
    sugar_ring_count = 0
    
    for ring in rings.AtomRings():
        if len(ring) in [5,6]:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Count oxygen atoms in ring
            ring_o_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'O')
            # Count OH groups attached to ring
            oh_count = 0
            for atom_idx in ring:
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                        oh_count += 1
            if ring_o_count >= 1 and oh_count >= 2:
                sugar_ring_count += 1
                
    if sugar_ring_count != 4:
        return False, f"Found {sugar_ring_count} sugar rings, expected 4"

    # Check for ceramide moiety
    # Look for N-C(=O) pattern
    amide_pattern = Chem.MolFromSmarts('[N;H1]-C(=O)')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide group found (required for ceramide)"
        
    # Look for long alkyl chains
    alkyl_pattern = Chem.MolFromSmarts('CCCCCCCCC')  # At least 9 carbons
    if len(mol.GetSubstructMatches(alkyl_pattern)) < 2:
        return False, "Missing required long alkyl chains"

    # Check for glycosidic linkages between sugars
    glycosidic_pattern = Chem.MolFromSmarts('[C]-O-[C]')
    glycosidic_bonds = len(mol.GetSubstructMatches(glycosidic_pattern))
    
    if glycosidic_bonds < 4:
        return False, f"Found {glycosidic_bonds} glycosidic bonds, expected at least 4"
        
    return True, "Molecule contains 4 sugar rings, ceramide moiety, and appropriate glycosidic linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23075',
                          'name': 'glycotetraosylceramide',
                          'definition': 'An oligoglycosylceramide consisting '
                                        'of a glycotetraosyl moiety attached '
                                        'to the ceramide oxygen with an '
                                        'unspecified N-acyl substituent '
                                        'attached to the ceramide nitrogen.',
                          'parents': ['CHEBI:36520']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 53634,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 0.6,
    'f1': 0.05555555555555556,
    'accuracy': 0.9981019371406241}