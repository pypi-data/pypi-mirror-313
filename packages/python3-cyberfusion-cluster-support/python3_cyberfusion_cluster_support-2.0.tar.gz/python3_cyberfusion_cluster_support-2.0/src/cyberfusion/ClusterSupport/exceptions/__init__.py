"""Generic exceptions."""


class ClusterInaccessibleException(Exception):
    """API user does not have access to cluster."""

    pass


class ClusterIDNotSetException(Exception):
    """Cluster ID is required, but not set."""

    pass
