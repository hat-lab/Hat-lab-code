from pulse import Pulse
import numpy as np

class SineWave(Pulse):

	def __init__(self, pulse, name, start, width, channel, a=.5, phase=0, factorOfPie=True ):
		super(SineWave, self).__init__(pulse,name, start, width, channel)
		self.a=a
		self.phase=phase
		self.factorOfPie=factorOfPie
		
	#This is where the program would calculate the values at each particular time	
	def getValues(self):
		print self.width
		wavedata=np.array(range(0,self.width))*1.0
		if (self.factorOfPie):
			for x in range(0,len(wavedata)):
				wavedata[x]=np.sin(self.a*x*np.pi+self.phase)
		else:
			for x in range(0,len(wavedata)):
				wavedata[x]=np.sin(self.a*x+self.phase)
		return wavedata