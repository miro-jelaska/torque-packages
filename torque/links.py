# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

from torque.v1 import link as link_v1


class DependencyLink(link_v1.Link):
    """TODO"""

    @staticmethod
    def validate_parameters(parameters: object) -> object:
        """TODO"""

        return {}

    @staticmethod
    def validate_configuration(configuration: object) -> object:
        """TODO"""

        return {}

    def on_create(self):
        """TODO"""

    def on_remove(self):
        """TODO"""

    def on_initialize(self, configuration: object):
        """TODO"""

    def on_build(self, deployment: str, profile: str) -> bool:
        """TODO"""

        return True

    def on_generate(self, deployment: str, profile: str) -> bool:
        """TODO"""

        return True
