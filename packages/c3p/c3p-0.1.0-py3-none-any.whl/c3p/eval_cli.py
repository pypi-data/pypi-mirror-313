from pathlib import Path
from typing import Iterator, Annotated, List, Optional

import typer
import yaml

import c3p.classifier as classifier
from c3p.datamodel import SMILES_STRING, Dataset, Config
from c3p.generator import evaluate_for_class

app = typer.Typer(help="CHEBI classifier - eval.")

import logging

# Set up logger
#logger = logging.getLogger(__name__)
logger = logging.getLogger()  # Get root logger


def configure_logging(verbosity: int):
    """Configure logging based on verbosity level"""
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Configure handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Set up logger
    logger.setLevel(level)
    logger.addHandler(handler)


def verbose_option(f):
    """Decorator to add verbose option to commands"""
    return typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Verbosity level: -v for INFO, -vv for DEBUG",
    )(f)

app = typer.Typer()


@app.command()
def eval_on_class(
        class_name: str = typer.Argument(..., help="class name"),
        dataset_path: Path = typer.Option(None, "--dataset", "-d", help="path to dataset"),
        model_name: Optional[str] = typer.Option(None, "--model", "-m", help="model name"),
        max_negative: Optional[int] = typer.Option(None, "--max-negative", "-n", help="max negative examples"),
        verbose: int = verbose_option,
) -> None:
    """
    Evaluate a model on a dataset using a single class.
    """
    n = 0
    configure_logging(verbose)
    with open(dataset_path, "r") as f:
        dataset = Dataset.model_validate_json(f.read())

    logger.info(f"Structures: {len(dataset.structures)}")
    cc = [c for c in dataset.classes if c.name == class_name].pop()
    config = Config(llm_model_name=model_name, max_negative_to_test=max_negative)
    result = evaluate_for_class(cc, config, dataset)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    app()