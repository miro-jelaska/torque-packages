# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

import argparse
import os
import sys
import traceback

from torque import commands


def main() -> int:
    """TODO"""

    verbose = os.getenv("VERBOSE") is not None

    # pylint: disable=W0703
    try:
        parser = argparse.ArgumentParser(prog="torque", description="torque command line interface.")
        subparsers = parser.add_subparsers(required=True, dest="main_cmd", metavar="command")

        parser.add_argument("--workspace",
                            default=".torque/workspace.yaml",
                            metavar="PATH",
                            help="workspace file to use")

        cmds = {
            "init": commands.init,
            "package": commands.package,
            "profile": commands.profile,
            "group": commands.group,
            "component": commands.component,
            "link": commands.link,
            "deployment": commands.deployment
        }

        for cmd in cmds.values():
            cmd.add_arguments(subparsers)

        args = parser.parse_args()

        cmds[args.main_cmd].run(args)

        return 0

    except Exception as exc:
        if verbose:
            traceback.print_exc()

        else:
            print(exc)

    return 1


if __name__ == "__main__":
    sys.exit(main())
