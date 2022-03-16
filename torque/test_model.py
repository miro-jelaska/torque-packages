# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""TODO"""

from torque import exceptions
from torque import model


def _has_cycles(dag: model.DAG) -> bool:
    """TODO"""

    try:
        dag.verify()
        return False

    except exceptions.CycleDetected:
        pass

    return True


def test_test1():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")
    dag.create_group("group2")
    dag.create_group("group3")

    dag.create_component("component1", "group1", "component_type", None)
    dag.create_component("component2", "group1", "component_type", None)
    dag.create_component("component3", "group1", "component_type", None)
    dag.create_component("component4", "group1", "component_type", None)

    dag.create_link("link1", "component1", "component2", "link_type", None)
    dag.create_link("link2", "component1", "component3", "link_type", None)
    dag.create_link("link3", "component2", "component3", "link_type", None)
    dag.create_link("link4", "component3", "component4", "link_type", None)

    assert _has_cycles(dag) is False

    dag.create_link("link5", "component4", "component2", "link_type", None)

    assert _has_cycles(dag) is True

    dag.create_link("link6", "component4", "component1", "link_type", None)

    assert _has_cycles(dag) is True


def test_test2():
    """TODO"""

    dag = model.DAG(0)

    try:
        dag.create_group("group1")
        dag.create_group("group1")

        assert False

    except exceptions.GroupExists:
        pass


def test_test3():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    try:
        dag.create_component("component1", "group1", "component_type", None)
        dag.create_component("component1", "group1", "component_type", None)

        assert False

    except exceptions.ComponentExists:
        pass


def test_test4():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)
    dag.create_component("component2", "group1", "component_type", None)

    try:
        dag.create_link("link1", "component1", "component2", "link_type", None)
        dag.create_link("link1", "component1", "component2", "link_type", None)

        assert False

    except exceptions.LinkExists:
        pass


def test_test5():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)
    dag.create_component("component2", "group1", "component_type", None)

    try:
        dag.create_component("component4", "group2", "component_type", None)

        assert False

    except exceptions.GroupNotFound:
        pass


def test_test6():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)

    try:
        dag.create_link("link1", "_component", "component1", "link_type", None)

        assert False

    except exceptions.ComponentNotFound:
        pass


def test_test7():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)

    try:
        dag.create_link("link1", "component1", "_component", "link_type", None)

        assert False

    except exceptions.ComponentNotFound:
        pass


def test_test8():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)

    try:
        dag.create_link("link1", "component1", "component1", "link_type", None)

        assert False

    except exceptions.CycleDetected:
        pass


def test_test9():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)
    dag.create_component("component2", "group1", "component_type", None)

    try:
        dag.create_link("link1", "component1", "component2", "link_type", None)
        dag.create_link("link2", "component1", "component2", "link_type", None)

        assert False

    except exceptions.ComponentsAlreadyConnected:
        pass


def test_test10():
    """TODO"""

    dag = model.DAG(0)

    assert not _has_cycles(dag)


def test_test11():
    """TODO"""

    dag = model.DAG(0)

    dag.create_group("group1")

    dag.create_component("component1", "group1", "component_type", None)
    dag.create_component("component2", "group1", "component_type", None)
    dag.create_component("component3", "group1", "component_type", None)

    dag.create_link("link1", "component1", "component2", "link_type", None)
    dag.create_link("link2", "component2", "component1", "link_type", None)

    assert _has_cycles(dag)
