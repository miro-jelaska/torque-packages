# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

import typing
import types

from torque import exceptions
from torque import model
from torque import v1


_REQUIREMENTS_SCHEMA = v1.schema.Schema({
    v1.schema.Optional(str): {
        "interface": type,
        "required": bool
    }
})


def _bind_to(for_type: type,
             name: str,
             bond_type: type,
             create_bond: typing.Callable,
             bind_provider: typing.Callable) -> [object]:
    """TODO"""

    interfaces = types.SimpleNamespace()
    requirements = bond_type.on_requirements()

    if not requirements:
        return interfaces

    requirements = _REQUIREMENTS_SCHEMA.validate(requirements)

    for r_name, r in requirements.items():
        interface = None

        if issubclass(r["interface"], v1.bond.Interface):
            interface = create_bond(for_type, name, r["interface"], r["required"])

        elif issubclass(r["interface"], v1.provider.Provider):
            interface = bind_provider(r["interface"], r["required"])

        else:
            raise exceptions.InvalidRequirement(name)

        setattr(interfaces, r_name, interface)

    return interfaces


def bind_to_bond(for_type: type,
                 name: str,
                 bond_type: type,
                 create_bond: typing.Callable,
                 bind_provider: typing.Callable) -> [object]:
    """TODO"""

    return _bind_to(for_type,
                    name,
                    bond_type,
                    create_bond,
                    bind_provider)


def bind_to_provider(provider_type: type,
                     create_bond: typing.Callable,
                     bind_provider: typing.Callable) -> [object]:
    """TODO"""

    return _bind_to(provider_type,
                    v1.utils.fqcn(provider_type),
                    provider_type,
                    create_bond,
                    bind_provider)


def bind_to_component(component_type: type,
                      component_name: str,
                      create_bond: typing.Callable) -> [object]:
    """TODO"""

    interfaces = types.SimpleNamespace()
    requirements = component_type.on_requirements()

    if not requirements:
        return interfaces

    requirements = _REQUIREMENTS_SCHEMA.validate(requirements)

    for r_name, r in requirements.items():
        interface = None

        if issubclass(r["interface"], v1.bond.Interface):
            interface = create_bond(component_type,
                                    component_name,
                                    r["interface"],
                                    r["required"])

        else:
            raise exceptions.InvalidRequirement(component_name)

        setattr(interfaces, r_name, interface)

    return interfaces


def bind_to_link(link_type: type,
                 link_name: str,
                 source: model.Component,
                 destination: model.Component,
                 create_bond: typing.Callable) -> [object]:
    """TODO"""

    interfaces = types.SimpleNamespace()
    requirements = link_type.on_requirements()

    if not requirements:
        return interfaces

    requirements = _REQUIREMENTS_SCHEMA.validate(requirements)

    for r_name, r in requirements.items():
        interface = None

        if issubclass(r["interface"], v1.component.SourceInterface):
            # pylint: disable=W0212
            interface = source._torque_interface(r["interface"], r["required"])

        elif issubclass(r["interface"], v1.component.DestinationInterface):
            # pylint: disable=W0212
            interface = destination._torque_interface(r["interface"], r["required"])

        elif issubclass(r["interface"], v1.bond.Interface):
            interface = create_bond(link_type,
                                    link_name,
                                    r["interface"],
                                    r["required"])

        else:
            raise exceptions.InvalidRequirement(link_name)

        setattr(interfaces, r_name, interface)

    return interfaces
