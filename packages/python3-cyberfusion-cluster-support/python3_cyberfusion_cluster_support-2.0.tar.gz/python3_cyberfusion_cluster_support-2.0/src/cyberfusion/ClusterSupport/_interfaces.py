"""Interfaces."""

from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import TYPE_CHECKING, Callable, TypeVar, cast

if TYPE_CHECKING:
    from cyberfusion.ClusterSupport import ClusterSupport

F = TypeVar("F", bound=Callable[..., None])


def sort_lists(f: F) -> F:
    """Sort lists.

    Lists returned by the Core API are not ordered.
    """

    @wraps(f)
    def wrapper(self: "APIObjectInterface", obj: dict) -> None:
        for _, value in obj.items():
            if not isinstance(value, list):
                continue

            if any(isinstance(item, dict) for item in value):
                continue

            value.sort()

        f(self, obj)

    return cast(F, wrapper)


class APIObjectInterface(metaclass=ABCMeta):
    """Interface for API object."""

    def __init__(self, support: "ClusterSupport") -> None:
        """Set attributes."""
        self.support = support

    @abstractmethod
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        pass

    @classmethod
    def _build(
        cls,
        support: "ClusterSupport",
        obj: dict,
    ) -> "APIObjectInterface":
        """Build class from dict with object attributes."""
        class_ = cls(support)

        class_._set_attributes_from_model(obj)

        return class_
