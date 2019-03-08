# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		erbsen.py
#		Purpose:	Generates variants for Wayne Erbsen's Clawhammer book
#		Date:		7th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,sys,re

class ErbsenNotePair:
	def __init__(self,defn,firstHalf):
		self.originalDefinition = defn 											# save definition and half
		self.isFirstHalf = firstHalf
		self.halfBeats = [[ None,None ]] * 4									# [fretting,string] for each 1/2 beat
		self.chord = ""															# extract chord if given
		if defn.find(":") >= 0:
			defn = defn.split(":")
			self.chord = defn[0]
			defn = defn[1]
		self.notes = [self.decodeNote(x) for x in defn.split("-")]				# one or two notes
		assert len(self.notes) == 1 or len(self.notes) == 2
		self.isDoubleNote = len(self.notes) == 2
		print(self.originalDefinition,self.chord,self.notes)

	def decodeNote(self,defn):
																				# add current string if missing
		defn = defn if defn.find(".") >= 0 else defn + "."+str(ErbsenNotePair.currentString)
		defn = defn.split(".")													# split up
		assert len(defn) == 2
		defn = { "fretting":int(defn[0]),"string":int(defn[1])}					# create note
		ErbsenNotePair.currentString = defn["string"]							# update current string
		return defn

	def action(self,type,source):
		if type == "melody":													# melody, write notes
			for i in range(0,len(self.notes)):
				self.halfBeats[i*2] = [self.notes[i]["fretting"],self.notes[i]["string"]]
		elif type == "drone":													# drone if quavers
			if self.isDoubleNote:
				self.halfBeats[1] = [0,1]
				self.halfBeats[3] = [0,1]
		elif type == "pinch":													# pinch if crotchet
			if not self.isDoubleNote:
				self.halfBeats[2] = [0,-1]
		elif type == "twofinger":												# patterns two finger
			self.renderPattern("*151",source)
		elif type == "alternating":												
			self.renderPattern("*251",source)
		elif type == "pegleg":
			self.renderPattern("*.51",source)
		elif type == "forward":
			self.renderPattern("*15*" if self.isFirstHalf else "15*1",source)
		elif type == "reverse":
			self.renderPattern("*215" if self.isFirstHalf else "12*1",source)
		elif type == "foggy":
			self.renderPattern("*1*1" if self.isFirstHalf else "5*15",source)
		else:
			assert False,type+"?"

	def renderPattern(self,pattern,source):
		if self.isDoubleNote:
			self.action("melody",source)
			#self.action("drone",source)
		else:
			for i in range(0,4):
				if pattern[i] != '.':
					if pattern[i] != '*':
						self.halfBeats[i] = [0,int(pattern[i])]
					else:
						self.halfBeats[i] = source.getFretString((0 if self.isFirstHalf else 4)+i)
				
ErbsenNotePair.currentString = 1

class ErbsenGenerator:
	def __init__(self,directory,sourceFile):
		self.directory = directory
		self.fileRoot = sourceFile[:-7]
																				# Read file and preprocess
		src = [x.replace("\t"," ").strip() for x in open(directory+os.sep+sourceFile).readlines()]
		src = [x if x.find("#") < 0 else x[:x.find("#")].strip() for x in src]
		src = [x.lower().strip() for x in src if x != ""]
		self.equates = { "beats":"2","tempo":"60","format":"1","step":"4" }		# Sort out equates
		for f in [x for x in src if x.find(":=") >= 0]:
			parts = [x.strip() for x in f.split(":=") if x.strip() != ""]
			assert len(parts) == 2
			self.equates[parts[0]] = parts[1]
		src = [x for x in src if x.find(":=") < 0]								# Remove equates
		typeList = [x for x in src if x.startswith("(") and x.endswith(")")]	# Find the list of options
		assert len(typeList) == 1
		self.typeList = [x.strip() for x in typeList[0][1:-1].split(":") if x.strip() != ""]
		src = [x for x in src if not(x.startswith("(") and x.endswith(")"))]	# remove options
																				# convert into bars in a list
		self.barSource = [x.strip() for x in "|".join(src).split("|") if x.strip() != ""]

		self.typeList = ["reverse"]

		for i in range(0,len(self.typeList)):									# for each type set
			descr = self.typeList[i]											# get the description
			for bar in self.barSource:											# for each bar, split up
				barParts = [x.strip() for x in bar.split(" ") if x.strip() != ""]
				assert len(barParts) == 2
				self.notePair1 = ErbsenNotePair(barParts[0],True)				# 4 beats each part
				self.notePair2 = ErbsenNotePair(barParts[1],False)
				for part in [x for x in descr.split(",") if x != ""]:			# apply the type set items.
					self.modifier = part
					self.notePair1.action(part,self)
					self.notePair2.action(part,self)
				print(self.notePair1.halfBeats)
				print(self.notePair2.halfBeats)

	def getFretString(self,offset):
		if offset == 3 and self.modifier == "forward":							# on forward,3 use 2nd half note
			if not self.notePair2.isDoubleNote:									# only if it's a single note
				offset = 4

		source = self.notePair1 if offset < 4 else self.notePair2 				# pick which one
		assert not source.isDoubleNote
		return [source.notes[0]["fretting"],source.notes[0]["string"]]			# return the note

for root,dirs,files in os.walk(".."):
	for f in [x for x in files if x.endswith(".erbsen")]:
		if f.find("road") >= 0:
			ErbsenGenerator(root,f)



