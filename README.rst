============
os-placement
============

`os-placement` is a library containing utilities for dealing with data that is
exposed and manipulated with the OpenStack Placement API.

* Free software: Apache license
* Documentation: https://docs.openstack.org/os-placement/latest/
* Source: http://git.openstack.org/cgit/openstack/os-placement
* Bugs: https://bugs.launchpad.net/os-placement

Usage
=====

The ``os_placement.provider.config`` module provides a few objects and a
``from_file`` function to easily read a file with the **``provider.yaml``**
syntax.

The ``os_placement.provider.config.from_file`` method takes a single positional
argument representing the path to the file to attempt to load. It returns a
``os_placement.provider.config.ProviderConfig`` object upon successful loading
of the file. This object may be used to examine various attributes about a
resource provider, its inventory record overrides and its trait overrides.

::

    from os_placement.provider import config

    conf_path = "/etc/nova/host-provider.conf"

    pconf = config.from_file(conf_path)

    print pconf.schema_version  # prints "1.0"

    if pconf.uuid:
        print "Override for the compute node's UUID: " + pconf.uuid

    if pconf.name:
        print "Override for the compute node's provider name: " + pconf.name

    if pconf.inventories:
        # pconf.inventories is a dict, keyed by resource class name, of
        # instances of `os_placement.provider.config.ProviderInventoryConfig`
        print "Found %d inventory override records" % len(pconf.inventories)
        for resource_class, inv_conf in pconf.inventories:
            if inv_conf.total is not None:
                print "Found override for %s total amount: %d" % (
                    resource_class, inv_conf.total)
            if inv_conf.reserved is not None:
                print "Found override for %s reserved amount: %d" % (
                    resource_class, inv_conf.reserved)

    if pconf.traits:
        # pconf.traits is an instance of
        # ``os_placement.provider.config.ProviderTraitsConfig``
        if pconf.traits.always:
            print "Found %d traits to always set on the provider: " % (
                pconf.traits.always)
        if pconf.traits.ignore:
            print "Found %d traits to ignore for the provider: " % (
                pconf.traits.ignore)
