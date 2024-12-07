"""Factories for API object."""

import factory.fuzzy

from cyberfusion.ClusterSupport.sites import Site
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class SiteFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Site

    name = factory.Faker("bothify", text="??-##", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    netbox_site_group_id = factory.Faker("random_int", min=500, max=2000)
    netbox_admin_prefix_ipv4_id = factory.Faker("random_int", min=500, max=2000)
    netbox_admin_prefix_ipv6_id = factory.Faker("random_int", min=500, max=2000)
    netbox_customer_prefix_container_ipv4_id = factory.Faker(
        "random_int", min=500, max=2000
    )
    netbox_customer_prefix_container_ipv6_id = factory.Faker(
        "random_int", min=500, max=2000
    )
    netbox_vlan_group_id = factory.Faker("random_int", min=500, max=2000)
    netbox_default_vm_cluster_id = factory.Faker("random_int", min=500, max=2000)
    netbox_borg_server_vm_cluster_id = factory.Faker("random_int", min=500, max=2000)
