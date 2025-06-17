# fm_transmitter flask REST API wrapper, for raspberry pi zero w.
# created by: yosefshalomtz@gmail.com

from flask import Flask, render_template, request
import json
import math
import subprocess
from time import sleep
import FmTransmitter


app = Flask(__name__)
host = "0.0.0.0"
port = 8080


uploaded_files = []
# fm_transmitter app
fmt = FmTransmitter()


# {frq} most be valid string=>float, {playmode} nost be "block" or "file",
# if {playmode}=="file", {uploadedfilename} most be one of {uploaded_files} list.
def isValidInput(frq, playmode, uploadedfilename):
	# debug:
	print(f"{frq} {playmode} {uploadedfilename}")
	# check if got three args
	if frq==None or playmode==None: return False
	# check if {frq} is valid float
	try:
		frq_num = float(frq)
		if not math.isfinite(frq_num): return False
	except Exception:
		return False
	#check {playmode} flag is valid option.
	if playmode=="block": return True
	if playmode!="file": return False
	#check if {uploadedfilename} is exsist file in server
	for file_n in uploaded_files:
		if file_n==uploadedfilename: return True
	return False

@app.route('/api/getstatus')
def getstatus():
	return fmt.status

# frq: frequency, m: playmode, (optional) uploadedfilename: uploadedfilename
# see also isValidInput() comments.
@app.route('/api/play')
def play():
	frq = request.args.get('frq')
	playmode = request.args.get('m')
	uploadedfilename = request.args.get('uploadedfilename')
	
	if not isValidInput(frq, playmode, uploadedfilename): return json.dumps({"status": "error invalid parameter"})
	# check if fm_transmitter is installed in $PATH
	if fmt.exsists_executable()==False: return json.dumps({"status": "error fm_transmitter not found in $PATH"})
	# check if fm_transmitter is already running
	if fmt.status=="playing": return json.dumps({"status": "error fm_transmitter already running"})
	# here the code that play fm_transmitter and update {status}
	wav_file = ""
	if playmode=="file": wav_file = "./wav_files/"+uploadedfilename
	else: wav_file = "block.wav"
	# now play the fm_transmitter
	fmt.frequency = frq
	fmt.file = wav_file
	fmt.play()
	return json.dumps({"status": "success"})

@app.route('/api/stop')
def stop():
	fmt.stop()
	return json.dumps({"status": "success"})


def test():
	# test fm_transmitter is working successfully
	print("Testing fm_transmitter...")
	exit(1)

if __name__ == '__main__':
	test()
	app.run(host=host, port=port, debug=False)
