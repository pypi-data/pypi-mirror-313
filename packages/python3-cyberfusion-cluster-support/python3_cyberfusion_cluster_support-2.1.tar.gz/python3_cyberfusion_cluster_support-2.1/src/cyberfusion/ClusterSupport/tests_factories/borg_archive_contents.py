"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.borg_archive_contents import (
    BorgArchiveContent,
    ContentObjectType,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _BorgArchiveContentFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BorgArchiveContent

    username = factory.Faker("user_name")
    group_name = factory.Faker("user_name")
    path = factory.Faker("file_name")
    modification_time = factory.Faker("iso8601")


class BorgArchiveContentRegularFileFactory(_BorgArchiveContentFactory):
    """Factory for specific object."""

    symbolic_mode = "-rw-r--r--"
    link_target = None
    object_type = ContentObjectType.REGULAR_FILE
    size = factory.Faker("random_int")


class BorgArchiveContentDirectoryFactory(_BorgArchiveContentFactory):
    """Factory for specific object."""

    symbolic_mode = "drwxr-xr-x"
    link_target = None
    object_type = ContentObjectType.DIRECTORY
    size = None


class BorgArchiveContentSymbolicLinkFactory(_BorgArchiveContentFactory):
    """Factory for specific object."""

    symbolic_mode = "lrwxr-xr-x"
    link_target = factory.Faker("file_name")
    object_type = ContentObjectType.SYMBOLIC_LINK
    size = None
