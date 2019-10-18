from .. import publisher, subscriber
import json
from time import sleep
from multiprocessing import Process, Queue
import re
import os


def test_pub_sub():
    q = Queue()
    # subscriber
    sub = subscriber.Subscriber("sub_test", q)
    # Run the listening function of subscriber in a child process
    # Use a queue to transfer data from child process to parent
    child_proc = Process(target=sub.start_listen, args=())
    child_proc.start()

    # publisher
    pub = publisher.Publisher("pub_test")
    pub.publish(json.dumps({"intercom": 1}))  # publish a dict

    # wait for subscriber to receive the msg
    while q.empty():
        sleep(1)
    # kill child process
    child_proc.terminate()
    child_proc.join()
    # End pub and sub
    sub.close()
    pub.close()
    # Test
    assert json.loads(q.get())["intercom"] == 1


def test_logger():
    os.remove("mqtt.log")  # remove any old logs
    test_pub_sub()  # this produces a new log
    with open("mqtt.log", "r") as f_obj:
        data = f_obj.read()
    num_success = len(re.findall(r"successful", data))  # should be 2
    num_closed = len(re.findall(r"closed", data))  # should be 2
    num_msg = len(re.findall(r"{\"intercom\": 1}", data))  # should be 2
    # Test
    assert sum([num_success, num_closed, num_msg]) == 6
    # clean up
    os.remove("mqtt.log")
