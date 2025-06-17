import subprocess
import threading

class FmTransmitter:
    def __init__(self):
        # status: stopped, playing, error
        self.status = "stopped"
        self.frequency = ""
        self.file = ""
        self.process = None
        pass

    def exsists_executable():
        """Check if the fm_transmitter executable exists in the system path."""
        try:
            subprocess.run(["fm_transmitter", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def play(self):
        """Start the fm_transmitter process with the specified frequency and file."""
        try:
            self.process = subprocess.Popen(['sudo', 'fm_transmitter', '-f', self.frequency, self.file, '-r'], 
                                            stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            self.status = "playing"
            # set thread for: on self.process exit, set status to stopped
            threading.Thread()#...
                
        except Exception as e:
            self.status = "error"
            raise e


    def stop(self):
        pass
