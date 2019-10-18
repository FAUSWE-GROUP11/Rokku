# RPi-to-RPi Communication
## Introduction
There are various ways to achieve communication between two RPis, such as setting one RPi as an access point and have the other connect to it. However, after googling all these methods, we have found that they are not particularly suitable for our needs. In particular, our RPi, `rpi_in` and `rpi_out`, are connected to a network that most likely forbids any device from setting up an access point. Furthermore, our implementation cannot allow ethernet cable connection between the two RPi. Given that both our RPi are connected to the internet, a logical solution is to send message from one RPi to the other via the internet. One way to do so is to use the MQTT messaging protocol, which is designed for communication among IoT devices. Luckily, there happens to be a Python library already available for this usage: `paho-mqtt` ([documentation](https://pypi.org/project/paho-mqtt/)). Thus, our implementation of RPi-to-RPi communication is through MQTT via that `paho-mqtt` library.

## Usage
The following sample code (also found in `tests/communication_sample.py`) shows a scenario where a macbook instantiates one publisher and one subscriber, both on different topics: publishing to `Rokku/mac_to_rpi` but subscribing to `Rokku/rpi_to_mac`.

If a RPi uses the same code but swaps the topics: publishing to `Rokku/rpi_to_mac` but subscribing to `Rokku/mac_to_rpi`, the macbook can receive the message published by the RPi, and vice versa. In other words, the two devices can talk to each other.

```python
# Instantiate publisher, specify which topic to publish to.
# This publisher can ONLY publish to the topic given at instantiation.
pub = publisher.Publisher(topic="Rokku/mac_to_rpi")

# Instantiate subscriber, specify which topic to subscribe to.
# This subscriber can ONLY subscribe to the topic given at instantiation.
sub = subscriber.Subscriber(q, topic="Rokku/rpi_to_mac")

# Have sub listen on the topic in a separate process
# because listening has to happen all the time. Use
# a queue to bridge the child and parent processes
q = Queue()
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
```

## Testing
Testing of our implementation of RPi-to-RPi communication has been conducted successfully between macbook and RPi, as well as between RPi and RPi (all RPi are running Raspbian Buster, kernel version 4.19)