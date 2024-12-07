"""
Classifies: CHEBI:22315 alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_alkaloid(smiles: str):
    """
    Determines if a molecule is an alkaloid based on the definition:
    'Any of the naturally occurring, basic nitrogen compounds (mostly heterocyclic) 
    occurring mostly in the plant kingdom, but also found in bacteria, fungi, and animals.'
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of nitrogen
    if not any(atom.GetAtomicNum() == 7 for atom in mol.GetAtoms()):
        return False, "No nitrogen atoms present"
    
    # Count number of nitrogen atoms
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    
    # Check for heterocycles containing nitrogen
    rings = mol.GetRingInfo()
    n_in_ring = False
    for ring in rings.AtomRings():
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if any(atom.GetAtomicNum() == 7 for atom in ring_atoms):
            n_in_ring = True
            break
    
    # Exclude peptides/proteins (high nitrogen content and peptide bonds)
    peptide_like = False
    for bond in mol.GetBonds():
        if (bond.GetBondType() == Chem.BondType.SINGLE and
            bond.GetBeginAtom().GetAtomicNum() == 6 and
            bond.GetEndAtom().GetAtomicNum() == 7 and
            any(n.GetAtomicNum() == 8 for n in bond.GetBeginAtom().GetNeighbors()) and
            any(n.GetAtomicNum() == 8 for n in bond.GetEndAtom().GetNeighbors())):
            peptide_like = True
            break

    # Exclude nucleotides/nucleic acids (presence of phosphate groups)
    has_phosphate = any(atom.GetAtomicNum() == 15 for atom in mol.GetAtoms())
    
    # Check for basic nitrogen (sp3 nitrogen with lone pair)
    basic_n = False
    for atom in mol.GetAtoms():
        if (atom.GetAtomicNum() == 7 and 
            atom.GetHybridization() == Chem.HybridizationType.SP3 and 
            not atom.GetFormalCharge()):
            basic_n = True
            break

    if peptide_like:
        return False, "Structure appears to be peptide-like"
    
    if has_phosphate:
        return False, "Contains phosphate group, likely nucleotide/nucleic acid"

    if not n_in_ring and basic_n:
        return False, "Contains only exocyclic amine, likely biogenic amine rather than alkaloid"
        
    if n_in_ring and basic_n:
        return True, "Contains basic nitrogen in heterocyclic ring system"
        
    if n_in_ring:
        return True, "Contains nitrogen heterocycle"
        
    return False, "Does not meet alkaloid criteria"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22315',
                          'name': 'alkaloid',
                          'definition': 'Any of the naturally occurring, basic '
                                        'nitrogen compounds (mostly '
                                        'heterocyclic) occurring mostly in the '
                                        'plant kingdom, but also found in '
                                        'bacteria, fungi, and animals. By '
                                        'extension, certain neutral compounds '
                                        'biogenetically related to basic '
                                        'alkaloids are also classed as '
                                        'alkaloids. Amino acids, peptides, '
                                        'proteins, nucleotides, nucleic acids, '
                                        'amino sugars and antibiotics are not '
                                        'normally regarded as alkaloids. '
                                        'Compounds in which the nitrogen is  '
                                        'exocyclic (dopamine, mescaline, '
                                        'serotonin, etc.) are usually classed '
                                        'as amines rather than alkaloids.',
                          'parents': ['CHEBI:35352']},
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
    'num_true_positives': 267,
    'num_false_positives': 100,
    'num_true_negatives': 155,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.7275204359673024,
    'recall': 0.978021978021978,
    'f1': 0.8343749999999999,
    'accuracy': 0.7992424242424242}