"""Base factories."""

from typing import Any

import factory

from cyberfusion.ClusterSupport import ClusterSupport
from cyberfusion.ClusterSupport._interfaces import APIObjectInterface


def get_support() -> ClusterSupport:
    """Get support object.

    Should be mocked by tests.
    """
    raise NotImplementedError


class BaseBackendFactory(factory.Factory):
    """Base factory for ClusterSupport backend."""

    class Meta:
        """Settings."""

        abstract = True

    @classmethod
    def _create(
        cls, model_class: APIObjectInterface, *args: Any, **kwargs: Any
    ) -> APIObjectInterface:
        """Create object.

        Used for Factory Boy's 'create' strategy.
        """
        support = get_support()

        obj = model_class(support)

        obj.create(**kwargs)

        return obj

    @classmethod
    def _build(
        cls, model_class: APIObjectInterface, *args: Any, **kwargs: Any
    ) -> APIObjectInterface:
        """Build object.

        Used for Factory Boy's 'build' strategy.
        """
        support = get_support()

        obj = model_class._build(support, obj=kwargs)

        return obj
