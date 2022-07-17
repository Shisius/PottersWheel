
import json

MSG_DELIM = b'|'
MSG_END = b'\r'

RNR_TCP_PORT = 9239

def create_rnr_msg(cmdl):
	if len(cmdl) == 1:
		return bytes(cmdl[0], 'UTF-8') + MSG_END
	if len(cmdl) >= 2:
		return bytes(cmdl[0], 'UTF-8') + MSG_DELIM + bytes(json.dumps(cmdl[1]), 'UTF-8') + MSG_END
	return MSG_END

def parse_rnr_msg(msg):
	msg = msg[:msg.find(MSG_END)]
	msgl = msg.split(MSG_DELIM)
	if len(msgl) > 1:
		try:
			msgl[1] = json.loads(msgl[1])
		except:
			pass
	return msgl
