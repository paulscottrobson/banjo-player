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

import os,re
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
		name = os.path.splitext(fileName.replace("_"," ").split(os.sep)[-1])[0]
		name = [x for x in name.split(" ") if x != ""]
		name = " ".join([x[0].upper()+x[1:].lower() for x in name])
		self.set("name",name)
		for s in [x for x in src if x.find(":=") >= 0]:
			s1 = [x.strip() for x in s.split(":=")]
			assert len(s1) == 2 and s1[0] != "","Bad key "+s
			self.set(s1[0].lower(),s1[1].lower())
		for s in [x for x in src if x.find(":=") < 0]:
			self.addBarGroup(s)
	#
	#		Get/set values
	#
	def get(self,key):
		key = key.strip().lower()
		return self.values[key] if key in self.values else None
	def set(self,key,value):
		self.values[key.strip().lower()] = value.strip()
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
	#
	#		Create Modified tune.
	#		
	def createModifiedTune(self,modifiers):
		for b in self.bars:														# Initially use normal
			b.resetDescription(None)
		self.applyModifiers(modifiers,True)										# pre-modifiers
		for b in self.bars:
			b.processDescription()												# create actual nodes
		self.applyModifiers(modifiers,False)									# post modifiers
	#
	#		Apply modifiers to tune
	#
	def applyModifiers(self,modifiers,isBefore):
		for mod in [x.strip() for x in modifiers.split(";") if x.strip() != ""]:# multiple mods split by ;
			mod1 = [x.strip() for x in mod.split(":")]							# : splits apply/modifier
			if len(mod1) != 2 or mod1[0] == "" or mod1[1] == "":				# valid ?
				raise MusicException("Bad modifier "+mod,0)	
			allowList = self.getAllowed(mod1[0])								# see which are okay.
			for i in range(0,len(self.bars)):
				if allowList[i+1]:
					self.bars[i].modify(mod1[1],isBefore)
	#
	#		Convert to list of allowed numbers.
	#
	def getAllowed(self,allowItems):
		allowed = [ False ] * (len(self.bars)+1)
		for part in [x for x in allowItems.replace(" ","").split(",") if x != ""]:
			m = re.match("^(\d+)\-(\d+)$",part)
			if m is not None:
				n1 = int(m.group(1))
				n2 = int(m.group(2))
				if n1 < 1 or n1 > len(self.bars) or n2 < 1 or n2 > len(self.bars) or n1 > n2:
					raise MusicException("Bad range "+part)
				for n in range(n1,n2+1):
					allowed[n] = True
			elif part == "*":
				allowed = [ True ] * (len(self.bars)+1)
			elif re.match("^\d+$",part):
				n = int(part)
				if n < 1 or n > len(self.bars):
					raise MusicException("Bar out of range")
				allowed[n] = True
			else:
				raise MusicExceptions("Unknown range part "+allowItems)
		return allowed
	#
	#		Render all options
	#
	def renderAll(self,targetDirectory):
		last = 0
		while self.get("option"+str(last+1)) is not None:
			last += 1
		for op in range(0,last+1):
			self.renderAdjustedTune(op,targetDirectory)
	#
	#		Render tune with given option number (0 = standard) in directory.
	#
	def renderAdjustedTune(self,optionID,targetDirectory):
		defn = self.get("option"+str(optionID))
		if optionID == 0:
			fileNameBase = self.get("name")
			self.createModifiedTune("")
		else:
			assert defn is not None,"Option "+str(optionID)
			rx = "^\\\"(.*?)\\\"\\s*(.*)$"
			m = re.match(rx,defn.strip())
			assert m is not None,"Bad option "+defn
			fileNameBase = self.get("name")+" ("+m.group(1).strip().lower()+")"
			self.createModifiedTune(m.group(2))
		fileNameBase = fileNameBase.lower().replace(" ","_")
		fileName = targetDirectory+os.sep+fileNameBase+".plux"
		h = open(fileName,"w")
		h.write(self.render())
		h.close()

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
	bt2.readFile("./boil_em_cabbage_down.bluegrass")
	#bt2.createModifiedTune("6-8:pluck;9:[#tlwh 1&2&3&4]")
	#for b in bt2.bars:
	#		print(b.toString())
	r = bt2.render()
	open("../agkbanjo/media/music/__test.plux","w").write(r)
	open("__test.plux","w").write(r)
	#
	bt2.renderAdjustedTune(0,".")
	bt2.renderAdjustedTune(1,".")	
	bt2.renderAdjustedTune(2,".")	
	#
	bt2.renderAll(".")