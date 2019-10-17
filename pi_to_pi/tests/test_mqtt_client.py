from .. import publisher, subscriber
import json
from time import sleep
from multiprocessing import Process, Queue


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
    pub.publish(json.dumps({"intercom": "ON"}))  # publish a dict

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
    assert json.loads(q.get())["intercom"] == "ON"
