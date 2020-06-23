from AlphaBot import AlphaBot
import RPi.GPIO as GPIO
from datetime import datetime
import time
import math

class AlphaBot1(AlphaBot):
	def __init__(self):
		super().__init__()



	def stop(self): # ok
		super().stop()
		print("Bot stopping")

	def capture_image(self,dest): #ok
		now = datetime.now()
		super().capture_image(dest)