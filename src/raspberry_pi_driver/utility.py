import argparse
from hashlib import blake2b
from time import sleep


def command_line_parser(prog_name: str):
    """
    Parse command line arguments for rpi_in_driver and rpi_out_driver

    Args:
        prog_name:  Name of the program using this command line parser
    Return:
        A namespace containing all command line arguments.
    Raises:
        None
    """
    parser = argparse.ArgumentParser(prog=prog_name)
    parser.add_argument(
        "-p",
        dest="public_id",
        required=True,
        help="Provide a public id for Rokku's MQTT topic. This id must be the same for both rpi_in_driver and rpi_out_driver",
    )
    args = parser.parse_args()
    return args


def hash_prefix(public_id: str) -> str:
    """
    Produce a hash for public_id, with salt included, to serve as a prefix for
    MQTT topic.

    Args:
        public_id:  A string supplied by the user when initializing
                    rpi_in_driver and rpi_out_driver
    Returns:
        64-bit hashed version of public_id + salt. This string should be the
        prefix for the MQTT topic
    Raises:
        None
    """
    SALT = "sYEuhMrWC6".encode("utf-8")  # This salt MUST NOT change!
    h_addr = blake2b(digest_size=32, salt=SALT)
    h_addr.update(public_id.encode("utf-8"))
    return h_addr.hexdigest()


def terminate_proc(proc):
    """
    Nicely terminate the given process

    Args:
        proc:   The object representing the process to be terminated
    Returns:
        None
    Rasies:
        None
    """
    proc.terminate()
    while proc.is_alive():
        sleep(1)
    proc.join()
