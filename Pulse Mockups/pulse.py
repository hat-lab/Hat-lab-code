import numpy as np

class Pulse(object):
	def __init__(self,pulse, name, start, width, channel):
		self.pulse=pulse
		self.name=name
		self.start=start
		self.width=width
		self.channel=channel
		self.end= start+width
		
	def getValues(self):
		return np.zeros(self.width)