import logging
from pathlib import Path
from typing import Iterator, Annotated, List, Union, Optional

from c3p.datamodel import ClassificationResult, SMILES_STRING
from c3p.generator import run_code
from c3p.programs import PROGRAM_DIR

logger = logging.getLogger(__name__)


def classify(smiles: Union[SMILES_STRING, List[SMILES_STRING]], program_directory: Optional[Path] = None, strict=False) -> Iterator[ClassificationResult]:
    """
    Classify a SMILES string

    Args:
        smiles: The SMILES string to classify
        program_directory: The directory containing the programs

    Returns:
        The classification result
    """
    # find all programs in path
    if program_directory is None:
        program_directory = PROGRAM_DIR
    programs = list(program_directory.glob("*.py"))
    logger.info(f"Found {len(programs)} programs in {program_directory}")
    smiles_list = [smiles] if isinstance(smiles, str) else smiles
    # load each program
    for program in programs:
        if program.name.startswith("__"):
            continue
        with open(program, "r") as f:
            code = f.read()
        found = False
        for line in code.split("\n"):
            # use re to check if matches ^def is_(.*)\(smiles: str):
            import re
            fn_match = re.match(r"^def (is_.*)\(smiles: str\):", line)
            if fn_match:
                found = True
                fn = fn_match.group(1)
                for smiles in smiles_list:
                    try:
                        for _, satisfies, reason, metadata in run_code(code, fn, [smiles], []):
                            cc = metadata.get("chemical_class", {})
                            metric = "precision" if satisfies else "recall"
                            yield ClassificationResult(
                                input_smiles=smiles,
                                class_id = cc.get("id", "-"),
                                class_name = cc.get("name", "-"),
                                is_match=satisfies,
                                reason=reason,
                                confidence=metadata.get(metric)
                            )
                    except Exception as e:
                        if strict:
                            raise e
                        logger.error(f"Error running {fn} in {program}: {e}")
                break
        if not found:
            raise ValueError(f"Could not find is_ function in {program}")

