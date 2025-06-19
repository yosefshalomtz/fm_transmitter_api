# FM Transmitter API (for Raspberry Pi Zero W)

This project provides a REST API and web interface to control an FM transmitter using a Raspberry Pi Zero W. It wraps the `fm_transmitter` command-line tool, allowing you to broadcast a WAV file at a specified FM frequency.

## Features
- REST API to start/stop FM transmission and check status
- Web interface for easy control
- Designed for use with the `fm_transmitter` executable

## Requirements
- Raspberry Pi Zero W (or compatible Linux system)
- `fm_transmitter` executable installed and available in PATH
- Python 3, Flask
- `sudo` access (for running the transmitter)

## Setup
1. **Install dependencies:**
   ```bash
   pip install flask
   ```
2. **Install `fm_transmitter`:**
   - Download and build from: https://github.com/markondej/fm_transmitter
   - Ensure it is in your PATH and executable.
3. **Place your WAV file:**
   - By default, the app uses `wav_files/block.wav`.
   - You can add more WAV files to the `wav_files/` directory and update the code if needed.

## Running the API
```bash
sudo python api.py
```
- The server listens on port 80 by default.
- Open a browser to `http://<raspberrypi-ip>/` to access the web UI.

## API Endpoints
- `GET /api/play?frq=<frequency>&uploadedfilename=block.wav`  
  Start transmitting at the given frequency (e.g., 101.1) using the specified WAV file.
- `GET /api/stop`  
  Stop transmission.
- `GET /api/getstatus`  
  Get current status (`playing` or `stopped`).

## Web Interface
- Located at `/static/main.html` (auto-served at root `/`)
- Enter a frequency and click **Play** or press **Enter** to start broadcasting.
- Click **Stop** to end transmission.

## Security Notes
- The API requires `sudo` to run the transmitter.
- Make sure your user can run `sudo` without a password for this script, or adjust permissions accordingly.

## Author
- Created by yosefshalomtz@gmail.com

---

**Disclaimer:** Broadcasting on FM frequencies may be subject to legal restrictions in your country. Use responsibly.

## License

This project is licensed under the MIT License. See the [LICENCE](./LICENCE) file for details.
