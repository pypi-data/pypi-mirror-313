from __future__ import annotations

from pydantic import Field

from digitalhub.entities.model._base.spec import ModelSpec, ModelValidator


class ModelSpecHuggingface(ModelSpec):
    """
    ModelSpecHuggingface specifications.
    """

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
        model_id: str | None = None,
        model_revision: str = None,
    ) -> None:
        super().__init__(path, framework, algorithm, base_model, parameters, metrics)
        self.model_id = model_id
        self.model_revision = model_revision


class ModelValidatorHuggingface(ModelValidator):
    """
    ModelValidatorHuggingface validator.
    """

    placeholder_model_id: str = Field(default=None, alias="model_id")
    """Huggingface model id. If not specified, the model is loaded from the model path."""

    placeholder_model_revision: str = Field(default=None, alias="model_revision")
    """Huggingface model revision."""
