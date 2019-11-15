import argparse
from hashlib import blake2b
from time import sleep
from typing import Any, List


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
        help="""Provide a public id for Rokku's MQTT topic.
        This id must be the same for both rpi_in_driver and rpi_out_driver""",
    )
    parser.add_argument(
        "--intercom-pwd",
        dest="intercom_pwd",
        required=False,
        default="",
        help="""Password for Mumble server. If not specified,
        intercom will not be functional.""",
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


def terminate_proc(proc) -> None:
    """Nicely terminate the given process.

    :param proc:   The object representing the process to be terminated

    :returns:   None
    """
    proc.terminate()
    while proc.is_alive():
        sleep(1)
    proc.join()


def terminate_cmd(cmd_proc) -> None:
    """Nicely terminate the given command process (from subprocess.run).

    :param cmd_proc:    The object representing the command process to be
                        terminated

    :returns:   None
    """
    cmd_proc.kill()
    while cmd_proc.poll() is None:
        sleep(1)
    cmd_proc.wait()


def clean_up(logger, processes: List[Any], cmds: List[Any]) -> None:
    """Clean up any running process in the system.

    :param logger:      Enable logging from the caller
    :param processes:   A list of processes to be terminated. Each list element
                        is a process object.
    :param cmds:        A list of command line processes to be killed. Each
                        list element is a tuple (cmd_proc, cmd_name).

    :return:    None
    """
    for proc in processes:
        logger.info(f"Terminating {proc.name}...")
        terminate_proc(proc)
        logger.info(f"{proc.name} terminated successfully!")
    for cmd_proc, cmd_name in cmds:
        logger.info(f"Terminating {cmd_name}...")
        terminate_cmd(cmd_proc)
        logger.info(f"{cmd_name} terminated successfully!")
