from flask import Flask, request, render_template
import RPi.GPIO as GPIO
import sys
import time
import board
import busio
import adafruit_tcs34725
from concurrent.futures import ThreadPoolExecutor
from flask_socketio import SocketIO, emit

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(1)
app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

pinLDR 	= 14 #8
pinLedR = 17 #11
pinLedG = 27 #13
pinLedB = 22 #15
pinLedY = 18 #12

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8080)

@app.route("/")
def index():
	executor.submit(rgb_sensor_data)
	return  render_template("index.html")

def rgb_sensor_data():
	while True:
		valueColor	= 0 # 0 = null, 1 = red, 2 = green, 3 = blue, 4 = yellow
		GPIO.setmode(GPIO.BCM)
		if (rc_time(pinLDR) > 10000):
			valueRGB = sensor.color_rgb_bytes
			if (valueRGB[0] > (valueRGB[1] + valueRGB[2])):
				valueColor = 1
				pinLed = pinLedR
			elif (valueRGB[1] > (valueRGB[0] + valueRGB[2])):
				valueColor = 2
				pinLed = pinLedG
			elif (valueRGB[2] > (valueRGB[0] + valueRGB[1])):
				valueColor = 3
				pinLed = pinLedB
			else :
				valueColor = 4
				pinLed = pinLedY
			socketio.emit('rgb_sensor_data', valueColor)
			led_blink(pinLed)
		else :
			time.sleep(0.1)
		GPIO.cleanup()
		
def rc_time (pinLDR):
	count = 0
	GPIO.setup(pinLDR, GPIO.OUT)
	GPIO.output(pinLDR, False)
	time.sleep(0.1)
	#Change the pin back to input
	GPIO.setup(pinLDR, GPIO.IN)
	#Count until the pin goes high
	while (GPIO.input(pinLDR) == 0):
		count += 1
	return count

def led_blink (pinLed):
	GPIO.setup(pinLed, GPIO.OUT)
	GPIO.output(pinLed, GPIO.HIGH)
	time.sleep(1.0)
	GPIO.output(pinLed, GPIO.LOW)