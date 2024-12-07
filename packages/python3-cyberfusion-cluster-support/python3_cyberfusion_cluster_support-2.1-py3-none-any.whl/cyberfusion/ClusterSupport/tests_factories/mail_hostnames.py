"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.mail_hostnames import MailHostname
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class MailHostnameFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = MailHostname

        exclude = (
            "cluster",
            "certificate",
        )

    domain = factory.Faker("domain_name")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterMailFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    certificate = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.certificates.CertificateSingleFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    certificate_id = factory.SelfAttribute("certificate.id")
