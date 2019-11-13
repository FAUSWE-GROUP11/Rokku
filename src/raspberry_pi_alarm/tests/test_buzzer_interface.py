import sys
import fake_rpi
sys.modules["RPi"] = fake_rpi.RPi
sys.modules["RPi.GPIO"] = fake_rpi.RPi.GPIO

from .. import buzzer_interface

alarm = buzzer_interface.Buzzer(24)

class TestBuzzer:
    def test_init(self):
        assert alarm.channel == 24

    def test_init(self):
        assert alarm.state is False
    
    def test_sound(self):
        alarm.sound()
        assert alarm.state is True
    
    def test_scilence(self):
        alarm.silence()
        assert alarm.state is False

    def test_get_state(self):
        alarm.get_state()
        assert alarm.get_state() is False

    def test_get_state2(self):
        alarm.sound()
        assert alarm.get_state() is True

    def test_get_state3(self):
        alarm.silence()
        assert alarm.get_state() is False