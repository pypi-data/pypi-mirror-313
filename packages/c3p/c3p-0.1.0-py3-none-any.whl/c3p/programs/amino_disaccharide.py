"""
Classifies: CHEBI:22480 amino disaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_amino_disaccharide(smiles: str):
    """
    Determines if a molecule is an amino disaccharide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an amino disaccharide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Count number of saccharide rings
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    
    # Get number of 5 or 6 membered rings containing oxygen
    sugar_rings = []
    for ring in rings:
        if len(ring) in [5,6]:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'O' for atom in atoms):
                sugar_rings.append(ring)
                
    if len(sugar_rings) < 2:
        return False, "Does not contain at least 2 sugar rings"
        
    # Check for amino groups
    num_nitrogens = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            num_nitrogens += 1
            
    if num_nitrogens == 0:
        return False, "No amino groups found"
        
    # Count glycosidic bonds (C-O-C between rings)
    glycosidic_bonds = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.rdchem.BondType.SINGLE:
            begin_atom = bond.GetBeginAtom()
            end_atom = bond.GetEndAtom() 
            if begin_atom.GetSymbol() == 'O' and end_atom.GetSymbol() == 'C':
                # Check if carbon atoms are in different rings
                for ring1 in sugar_rings:
                    for ring2 in sugar_rings:
                        if ring1 != ring2:
                            if end_atom.GetIdx() in ring1 and any(n.GetIdx() in ring2 for n in begin_atom.GetNeighbors()):
                                glycosidic_bonds += 1
                                
    if glycosidic_bonds == 0:
        return False, "No glycosidic bonds found between sugar rings"
        
    return True, f"Contains {len(sugar_rings)} sugar rings, {num_nitrogens} amino groups, and {glycosidic_bonds} glycosidic bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22480',
                          'name': 'amino disaccharide',
                          'definition': 'A disaccharide derivative that is a '
                                        'disaccharide having one or more '
                                        'substituted or unsubstituted amino '
                                        'groups in place of hydroxy groups at '
                                        'unspecified positions.',
                          'parents': ['CHEBI:22483', 'CHEBI:63353']},
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
    'num_true_positives': 24,
    'num_false_positives': 100,
    'num_true_negatives': 1139,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.1935483870967742,
    'recall': 0.8,
    'f1': 0.3116883116883117,
    'accuracy': 0.9164696611505122}