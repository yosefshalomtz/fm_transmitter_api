# fm_transmitter flask REST API wrapper, for raspberry pi zero w.
# created by: yosefshalomtz@gmail.com

from flask import Flask, render_template, request
import json
import math
import subprocess


app = Flask(__name__)
host = "localhost"
port = 8080


# status of fm_transmitter app arguments:
# {frq} - frequency {playmode} "block" or "file" {uploadedfilename} uploaded file name
status = {}
uploaded_files = ["test.wav"]
# fm_transmitter app
fm_transmitter = None

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
	return json.dumps(status)

# upload wav file to server, and add it to {uploaded_files} list.
@app.route('/api/uploadwavfile', methods=['POST'])
def uploadwavfile():
	# here logic to upload wav file
	
	return json.dumps({"status": "success"})

# frq: frequency, m: playmode, (optional) uploadedfilename: uploadedfilename
# see also isValidInput() comments.
@app.route('/api/play')
def play():
	frq = request.args.get('frq')
	playmode = request.args.get('m')
	uploadedfilename = request.args.get('uploadedfilename')
	
	if not isValidInput(frq, playmode, uploadedfilename): return json.dumps({"status": "error invalid parameter"})
	# here the code that play fm_transmitter and update {status}
	wav_file = ""
	if playmode=="file": wav_file = "./wav_files/"+uploadedfilename
	else: wav_file = "block.wav"
	fm_transmitter = subprocess.Popen(["fm_transmitter", "-f", frq, wav_file])
	if fm_transmitter.poll():
		if fm_transmitter.returncode!=0: ({"status": "error fm_transmitter failed to start"})
	else:
		status["frq"] = frq
		status["playmode"] = playmode
		status["uploadedfilename"] = uploadedfilename
		status["status"] = "playing"
	return json.dumps({"status": "success"})

@app.route('/api/test')
def test():
	return json.dumps({"status":"success"})


if __name__ == '__main__':
	app.run(host=host, port=port, debug=False)
