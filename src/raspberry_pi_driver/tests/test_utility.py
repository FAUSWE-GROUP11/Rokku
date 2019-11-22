import shlex
import subprocess
from multiprocessing import Process
from time import sleep

from src.raspberry_pi_driver.utility import (
    hash_prefix,
    terminate_cmd,
    terminate_proc,
)


def test_hash_prefix():
    res = hash_prefix("rokku")
    expected = (
        "320bda34a3c7f8dc49e5c976792f20ef5ec6f400b970138393020709bc2c1bc1"
    )
    assert res == expected


def test_terminate_proc(logger):
    def test_fun():
        while True:
            sleep(1)

    test_proc = Process(target=test_fun, name="Test Fun", args=())
    test_proc.start()
    terminate_proc(test_proc, logger)
    assert not test_proc.is_alive()


def test_terminate_cmd(logger):
    test_cmd = subprocess.Popen(shlex.split("sleep 10"))
    terminate_cmd(test_cmd, "Test CMD", logger)
    assert test_cmd.poll() is not None
