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
	def __init__(self,barNumber,description,beats = 4,stringCount = 5,entryFretting = None):
		self.barNumber = barNumber
		self.defaultDescription = description
		self.beats = beats
		self.stringCount = stringCount
		self.initialFretting = entryFretting if entryFretting is not None else [ 0 ] * self.stringCount
		self.resetDescription(None)
		self.processDescription()
	#
	#		Set the description, using either this one or the overridden one.
	#
	def resetDescription(self,override):
		self.description = override if override is not None else self.defaultDescription
	#
	#		Convert the initial fretting/strings and the descriptor into a set of notes played
	#		at each half beat.
	#
	def processDescription(self):
		self.notes = [] 														# create empty note structure
		self.isUsed = [ False ] * 8												# checks if note played any 1/2 beat		
		for b in range(0,self.beats * 2):
			self.notes.append([None] * self.stringCount)						# note, modifier, count
		self.position = 0 														# 1/2 beat position
		self.chords = [ None ] * (self.beats*2)									# chords
		self.fretting = [x for x in self.initialFretting]						# fretting.and strings
		self.activeString = [ None ] * (self.beats * 2) 						# string played each pos
		self.activeFret = [ None ] * (self.beats * 2)							# fret played each pos
		self.lastNote = None 													# last note created
		desc = self.description.strip().lower() 								# preprocess.
		while desc != "":														# while something left
			desc = self.processOne(desc).strip()								# keep going
		self.finalFretting = [x for x in self.fretting] 						# remember final fretting/strings
	#
	#		Get end fretting
	#
	def getEndFretting(self):
		return self.finalFretting
	#
	#		Pluck one string.
	#
	def setPluck(self,pos,string):
		if string < 1 or string > self.stringCount:
			raise MusicException("Bad String {0}".format(string),self.barNumber)
		if pos < 0 or pos >= self.beats * 2:
			raise MusicException("Bad position {0}".format(string),self.barNumber)			
		self.notes[pos][string-1] = [self.fretting[string-1],None,0]
		self.isUsed[pos] = True 	
		self.lastNote = pos
		for b in range(pos,self.beats*2):
			self.activeString[b] = string
			self.activeFret[b] = self.fretting[string-1]
		return string
	#
	#		Set a display chord
	#
	def setChord(self,pos,dispChord):
		if pos < 0 or pos >= self.beats * 2:
			raise MusicException("Bad position {0}".format(string),self.barNumber)			
		self.chords[self.position] = dispChord
	#
	#		Update positional fretting forward
	#
	def nextPosition(self):
		self.position += 1
	#
	#		Set a fretting
	#
	def setFretting(self,string,fretPos):
		if string < 1 or string > self.stringCount:
			raise MusicException("Bad String {0}".format(string),self.barNumber)
		self.fretting[string-1] = fretPos
	#
	#		Convert to string
	#
	def toString(self):
		s = "Bar:{0} Beats:{1} Descriptor:\"{2}\" Output:\"{3}\"\n".format(self.barNumber,self.beats,self.description,self.toOutput())
		s = s + "Start Fretting:"+",".join([str(x) for x in self.initialFretting])
		s = s + " End Fretting:"+",".join([str(x) for x in self.finalFretting])+"\n"
		for st in range(0,self.stringCount):
			s = s + str(st+1)+" |"
			for be in range(0,self.beats * 2):
				pluck = self.notes[be][st]
				s = s + ("---.---" if pluck is None else ("---"+str(pluck[0])+"---")[:7])
			s = s + "|\n"
		return s
	#
	#		Convert to output format.
	#
	def toOutput(self):
		return ".".join([self.__renderNote(n) for n in range(0,len(self.notes))])
	#
	def __renderNote(self,pos):
		note = "".join(["" if self.notes[pos][i] is None else self.__renderPluck(pos,i) for i in range(0,self.stringCount)])
		note = note if self.chords[pos] is None else "({0}){1}".format(self.chords[pos],note)
		return note
	#
	def __renderPluck(self,pos,strn):
		return str(strn+1)+chr(self.notes[pos][strn][0]+97)		


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
		if d.startswith("."):													# skip 
			self.position += 1
			return d[1:]
		#
		if d.startswith("&"):													# & advance to next beat
			self.nextPosition()
			if self.position % 2 != 0:
				self.nextPosition()
			return d[1:]
		#
		if d[0] >= '1' and d[0] <= chr(self.stringCount+48):					# 1-5 pluck string/advance
			self.setPluck(self.position,int(d[0]))
			self.nextPosition()
			return d[1:]
		#
		m = re.match("^\\#(["+Bar.FRETS+"]*)(.*)$",d)							# reset fretting.
		if m is not None:														# padded right with 0s.
			newFretting = [Bar.FRETS.find(x) for x in (m.group(1)+"00000")[:5]]
			for i in range(0,len(newFretting)):
				self.setFretting(i+1,newFretting[i])
			return m.group(2)
		#
		m = re.match("^\\(([a-g][\\#b]?)\\)(.*)$",d)							# Chord definition
		if m is not None:
			self.setChord(self.position,m.group(1))
			return m.group(2)
		#																		# Single note format.
		m = re.match("^\\%(x*)(["+Bar.FRETS+"])(.*)$",d)
		if m is not None:
			for i in range(1,self.stringCount+1):								# zero all frets
				self.setFretting(i,0)
			string = len(m.group(1))+1											# string to play
			self.setFretting(string,Bar.FRETS.find(m.group(2)))					# set its fretting
			self.setPluck(self.position,string)									# pluck it.
			self.nextPosition()
			return m.group(3)
		#		
		raise MusicException("Cannot process '{0}'".format(d),self.barNumber)	# give up.
	#
	#		These are for Wayne Erbsen's lick modifications, tests for whether each half of a
	#		bar is one or two notes (the music is in 2/4 time)
	#
	def isNoteQuaver(self,note):
		return self.isUsed[(note-1)*4+2]
	#
	#		Check there is a note at all
	#
	def isNotePresent(self,note):
		return self.isUsed[(note-1)*4]
	#
	#		Apply modifiers
	#
	def modify(self,modifier,isBefore):
		modifier = modifier.strip().lower()
		if modifier == "pinch":
			self.modifyPinch(isBefore)
		elif modifier == "drone":
			self.modifyDrone(isBefore)
		elif modifier == "twofinger":
			self.convertToRoll("*151*151",isBefore)
		elif modifier == "forward":
			self.convertToRoll("*15*15*1",isBefore)
		elif modifier == "reverse":
			self.convertToRoll("*21512*1",isBefore,[3,4])
		elif modifier == "pegleg":
			self.convertToRoll("*_51*_51",isBefore)
		elif modifier == "altthumb":
			self.convertToRoll("*251*251",isBefore,[3,4])
		elif modifier == "foggy":
			self.convertToRoll("*1*15*15",isBefore)
		elif modifier == "chords":
			self.modifyChords(isBefore)
		elif modifier.startswith("[") and modifier.endswith("]"):
			if isBefore:
				self.resetDescription(modifier[1:-1].strip())
		else:
			assert False,"Unknown modifier "+modifier
	#
	#		Pinch modification
	#
	def modifyPinch(self,isBefore):
		if not isBefore:
			for beat in range(1,int(self.beats/2)+1):
				if not self.isNoteQuaver(beat) and self.isNotePresent(beat):
					self.notes[beat*4-2][0] = [0,None,None]
					self.notes[beat*4-2][4] = [0,None,None]
					self.isUsed[beat*4-2] = True
	#
	#		Drone modification
	#
	def modifyDrone(self,isBefore):
		if not isBefore:
			for beat in range(1,int(self.beats/2)+1):
				if self.isNoteQuaver(beat) and self.isNotePresent(beat):
					self.notes[beat*4-1][0] = [0,None,None]
					self.notes[beat*4-3][0] = [0,None,None]
					self.isUsed[beat*4-1] = True
					self.isUsed[beat*4-3] = True
	#
	#		Chord modification
	#
	def modifyChords(self,isBefore):
		if not isBefore:
			for beat in range(0,self.beats*2):
				if self.chords[beat] is not None:
					chordDef = self.getChord(self.chords[beat])
					self.isUsed[beat] = True
					for i in range(0,4):
						f = Bar.FRETS.find(chordDef[i])
						self.notes[beat][i] = [f,None,None]
	#
	#		Convert to roll.
	#
	def convertToRoll(self,rollDefinition,isBefore,allowedStrings = [2,3,4]):
		if not isBefore:
			for beat in range(1,int(self.beats/2)+1):
				if not self.isNoteQuaver(beat) and self.isNotePresent(beat):
					start = (beat - 1) * 4			
					if self.activeString[start] in allowedStrings:
						for pos in range(start,start + 4):
							self.notes[pos] = [None,None,None] * 5
							string = rollDefinition[pos % len(rollDefinition)]
							if string != '_':
								self.isUsed[pos] = True
								if string != '*':							
									self.notes[pos][int(string)-1] = [0,None,None]								
								else:
									p = pos
									if p % 4 == 3 and p < self.beats*2-1:
										p += 1
									self.notes[pos][self.activeString[p]-1] = [self.activeFret[p],None,None]
	#
	#		Get chord fretting
	#
	def getChord(self,chord):
		if chord == "c":
			return "21020"
		assert False,"Unknown chord "+c
Bar.FRETS = "0123456789tlwhufxv"

if __name__ == "__main__":
	# So bluegrass stuff can be done like this
	b = BluegrassBar(1,"123 #56789 12345",4,5)
	print(b.toString())
	# and Wayne Erbsen's tunes like this.
	b1 = BluegrassBar(1,"#00370 3 && (C)4 &&")	
	b1.modify("chords",False)
	print(b1.toString())
	# or this
	b1 = BluegrassBar(1,"%xx3 & %5 & %xxx4 &&")	
	print(b1.toString())
	print(b1.isNoteQuaver(1))
	print(b1.isNoteQuaver(2))	
