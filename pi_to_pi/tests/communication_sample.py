import os
import sys

# add parent dir to sys path such that we can import modules from parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import publisher
import subscriber
from time import sleep
from multiprocessing import Process, Queue

"""
This code serves as an example for communication between two devices via mqtt.
This file is NOT supposed to be tested by `pytest`
"""

# For testing purpose only
try:
    os.remove("mqtt.log")
except Exception:
    pass

# Instantiate publisher, specify which topic to publish to.
# This publisher can ONLY publish to the topic given at instantiation.
pub = publisher.Publisher(topic="Rokku/mac_to_rpi")


q = Queue()
# Instantiate subscriber, specify which topic to subscribe to.
# This subscriber can ONLY subscribe to the topic given at instantiation.
sub = subscriber.Subscriber(q, topic="Rokku/rpi_to_mac")
# listen in a separate process
child_proc = Process(target=sub.start_listen, args=())
child_proc.start()


counter = 0
# main loop to publish 5 messages while also printing out any messages received
while counter <= 10:
    if not q.empty():
        print(q.get())  # message received is retrieved from the queue
    else:
        pub.publish(f"hello from macbook {counter}")
        sleep(2)
        counter += 1

# gracefully end all processes
child_proc.terminate()
child_proc.join()
sub.close()
pub.close()
