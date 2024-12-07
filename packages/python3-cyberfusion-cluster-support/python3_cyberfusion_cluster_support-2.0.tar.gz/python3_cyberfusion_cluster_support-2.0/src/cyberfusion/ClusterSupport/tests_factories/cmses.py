"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.cmses import CMS, CMSSoftwareName
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class CMSFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = CMS

        exclude = ("virtual_host",)

    software_name = factory.fuzzy.FuzzyChoice(CMSSoftwareName)
    virtual_host = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.virtual_hosts.VirtualHostFactory",
    )
    virtual_host_id = factory.SelfAttribute("virtual_host.id")
    is_manually_created = True
