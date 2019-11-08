import json
import os
import re
from multiprocessing import Process, Queue
from time import sleep

from .. import publisher, subscriber


def test_pub_sub():
    q = Queue()
    # subscriber
    sub = subscriber.Subscriber(q)
    # Run the listening function of subscriber in a child process
    # Use a queue to transfer data from child process to parent
    child_proc = Process(target=sub.start_listen, args=())
    child_proc.start()

    # publisher
    pub = publisher.Publisher()
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
    log_name = f"{os.path.dirname(__file__)}/../../../rokku.log"
    try:
        os.remove(log_name)  # remove any old logs
    except Exception:
        pass
    test_pub_sub()  # this produces a new log
    with open(log_name, "r") as f_obj:
        data = f_obj.read()
    num_success = len(re.findall(r"successful", data))  # should be 2
    num_closed = len(re.findall(r"closed", data))  # should be 2
    num_msg = len(re.findall(r"{\"intercom\": 1}", data))  # should be 2
    # Test
    assert sum([num_success, num_closed, num_msg]) == 6
    # clean up
    os.remove(log_name)
