import network
import socket
import json
import os
import time
from rnrproto import *

WIFI_CONFIG_FILE = 'wifi.config'
SSID_LABEL = 'ssid'
PWD_LABEL = 'password'
WIFI_AP_NAME = 'EspRnRap'
WIFI_AP_PWD = 'hep239'
WIFI_AP_CH = 11
WIFI_CONNECT_TIMEOUT = 10

TCP_SERVER_TIMEOUT = 1
TCP_MSG_MAX_SIZE = 1024

def load_wifi_config():
	wifis = []
	if WIFI_CONFIG_FILE in os.listdir():
		f = open(WIFI_CONFIG_FILE, 'rb')
	else:
		return wifis
	content = f.read()
	for w in content.split(MSG_DELIM):
		try:
			sample = json.loads(w)
		except:
			continue
		if type(sample) is dict:
			if (SSID_LABEL in sample.keys()) and (PWD_LABEL in sample.keys()):
				wifis += [sample]
	f.close()
	return wifis

def add_wifi2config(wifi_settings):
	if type(wifi_settings) is not dict:
		return False
	if not (SSID_LABEL in wifi_settings.keys()) or not (PWD_LABEL in wifi_settings.keys()):
		return False
	if WIFI_CONFIG_FILE not in os.listdir():
		return False
	f = open(WIFI_CONFIG_FILE, 'rb+')
	f.write(MSG_DELIM)
	json.dump(wifi_settings, f)
	f.close()
	return True

def echo_callback(msgl):
	print(msgl)
	return msgl

class RnRserver:

	def wifi_connect(self, wifi_settings):
		if type(wifi_settings) is not dict:
			return False
		if not (SSID_LABEL in wifi_settings.keys()) or not (PWD_LABEL in wifi_settings.keys()):
			return False
		self.apoint.active(False)
		self.station.active(True)
		self.station.connect(wifi_settings[SSID_LABEL], wifi_settings[PWD_LABEL])
		for i in range(WIFI_CONNECT_TIMEOUT):
			if self.station.isconnected():
				self.ip = self.station.ifconfig()[0]
				return True
			time.sleep(1)
		return False

	def is_connected(self):
		if self.apoint.active():
			return True
		if self.station.isconnected():
			return True
		return False

	def start_wifi_ap(self):
		self.station.active(False)
		self.apoint.active(True)
		time.sleep(1)
		self.apoint.config(essid = WIFI_AP_NAME, channel = WIFI_AP_CH)
		self.ip = self.apoint.ifconfig()[0]

	def start_wifi(self):
		self.station.active(False)
		self.apoint.active(False)
		wifis = load_wifi_config()
		if len(wifis) > 0:
			for w in wifis:
				if self.wifi_connect(w):
					self._print("CONNECTED", w)
					return True
		self.start_wifi_ap()
		self._print("START AP", WIFI_AP_NAME)
		return True

	def mainloop(self):
		self.start_wifi()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(TCP_SERVER_TIMEOUT)
		self.sock.bind(('', 9239))
		self.sock.listen(1)
		while True:
			try:
				if not self.is_connected():
					self.start_wifi()
				self.cli_sock, cli_addr = self.sock.accept()
				self.cli_sock.settimeout(TCP_SERVER_TIMEOUT)
				self._print("Accepted", cli_addr)
				while True:
					try:
						req = self.cli_sock.recv(TCP_MSG_MAX_SIZE)
						if not req:
							break
						if self.callback:
							ans = self.callback(parse_rnr_msg(req))
							self.cli_sock.send(create_rnr_msg(ans))
					except OSError as e:
						self._print("RECV OS ERROR", e)
						if e.value == 9:	
							self._print("CLIENT CLCOSED")
							break
						elif e.value == 110:
							self._print("RECV TIMEOUT")
							if not self.is_connected():
								self.start_wifi()
							continue
					except Exception as e:
						self._print("RECV ERROR", e)
						continue
			except OSError as e:
				self._print("ACCEPT OS ERROR", e)
				continue
			except Exception as e:
				self._print("ACCEPT ERROR", e)
				break
			self.cli_sock.close()
		self.sock.close()

	def _print(self, *args):
		if self.debug:
			print(args)

	def __init__(self, callback = None, debug = False):
		self.debug = debug
		self.station = network.WLAN(network.STA_IF)
		self.apoint = network.WLAN(network.AP_IF)
		self.station.active(False)
		self.apoint.active(False)
		self.ip = '127.0.0.1'
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.callback = callback
		if self.debug and self.callback is None:
			self.callback = echo_callback

