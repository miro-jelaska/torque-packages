# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

from torque import v1

from demo import interfaces
from demo import types
from demo import utils


class Component(v1.component.Component):
    """TODO"""

    _PARAMETERS = {
        "defaults": {},
        "schema": {}
    }

    _CONFIGURATION = {
        "defaults": {
            "version": "14.2",
            "password": None
        },
        "schema": {
            "version": str,
            "password": str
        }
    }

    @classmethod
    def on_parameters(cls, parameters: object) -> object:
        """TODO"""

        return v1.utils.validate_schema(cls._PARAMETERS["schema"],
                                        cls._PARAMETERS["defaults"],
                                        parameters)

    @classmethod
    def on_configuration(cls, configuration: object) -> object:
        """TODO"""

        defaults = v1.utils.merge_dicts(cls._CONFIGURATION["defaults"], {
            "password": utils.generate_password()
        })

        return v1.utils.validate_schema(cls._CONFIGURATION["schema"],
                                        defaults,
                                        configuration)

    @classmethod
    def on_requirements(cls) -> [v1.provider.Interface]:
        """TODO"""

        return [
            v1.utils.InterfaceRequirement(interfaces.SecretsInterface, "provider", "secrets"),
            v1.utils.InterfaceRequirement(interfaces.ServicesInterface, "provider", "services"),
            v1.utils.InterfaceRequirement(interfaces.DeploymentsInterface, "provider", "deployments")
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._volume_links = []

        self._service_link = None
        self._secret_link = None

    def _image(self) -> str:
        return f"postgres:{self.configuration['version']}"

    def _add_volume_link(self, name: str, mount_path: str, link: v1.utils.Future[object]):
        """TODO"""

        link = types.VolumeLink(name, mount_path, link)
        self._volume_links.append(link)

    def _link(self) -> v1.utils.Future[object]:
        """TODO"""

        return self._service_link

    def _admin(self) -> v1.utils.Future[object]:
        """TODO"""

        return self._secret_link

    def _pg_data(self) -> str:
        """TODO"""

        return "/data"

    def on_interfaces(self) -> [v1.component.Interface]:
        """TODO"""

        return [
            interfaces.VolumeLink(add=self._add_volume_link),
            interfaces.PostgresService(link=self._link,
                                       admin=self._admin,
                                       pg_data=self._pg_data)
        ]

    def on_create(self):
        """TODO"""

    def on_remove(self):
        """TODO"""

    def on_build(self, deployment: v1.deployment.Deployment):
        """TODO"""

    def on_apply(self, deployment: v1.deployment.Deployment):
        """TODO"""

        self._secret_link = self.interfaces.secrets.create(f"{self.name}_admin", [
            types.KeyValue("user", "postgres"),
            types.KeyValue("password", self.configuration["password"])
        ])

        self._service_link = self.interfaces.services.create(self.name, [5432], None)

        env = [
            types.KeyValue("PGDATA", "/data")
        ]

        secret_links = [
            types.SecretLink("POSTGRES_PASSWORD", "password", self._secret_link)
        ]

        self.interfaces.deployments.create(self.name,
                                           self._image(),
                                           None,
                                           None,
                                           None,
                                           env,
                                           None,
                                           self._volume_links,
                                           secret_links,
                                           1)
