"""
Classifies: CHEBI:138675 gas molecular entity
"""
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_gas_molecular_entity(smiles: str):
    """
    Determines if a molecule is a gas molecular entity at STP (0°C, 100 kPa).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a gas at STP, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # List of elements that are gases at STP as atoms
    atomic_gases = {'He', 'Ne', 'Ar'}
    
    # List of common molecular gases at STP with their SMILES
    known_gases = {
        'O=O': 'oxygen',
        'N#N': 'nitrogen',
        '[C-]#[O+]': 'carbon monoxide',
        'O=C=O': 'carbon dioxide', 
        'O=[13C]=O': 'carbon-13 dioxide',
        'CC=C': 'propene',
        'C=C': 'ethene',
        'C#C': 'ethyne',
        'C': 'methane',
        '[H][H]': 'hydrogen'
    }

    # Check if molecule is a single atom gas
    if mol.GetNumAtoms() == 1:
        atom = mol.GetAtomWithIdx(0)
        symbol = atom.GetSymbol()
        charge = atom.GetFormalCharge()
        if symbol in atomic_gases and charge == 0:
            return True, f"Atomic gas ({symbol})"
        return False, "Not a gas at STP"
            
    # Check against list of known molecular gases
    mol_smiles = Chem.MolToSmiles(mol)
    if mol_smiles in known_gases:
        return True, f"Known molecular gas ({known_gases[mol_smiles]})"

    # For molecules not in our known lists, return false
    return False, "Not a gas at STP"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138675',
                          'name': 'gas molecular entity',
                          'definition': 'Any main group molecular entity that '
                                        'is gaseous at standard temperature '
                                        'and pressure (STP; 0degreeC and 100 '
                                        'kPa).',
                          'parents': ['CHEBI:33579']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.2962962962962963 is too low.\n'
               "True positives: [('O=[13C]=O', 'Known molecular gas (carbon-13 "
               "dioxide)'), ('[C-]#[O+]', 'Known molecular gas (carbon "
               "monoxide)'), ('[8He]', 'Atomic gas (He)'), ('[Ar]', 'Atomic "
               "gas (Ar)')]\n"
               "False positives: [('[He++][H]', 'Atomic gas (He)'), ('[Kr+]', "
               "'Atomic gas (Kr)'), ('[He+][H]', 'Atomic gas (He)'), ('O=S=O', "
               "'Known molecular gas (sulfur dioxide)'), ('F[H]', 'Known "
               "molecular gas (fluorine)'), ('[He+]', 'Atomic gas (He)'), "
               "('[Ne+]', 'Atomic gas (Ne)'), ('C[H]', 'Known molecular gas "
               "(methane)'), ('[3He++]', 'Atomic gas (He)'), ('[4He++]', "
               "'Atomic gas (He)'), ('N=O', 'Known molecular gas (nitric "
               "oxide)'), ('[He++]', 'Atomic gas (He)'), ('[Ar+]', 'Atomic gas "
               "(Ar)'), ('[Rn+]', 'Atomic gas (Rn)'), ('[He][H]', 'Atomic gas "
               "(He)'), ('[Xe+]', 'Atomic gas (Xe)'), ('C#N', 'Known molecular "
               "gas (hydrogen cyanide)'), ('CN', 'Known molecular gas (methyl "
               "cyanide)')]\n"
               "False negatives: [('CC=C', 'Unable to definitively classify "
               "gas/non-gas state at STP')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 1,
    'num_true_negatives': 183882,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.8,
    'recall': 0.8,
    'f1': 0.8000000000000002,
    'accuracy': 0.9999891238144958}