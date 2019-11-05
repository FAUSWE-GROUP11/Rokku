from src.raspberry_pi_ui.rokku import Main
from rpi_out_driver import set_up_pub_sub as sups_out
from rpi_in_driver import set_up_pub_sub as sups_in
import json
from time import sleep
import pytest


@pytest.fixture(scope="module")
def mqtt_out():
    # set up mqtt components of rpi_out
    mqtt_out = sups_out()
    yield mqtt_out
    print("tear down mqtt_out")
    _, _, out_listen_proc = mqtt_out
    out_listen_proc.terminate()
    while out_listen_proc.is_alive():
        sleep(1)
    out_listen_proc.join()


@pytest.fixture(scope="module")
def ui():
    # set up ui
    in_pub, in_msg_q, in_listen_proc = sups_in()
    ui = Main(in_pub, in_msg_q)
    yield ui
    print("tear down ui")
    ui.close_application("", "")
    in_listen_proc.terminate()
    while in_listen_proc.is_alive():
        sleep(1)
    in_listen_proc.join()


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
