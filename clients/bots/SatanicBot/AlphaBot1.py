from AlphaBot import AlphaBot
import RPi.GPIO as GPIO
from datetime import datetime
import time
import math

class AlphaBot1(AlphaBot):
	def __init__(self):
		super().__init__()
		self.SERVO1 = 22
		self.SERVO2 = 27
		
		GPIO.setup(self.SERVO1, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.SERVO2, GPIO.OUT, initial=GPIO.LOW)
		
		print("Servo1 (pin 22) connection")
		self.p1 = GPIO.PWM(self.SERVO1, 50)
		self.p1.start(0)
		print("Servo1 connected and running")
		
		print("Servo2 (pin 27) connection")
		self.p2 = GPIO.PWM(self.SERVO2, 50)
		self.p2.start(0)
		print("Servo2 connected and running")
		
	def lookAt(self, theta, phi):
		self.p1.ChangeDutyCycle(2.5 + 10.0 * theta / 180)
		print("looking at theta = "+str(theta))
		time.sleep(0.02)
		self.p2.ChangeDutyCycle(2.5 + 10.0 * phi / 180)
		print("looking at phi = "+str(phi))
		time.sleep(0.02)



	def stop(self): # ok
		super().stop()
		print("Bot stopping")

	def capture_image(self,dest): #ok
		now = datetime.now()
		super().capture_image(dest)
