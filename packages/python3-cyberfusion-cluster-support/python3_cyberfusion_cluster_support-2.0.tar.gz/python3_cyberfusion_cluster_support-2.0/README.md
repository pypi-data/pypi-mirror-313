# python3-cyberfusion-cluster-support

API library for Core API.

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-cluster-support

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

## Config file options

* Section `clusterapi`, key `clusterid`. Only objects belonging to the specified cluster are loaded.
* Section `clusterapi`, key `serviceaccountid`. Only objects belonging to a cluster for which a service account to cluster exists for the specified service account are loaded.

## Class options

* `config_file_path`. Non-default config file path.
* `cluster_ids`. Only objects belonging to the specified clusters are loaded.

## Cluster IDs: order of precedence

The `cluster_ids` class option takes precedence over the `clusterid` config file option.

If neither is set, all objects are loaded.

If the `clusterid` config file option is set, but you want to load all objects, setting the `cluster_ids` class option to `None` (default) will not work. Instead, use the sentinel value `cyberfusion.ClusterSupport.ALL_CLUSTERS`.

# Usage

## Basic

```python
from cyberfusion.ClusterSupport import ClusterSupport

s = ClusterSupport()
```

## Read

### API objects without parameters

Some API objects do not require parameters to be retrieved.

These API objects are retrieved from the Core API once. They are then cached.

Examples:

```python
print(s.database_users)
print(s.unix_users)
print(s.fpm_pools)
```

### API objects with parameters

Some API objects require parameters to be retrieved.

These API objects are retrieved from the Core API on every call.

Example:

```python
print(s.access_logs(virtual_host_id=s.virtual_hosts[0].id, ...))
```

## Update

Example:

```python
d = s.database_users[0]
d.password = "newpassword"
d.update()
```

## Create

Example:

```python
from cyberfusion.ClusterSupport import ClusterSupport
from cyberfusion.ClusterSupport.certificates import Certificate

s = ClusterSupport()

c = Certificate(s)
assert c.id is None

c.create(common_names=["domlimev.nl", "www.domlimev.nl"])
assert c.id is not None
assert c.common_names == common_names=["domlimev.nl", "www.domlimev.nl"]
```

## Delete

Example:

```python
from cyberfusion.ClusterSupport import ClusterSupport

s = ClusterSupport()

c = s.certificates[0]
c.delete()
```
