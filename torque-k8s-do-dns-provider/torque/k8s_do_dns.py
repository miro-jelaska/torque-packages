# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""DOCSTRING"""

import base64
import jinja2
import yaml

from torque import do
from torque import k8s
from torque import k8s_load_balancer
from torque import v1


_EXTERNAL_DNS = jinja2.Template("""apiVersion: v1
kind: Namespace
metadata:
  name: external-dns
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-dns
  namespace: external-dns
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: external-dns
  namespace: external-dns
rules:
- apiGroups:
  - ''
  resources:
  - services
  - endpoints
  - pods
  verbs:
  - get
  - watch
  - list
- apiGroups:
  - extensions
  - networking.k8s.io
  resources:
  - ingresses
  verbs:
  - get
  - watch
  - list
- apiGroups:
  - ''
  resources:
  - nodes
  verbs:
  - get
  - watch
  - list
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: external-dns-viewer
  namespace: external-dns
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: external-dns
subjects:
- kind: ServiceAccount
  name: external-dns
  namespace: external-dns
---
apiVersion: v1
kind: Secret
metadata:
  name: do-auth
  namespace: external-dns
type: Opaque
data:
  token: {{token}}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
  namespace: external-dns
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: external-dns
  template:
    metadata:
      labels:
        app: external-dns
    spec:
      serviceAccountName: external-dns
      containers:
      - name: external-dns
        image: k8s.gcr.io/external-dns/external-dns:v0.12.2
        args:
        - --source=service
        - --provider=digitalocean
        env:
        - name: DO_TOKEN
          valueFrom:
            secretKeyRef:
              name: do-auth
              key: token
              optional: false
""")


class V1Provider(v1.provider.Provider):
    """DOCSTRING"""

    @classmethod
    def on_requirements(cls) -> dict[str, object]:
        """DOCSTRING"""

        return {
            "do": {
                "interface": do.V1Provider,
                "required": True
            },
            "k8s": {
                "interface": k8s.V1Provider,
                "required": True
            },
            "lb": {
                "interface": k8s_load_balancer.V1Provider,
                "required": True
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.interfaces.k8s as p:
            p.add_hook("apply-utils", self._apply)

    def _apply(self):
        """DOCSTRING"""

        token = self.interfaces.do.token()

        token = token.encode()
        token = base64.b64encode(token)
        token = token.decode()

        objs = _EXTERNAL_DNS.render(token=token)

        for obj in objs.split("---"):
            self.interfaces.k8s.add_object(yaml.safe_load(obj))

        for entry in self.interfaces.lb.get_entries():
            hosts = sorted([f"{host}.{entry.domain}." for host in entry.hosts])
            hosts = ",".join(hosts)

            service_obj = self.interfaces.k8s.object(entry.service)

            service_obj["metadata"]["annotations"].update({
                "external-dns.alpha.kubernetes.io/hostname": hosts
            })


repository = {
    "v1": {
        "providers": [
            V1Provider
        ]
    }
}
