# Copyright ZettaBlock Labs 2024
import pkg_resources

import zetta_version

def test_version():
    mod_version = zetta_version.__version__
    pkg_version = pkg_resources.require("zetta")[0].version

    assert pkg_resources.parse_version(mod_version) > pkg_resources.parse_version("0.0.0")
    assert pkg_resources.parse_version(pkg_version) > pkg_resources.parse_version("0.0.0")

    assert mod_version == pkg_version
