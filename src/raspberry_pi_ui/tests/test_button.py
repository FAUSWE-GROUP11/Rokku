import json
from time import sleep


def empty_queues(out_msg_q, in_msg_q):
    """
    Utility function for these tests to make sure message queues are
    empty before test begins
    """
    while not out_msg_q.empty():
        out_msg_q.get()
    while not in_msg_q.empty():
        in_msg_q.get()


def test_button_publish(mqtt_out, button):
    """Test message sent from in to out."""
    out_pub, out_msg_q, out_listen_proc = mqtt_out
    empty_queues(out_msg_q, button.msg_q)
    button.pub.publish(json.dumps(["test_4", True]))
    while out_msg_q.empty():
        sleep(1)
    out_received_msg = out_msg_q.get()
    out_received_list = json.loads(out_received_msg)
    assert out_received_list[0] == "test_4" and out_received_list[1]


def test_button_set_color(button):
    """Test button base class's set_color method"""
    button.set_color("pink")
    assert button._color == "pink"


def test_button_get_color(button):
    """Test button base class's get_color method"""
    button._color = "pink"
    assert button.get_color() == "pink"


def test_button_set_get_label(button):
    """Test button base class's set_label and ge_label methods"""
    button.set_label("testing")
    assert button.get_label() == "testing"
