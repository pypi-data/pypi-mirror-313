"""
Classifies: CHEBI:18085 glycosaminoglycan
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glycosaminoglycan(smiles: str):
    """
    Determines if a molecule is a glycosaminoglycan based on presence of aminomonosaccharide residues.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycosaminoglycan, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"

        # Count atoms
        num_atoms = mol.GetNumAtoms()
        if num_atoms < 10:  # Arbitrary minimum size for GAG
            return False, "Molecule too small for a glycosaminoglycan"

        # Check for presence of nitrogen and oxygen
        num_N = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
        num_O = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)

        if num_N == 0:
            return False, "No nitrogen atoms found - required for aminosaccharides"
        if num_O < 3:
            return False, "Too few oxygen atoms for glycosaminoglycan structure"

        # Look for amide groups (N-C=O)
        amide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])')
        num_amides = len(mol.GetSubstructMatches(amide_pattern))

        # Look for hydroxyl groups
        hydroxyl_pattern = Chem.MolFromSmarts('[OH]')
        num_hydroxyls = len(mol.GetSubstructMatches(hydroxyl_pattern))

        # Look for amine groups
        amine_pattern = Chem.MolFromSmarts('[NX3;H2,H1;!$(NC=O)]')
        num_amines = len(mol.GetSubstructMatches(amine_pattern))

        # Calculate ratio of O and N to total atoms
        o_n_ratio = (num_O + num_N) / num_atoms

        # Define criteria for classification
        is_gag = (num_amides >= 1 and  # Contains amide bonds
                 num_hydroxyls >= 1 and  # Contains hydroxyl groups
                 (num_amines >= 1 or num_amides >= 2) and  # Contains amine groups or multiple amides
                 o_n_ratio >= 0.2)  # High proportion of O and N atoms

        if is_gag:
            return True, f"Contains {num_amides} amide bonds, {num_hydroxyls} hydroxyl groups, {num_amines} amine groups"
        else:
            return False, "Does not meet structural requirements for glycosaminoglycan"

    except Exception as e:
        return False, f"Error analyzing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18085',
                          'name': 'glycosaminoglycan',
                          'definition': 'Any polysaccharide containing a '
                                        'substantial proportion of '
                                        'aminomonosaccharide residues.',
                          'parents': ['CHEBI:22506']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               'False negatives: '
               "[('O=C1N(O)CCCCCNC(=O)CCC(=O)N(O)CCCCCCNC(CCC(N(CCCCCCNC(CC1)=O)O)=O)=O', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1C)C(=O)NC(C=3SC=C(N3)C(=O)NCC(=O)NC(C(C)C)C4=NC(C5=NC(C6=C(C7=NC(C(NC2CC(=O)NC)=O)=CS7)C=CC(=N6)C=8SC=C(N8)C=9OCC(N9)C(=O)N%10C(C(=O)N)CCC%10)=CS5)=CS4)C(C)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('ClC(CCCCCCC[C@@H]([C@H]1NC(=O)[C@H]2N(C(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](CCC(=O)N)NC([C@@H](NC([C@@H](NC(\\\\C(\\\\NC([C@@H](NC([C@@H]1O)=O)C(C)C)=O)=C/C)=O)[C@H](O)C)=O)[C@H](O)C)=O)C)[C@H](OC)C)C)CC(=O)N)CCC2)C)CC', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1NCC[C@H](O)[C@@H]2NC(=O)C(C2=O)=C(O)C=C[C@H]3[C@H](CC=C1)[C@H]4C=C[C@H]5[C@H](C(=O)CO)[C@@H](C[C@@H]5[C@H]4C3)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1NC(CC=CC=C(C=CC=CC(CC=C(C=CC=C1)C)O)C)C/C=C/CCC', 'Error "
               'analyzing molecule: Python argument types in\\n    '
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('CC(=O)N[C@@H]1[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H](CO)O[C@H]1NC(=O)C[C@H](N)C(O)=O', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O1C=2C=C(C=CC(=O)NCCCCNCCCNC(=O)C=CC3=CC=C1C=C3)C=CC2O', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1)C(=O)N[C@@H](C=3SC=C(N3)C(=O)N[C@H](C4=NC(C(N[C@H]2[C@H](CC)C)=O)=C(O4)C)C)CC(=O)O', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1)C(=O)NC(C(=O)NC(C(=O)NCC(=O)NC(C(NC(C(N(CC(NC2)=O)C)=O)=C)=O)C)CC=3C4=C(OC)C=CC=C4NC3)CC=5C6=C(C=CC=C6)NC5', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1N([C@H](C(=O)N(CC(=O)N([C@H](C(=O)N2[C@H](C(=O)N(C)[C@H](C(N[C@H](C(N([C@H](C(N([C@H](C(N([C@H]1[C@H](CC)C)C)=O)CC(C)C)C)=O)C(C)C)C)=O)C)=O)CC3=CC=C(OC)C=C3)CCC2)CC(C)C)C)C)C)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1NCCC[C@H](NC(=O)C)C(=O)OCCC(=C1)C', 'Error analyzing "
               'molecule: Python argument types in\\n    '
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('Cl[C@@H]1[C@H](O)C2[C@@H]3[C@H](C=CC(O)=C4C(=O)N[C@H](C4=O)[C@@H](O)CCNC(C=CC3)=O)CC2[C@@H]5[C@@H]1[C@@H]([C@H](C)C5)C(OC)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1N([C@H](C(=O)NCCCC[C@H](C(N([C@H]1C(C)C)C)=O)NC(=O)/C=C/C2=CC=C(OCC=C=C)C=C2)C)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@@H](C(NC(C(N(CC(N[C@@H]2CO)=O)C)=O)=C)=O)C)CC=3C4=C(OC)C=CC=C4NC3)CC=5C6=C(C=CC=C6)NC5', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C/1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N([C@H](C(N2[C@H](C(N[C@@H]([C@H](C(N[C@H](C(N\\\\C1=C\\\\C)=O)C(C)C)=O)O)[C@H](CCCCCCCCCCC(=O)CCC)C)=O)CCC2)=O)CC(=O)N)C)[C@H](OC)C)CCC(=O)N)[C@H](O)C)[C@H](O)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@@H](C(NC(C(N(CC(N[C@@H]2C)=O)C)=O)=C)=O)C)CC=3C4=C(OC)C=CC=C4NC3)CC=5C6=C(C=CC=C6)NC5', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1NC=2C(O)=C(C(=O)C(C2)=O)CCC=C(C(OC(=O)C(NC(=O)C3CCCCC3)C)C(C)C(CC=CC=CC=CC(C1)OC)O)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1[C@H]2[C@@H]([C@H](O)[C@H]([C@@H](O)[C@H]([C@H](OC(=O)C)[C@@H]([C@@H](OC)C=CO[C@@]3(C(C4=C5C(C=6O[C@@](C1)(C(=O)NC6C=C5O)C)=C(O)C(=C4O3)C)=O)C)C)C)C)C2', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('ClC1=C(O)C=C2CC(=CC=C[C@@H](OC)C(=O)C[C@@H]([C@H](C=C([C@H](CC(NC1=C2)=O)O)C)C)O)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1NC=2C(=O)C(=C(OC)C(C2[C@H](OC)C(=O)C[C@H](O)C)=O)C[C@H](C[C@H](OC)[C@H](O)[C@H](C=C([C@@H]([C@H](C=CC=C1C)OC)OC(=O)N)C)C)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C=3OC(=C(N3)C(=O)NCC=4SC=C(N4)C(=O)N[C@@H]2C(C)C)C)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1C2=NC(=C1)C(=O)N[C@H](C=3SC=C(N3)C(=O)N[C@H](C4=NC(C(N[C@H]2[C@H](CC)C)=O)=C(O4)C)C)CC=5N(C=NC5)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1S[C@@]23N4[C@@H]5[C@@H](OC(=O)C=6C=CC(=C(OC=7C=C([C@@H]([C@]1(N(C)C2=O)C4=O)O)C=CC7O)C6)OC)C=COC=C5[C@H]3O', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O([C@H]1[C@@H]([C@H](O)[C@@H]([C@@H](O)[C@@H](CO)C=CC=C(C(=O)N=C2C3=NC4(NC3=C5C(=C2O)C(O)=C(C=6O[C@](OC=C[C@H](OC)[C@H]1C)(C(=O)C56)C)C)CCN(CC4)CC(C)C)C)C)C)C(=O)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C/1N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N([C@H](C(N2[C@H](C(N[C@@H]([C@H](C(N[C@H](C(N\\\\C1=C\\\\C)=O)C(C)C)=O)O)[C@H](CCCCCCCCCCC(O)CCC)C)=O)CCC2)=O)CC(=O)N)C)[C@H](OC)C)CCC(=O)N)[C@H](O)C)[C@H](O)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1O[C@@H](C=C[C@@H](CCC(C=2C=3C(C=4[C@@]1(C=CC(=O)NC4C(=O)C3C=C(C)C2O)C)=O)=O)CC)[C@@H](O)C=C(C)C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S1CCN(O)C(=O)CCC(=O)NCCSCCN(O)C(=O)CCC(NCCSCCN(C(CCC(NCC1)=O)=O)O)=O', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('O=C1N[C@@H](CC=CC=C(C=CC=C[C@H]([C@H](C=C(C=CC=C1)C)O)O)C)C/C=C/C=C/C', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)'), "
               "('S(=O)(=O)(NC(=O)[C@]12NC(=O)[C@H]3N(C[C@H](OC(=O)N4CC5=C(C4)C=CC=C5F)C3)C(=O)[C@@H](NC(OC(C)(C)C)=O)CCCCCC=C[C@@H]1C2)C6CC6', "
               "'Error analyzing molecule: Python argument types in\\n    "
               'rdkit.Chem.rdMolDescriptors.CalcNumAtoms(Mol)\\ndid not match '
               "C++ signature:\\n    CalcNumAtoms(RDKit::ROMol mol)')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 309,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 0.4827586206896552,
    'f1': 0.1958041958041958,
    'accuracy': 0.7374429223744292}