# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		tune.py
#		Purpose:	Tune class
#		Date:		12th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re
from note import *
from musicex import *
from bar import *

# ***************************************************************************************************
#
#									Class representing a tune
#
# ***************************************************************************************************

class Tune(object):
	#
	def __init__(self,beatsPerBar = 4,tempo = 100):
		self.info = {"tuning":"gdgbd","step":"4","tempo":str(tempo),"beats":str(beatsPerBar)}
		self.beatsPerBar = 4
		self.bars = []
		self.fretting = [0,0,0,0,0]
	#
	def addSource(self,source):
		source = source.split("\n")
		MusicException.Number = 0
		for s in [x for x in source if x.find(":=") >= 0]:
			parts = [x.strip().lower() for x in s.split(":=") if x.strip() != ""]
			if len(parts) != 2:
				raise MusicException("Bad assignment "+s)
			self.info[parts[0]] = parts[1]
		for s in [x for x in source if x.find(":=") < 0]:
			for bd in [x.strip() for x in s.split("|") if x.strip() != ""]:
				self.addBar(bd.lower())
	#
	def addBar(self,barDefinition):
		newBar = Bar(len(self.bars)+1,barDefinition,self.fretting,self.beatsPerBar)
		self.bars.append(newBar)
	#
	def toString(self):
		music = "\n\n".join([x.toString() for x in self.bars])
		music = music + "\n"+"  ".join(["{0}:={1}".format(x,self.info[x]) for x in self.info.keys()])+"\n"
		return music

if __name__ == "__main__":
	tn = Tune()
	tn.addBar("#5 1 !. #7 1 !.")
	tn.addBar("#3 1 !. #5 1 !.")
	tn.addBar("#2 1 !. #3 1 #2 1")
	tn.addBar("#004 1 3 2 #200 !.")
	tn.addSource("tempo := 120\ntuning := gcgcd\n#2 1 !. #3 1 !.| #2 1 !. #0 1 !.| #2 1 !. #3 1 #2 1 |#004 1 3 2 #200 !.")
	print(tn.toString())

