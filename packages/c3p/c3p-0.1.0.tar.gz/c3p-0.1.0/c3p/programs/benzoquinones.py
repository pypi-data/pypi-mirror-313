"""
Classifies: CHEBI:22729 benzoquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_benzoquinones(smiles: str):
    """
    Determines if a molecule is a benzoquinone derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a benzoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate the ring information
    rings = mol.GetRingInfo()
    
    # Check for at least one 6-membered ring
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered rings found"

    # Find all 6-membered rings
    six_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            six_rings.append(ring)
            
    # For each 6-membered ring, check if it matches benzoquinone pattern
    for ring in six_rings:
        # Get atoms in ring
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Count carbons and oxygens
        carbon_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'C')
        oxygen_count = sum(1 for atom in ring_atoms if atom.GetSymbol() == 'O')
        
        # Count double bonds to oxygen (carbonyl groups)
        carbonyl_count = 0
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'C':
                for bond in atom.GetBonds():
                    other_atom = bond.GetOtherAtom(atom)
                    if other_atom.GetSymbol() == 'O' and bond.GetBondType() == Chem.BondType.DOUBLE:
                        carbonyl_count += 1

        # Basic benzoquinone pattern requires:
        # - 6-membered ring
        # - At least 4 carbons
        # - 2 carbonyl groups
        if carbon_count >= 4 and carbonyl_count == 2:
            # Check for para pattern (1,4-benzoquinone)
            para_pattern = Chem.MolFromSmarts('[#6]-1-[#6]=[#6]-[#6](=[O])-[#6]=[#6]-[#6](=[O])-1')
            # Check for ortho pattern (1,2-benzoquinone)
            ortho_pattern = Chem.MolFromSmarts('[#6]-1-[#6](=[O])-[#6](=[O])-[#6]=[#6]-[#6]=[#6]-1')
            
            if mol.HasSubstructMatch(para_pattern):
                return True, "Para-benzoquinone (1,4-benzoquinone) pattern found"
            elif mol.HasSubstructMatch(ortho_pattern):
                return True, "Ortho-benzoquinone (1,2-benzoquinone) pattern found"
                
    return False, "No benzoquinone pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22729',
                          'name': 'benzoquinones',
                          'definition': 'Any quinone resulting from the formal '
                                        'oxidation of catechol, hydroquinone, '
                                        'or their C-substituted derivatives.',
                          'parents': ['CHEBI:36141']},
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
    'num_true_negatives': 183762,
    'num_false_negatives': 17,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999074975922168}