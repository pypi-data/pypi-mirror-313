
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

SMILES_STRING = str


# make this hashable?
class ChemicalStructure(BaseModel):
    """Represents a chemical entity with a known specific structure/formula."""
    name: str = Field(..., description="rdfs:label of the structure in CHEBI")
    smiles: SMILES_STRING = Field(..., description="SMILES string derived from CHEBI")

    def __hash__(self):
        return hash(self.smiles)

    def __eq__(self, other):
        if not isinstance(other, ChemicalStructure):
            return NotImplemented
        return self.smiles == other.smiles


class ChemicalClass(BaseModel):
    """Represents a class/grouping of chemical entities."""
    id: str = Field(..., description="id/curie of the CHEBI class")
    name: str = Field(..., description="rdfs:label of the class in CHEBI")
    definition: str = Field(..., description="definition of the structure from CHEBI")
    parents: Optional[List[str]] = Field(default=None, description="parent classes")
    instances: List[ChemicalStructure] = Field(..., description="positive examples")
    negative_instances: Optional[List[ChemicalStructure]] = Field(default=None, description="negative examples")


class Dataset(BaseModel):
    """
    Represents a dataset of chemical classes.
    """
    ontology_version: Optional[str] = None
    min_members: Optional[int] = None
    max_members: Optional[int] = None
    classes: List[ChemicalClass]
    structures: List[ChemicalStructure] = None

    @property
    def name(self):
        return f"bench-{self.ontology_version}-{self.min_members}-{self.max_members}"

from typing import Optional


class Config(BaseModel):
    """Experimental setup"""
    llm_model_name: str = "gpt-4o"
    f1_threshold: float = 0.8
    max_attempts: int = 4
    max_negative_to_test: Optional[int] = None
    max_positive_in_prompt: int = 50
    max_negative_in_prompt: int = 20
    max_instances_in_prompt: Optional[int] = 100
    test_proportion: float = 0.2


OUTCOME = Tuple[str, Optional[str]]


class Result(BaseModel):
    """Result of running workflow on a chemical class"""
    chemical_class: ChemicalClass
    config: Optional[Config] = None
    code: str
    message: Optional[str] = None
    true_positives: Optional[List[OUTCOME]] = None
    false_positives: Optional[List[OUTCOME]] = None
    true_negatives: Optional[List[OUTCOME]] = None
    false_negatives: Optional[List[OUTCOME]] = None
    attempt: int = 0
    success: bool = True
    best: bool = False
    error: Optional[str] = None
    stdout: Optional[str] = None

    num_true_positives: Optional[int] = None
    num_false_positives: Optional[int] = None
    num_true_negatives: Optional[int] = None
    num_false_negatives: Optional[int] = None
    num_negatives: Optional[int] = None

    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    accuracy: Optional[float] = None

    def calculate(self):
        """Calculate derived statistics"""
        self.num_true_positives = len(self.true_positives or [])
        self.num_false_positives = len(self.false_positives or [])
        if self.num_true_negatives is None:
            self.num_true_negatives = len(self.true_negatives or [])
        if self.num_false_negatives is None:
            self.num_false_negatives = len(self.false_negatives or [])
        if self.num_true_positives + self.num_false_positives:
            self.precision = self.num_true_positives / (self.num_true_positives + self.num_false_positives)
        else:
            self.precision = 0.0
        if self.num_true_positives + self.num_false_negatives:
            self.recall = self.num_true_positives / (self.num_true_positives + self.num_false_negatives)
        else:
            self.recall = 0
        if self.precision and self.recall:
            self.f1 = 2 * (self.precision * self.recall) / (self.precision + self.recall)
        else:
            self.f1 = 0
        if self.num_true_positives + self.num_true_negatives + self.num_false_positives + self.num_false_negatives:
            self.accuracy = (self.num_true_positives + self.num_true_negatives) / (
                    self.num_true_positives + self.num_true_negatives + self.num_false_positives + self.num_false_negatives)

class ResultSet(BaseModel):
    """A set of results"""
    best_result: Optional[Result] = None
    results: List[Result]

    @classmethod
    def from_results(cls, results: List[Result]) -> "ResultSet":
        """Populate the result set from a list of results"""
        obj = cls(results=results, best_result=max(results, key=lambda r: r.f1))
        if obj.best_result:
            obj.best_result.best = True
        return obj

class EvaluationResult(BaseModel):
    """Result of evaluating a model"""
    train_results: ResultSet
    test_result: Result

class EvaluationExperiment(BaseModel):
    """Represents an evaluation experiment"""
    config: Config
    evaluation_results: List[EvaluationResult]

class ClassificationResult(BaseModel):
    input_smiles: SMILES_STRING
    class_id: str
    class_name: Optional[str] = None
    is_match: bool
    reason: Optional[str] = None
    confidence: Optional[float] = None
