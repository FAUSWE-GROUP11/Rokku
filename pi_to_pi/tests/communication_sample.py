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

# Instantiate publisher
pub = publisher.Publisher(topic="Rokku/mac_to_rpi")

# Instantiate subscriber
q = Queue()
sub = subscriber.Subscriber(q, topic="Rokku/rpi_to_mac")
# listen in a separate process
child_proc = Process(target=sub.start_listen, args=())
child_proc.start()


counter = 0
# main loop
while counter <= 10:
    if not q.empty():
        print(q.get())
    else:
        pub.publish(f"hello from macbook {counter}")
        sleep(2)
        counter += 1
