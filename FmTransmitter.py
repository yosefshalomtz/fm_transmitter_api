import subprocess

class FmTransmitter:
    def __init__(self):
        # status: stopped, playing, error
        self.status = "stopped"
        self.frequency = ""
        self.file = ""
        pass

    def exsists_executable():
        """Check if the fm_transmitter executable exists in the system path."""
        try:
            subprocess.run(["fm_transmitter", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def play(self):
        pass

    def stop(self):
        pass
