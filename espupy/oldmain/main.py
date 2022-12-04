from machine import Pin
from machine import Timer
import time



PIN_EN = 13
PIN_DIR = 12
PIN_STEP = 14
PIN_LED = 2

STEP_PRECS = 8.0
ANG_PER_STEP = 1.8

pin_en = Pin(PIN_EN, Pin.OUT)
pin_dir = Pin(PIN_DIR, Pin.OUT)
pin_step = Pin(PIN_STEP, Pin.OUT)
pin_led = Pin(PIN_LED, Pin.OUT)

def speed2sleep_us(speed):
	if (speed <= 0.0):
		return 0.0
	return round(1e6 * ANG_PER_STEP / (speed * STEP_PRECS * 2))

def accelrot(start_angle, end_angle, start_speed, end_speed, dir):
	cur_angle = start_angle

pin_led.on()

#step_tmr = Timer(-1)

start_p = 100
fin_p = 1

#step_tmr.init(period=start_p, mode=Timer.PERIODIC, callback=lambda t:print(2))

cur_angle = 0.0
step_prescaler = 8.0
angle_per_step = 1.8
step_sleep = 0
full_rotation = 2720.0
while True:
	pin_en.off()
	pin_step.off()
	step_sleep = 1000
	pin_dir.on()
	#if pin_dir.value() == 1:
	#	pin_dir.off()
	#else:
	#	pin_dir.on()
	while True: #cur_angle < full_rotation:
		pin_step.on()
		time.sleep_us(step_sleep)
		pin_step.off()
		time.sleep_us(step_sleep)
		#cur_angle += angle_per_step / step_prescaler
		#if cur_angle < full_rotation / 2:
		if step_sleep > 400:
			step_sleep = round(step_sleep * 0.9)
		#else:
		#	step_sleep += 1
	cur_angle = 0.0
	pin_en.on()
	pin_led.off()
	time.sleep_ms(300)
	pin_led.on()


