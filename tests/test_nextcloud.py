#
# foris-controller-nextcloud-module
# Copyright (C) 2020 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
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

from foris_controller_testtools.fixtures import (
    only_backends,
    only_message_buses,
    backend,
    infrastructure,
    FILE_ROOT_PATH,
    notify_api
)

from foris_controller_testtools.utils import FileFaker


@pytest.fixture(scope="function")
def nextcloud_configs():
    with FileFaker(
        FILE_ROOT_PATH, "/srv/www/nextcloud/index.php", False, ""
    ) as res1, FileFaker(
        FILE_ROOT_PATH, "/tmp/nextcloud_configuring", False, ""
    ) as res2, FileFaker(
        FILE_ROOT_PATH, "/srv/www/nextcloud/config/config.php", False, ""
    ) as res3:
        yield res1, res2, res3


def test_get_status(infrastructure):
    res = infrastructure.process_message(
        {"module": "nextcloud", "action": "get_status", "kind": "request"}
    )
    assert res["data"].keys() == {"nextcloud_installed", "nextcloud_configured", "nextcloud_configuring"}


@pytest.mark.only_backends(["openwrt"])
def test_configure_nextcloud(infrastructure, nextcloud_configs):
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

    assert all(res1['data'].values())
