from __future__ import annotations

from pydantic import Field

from digitalhub.entities.model._base.spec import ModelSpec, ModelValidator
from digitalhub.entities.model.mlflow.models import Dataset, Signature


class ModelSpecMlflow(ModelSpec):
    """
    ModelSpecMlflow specifications.
    """

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
        flavor: str | None = None,
        model_config: dict | None = None,
        input_datasets: list[Dataset] | None = None,
        signature: Signature = None,
    ) -> None:
        super().__init__(path, framework, algorithm, base_model, parameters, metrics)
        self.flavor = flavor
        self.model_config = model_config
        self.input_datasets = input_datasets
        self.signature = signature


class ModelValidatorMlflow(ModelValidator):
    """
    ModelValidatorMlflow validator.
    """

    flavor: str = None
    """Mlflow model flavor."""

    placeholder_cfg_: dict = Field(default=None, alias="model_config")
    """Mlflow model config."""

    input_datasets: list[Dataset] = None
    """Mlflow input datasets."""

    signature: Signature = None
    """Mlflow model signature."""
