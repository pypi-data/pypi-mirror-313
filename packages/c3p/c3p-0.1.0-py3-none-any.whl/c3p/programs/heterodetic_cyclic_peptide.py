"""
Classifies: CHEBI:24533 heterodetic cyclic peptide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_heterodetic_cyclic_peptide(smiles: str):
    """
    Determines if a molecule is a heterodetic cyclic peptide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a heterodetic cyclic peptide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule has rings
    if not mol.GetRingInfo().NumRings():
        return False, "No rings found"

    # Look for peptide bonds (amide bonds)
    amide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])')
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if not amide_matches:
        return False, "No peptide bonds found"

    # Look for amino acid residues
    aa_pattern = Chem.MolFromSmarts('[NX3][CX4][CX3](=[OX1])')
    aa_matches = mol.GetSubstructMatches(aa_pattern)
    if not aa_matches:
        return False, "No amino acid residues found"

    # Look for non-peptide bonds that could form cycles
    # Disulfide bonds
    ss_pattern = Chem.MolFromSmarts('[SX2]-[SX2]') 
    ss_matches = mol.GetSubstructMatches(ss_pattern)
    
    # Ester bonds
    ester_pattern = Chem.MolFromSmarts('[CX3](=[OX1])[OX2]')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    # Thioester bonds
    thioester_pattern = Chem.MolFromSmarts('[CX3](=[OX1])[SX2]')
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)

    # Check if molecule has at least one cycle and contains non-peptide bonds
    if mol.GetRingInfo().NumRings() > 0 and (ss_matches or ester_matches or thioester_matches):
        non_peptide_bonds = []
        if ss_matches:
            non_peptide_bonds.append("disulfide")
        if ester_matches:
            non_peptide_bonds.append("ester") 
        if thioester_matches:
            non_peptide_bonds.append("thioester")
            
        return True, f"Heterodetic cyclic peptide containing {', '.join(non_peptide_bonds)} bonds"

    # If only peptide bonds are found in cycles, it's homodetic
    return False, "Only peptide bonds found in cycles (homodetic) or no cyclic structure detected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24533',
                          'name': 'heterodetic cyclic peptide',
                          'definition': 'A heterodetic cyclic peptide is a '
                                        'peptide consisting only of amino-acid '
                                        'residues, but in which the linkages '
                                        'forming the ring are not solely '
                                        'peptide bonds; one or more is an '
                                        'isopeptide, disulfide, ester, or '
                                        'other bond.',
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1483,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 0.8333333333333334,
    'f1': 0.09009009009009009,
    'accuracy': 0.9364380113278792}