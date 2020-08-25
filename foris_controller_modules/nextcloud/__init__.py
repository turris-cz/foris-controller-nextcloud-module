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

from foris_controller.module_base import BaseModule
from foris_controller.handler_base import wrap_required_functions


class NextcloudModule(BaseModule):
    logger = logging.getLogger(__name__)

    def action_get_status(self, data):
        return self.handler.get_status()

    def action_configure_nextcloud(self, data):
        return self.handler.configure_nextcloud(data)


@wrap_required_functions(["get_status", "configure_nextcloud"])
class Handler(object):
    pass