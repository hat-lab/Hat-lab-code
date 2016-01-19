from pulse import Pulse
from cosine import CosineWave
from sine import SineWave

def makePulse(recieved):
		recieved=recieved.split(',')
		if (recieved[0].startswith('sin')):
			print 'sin'
			pulse=SineWave(recieved[0],(recieved[1]),int(recieved[2]), int(recieved[3]), (recieved[4]), a=float(recieved[5]), phase=int(recieved[6]), factorOfPie=bool(recieved[7]))
		elif (recieved[0] is 'cos'):
			print 'cos'
			pulse=CosineWave(recieved[0],(recieved[1]),int(recieved[2]), int(recieved[3]), (recieved[4]), a=float(recieved[5]), phase=int(recieved[6]), factorOfPie=bool(recieved[7]))
		else:
			print 'default'
			pulse=Pulse(recieved[0], recieved[1], int(recieved[2]),int(recieved[3]), recieved[4])
		return pulse

f=open("pulses.txt",'r')
pulses=[]
f=f.readlines()
for x in range(0,len(f)):
	f[x]=f[x].strip('\n')
	print f[x]
	pulses.append(makePulse(f[x]))
for x in range(0, len(pulses)):
	print pulses[x].getValues(),'\n'