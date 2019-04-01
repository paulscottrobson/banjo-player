# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar representation
#		Date:		1st April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from musicex import *
import re

# ***************************************************************************************************
#
#											BAR Base Class
#
# ***************************************************************************************************

class Bar(object):
	#
	#		Initialise.
	#
	def __init__(self,barNumber,description,beats = 4,entryFretting = None,entryStrings = None):
		self.barNumber = barNumber
		self.description = description
		self.beats = beats
		self.initialFretting = entryFretting if entryFretting is not None else [ 0 ] * 5
		self.entryStrings = entryStrings if entryStrings is not None else [ None ] * (beats * 2)
		self.processDescription()
	#
	#		Convert the initial fretting/strings and the descriptor into a set of notes played
	#		at each half beat.
	#
	def processDescription(self):
		fretting = self.initialFretting
		self.notes = [] 														# create empty note structure
		self.modifiers = []														# modifiers for each note
		self.isUsed = [ False ] * 8												# checks if note played any 1/2 beat		
		for b in range(0,self.beats * 2):
			self.notes.append([None] * 5)
			self.modifiers.append([None] * 5)
		self.position = 0 														# 1/2 beat position
		self.fretting = [x for x in self.initialFretting]						# fretting.
		self.stringOverride = None 												# override
		self.lastNote = None 													# last note created
		desc = self.description.strip().lower() 								# preprocess.
		while desc != "":														# while something left
			desc = self.processOne(desc).strip()								# keep going
		self.finalFretting = self.fretting 										# remember final fretting
	#
	#		Convert to string
	#
	def toString(self):
		s = "Bar:{0} Beats:{1} Descriptor:\"{2}\" Output:\"{3}\"\n".format(self.barNumber,self.beats,self.description,self.toOutput())
		s = s + "Start Fretting:"+",".join([str(x) for x in self.initialFretting])
		s = s + " Strings:"+"".join([str(x) if x is not None else "-" for x in self.entryStrings])
		s = s + " End Fretting:"+",".join([str(x) for x in self.finalFretting])+"\n"
		for st in range(0,5):
			s = s + "|"
			for be in range(0,self.beats * 2):
				pluck = self.notes[be][st]
				s = s + ("---.---" if pluck is None else ("---"+str(pluck)+"---")[:7])
			s = s + "|\n"
		return s
	#
	#		Convert to output format.
	#
	def toOutput(self):
		return "???"
# ***************************************************************************************************
#
#										Bar that decodes BlueGrass
#
# ***************************************************************************************************

class BluegrassBar(Bar):
	#
	#		Process a single "command"
	#
	def processOne(self,d):
		#
		if d.startswith("*"):													# * take from current.
			strn = self.entryStrings[self.position]								# which string.
			if self.stringOverride is not None:									# handle string override
				strn = self.stringOverride
				self.stringOverride = None
			if strn is not None:												# if one is played
				self.notes[self.position][strn-1] = self.fretting[strn-1] 		# pluck that string with that fretting				
				self.isUsed[self.position] = True 	
				self.lastNote = self.position
			self.position += 1 													# next position
			return d[1:]
		#
		if d.startswith("."):													# skip 
			self.position += 1
			return d[1:]
		#
		m = re.match("^\\@([1-5])(.*)$",d)										# string override.
		if m is not None:
			self.stringOverride = int(m.group(1))
			return m.group(2)
		#
		if d.startswith("&"):													# & advance to next beat
			self.position = int((self.position+2)/2) * 2
			return d[1:]
		#
		m = re.match("^([\\-"+Bar.FRETS+"]+)(.*)$",d)							# list of frets
		if m is not None:
			strn = self.entryStrings[self.position]								# which string.
			if self.stringOverride is not None:									# handle string override
				strn = self.stringOverride
				self.stringOverride = None
			for cFret in m.group(1):											# put notes out.
				if cFret != "-":
					self.notes[self.position][strn-1] = Bar.FRETS.find(cFret)
					self.isUsed[self.position] = True 	
					self.lastNote = self.position
				strn += 1
			self.position += 1
			return m.group(2)
		#
		raise MusicException("Cannot process '{0}'".format(d),self.barNumber)	# give up.

Bar.FRETS = "0123456789tlwhufxv"


if __name__ == "__main__":
	# So bluegrass stuff can be done like this
	b = BluegrassBar(1,"*.**@1**4-5*",4,[12,3,4,1,2],[1,2,None,4,5,1,2,3])
	# and Wayne Erbsen's tunes like this.
	print(b.toString())
	b1 = BluegrassBar(1,"@2 3 && @4 7 &&")	
	print(b1.toString())