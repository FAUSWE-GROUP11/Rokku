import json
from time import sleep

import pytest

from src.pi_to_pi.utility import set_up_pub_sub
from src.raspberry_pi_driver.utility import hash_prefix, terminate_proc
from src.raspberry_pi_ui.rokku import Main


# For more info about pytest.fixture, read
# http://doc.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
# and https://pybit.es/pytest-fixtures.html
@pytest.fixture(scope="module")
def mqtt_out():
    # set up mqtt components of rpi_out
    mqtt_out = set_up_pub_sub(
        hash_prefix("Rokku/test_topic"), "out_to_in", "in_to_out"
    )
    yield mqtt_out
    print("tear down mqtt_out")
    _, _, out_listen_proc = mqtt_out
    terminate_proc(out_listen_proc)


@pytest.fixture(scope="module")
def ui():
    # set up ui
    in_pub, in_msg_q, in_listen_proc = set_up_pub_sub(
        hash_prefix("Rokku/test_topic"), "in_to_out", "out_to_in"
    )
    ui = Main(in_pub, in_msg_q)
    yield ui
    print("tear down ui")
    ui.close_application("", "")
    terminate_proc(in_listen_proc)


def empty_queues(out_msg_q, in_msg_q):
    """
    Utility function for these tests to make sure message queues are
    empty before test begins
    """
    while not out_msg_q.empty():
        out_msg_q.get()
    while not in_msg_q.empty():
        in_msg_q.get()


def test_in_to_out(mqtt_out, ui):
    """ Test message sent from in to out """
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, ui.msg_q)
    ui.pub.publish(json.dumps(["test_id", True]))
    while out_msg_q.empty():
        sleep(1)
    out_received_msg = out_msg_q.get()
    out_received_list = json.loads(out_received_msg)
    assert out_received_list[0] == "test_id" and out_received_list[1]


def test_wait_msg_normal(mqtt_out, ui):
    """ Essentially, we are testing message sent from out to in """
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, ui.msg_q)
    out_pub.publish(json.dumps(["test_id", True]))
    in_received_list = ui._wait_msg("test_id")
    assert in_received_list[0] == "test_id" and in_received_list[1]


def test_wait_msg_timeout(mqtt_out, ui):
    """ Test timeout functionality of _wait_msg() """
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, ui.msg_q)
    in_received_list = ui._wait_msg("test_id", timeout=1)
    sleep(2)
    assert in_received_list == []


def test_wait_msg_wrong_id(mqtt_out, ui):
    """
    Test situation where the message id sent from out is not the one
    currently being expected from in. We should not receive anything and the
    in_msg_q should still contain the unmatched message
    """
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, ui.msg_q)
    sent_list = ["foo", True]
    out_pub.publish(json.dumps(sent_list))
    in_received_list = ui._wait_msg("bar", timeout=1)
    sleep(2)
    remain_list = json.loads(ui.msg_q.get())
    assert in_received_list == [] and sent_list == remain_list
