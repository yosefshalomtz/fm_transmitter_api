# fm_transmitter flask REST API wrapper, for raspberry pi zero w.
# created by: yosefshalomtz@gmail.com

from flask import Flask, request
import json
import math
from time import sleep
from fmTransmitter import FmTransmitter


app = Flask(__name__)
host = "0.0.0.0"
port = 8080


uploaded_files = ["block.wav"]
# fm_transmitter app
fmt = FmTransmitter()

def init():
	# check if fm_transmitter executable is exsists
	if not fmt.exists_executable():
		print("fm_transmitter executable not found, please install it first.")
		return False
	# TODO:
	# check if wav_files directory exists
	# check if user has permission to perform sudo without password
	return True



# {frq} most be valid string=>float, {uploadedfilename} most be one of {uploaded_files} list.
def isValidInput(frq, uploadedfilename):
	# check if got two args
	if frq==None or uploadedfilename==None: return False
	# check if {frq} is valid float
	try:
		frq_num = float(frq)
		if not math.isfinite(frq_num): return False
	except Exception:
		return False
	# check if {uploadedfilename} is exists file in server
	for file_n in uploaded_files:
		if file_n==uploadedfilename: return True
	return False

@app.route('/')
def index():
	return app.send_static_file('main.html')

@app.route('/test')
def test():
	return app.send_static_file('test.html')

@app.route('/api/getstatus')
def getstatus():
	return fmt.status

# frq: frequency, uploadedfilename: uploaded file name to play
# see also isValidInput() comments.
@app.route('/api/play')
def play():
	frq = request.args.get('frq')
	uploadedfilename = request.args.get('uploadedfilename')
	
	if not isValidInput(frq, uploadedfilename): return json.dumps({"status": "error invalid parameter"})
	# check if fm_transmitter is already running
	if fmt.status=="playing": return json.dumps({"status": "error fm_transmitter already running"})
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
	print("Waiting 2 seconds...")
	sleep(6)
	print("fmt status:", fmt.status)
	print("Stopping fmt...")
	fmt.stop()
	print("fmt status:", fmt.status)
	print("Test completed successfully. exiting...")
	exit(0)

if __name__ == '__main__':
	if not init(): exit(1)
	# if first arg is "test", run test function
	import sys
	if len(sys.argv) > 2 and sys.argv[1] == "test":
		test(float(sys.argv[2]))
	app.run(host=host, port=port, debug=False)
