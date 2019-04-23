# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar (and Note) class
#		Date:		22nd April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re
from musicex import *

# ***************************************************************************************************
#
#									   Note class
#
# ***************************************************************************************************

class Note(object):
	def __init__(self,fretting,string):
		self.fretting = fretting
		self.string = string
		self.modifier = None 
		self.modifierOffset = 0
	#
	def getString(self):
		return self.string
	#
	def getFinalFretting(self):
		return self.fretting+self.modifierOffset
	#
	def toString(self):
		s = str(self.fretting)		
		if self.modifier is not None:
			s = s + ("/" if self.modifier == "/" else "^")+str(self.getFinalFretting())
		return s+"."+str(self.string)
	#
	def modify(self,c):
		if self.modifier is not None:
			if self.modifier != c:
				raise MusicException("Note modifier changed")
		self.modifier = c;
		self.modifierOffset += (-1 if c == "^" else 1)

Note.FRETTING = "0123456789tewhufs"

# ***************************************************************************************************
#
#										Bar class
#
# ***************************************************************************************************

class Bar(object):
	def __init__(self,barNumber,definition,beats,keys):
		self.barNumber = barNumber										# save basic info
		self.keys = keys
		self.beats = beats
		self.definition = definition.strip().lower()
		self.alternateText = None 										# override text
		self.notes = None
		self.noteCount = None
	#
	#		Convert bar into an array of notes
	#
	def convert(self,modifierList,entryFrets = None,entryStrings = None):
		MusicException.Number = self.barNumber							# set error position.
																		# set up initial strings/frets
		self.fretting = entryFrets if entryFrets is not None else [0,0,0,0,0]
		self.strings = entryStrings if entryStrings is not None else [ None ] * (self.beats*2)

		self.preRendering(modifierList)									# changes to source, maybe
		self.generateNotes()											# process source.
		self.postRendering(modifierList)								# after render effects
	#
	#		Get post conversion setup
	#		
	def getPostFretting(self):
		return [x for x in self.fretting]
	def getPostStrings(self):
		return [x for x in self.strings]
	#
	#		Pre-rendering (overwrite the modifiers)
	#
	def preRendering(self,modifierList):
		self.alternateText = None 										# initially no alt-text
		for m in modifierList:											# look for to xxxxx
			if m.lower().startswith("to"):								# if to xxxxx
				self.alternateText = m[2:].lower().strip()				# set the alternate text
	#
	#		Post rendering options
	#
	def postRendering(self,modifierList):
		for m in modifierList:											# for each modifier
			if m.startswith("roll"):									# if roll xxxxx/nnn
				if self.isSingleNote(0) and self.isSingleNote(1):		# if rollable
					self.processRoll(m[4:].strip())						# do roll processor.
			elif m == "drone":											# drone
				for h in range(0,2):									# add drone to quavers
					if not self.isSingleNote(h):
						self.notes[h*4+1][0] = Note(1,0)
						self.notes[h*4+3][0] = Note(1,0)
			elif m == "pinch":											# pinch 
				for h in range(0,2):									# add pinch to crotchets
					if self.isSingleNote(h):
						self.notes[h*4+2][0] = Note(1,0)
						self.notes[h*4+2][4] = Note(5,0)
			elif m == "chord":											# chord
				for p in range(0,8):									# look for chords in bar
					if self.chords[p] is not None:
						key = self.chords[p]							# check chord known and format
						if "chord_"+key not in self.keys:
							raise MusicException("Unknown chord "+key)
						chord = self.keys["chord_"+key].lower().strip()
						if len(chord) != 4 or re.match("^["+Note.FRETTING+"]+$",chord) is None:
							raise MusicException("Chord {0} badly defined ".format(key))
						for i in range(0,4):							# copy chord in.
							self.notes[p][i] = Note(Note.FRETTING.find(chord[i]),i+1)
						self.notes[p][4] = None
			else:
				raise MusicException("Unknown modifier "+m)
	#
	#		Convert notes to a predefined roll.
	#				
	def processRoll(self,rollDef):
		m = re.match("^([1-5x]+)\\/([1-5]+)$",rollDef)					# validate roll
		if m is None or len(m.group(1)) != 8:
			raise MusicException("Bad roll Definition "+rollDef)		# check roll playable
		isPlayable = True
		for r in range(0,self.beats * 2):								# look at each string
			if self.rollNote[r] is not None:
				if m.group(2).find(str(self.rollNote[r].getString()))<0: # error if not in useable strings
					isPlayable = False
		if isPlayable:													# if okay
			for r in range(0,self.beats*2):								# work through roll
				self.notes[r] = [ None,None,None,None,None ]
				if self.rollNote[r] is not None:						# copying roll strings in
					if m.group(1)[r] == "x":							# melody note
						note = self.rollNote[r if r%4 != 3 else 4]		# taken from 3 if at pos 4 (fwd)
						self.notes[r][note.getString()-1] = note 		# put note in.
					else:
						string = int(m.group(1)[r])						# plucked note.
						self.notes[r][string-1] = Note(0,string)
	#
	#		Is a half-bar a single or double note
	#		
	def isSingleNote(self,barHalf):
		return (self.noteCount[barHalf*4+1]+self.noteCount[barHalf*4+2]+self.noteCount[barHalf*4+3] == 0)
	#
	#		Generate all the notes
	#
	def generateNotes(self):		
		self.noteCount = [ 0 ] * (self.beats * 2)						# count of notes
		self.notes = []													# empty notes structure
		self.rollNote = [ None ] * 8 									# roll note here
		for i in range(0,self.beats * 2):
			self.notes.append([ None,None,None,None,None ])
		self.chords = [ None ] * (self.beats * 2)						# chords to show maybe play			
		self.pos = 0 													# position.
		definition = self.alternateText if self.alternateText is not None else self.definition
		definition = definition.strip().lower()							
		while definition != "":											# process definition.
			definition = self.generateOne(definition).strip()
		while self.pos < self.beats * 2:								# fill out the rest.
			self.advance()
	#
	#		Generate one note.
	#
	def generateOne(self,d):
		#
		if d.startswith("*"):											# * single note.
			s = self.strings[self.pos]
			if s is not None:
				self.insertNote(s,self.fretting[s-1])				
			self.advance()
			return d[1:]
		#
		if d.startswith("&"):											# & advance to next beat
			self.advance()
			if self.pos % 2 != 0:
				self.advance()
			return d[1:]
		#
		if d.startswith("."):											# . one byte rest
			self.advance()
			return d[1:]
		#
		m = re.match("^(x*)(["+Note.FRETTING+"]+)(.*)$",d)				# standard note.
		if m is not None:
			string = len(m.group(1))									# start string
			for note in m.group(2):										# note for each fret
				if string >= 5:
					raise MusicException("Out of range "+m.group(1)+m.group(2))
				self.insertNote(string+1,Note.FRETTING.find(note))
				self.fretting[string] = Note.FRETTING.find(note)
				string += 1
			self.advance()
			return m.group(3)
		#
		m = re.match("^([\\/v\\^\\=]+)(.*)$",d)							# modifiers.
		if m is not None:
			fullModifier = True 
			modifyNote = self.getNoteToModify()							# get the note to modify
			for mc in m.group(1):										# do each note.
				if mc == "=":
					fullModifier = False
				else:
					modifyNote.modify(mc)
					self.fretting[modifyNote.getString()-1] = modifyNote.getFinalFretting()
			if fullModifier:											# no '=' so 1 beat
				self.advance()
			return m.group(2)
		#
		m = re.match("^\\((.*?)\\)(.*)$",d)								# (chord)
		if m is not None:
			if self.pos >= self.beats * 2:
				raise MusicException("Bar overflow")
			self.chords[self.pos] = m.group(1).strip()
			return m.group(2)
		#																# $(strings)
		m = re.match("^\\$([1-5\\.]+)(.*)",d)
		if m is not None:
			if len(m.group(1)) != self.beats * 2:
				raise MusicException("String definition not {0}",self.beats * 2)
			self.strings = [ None if s == "." else int(s) for s in m.group(1)]
			return m.group(2)
		#
		m = re.match("#(["+Note.FRETTING+"]+)(.*)",d)					# #(fretting)
		if m is not None:
			self.fretting = [Note.FRETTING.find(x) for x in (m.group(1)+"00000")[:5]]
			return m.group(2)
		#
		raise MusicException("Syntax error "+d)
	#
	#		Insert a note. Update fretting.
	#		
	def insertNote(self,string,fretPosition):
		if string > 5:													# check sring
			raise MusicException("Bad String")
		if self.pos >= self.beats * 2:									# check pos
			raise MusicException("Bar overflow")
		self.notes[self.pos][string-1] = Note(fretPosition,string)		# set string/pos to pluck
		for i in range(self.pos,self.beats*2):							# make roll note for rest of bar
			self.rollNote[i] = self.notes[self.pos][string-1]
		self.noteCount[self.pos] += 1									# add one to counter.
	#
	#		Get note to modify - the last note before current position
	#		must be only *one* note.
	#
	def getNoteToModify(self):
		p = self.pos 
		while self.noteCount[p] == 0:									# keep going backwards till found
			if p == 0:
				raise MusicException("No note to modify")
			p = p - 1
		if self.noteCount[p] != 1:										# can only be one note.
			raise MusicException("Cannot modify multiple notes")
		for i in range(0,5):											# return the first note found
			if self.notes[p][i] is not None:							# must be the only one
				return self.notes[p][i]
		assert False 													# ???
	#
	#		Advance forward one.
	#
	def advance(self):
		self.pos += 1
	#
	#		Convert to string
	#
	def toString(self):
		s = " "+"".join([("   {0}    ".format(x if x is not None else " "))[:7] for x in self.chords])
		s = s + "\n"
		s = s + "\n".join([self.__toString(s) for s in range(0,5)])
		return s+"\n"
	#
	def __toString(self,string):
		s = str(string+1)+"---"
		for b in range(0,self.beats * 2):
			n = ".------" if self.notes[b][string] is None else (self.notes[b][string].toString()+"-------")[:7]
			s = s + n
		return s

if __name__ == "__main__":
	b = Bar(1,"xx23 (c#).x4//= 4v xxxx2 (c#)",4,{"chord_c#":"1235"})			
	b.convert([])
	print(b.toString())
	print(b.getPostStrings())
	print(b.getPostFretting())
	print(b.isSingleNote(0),b.isSingleNote(1))
	print("===========================================")

	b = Bar(2,"#6789t $12345.23 ********",4,{})
	b.convert([])
	print(b.toString())
	print(b.getPostStrings())
	print(b.getPostFretting())
	print(b.isSingleNote(0),b.isSingleNote(1))

	print("===========================================")

	b = Bar(3,"xx1 && (c)x2 & xxx3",4,{ "chord_c":"2321" })
	b.convert([])
	print(b.toString())
	print(b.getPostStrings())
	print(b.getPostFretting())
	print(b.isSingleNote(0),b.isSingleNote(1))
	print(" ".join([x.toString() if x is not None else "." for x in b.rollNote]))

	print("===========================================")
	b.convert(["drone"])
	print(b.toString())
	print("===========================================")
	b.convert(["pinch"])
	print(b.toString())
	print("===========================================")
	b.convert(["chord"])
	print(b.toString())
	print("===========================================")
	b = Bar(4,"xx1 && x2",4,{})
	b.convert(["roll x15x15x1/234"])
	print(b.toString())


