from pulse import Pulse
from cosine import CosineWave
from sine import SineWave

class Test:
	def __init__(self):
		recieved=input("Please enter a valid pulse command: ")
		recieved=recieved.split(",")
		if (recieved[0].startswith('sin')):
			pulse=SineWave(recieved[0],(recieved[1]),int(recieved[2]), int(recieved[3]), int(recieved[4]), a=float(recieved[5]), phase=int(recieved[6]), factorOfPie=bool(recieved[7]))
		elif (recieved[0] is 'cos'):
			pulse=CosineWave(recieved[0],(recieved[1]),int(recieved[2]), int(recieved[3]), int(recieved[4]), a=float(recieved[5]), phase=int(recieved[6]), factorOfPie=bool(recieved[7]))
		else:
			pulse=Pulse(recieved[0], recieved[1], int(recieved[2]),int(recieved[3]), recieved[4])
		print pulse.getValues()
t=Test()