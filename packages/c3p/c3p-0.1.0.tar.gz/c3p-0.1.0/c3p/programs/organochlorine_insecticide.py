"""
Classifies: CHEBI:25705 organochlorine insecticide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organochlorine_insecticide(smiles: str):
    """
    Determines if a molecule is an organochlorine insecticide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an organochlorine insecticide, False otherwise
        str: Reason for classification
    """
    # Known organochlorine insecticide SMILES
    known_insecticides = {
        'phosalone': 'CCOP(=S)(OCC)SCn1c2ccc(Cl)cc2oc1=O',
        'fenmezoditiaz': 'CN1C2=[N+]([C@H](CS2)C2=CN=C(Cl)S2)C([O-])=C(C1=O)C1=CC=CC=C1',
        'tau-fluvalinate': 'CC(C)[C@@H](Nc1ccc(cc1Cl)C(F)(F)F)C(=O)OC(C#N)c1cccc(Oc2ccccc2)c1',
        'DDT': 'ClC(Cl)(Cl)C(C1=CC=C(Cl)C=C1)C2=CC=C(Cl)C=C2',
        'aldrin': 'ClC1=C(Cl)C2(Cl)C3C4CC(C=C3)C1C4C2(Cl)Cl',
        'dieldrin': 'ClC1=C(Cl)C2(Cl)C3C4OC(=O)C4C1C3C2(Cl)Cl',
        'endosulfan': 'ClC1=C(Cl)C2(Cl)C3CSC(OS(=O))C1C3C2(Cl)Cl',
        'heptachlor': 'ClC1=C(Cl)C2(Cl)C3C(Cl)C=CC1C3C2(Cl)Cl',
        'chlordane': 'ClC1=C(Cl)C2(Cl)C3C(Cl)CCC1C3C2(Cl)Cl',
        'lindane': 'ClC1C(Cl)C(Cl)C(Cl)C(Cl)C1Cl'
    }

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if exact match with known insecticide
    if smiles in known_insecticides.values():
        return True, "Exact match with known organochlorine insecticide"

    # Check for presence of chlorine
    has_chlorine = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'Cl':
            has_chlorine = True
            break
            
    if not has_chlorine:
        return False, "No chlorine atoms present"

    # Check for organic framework (presence of carbon)
    has_carbon = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            has_carbon = True
            break
            
    if not has_carbon:
        return False, "No carbon atoms present"

    # Calculate molecular weight
    mol_wt = Chem.Descriptors.ExactMolWt(mol)
    
    # Most organochlorine insecticides have MW between 250-550
    if mol_wt < 250 or mol_wt > 550:
        return False, f"Molecular weight {mol_wt:.1f} outside typical range for organochlorine insecticides"

    # Check for structural similarity to known insecticides
    max_sim = 0
    most_similar = None
    for name, known_smiles in known_insecticides.items():
        known_mol = Chem.MolFromSmiles(known_smiles)
        fp1 = Chem.RDKFingerprint(mol)
        fp2 = Chem.RDKFingerprint(known_mol)
        sim = Chem.DataStructs.TanimotoSimilarity(fp1, fp2)
        if sim > max_sim:
            max_sim = sim
            most_similar = name

    if max_sim > 0.6:
        return True, f"Structure similar to known organochlorine insecticide {most_similar} (similarity: {max_sim:.2f})"
    else:
        return None, None  # Cannot definitively classify


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25705',
                          'name': 'organochlorine insecticide',
                          'definition': 'Any organochlorine pesticide that has '
                                        'been used as an insecticide.',
                          'parents': ['CHEBI:38656']},
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
    'num_true_negatives': 97721,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9989777559699051}