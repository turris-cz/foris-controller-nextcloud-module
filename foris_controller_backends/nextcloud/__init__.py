#
# foris-controller-nextcloud-module
# Copyright (C) 2020-2022 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
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

import logging
import os

from foris_controller_backends.cmdline import BaseCmdLine
from foris_controller_backends.files import BaseFile, inject_file_root

logger = logging.getLogger(__name__)


class NextcloudWrapper:
    def get_status(self):
        return {
            'nextcloud_installed': os.path.isfile(inject_file_root('/srv/www/nextcloud/index.php')),
            'nextcloud_configuring': os.path.isfile(inject_file_root('/tmp/nextcloud_configuring')),
            'nextcloud_configured': os.path.isfile(inject_file_root('/srv/www/nextcloud/config/config.php'))
        }


class SoftwareManager(BaseCmdLine, BaseFile):
    def configure_nextcloud(self, creds):
        retval, _, _ = self._run_command(
            "/usr/bin/nextcloud_install", "--daemon", "--batch", creds['credentials']['login'], creds['credentials']['password']
        )
        return {"result": retval == 0}
