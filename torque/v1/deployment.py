# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

import threading

from torque.v1 import interface
from torque.v1 import provider
from torque.v1 import utils


class Deployment:
    """TODO"""

    def __init__(self, name: str, profile: str, dry_run: bool, providers: [provider.Provider]):
        self.name = name
        self.profile = profile
        self.dry_run = dry_run

        self._providers = providers
        self._lock = threading.Lock()
        self._interfaces: dict[str, provider.Provider] = {}

    def _interface(self, cls: type, labels: [str]) -> interface.Context:
        """TODO"""

        name = utils.fqcn(cls)

        if name in self._interfaces:
            return self._interfaces[name].interface(cls)

        for provider in self._providers:
            if not provider.has_interface(cls):
                continue

            return provider.interface(cls)

        return interface.Context(self._lock, None)

    def interface(self, cls: type, labels: [str]) -> interface.Context:
        """TODO"""

        with self._lock:
            return self._interface(cls, labels)


def create(name: str, profile: str, dry_run: bool, providers: [provider.Provider]) -> Deployment:
    """TODO"""

    return Deployment(name, profile, dry_run, providers)
