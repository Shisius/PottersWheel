from machine import Pin, PWM, Timer
import time

# TASK = [angle, begin_speed, end_speed]

PIN_EN = 13
PIN_DIR = 12
PIN_STEP = 14
PIN_LED = 2
PIN_ISR = 5

DRV_PRESC = 8
RED_RATIO = 4
ANG_PER_STEP = 1.8

TMR_PERIOD_MS = 10

def speed2pwm(speed):
	return int(round(abs(speed) * DRV_PRESC * RED_RATIO / ANG_PER_STEP))

def cnt2angle(cnt):
	return cnt * ANG_PER_STEP / (DRV_PRESC * RED_RATIO)

def angle2cnt(angle):
	return int(round(abs(angle) * DRV_PRESC * RED_RATIO / ANG_PER_STEP))

def task2accel(task):
	dspeed = task[2] - task[1]
	if task[0] == 0:
		return 0.0
	return dspeed * (task[1] + dspeed/2) / task[0]

def state2speed(accel, angle, start_speed):
	speed_sqr = 2 * accel * angle + start_speed**2
	if speed_sqr < 0:
		return 0
	return speed_sqr**0.5

class WheelCtl:

	CMD_DICT = {b'START'  : lambda s, value: s.start_tasklist(value),
				b'TASK' : lambda s, value: s.set_task(value),
				b'LIST' : lambda s, value: s.set_tasklist(value),
				b'STOP' : lambda s, value: s.stop_tasklist(value)}

	def cmd_handler(self, cmdl):
		cmd = None
		value = None
		ansl = []
		res = False
		if len(cmdl) > 0:
			cmd = cmdl[0]
			ansl = [cmd]
		if len(cmdl) > 1:
			value = cmdl[1]
		if cmd in WheelCtl.CMD_DICT.keys():
			res = WheelCtl.CMD_DICT[cmd](self, value)
		if res == True:
			ansl += ['Accepted']
		elif (res == False) or (res is None):
			ansl += ['Denied']
		else:
			ansl += [res]
		return ansl

	def pwm_handler(self, pin):
		self.cnt += 1

	def tmr_handler(self, _tmr):
		self.angle = cnt2angle(self.cnt)
		self.speed = state2speed(self.accel, self.angle, self.task[1])
		self.pwm.freq(speed2pwm(self.speed))
		if self.angle >= self.task[0]:
			self.stop_task(None)
		print(self.angle, self.speed)

	def set_one_task(self, task):
		self.tasklist = [task]
		self.task_cnt = 0
		self.set_task(task)

	def set_task(self, task):
		if not(type(task) is list):
			return False
		if len(task) < 3:
			return False
		self.task = task
		self.accel = task2accel(task)
		self.speed = task[1]
		self.angle = 0
		print("accel", self.accel)
		return True

	def set_tasklist(self, taskl):
		if len(taskl) == 0:
			return False
		self.tasklist = taskl
		self.task_cnt = 0
		self.set_task(self.tasklist[0])
		return True

	def next_task(self):
		self.task_cnt += 1
		if len(self.tasklist) >= self.task_cnt + 1:
			self.set_task(self.tasklist[self.task_cnt])
			return True
		return False

	def start_task(self, v):
		self.cnt = 0
		self.cnt_last = 0
		self.pin_en.off()
		self.tmr.init(period=TMR_PERIOD_MS, mode=Timer.PERIODIC, callback=self.tmr_handler)
		self.pwm.freq(speed2pwm(self.speed))
		self.pwm.duty(512)
		return True

	def stop_task(self, v):
		if self.next_task():
			self.start_task(None)
		else:
			self.tmr.deinit()
			self.pwm.deinit()
			self.pin_en.on()
		print("end", self.angle)
		return True

	def start_tasklist(self):
		self.task_cnt = 0
		self.set_task(self.tasklist[0])
		self.start_task(None)

	def stop_tasklist(self):
		self.task_cnt = len(self.tasklist)
		self.stop_task(None)

	def setup(self):
		self.isr.irq(trigger=Pin.IRQ_FALLING, handler=self.pwm_handler)

	def __init__(self):
		self.cnt = 0
		self.tmr = Timer(-1)
		self.cnt_last = 0
		self.isr = Pin(PIN_ISR, Pin.IN)
		self.pwm = PWM(Pin(PIN_STEP))
		self.pin_en = Pin(PIN_EN, Pin.OUT)
		self.pin_dir = Pin(PIN_DIR, Pin.OUT)
		self.pin_led = Pin(PIN_LED, Pin.OUT)

		self.angle = 0
		self.speed = 0
		self.accel = 0
		self.task = [0, 0, 0]
		self.tasklist = []
		self.task_cnt = 0
		self.setup()
