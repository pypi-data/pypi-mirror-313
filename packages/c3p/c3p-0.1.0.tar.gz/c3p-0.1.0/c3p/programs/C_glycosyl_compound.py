"""
Classifies: CHEBI:20857 C-glycosyl compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_C_glycosyl_compound(smiles: str):
    """
    Determines if a molecule is a C-glycosyl compound based on the presence of a C-C bond
    between a glycosidic moiety and another carbon atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a C-glycosyl compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for pyranose rings (6-membered rings with oxygen)
    rings = mol.GetRingInfo()
    pyranose_rings = []
    
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring contains exactly one oxygen and rest carbons
            if sum(1 for atom in atoms if atom.GetSymbol() == 'O') == 1:
                # Check for hydroxyl groups typical in sugars
                hydroxyls = 0
                for atom in atoms:
                    if atom.GetSymbol() == 'C':
                        for neighbor in atom.GetNeighbors():
                            if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
                                hydroxyls += 1
                if hydroxyls >= 2:  # Typical sugar has multiple OH groups
                    pyranose_rings.append(ring)

    if not pyranose_rings:
        return False, "No pyranose ring found"

    # For each pyranose ring, look for C-C bond to non-ring carbon
    for ring in pyranose_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'C':
                for neighbor in atom.GetNeighbors():
                    # Check if neighbor is carbon and not part of the same ring
                    if (neighbor.GetSymbol() == 'C' and 
                        neighbor.GetIdx() not in ring_atoms and 
                        not neighbor.GetIsAromatic()):
                        # Verify this carbon is not part of a glycosidic O-C-O linkage
                        is_glycosidic = False
                        oxygen_count = 0
                        for n2 in neighbor.GetNeighbors():
                            if n2.GetSymbol() == 'O':
                                oxygen_count += 1
                        if oxygen_count < 2:  # Not a typical glycosidic linkage
                            return True, "C-C bond found between pyranose ring and non-glycosidic carbon"

    return False, "No C-glycosidic linkage found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20857',
                          'name': 'C-glycosyl compound',
                          'definition': 'A glycosyl compound arising formally '
                                        'from the elimination of water from a '
                                        'glycosidic hydroxy group and an H '
                                        'atom bound to a carbon atom, thus '
                                        'creating a C-C bond.',
                          'parents': ['CHEBI:63161', 'CHEBI:63299']},
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
    'num_true_positives': 23,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.18699186991869918,
    'f1': 0.3150684931506849,
    'accuracy': 0.18699186991869918}