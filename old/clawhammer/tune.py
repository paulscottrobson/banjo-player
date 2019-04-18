# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		tune.py
#		Purpose:	Tune class.
#		Date:		17th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re
from musicex import *
from entity import *
from bar import *

# ***************************************************************************************************
#
#												Tune class
#
# ***************************************************************************************************

class Tune(object):
	def __init__(self):
		self.bars = []
		self.keys = { "beats":"4","tempo":"100","tuning":"gdgbd","step":"4" }
	#
	#		Load in a file
	#
	def loadFile(self,srcFile):
		self.loadDefinition(open(srcFile).readlines())
	#
	#		Load in a text list.
	#
	def loadDefinition(self,src):
		src = [x.replace("\t","").lower() for x in src]
		src = [x if x.find("//") < 0 else x[:x.find("//")] for x in src]
		src = [x.strip() for x in src if x.strip() != ""]
		for assign in [x for x in src if x.find(":=") >= 0]:
			parts = [x.strip() for x in assign.split(":=")]
			self.keys[parts[0]] = parts[1]
		for music in [x for x in src if x.find(":=") < 0]:
			for bar in [x for x in music.split("|") if x.strip() != ""]:
				self.bars.append(Bar(bar,self.keys,len(self.bars)+1,int(self.keys["beats"])))
	#
	#		Convert to string
	#
	def toString(self):
		return "\n".join([x.toString() for x in self.bars])

if __name__ == "__main__":
	src = """
		tempo := 60
		tuning := gcgcd
		chord_c := 2000

		5!. 7!. |3 !.5!. | 2 !. 3 2 | 0 xx4 x0 (c)!.
		2 !. 3!. | 2 (c)!.  0 !. | 2 (c)!. 3 2 | 0 xx4 x0 (c)!.	
	""".split("\n")
	tune = Tune()
	tune.loadDefinition(src)
	print(tune.toString())
	print("==========================")
	tune = Tune()
	tune.loadFile("littlebirdie.claw")
	print(tune.toString())
