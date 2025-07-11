# fm_transmitter flask REST API wrapper, for raspberry pi zero w.
# created by: yosefshalomtz@gmail.com

from flask import Flask, request, send_from_directory
import os
import json
import math
import sys
from time import sleep
from fmTransmitter import FmTransmitter


app = Flask(__name__)
host = "0.0.0.0"
port = 80


uploaded_files = ["block.wav"]
# fm_transmitter app
fmt = FmTransmitter()

def init():
	# check if fm_transmitter executable is exsists
	if not fmt.exists_executable():
		print("fm_transmitter executable not found, please install it first.")
		return False
	return True



# {frq} most be valid string=>float, {uploadedfilename} most be one of {uploaded_files} list.
def isValidInput(frq, uploadedfilename):
	# check if got two args
	if frq==None or uploadedfilename==None: return "too few arguments"
	# check if {frq} is valid float
	try:
		frq_num = float(frq)
		if not math.isfinite(frq_num): return "invalid frequency"
	except Exception:
		return "invalid frequency"
	# check if {uploadedfilename} is exists file in server
	for file_n in uploaded_files:
		if file_n==uploadedfilename: return True
	return "invalid uploaded file name (not exists in server)"

@app.route('/<path:filename>')
def serve_static_files(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, filename)
    return "404 Not Found", 404

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'main.html')

@app.route('/api/getstatus')
def getstatus():
	return fmt.status

# frq: frequency, uploadedfilename: uploaded file name to play
# see also isValidInput() comments.
@app.route('/api/play')
def play():
	frq = request.args.get('frq')
	uploadedfilename = request.args.get('uploadedfilename')
	
	input_validation = isValidInput(frq, uploadedfilename)
	if not input_validation==True: return json.dumps({"status": f"error invalid parameter: {input_validation}"})
	# check if fm_transmitter is already running
	# if frq is same as current frequency, return success. otherwise, stop current fm_transmitter and start new one.
	if (fmt.status=="playing"):
		if fmt.frequency==frq and (fmt.file=="./wav_files/" + uploadedfilename): return json.dumps({"status": "success"})
		else:
			fmt.stop()
			# then play new frequency and file
	# play the fm_transmitter
	fmt.frequency = frq
	fmt.file = "./wav_files/" + uploadedfilename
	try:
		fmt.play()
	except Exception as e:
		print(f"Error starting fm_transmitter: {e}")
		return json.dumps({"status": "error starting fm_transmitter"})
	return json.dumps({"status": "success"})

@app.route('/api/stop')
def stop():
	fmt.stop()
	return json.dumps({"status": "success"})


def test(frq):
	# test fm_transmitter is working successfully
	print("Testing fm_transmitter...")
	fmt.frequency = frq
	fmt.file = "./wav_files/block.wav"
	print("fmt playing...")
	fmt.play()
	print("fmt status:", fmt.status)
	print("Waiting 6 seconds...")
	sleep(6)
	print("fmt status:", fmt.status)
	print("Stopping fmt...")
	fmt.stop()
	print("fmt status:", fmt.status)
	print("Test completed successfully. exiting...")
	exit(0)

if __name__ == '__main__':
	print("Starting fm_transmitter flask API wrapper...")
	if not init(): exit(1)
	# if first arg is "test", run test function
	if len(sys.argv) > 2 and sys.argv[1] == "test":
		test(float(sys.argv[2]))
	app.run(host=host, port=port, debug=False)
