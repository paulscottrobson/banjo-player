# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		tune.py
#		Purpose:	Representation of a complete tune
#		Date:		3rd April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from musicex import *
from bar import *

# ***************************************************************************************************
#
#										Base Tune Class
#
# ***************************************************************************************************

class Tune(object):
	def __init__(self):
		self.values = { "beats":"4","tempo":"100","step":"4" }					# default settings.
		self.barCount = 0
		self.bars = [] 															# bars in tune.		
	#
	#		Read file in
	#
	def readFile(self,fileName):
		src = [x.strip().replace("\t"," ") for x in open(fileName).readlines()]
		src = [x for x in src if x != ""]
		src = [x if x.find("##") < 0 else x[:x.find("##")] for x in src]
		for s in [x for x in src if x.find(":=") >= 0]:
			s1 = [x.strip() for x in s.split(":=")]
			assert len(s1) == 2 and s1[0] != "","Bad key "+s
			self.set(s1[0],s1[1])
		for s in [x for x in src if x.find(":=") < 0]:
			self.addBarGroup(s)
	#
	#		Get/set values
	#
	def get(self,key):
		key = key.strip().lower()
		return self.values[key] if key in self.values else None
	def set(self,key,value):
		self.values[key.strip().lower()] = value.strip().lower()
	#
	def getBeats(self):
		return int(self.values["beats"])
	#
	#		Add bars seperated by |
	#
	def addBarGroup(self,barGroupDefinition):
		bars = [x.strip() for x in barGroupDefinition.split("|") if x.strip() != ""]
		for b in bars:
			self.addBar(b)
	#
	#		Render output
	#
	def render(self):
		render = "".join([".{0}:={1}\n".format(k,self.values[k]) for k in self.values.keys()])
		render += "".join(["|{0}\n".format(b.toOutput()) for b in self.bars])
		return render
		
# ***************************************************************************************************
#
#									Bluegrass Specific Tune
#
# ***************************************************************************************************

class BluegrassTune(Tune):
	#
	#		Add a new bar
	#
	def addBar(self,barDefinition):
		prevFretting = None if self.barCount == 0 else self.bars[-1].getEndFretting()
		newBar = BluegrassBar(self.barCount+1,barDefinition,self.getBeats(),5,prevFretting)
		self.bars.append(newBar)
		self.barCount += 1

if __name__ == "__main__":
	bt = BluegrassTune()
	bt.addBar("#0 2 && 2 && ")
	bt.addBarGroup("#01 2 && 2 && | #0 2 && 2 && | #002 3 && 3 &&")
	bt.addBarGroup("# 2&&2&&|#01 2&&2&&|#002 2&&3&&|#0 3&2&3&4&")
	for i in range(0,bt.barCount):
		print(bt.bars[i].toString())

	bt2 = BluegrassTune()
	bt2.readFile("boilemcabbage.bluegrass")
	for i in range(0,bt2.barCount):
		print(bt2.bars[i].toString())
	r = bt2.render()
	open("../agkbanjo/media/music/__test.plux","w").write(r)
