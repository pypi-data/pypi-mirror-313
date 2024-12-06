from __future__ import annotations

from digitalhub.entities._base.material.spec import MaterialSpec, MaterialValidator


class ModelSpec(MaterialSpec):
    """
    ModelSpec specifications.
    """

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
    ) -> None:
        self.path = path
        self.framework = framework
        self.algorithm = algorithm
        self.base_model = base_model
        self.parameters = parameters
        self.metrics = metrics


class ModelValidator(MaterialValidator):
    """
    ModelValidator validator.
    """

    path: str
    """Path to the model."""

    framework: str = None
    """Model framework (e.g. 'pytorch')."""

    algorithm: str = None
    """Model algorithm (e.g. 'resnet')."""

    base_model: str = None
    """Base model."""

    parameters: dict = None
    """Model validator."""

    metrics: dict = None
    """Model metrics."""
