from __future__ import annotations

import typing

from digitalhub.utils.exceptions import BuilderError

if typing.TYPE_CHECKING:
    from digitalhub.runtimes._base import Runtime


class RuntimeBuilder:
    """
    Builder class for building runtimes.
    """

    # Class variables
    RUNTIME_CLASS: Runtime = None

    def __init__(self) -> None:
        if self.RUNTIME_CLASS is None:
            raise BuilderError("RUNTIME_CLASS must be set")

    def build(self, project: str, *args, **kwargs) -> Runtime:
        """
        Build runtime object.

        Returns
        -------
        Runtime
            Runtime object.
        """
        return self.RUNTIME_CLASS(project, *args, **kwargs)
