from __future__ import annotations


class BuilderError(Exception):
    """
    Raised when incontered errors on builders.
    """


class StoreError(Exception):
    """
    Raised when incontered errors on stores.
    """


class BackendError(Exception):
    """
    Raised when incontered errors from backend.
    """


class EntityNotExistsError(BackendError):
    """
    Raised when entity not found.
    """


class EntityAlreadyExistsError(BackendError):
    """
    Raised when entity already exists.
    """


class MissingSpecError(BackendError):
    """
    Raised when spec is missing in backend.
    """


class UnauthorizedError(BackendError):
    """
    Raised when unauthorized.
    """


class ForbiddenError(BackendError):
    """
    Raised when forbidden.
    """


class BadRequestError(BackendError):
    """
    Raised when bad request.
    """


class EntityError(Exception):
    """
    Raised when incontered errors on entities.
    """


class ContextError(Exception):
    """
    Raised when context errors.
    """


class ReaderError(Exception):
    """
    Raised when incontered errors on readers.
    """
