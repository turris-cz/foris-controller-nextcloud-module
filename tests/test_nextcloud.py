#
# foris-controller-nextcloud-module
# Copyright (C) 2020-2023 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#

import pytest

from foris_controller_testtools.fixtures import FILE_ROOT_PATH
from foris_controller_testtools.utils import FileFaker


@pytest.fixture(scope="function")
def nextcloud_files_configured():
    """Mock that nextcloud is installed and configured."""
    with FileFaker(
        FILE_ROOT_PATH, "/srv/www/nextcloud/index.php", False, ""
    ) as res1, FileFaker(
        FILE_ROOT_PATH, "/srv/www/nextcloud/config/config.php", False, ""
    ) as res2:
        yield res1, res2


@pytest.fixture(scope="function")
def nextcloud_files_installed():
    """Mock that nextcloud is installed, but not configured."""
    with FileFaker(
        FILE_ROOT_PATH, "/srv/www/nextcloud/index.php", False, ""
    ) as res:
        yield res


@pytest.fixture(scope="function")
def nextcloud_installer_ok():
    """Mock the sucessful nextcloud install script."""
    content = """\
#!/bin/sh

exit 0
"""

    with FileFaker(FILE_ROOT_PATH, "/usr/bin/nextcloud_install", True, content) as res:
        yield res


@pytest.fixture(scope="function")
def nextcloud_installer_botched():
    """Mock the botched install script, which will return non-zero exit code."""
    content = """\
#!/bin/sh

exit 2
"""

    with FileFaker(FILE_ROOT_PATH, "/usr/bin/nextcloud_install", True, content) as res:
        yield res


def test_get_status(infrastructure):
    res = infrastructure.process_message(
        {"module": "nextcloud", "action": "get_status", "kind": "request"}
    )
    assert res["data"].keys() == {"nextcloud_installed", "nextcloud_configured", "nextcloud_configuring"}


@pytest.mark.only_backends(["openwrt"])
def test_configure_nextcloud_success(nextcloud_installer_ok, infrastructure, nextcloud_files_configured):
    res = infrastructure.process_message(
        {
            "module": "nextcloud",
            "action": "configure_nextcloud",
            "kind": "request",
            "data": {
                "credentials": {
                    "login": "username",
                    "password": "passw0rd"
                }
            }
        }
    )

    assert res == {
        "module": "nextcloud",
        "action": "configure_nextcloud",
        "kind": "reply",
        "data": {
            "result": True
        }
    }

    res1 = infrastructure.process_message(
        {"module": "nextcloud", "action": "get_status", "kind": "request"}
    )

    assert res1["data"]["nextcloud_installed"] is True
    assert res1["data"]["nextcloud_configuring"] is False
    assert res1["data"]["nextcloud_configured"] is True


@pytest.mark.only_backends(["openwrt"])
def test_configure_nextcloud_failure(nextcloud_installer_botched, infrastructure, nextcloud_files_installed):
    res = infrastructure.process_message(
        {
            "module": "nextcloud",
            "action": "configure_nextcloud",
            "kind": "request",
            "data": {
                "credentials": {
                    "login": "username",
                    "password": "passw0rd"
                }
            }
        }
    )

    assert res == {
        "module": "nextcloud",
        "action": "configure_nextcloud",
        "kind": "reply",
        "data": {
            "result": False
        }
    }

    res1 = infrastructure.process_message(
        {"module": "nextcloud", "action": "get_status", "kind": "request"}
    )
    assert res1["data"]["nextcloud_installed"] is True
    assert res1["data"]["nextcloud_configuring"] is False
    assert res1["data"]["nextcloud_configured"] is False
