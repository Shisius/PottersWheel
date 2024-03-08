
import json

MSG_DELIM = b'|'
MSG_END = b'\r'

RNR_TCP_PORT = 9239

def create_rnr_msg(cmdl):
	msg = b''
	if len(cmdl) >= 1:
		if type(cmdl[0]) is bytes:
			msg += cmdl[0]
		else:
			msg += bytes(str(cmdl[0]), 'UTF-8')
	if len(cmdl) >= 2:
		msg += MSG_DELIM + bytes(json.dumps(cmdl[1]), 'UTF-8')
	return msg + MSG_END

def parse_rnr_msg(msg):
	msg = msg[:msg.find(MSG_END)]
	msgl = msg.split(MSG_DELIM)
	if len(msgl) > 1:
		try:
			if type(msgl[1]) is bytes:
				msgl[1] = msgl[1].decode('UTF-8')
			msgl[1] = json.loads(msgl[1])
		except:
			pass
	return msgl
