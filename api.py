# fm_transmitter flask REST API wrapper, for raspberry pi zero w.
# created by: yosefshalomtz@gmail.com

from flask import Flask, render_template, request
import json
import math
import subproccess


app = Flask(__name__)

# status of fm_transmitter app arguments
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

# frq: frequency, m: playmode, (optional) uploadedfilename: uploadedfilename
# see also isValidInput() comments.
@app.route('/api/play')
def play():
	frq = request.args.get('frq')
	playmode = request.args.get('m')
	uploadedfilename = request.args.get('uploadedfilename')
	
	if not isValidInput(frq, playmode, uploadedfilename): return json.dumps({"status": "error invalid parameter"})
	# here the code that play fm_transmitter and update {status}
	fm_transmitter = subproccess.Popen(["fghjkiuhygt"])
	return json.dumps({"status": "success"})

@app.route('/api/test')
def test():
	return json.dumps({"status":"success"})


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=False)
