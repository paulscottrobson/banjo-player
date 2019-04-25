# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		song.py
#		Purpose:	Song Class
#		Date:		23nd April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,re
from musicex import *
from bar import *

# ***************************************************************************************************
#
#										Song class
#
# ***************************************************************************************************

class Song(object):
	def __init__(self,fileName):
		self.sourceFile = fileName										# process filename
		tmp,namePart = os.path.split(self.sourceFile)
		self.baseName,tmp = os.path.splitext(namePart)
		print("Loading "+self.baseName)
		self.loadFile(self.sourceFile)									# load everything in.
	#
	#		Load file, create keys and bars
	#
	def loadFile(self,srcFile):
		MusicException.Number = 0
		src = [x.replace("\t"," ") for x in open(srcFile).readlines()]	# preprocess
		src = [x if x.find("##") < 0 else x[:x.find("##")] for x in src]
		src = [x.strip().lower() for x in src if x.strip() != ""]				
		self.keys = {"beats":"4","tempo":"100","step":"4" }				# extract keys.
		for l in [x for x in src if x.find(":=") >= 0]:
			parts = [x.strip() for x in l.split(":=") if x.strip() != ""]
			if len(parts) != 2 or parts[0] == "":
				raise MusicException("Bad definition "+l)
			self.keys[parts[0]] = parts[1]
		self.introBar = None 											# intro bar if reqd.
		if self.keys["intro"] == "1":
			self.introBar = Bar(0,".",int(self.keys["beats"]),self.keys)# create it
			self.introBar.convert([])									# never modified
		self.bars = [] 													# bars.
		for l in [x for x in src if x.find(":=") < 0]:					# lines with bars.
			for barDesc in [x.strip() for x in l.split("|") if x.strip() != ""]:
				newBar = Bar(len(self.bars)+1,barDesc,int(self.keys["beats"]),self.keys)
				self.bars.append(newBar)
		self.barCount = len(self.bars)									# they're numbered
	#
	#		Render all	
	#
	def renderAll(self,targetDirectory):
		self.render(targetDirectory)
		for options in [x for x in self.keys if x[:7] == "option_"]:
			self.render(targetDirectory,options[7:],self.keys[options])
	#
	#		Render, possibly modified.
	#
	def render(self,targetDirectory,modifierName = None,modifierDescriptor = None,overrideName = None):
		frets = [ 0,0,0,0,0 ]											# frets/strings state
		strings = [ None ] * (int(self.keys["beats"]) * 2)				# carried forward
		if modifierDescriptor is None:									# no mods
			for barNumber in range(0,self.barCount):				
				self.bars[barNumber].convert([],frets,strings)			
				frets = self.bars[barNumber].getPostFretting()
				strings = self.bars[barNumber].getPostStrings()
			baseName = self.baseName+".plux"
		else:															# mods
			modifiers = self.createModifiers(modifierDescriptor)		# identify them
			for barNumber in range(0,self.barCount):
				self.bars[barNumber].convert(modifiers[barNumber],frets,strings)
				frets = self.bars[barNumber].getPostFretting()
				strings = self.bars[barNumber].getPostStrings()
			if modifierName is not None:
				baseName = self.baseName+"-("+modifierName+").plux"


		baseName = baseName if overrideName is None else overrideName 	# Possible override.
		print("\tRendering "+baseName+".	")
		h = open(targetDirectory+os.sep+baseName,"w")					# create file, then keys
		h.write("\n".join([".{0}:={1}".format(k,self.keys[k]) for k in self.keys.keys()]))
		h.write("\n")
		if self.introBar:												# intro bar
			h.write("|"+self.introBar.render()+"\n")
		h.write("\n".join(["|"+x.render() for x in self.bars]))			# music.
		h.write("\n")
		h.close()
	#
	#		Create list of modifiers, one per bar, indexed from 0 from descriptor
	#
	def createModifiers(self,descriptor):
		mods = []														# create empty lists
		for i in range(0,self.barCount):
			mods.append([])
		for d in [x.strip() for x in descriptor.split(";") if x.strip() != ""]:
			m = re.match("^([0-9\\,\\-]*)\s*(.*)$",d)					# split into bars/name
			if m is None:	
				raise MusicException("Bad modifier "+d)
																		# range, default is 1-c
			rangeDef = m.group(1) if m.group(1) != "" else "1-"+str(self.barCount)
			mod = m.group(2)											# get the modifier
			if mod in Song.ROLLS:										# convert to roll ?
				mod = "roll "+Song.ROLLS[mod]
			for r in rangeDef.split(","):								# look for , subparts
				if r.find("-") >= 0:									# a-b range
					m2 = re.match("^(\d+)-(\d+)",r)
					if m2 is None:
						raise MusicException("Bad modifier "+d)
					for n in range(int(m2.group(1)),int(m2.group(2))+1):
						mods[n-1].append(mod)
				else:													# a single.
					mods[int(r)-1].append(mod)
		return mods 

Song.ROLLS = {															# roll definitions.
		"twofinger":"x151x151/234",
		"altthumb":	"x251x251/34",
		"forward":	"x15x15x1/234",
		"backward":	"x21512x1/345",
		"foggy":	"x1x15x15/234"
}

if __name__ == "__main__":
	s = Song("./down-the-road.blue")
	s.render("./","pinch","pinch")
	s.render("../agkbanjo/media/music",None,None,"__test.plux")
	s.render("../agkbanjo/media/music","demo","1 to xxx2///= && xx0 ; drone ; twofinger ; altthumb","__test.plux")
	print("=======================")
	s.renderAll("test")
	print("=======================")
	s = Song("./bile-em-cabbage-down.blue")
	s.render("../agkbanjo/media/music",None,"pinch;chord","__test.plux")
	s.renderAll("test")
#	s = Song("./carrythrough.blue")	
#	s.render("../agkbanjo/media/music",None,None,"__test.plux")

#
#	TODO: If a previous note is a long slide don't generate the roll pattern (Erbsen)
#	