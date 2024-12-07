"""
Classifies: CHEBI:26469 quaternary nitrogen compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_quaternary_nitrogen_compound(smiles: str):
    """
    Determines if a molecule contains a quaternary nitrogen (N+) that is electronically neutral.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains quaternary nitrogen, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # Look for quaternary nitrogen atoms (N+)
        quaternary_nitrogens = []
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 1:
                # Check if nitrogen has 4 bonds
                if len(atom.GetBonds()) == 4:
                    quaternary_nitrogens.append(atom)
                    
        if not quaternary_nitrogens:
            return False, "No quaternary nitrogen atoms found"
            
        # Check if molecule is electronically neutral overall
        total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
        if total_charge != 0:
            return False, "Molecule is not electronically neutral"
            
        # Get substituents on quaternary nitrogens
        substituents = []
        for n in quaternary_nitrogens:
            for neighbor in n.GetNeighbors():
                substituents.append(neighbor.GetSymbol())
                
        return True, f"Contains quaternary nitrogen with substituents: {', '.join(set(substituents))}"
        
    except Exception as e:
        return None, f"Error processing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26469',
                          'name': 'quaternary nitrogen compound',
                          'definition': 'A nitrogen molecular entity that is '
                                        'electronically neutral but which '
                                        'contains a quaternary nitrogen.',
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
    'num_true_positives': 200,
    'num_false_positives': 100,
    'num_true_negatives': 26059,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.6666666666666666,
    'recall': 0.9615384615384616,
    'f1': 0.7874015748031495,
    'accuracy': 0.9959039708726818}