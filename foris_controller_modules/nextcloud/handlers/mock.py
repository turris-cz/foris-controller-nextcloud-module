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

import logging

from foris_controller.handler_base import BaseMockHandler
from foris_controller.utils import logger_wrapper

from .. import Handler

logger = logging.getLogger(__name__)


class MockNextcloudHandler(Handler, BaseMockHandler):
    nextcloud_installed = False
    nextcloud_configured = False
    nextcloud_configuring = False

    @logger_wrapper(logger)
    def get_status(self):
        return {
            "nextcloud_installed": MockNextcloudHandler.nextcloud_installed,
            "nextcloud_configured": MockNextcloudHandler.nextcloud_configured,
            "nextcloud_configuring": MockNextcloudHandler.nextcloud_configuring,
        }

    @logger_wrapper(logger)
    def configure_nextcloud(self):
        raise NotImplementedError
