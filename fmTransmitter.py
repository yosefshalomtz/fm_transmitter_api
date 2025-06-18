import subprocess
import threading
import time
import shutil

class FmTransmitter:
    def __init__(self):
        # status: stopped, playing
        self.status = "stopped"
        self.frequency = "88.0"  # default frequency
        self.file = "./wav_files/block.wav" # default file
        self.process = None
        threading.Thread(target=self.check_process, daemon=True).start()

    def check_process(self):
        while True:
            # check if self.process is process object and if it is running
            if (self.process is not None) and (self.process.poll() is None):
                self.status = "playing"
            else:
                self.status = "stopped"

    def exists_executable(self):
        """Check if the fm_transmitter executable exists in the system path."""
        try:
            subprocess.run(["fm_transmitter", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def play(self):
        """Start the fm_transmitter process with the specified frequency and file."""
        self.process = subprocess.Popen(['sudo', shutil.which("fm_transmitter"), '-f', str(self.frequency), self.file, '-r'],
            stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


    def stop(self):
        if self.status == "playing":
            subprocess.run(["sudo", "pkill", '-f', 'fm_transmitter'],
                stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
