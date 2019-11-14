import json
from time import sleep

from src.raspberry_pi_ui.utility import set_button_property, wait_msg


def empty_queues(out_msg_q, in_msg_q):
    """
    Utility function for these tests to make sure message queues are
    empty before test begins
    """
    while not out_msg_q.empty():
        out_msg_q.get()
    while not in_msg_q.empty():
        in_msg_q.get()


def test_wait_msg_normal(mqtt_out, button, logger):
    """Essentially, we are testing message sent from out to in."""
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, button.msg_q)
    out_pub.publish(json.dumps(["test_1", True]))
    in_received_list = wait_msg("test_1", logger, button.msg_q)
    assert in_received_list[0] == "test_1" and in_received_list[1]


def test_wait_msg_timeout(mqtt_out, button, logger):
    """Test timeout functionality of wait_msg()."""
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, button.msg_q)
    in_received_list = wait_msg("test_2", logger, button.msg_q, timeout=1)
    sleep(2)
    assert in_received_list == []


def test_wait_msg_wrong_id(mqtt_out, button, logger):
    """
    Test situation where the message id sent from out is not the one
    currently being expected from in. We should not receive anything and the
    in_msg_q should still contain the unmatched message
    """
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, button.msg_q)
    sent_list = ["foo", True]
    out_pub.publish(json.dumps(sent_list))
    in_received_list = wait_msg("test_3", logger, button.msg_q, timeout=1)
    sleep(2)
    remain_list = json.loads(button.msg_q.get())
    assert in_received_list == [] and sent_list == remain_list


def test_set_button_color(button):
    """Test whether button color can be properly set."""
    set_button_property(button, "red", "")
    assert button.get_color() == "red"


def test_set_button_label(button):
    """Test whether button label can be properly set."""
    set_button_property(button, "red", "test_button")
    assert button.get_label() == "test_button"
