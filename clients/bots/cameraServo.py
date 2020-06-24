# camera servo
import time
import math

#from AlphaBot2 import AlphaBot2
#bot = AlphaBot2()

from AlphaBot1 import AlphaBot1
bot = AlphaBot1()


def sayYes(r = 60, c = [0,0], speed = 1):
	i = 0
	while True : 
		phi = c[1]+math.cos(i)*r
		bot.lookAt(c[0], phi)	
		i+=speed
		time.sleep(0.02)

def sayNo(r = 60, c = [0,0], speed = 1):
	i = 0
	while True : 
		theta = c[0]+math.cos(i)*r
		bot.lookAt(theta, c[1])
		i+=speed
		time.sleep(0.02)


def spinningHead(r = 60, c = [0,0], speed = 1):
	i = 0
	while True : 
		theta = c[0]+math.cos(i)*r
		phi =   c[1]+math.sin(i)*r
		bot.lookAt(theta, phi)
		i+=speed
		time.sleep(0.02)
