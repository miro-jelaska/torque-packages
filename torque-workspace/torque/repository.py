# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

import importlib
import traceback
import sys

from torque import defaults
from torque import exceptions
from torque import v1


def _is_component(obj: type) -> bool:
    """TODO"""

    if not isinstance(obj, type):
        return False

    return issubclass(obj, v1.component.Component)


def _is_link(obj: type) -> bool:
    """TODO"""

    if not isinstance(obj, type):
        return False

    return issubclass(obj, v1.link.Link)


def _is_provider(obj: type) -> bool:
    """TODO"""

    if not isinstance(obj, type):
        return False

    return issubclass(obj, v1.provider.Provider)


def _is_bond(obj: type) -> bool:
    """TODO"""

    if not isinstance(obj, type):
        return False

    if not issubclass(obj, v1.bond.Bond):
        return False

    if not issubclass(obj.PROVIDER, v1.provider.Provider):
        return False

    return issubclass(obj.IMPLEMENTS, v1.bond.Interface)


def _is_context(obj: type) -> bool:
    """TODO"""

    if not isinstance(obj, type):
        return False

    return issubclass(obj, v1.deployment.Context)


_REPOSITORY_SCHEMA = v1.schema.Schema({
    v1.schema.Optional("v1"): v1.schema.Schema({
        v1.schema.Optional("contexts"): [
            _is_context
        ],
        v1.schema.Optional("components"): [
            _is_component
        ],
        v1.schema.Optional("links"): [
            _is_link
        ],
        v1.schema.Optional("providers"): [
            _is_provider
        ],
        v1.schema.Optional("bonds"): [
            _is_bond
        ]
    })
}, ignore_extra_keys=True)

_DEFAULT_REPOSITORY = {
    "v1": {
        "contexts": {
            v1.utils.fqcn(defaults.V1LocalContext): defaults.V1LocalContext
        },
        "components": {},
        "links": {
            v1.utils.fqcn(defaults.V1DependencyLink): defaults.V1DependencyLink
        },
        "providers": {},
        "bonds": {}
    }
}


class Repository:
    """TODO"""

    def __init__(self, repo: dict[str, object]):
        self._repo = repo

    def contexts(self) -> dict[str, object]:
        """TODO"""

        return self._repo["v1"]["contexts"]

    def components(self) -> dict[str, object]:
        """TODO"""

        return self._repo["v1"]["components"]

    def links(self) -> dict[str, object]:
        """TODO"""

        return self._repo["v1"]["links"]

    def providers(self) -> dict[str, object]:
        """TODO"""

        return self._repo["v1"]["providers"]

    def bonds(self) -> dict[str, object]:
        """TODO"""

        return self._repo["v1"]["bonds"]

    def context(self, name: str) -> v1.deployment.Context:
        """TODO"""

        contexts = self.contexts()

        if name not in contexts:
            raise exceptions.ContextNotFound(name)

        return contexts[name]

    def component(self, name: str) -> v1.component.Component:
        """TODO"""

        components = self.components()

        if name not in components:
            raise exceptions.ComponentTypeNotFound(name)

        return components[name]

    def link(self, name: str) -> v1.link.Link:
        """TODO"""

        links = self.links()

        if name not in links:
            raise exceptions.LinkTypeNotFound(name)

        return links[name]

    def provider(self, name: str) -> v1.provider.Provider:
        """TODO"""

        providers = self.providers()

        if name not in providers:
            raise exceptions.ProviderNotFound(name)

        return providers[name]

    def bond(self, name: str) -> v1.bond.Bond:
        """TODO"""

        bonds = self.bonds()

        if name not in bonds:
            raise exceptions.BondNotFound(name)

        return bonds[name]


def _system_repository() -> list:
    """TODO"""

    entry_points = importlib.metadata.entry_points()

    if "torque" in entry_points:
        return list(entry_points["torque"])

    return []


def _local_repository() -> list:
    """TODO"""

    try:
        importlib.import_module("local")

        return [
            importlib.metadata.EntryPoint(name="local",
                                          value="local:repository",
                                          group="torque")
        ]

    except ModuleNotFoundError:
        return []


def _process_items(repository: dict[str, object], name: str) -> dict[str, object]:
    """TODO"""

    if name not in repository["v1"]:
        return repository

    repository["v1"][name] = {
        v1.utils.fqcn(item): item
        for item in repository["v1"][name]
    }

    return repository


def load() -> Repository:
    """TODO"""

    repository = {} | _DEFAULT_REPOSITORY

    entry_points = _system_repository()
    entry_points += _local_repository()

    for entry_point in entry_points:
        # pylint: disable=W0703

        try:
            package_repository = entry_point.load()
            package_repository = _REPOSITORY_SCHEMA.validate(package_repository)

            package_repository = _process_items(package_repository, "contexts")
            package_repository = _process_items(package_repository, "components")
            package_repository = _process_items(package_repository, "links")
            package_repository = _process_items(package_repository, "providers")
            package_repository = _process_items(package_repository, "bonds")

            repository = v1.utils.merge_dicts(repository, package_repository)

        except v1.schema.SchemaError as exc:
            exc_str = str(exc)
            exc_str = " " + exc_str.replace("\n", "\n ")

            print(f"WARNING: {entry_point.name}: unable to load repository:\n{exc_str}")

        except Exception as exc:
            traceback.print_exc()

            print(f"WARNING: {entry_point.name}: unable to load repository: {exc}", file=sys.stderr)

    return Repository(repository)
