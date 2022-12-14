# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

from torque import v1


class InternalError(v1.exceptions.TorqueException):
    """TODO"""


class ComponentNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: component not found"


class ComponentExists(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: component already exists"


class ComponentStillConnected(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: component still connected"


class LinkNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: link not found"


class LinkExists(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: link already exists"


class CycleDetected(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return "cycle detected, can't continue"


class ComponentsNotConnected(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]},{self.args[1]}: components not connected"


class ComponentTypeNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: component type not found"


class LinkTypeNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: link type not found"


class ProviderNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: provider not found"


class InterfaceNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: interface not found"


class BondNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: bond not found"


class InvalidRequirement(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: invalid requirements"


class InvalidName(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: invalid name"


class DeploymentExists(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: deployment already exists"


class DeploymentNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: deployment not found"


class ContextNotFound(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: context not found"


class NoComponentsSelected(v1.exceptions.TorqueException):
    """TODO"""

    def __str__(self) -> str:
        return f"{self.args[0]}: no components selected"


class OperationAborted(v1.exceptions.TorqueException):
    """TODO"""
