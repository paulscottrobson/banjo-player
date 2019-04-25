# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		tune.py
#		Purpose:	Clawhammer Tune class
#		Date:		25th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re,os
from musicex import *
from bar import *

class ClawhammerTune(object):
	def __init__(self,tuneSource):
		self.tuneName = os.path.split(tuneSource)[1][:-5].strip()
														# Preprocess
		src = [x.lower().replace("\t"," ") for x in open(tuneSource).readlines()]
		src = [x.strip() if x.find("//") < 0 else x[:x.find("//")].strip() for x in src]
														# Do keys.
		MusicException.NUMBER = 0														
		self.keys = { "beats":"4","step":"4","tempo":"60","tuning":"gdgbd" }
		for s in [x for x in src if x.find(":=") >= 0]:
			parts = [x.strip() for x in s.split(":=") if x.strip() != ""]
			if len(parts) != 2 or parts[0] == "":
				raise MusicException("Bad assignment "+s)
			self.keys[parts[0]] = parts[1]

		self.bars = []									# Create the bars
		for s in [x for x in src if x.find(":=") < 0]:
			while s.find("{") >= 0:						# replace all equates.
				s = re.split("(\\{.*?\\})",s)			# split into bits.
				for i in range(0,len(s)):				# replace the macro bits
					if s[i].startswith("{"):
						if s[i][1:-1] not in self.keys:
							raise MusicException("Unknown macro "+s[i])
						s[i] = self.keys[s[i][1:-1]]
				s = "".join(s)
			for b in [x.strip() for x in s.split("|") if x.strip() != ""]:
				newBar = Bar(len(self.bars)+1,b)
				self.bars.append(newBar)

	def render(self,targetDirectory,overwrite = None):
		target = self.tuneName+".plux" if overwrite is None else overwrite
		h = open(targetDirectory+os.sep+target,"w")
		h.write("".join(".{0} := {1}\n".format(k,self.keys[k]) for k in self.keys.keys()))
		h.write("".join(["|{0}\n".format(x.render()) for x in self.bars]))
		h.close()

	def toString(self):
		return "\n\n".join([x.toString() for x in self.bars])

if __name__ == "__main__":
	tn = ClawhammerTune("cripple.claw")
	tn.render("./")
	tn.render("../agkbanjo/media/music","__test.plux")