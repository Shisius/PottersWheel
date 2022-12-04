from machine import Pin, PWM, Timer
import time

_counter = 0
_tmr = Timer(-1)
_cnt_cur = 0

def pwm_handler(pin):
	global _counter
	_counter += 1

_pwm = PWM(Pin(2))

def tmr_handler(t):
	global _counter
	global _cnt_cur
	global _pwm
	if (_counter > _cnt_cur + 10):
		_cnt_cur = _counter
		_pwm.freq(10 + (_counter // 10))
	if _counter > 10000:
		_pwm.deinit()
		print("end", _counter)
		t.deinit()
	print(_counter)

_isr = Pin(5, Pin.IN)
_isr.irq(trigger=Pin.IRQ_FALLING, handler=pwm_handler)

def start_pwm():
	global _counter
	global _cnt_cur
	_counter = 0
	_cnt_cur = 0
	_tmr.init(period=10, mode=Timer.PERIODIC, callback=tmr_handler)
	_pwm.freq(10)
	_pwm.duty(512)


def stop_pwm():
	_tmr.deinit()
	_pwm.deinit()
	print("end", _counter)

def mainloop():
	while _counter < 10000:
		
		if _counter % 100 == 0:
			print(_counter)
		time.sleep_ms(100)

#start_time = time.time()
#start_pwm()
#mainloop()
#stop_pwm()
#stop_time = time.time()

#time.sleep_ms(1000)
#print("end", _counter)
