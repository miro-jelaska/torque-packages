# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

import functools
import os
import subprocess
import threading

from torque import v1


class ClientInterface(v1.bond.Interface):
    """TODO"""

    def prefix(self) -> str:
        """TODO"""

    def auth(self) -> dict[str, dict]:
        """TODO"""


class Provider(v1.provider.Provider):
    """TODO"""

    _CONFIGURATION = {
        "defaults": {},
        "schema": {
            v1.schema.Optional("prefix"): str
        }
    }

    @classmethod
    def on_requirements(cls) -> dict[str, object]:
        """TODO"""

        return {
            "client": {
                "interface": ClientInterface,
                "required": True
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._images = {}
        self._auth = None
        self._prefix = None
        self._lock = threading.Lock()

        with self.context as ctx:
            ctx.add_hook("apply", self._apply)

    def _connect(self):
        """TODO"""

        self._auth = self.interfaces.client.auth()
        self._prefix = self.interfaces.client.prefix()

    def _login(self):
        """TODO"""

        cmd = [
            "docker", "login",
            "--username", self._auth["username"],
            "--password-stdin",
            self._auth["server"]
        ]

        print(f"+ {' '.join(cmd)}")
        subprocess.run(cmd,
                       env=os.environ,
                       cwd=self.context.path(),
                       input=bytes(self._auth["password"], encoding="utf-8"),
                       check=True)

    def _push(self):
        """TODO"""

        for image, tag in self._images.items():
            tag = v1.utils.resolve_futures(tag)

            cmd = [
                "docker", "tag",
                image, tag
            ]

            print(f"+ {' '.join(cmd)}")
            subprocess.run(cmd,
                           env=os.environ,
                           cwd=self.context.path(),
                           check=True)

            cmd = [
                "docker", "push",
                tag
            ]

            print(f"+ {' '.join(cmd)}")
            subprocess.run(cmd,
                           env=os.environ,
                           cwd=self.context.path(),
                           check=True)

    def _apply(self):
        """TODO"""

        self._connect()

        self._login()
        self._push()

    def _resolve_tag(self, image: str) -> str:
        """TODO"""

        el = filter(lambda x: x != "", [self._auth["server"],
                                        self._prefix,
                                        self.configuration.get("prefix", ""),
                                        image])
        tag = "/".join(el)

        return tag

    def push(self, image: str) -> v1.utils.Future[str]:
        """TODO"""

        with self._lock:
            if image in self._images:
                raise v1.exceptions.RuntimeError(f"{image}: already exists")

            future = v1.utils.Future(functools.partial(self._resolve_tag, image))
            self._images[image] = future

            return future


class ImageInterface(v1.bond.Interface):
    """TODO"""

    def push(self, image: str) -> v1.utils.Future[str]:
        """TODO"""


class Image(v1.bond.Bond):
    """TODO"""

    PROVIDER = Provider
    IMPLEMENTS = ImageInterface

    @classmethod
    def on_requirements(cls) -> dict[str, object]:
        """TODO"""

        return {
            "cr": {
                "interface": Provider,
                "required": True
            }
        }

    def push(self, image: str) -> v1.utils.Future[str]:
        """TODO"""

        return self.interfaces.cr.push(image)


repository = {
    "v1": {
        "providers": [
            Provider
        ],
        "bonds": [
            Image
        ]
    }
}