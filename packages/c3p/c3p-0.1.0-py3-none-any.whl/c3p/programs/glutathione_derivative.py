"""
Classifies: CHEBI:24337 glutathione derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS

def is_glutathione_derivative(smiles: str):
    """
    Determines if a molecule is a glutathione derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glutathione derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # SMILES pattern for glutathione core structure (Glu-Cys-Gly)
    # This pattern matches the core tripeptide backbone while allowing for modifications
    gsh_core = "NC(CCC(=O)NC(CS)C(=O)NCC(=O)O)C(=O)O"
    gsh_mol = Chem.MolFromSmiles(gsh_core)
    
    # Find maximum common substructure between input molecule and GSH core
    mcs = rdFMCS.FindMCS([mol, gsh_mol], 
                        atomCompare=rdFMCS.AtomCompare.CompareElements,
                        bondCompare=rdFMCS.BondCompare.CompareOrder,
                        matchValences=True,
                        ringMatchesRingOnly=True,
                        completeRingsOnly=False,
                        timeout=2)
                        
    if mcs.numAtoms < 10:  # Threshold for minimum matching atoms
        return False, "Structure does not contain glutathione core"
        
    # Check for key functional groups
    patt1 = Chem.MolFromSmarts("[NH2][CH]CC[CH2]C(=O)")  # Glu portion
    patt2 = Chem.MolFromSmarts("[CH2]CS")  # Cys portion with thiol/thioether
    patt3 = Chem.MolFromSmarts("NCC(=O)[OH]")  # Gly portion
    
    matches = []
    matches.append(len(mol.GetSubstructMatches(patt1)) > 0)
    matches.append(len(mol.GetSubstructMatches(patt2)) > 0) 
    matches.append(len(mol.GetSubstructMatches(patt3)) > 0)
    
    if not all(matches):
        return False, "Missing essential glutathione components"
        
    # Check for peptide bonds
    peptide_bond = Chem.MolFromSmarts("[NX3][CX3](=[OX1])")
    if len(mol.GetSubstructMatches(peptide_bond)) < 2:
        return False, "Missing peptide bonds"
        
    # Analyze modifications
    modifications = []
    
    # Check for S-modifications
    if len(mol.GetSubstructMatches(Chem.MolFromSmarts("CS[!S]"))) > 0:
        modifications.append("S-modified")
        
    # Check for C-terminal modifications
    if len(mol.GetSubstructMatches(Chem.MolFromSmarts("CC(=O)[!O]"))) > 0:
        modifications.append("C-terminal modified")
        
    # Check for N-terminal modifications  
    if len(mol.GetSubstructMatches(Chem.MolFromSmarts("[!N]C(CCC(=O))"))) > 0:
        modifications.append("N-terminal modified")
        
    if modifications:
        return True, f"Glutathione derivative with {', '.join(modifications)}"
    else:
        return True, "Unmodified glutathione"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24337',
                          'name': 'glutathione derivative',
                          'definition': 'Any organonitrogen compound derived '
                                        'from the Glu-Cys-Gly tripeptide '
                                        'glutathione.',
                          'parents': [   'CHEBI:33261',
                                         'CHEBI:35352',
                                         'CHEBI:36963']},
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
    'num_true_negatives': 183871,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673694915623}