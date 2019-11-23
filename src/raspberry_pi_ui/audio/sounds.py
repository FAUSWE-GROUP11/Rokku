import subprocess

def play_notification_sound(duration: int, logger):
    """
    Plays a sound from a .wav file within sounds.
    
    :param duration: Allows you to shorten a sound from its original length. If it is bigger than
    length of audio time the process will finish when the audio file is done playing.

    :param logger: Logs when an audio message is played.
    """
    
    dur_param = "-d" + str(duration) 
    play = subprocess.run(['aplay', '-q', dur_param, 'notify.wav'], check=True)
    logger.info(f"Notification sound: {play}")