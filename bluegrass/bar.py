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
		return s 
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
		self.barNumber = barNumber
		self.keys = keys
		self.definition = definition.strip().lower()
		self.alternateText = None
		self.beats = beats
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
			if m.lower().startswith("to"):		
				self.alternateText = m[2:].lower().strip()
	#
	#		Post rendering options
	#
	def postRendering(self,modifierList):
		pass
	#
	#		Generate all the notes
	#
	def generateNotes(self):		
		self.noteCount = [ 0 ] * (self.beats * 2)						# count of notes
		self.notes = []													# empty notes structure
		for i in range(0,self.beats * 2):
			self.notes.append([ None,None,None,None,None ])
		self.chords = [ None ] * (self.beats * 2)						# chords to show maybe play			
		self.pos = 0 													# position.
		definition = self.alternateText if self.alternateText is not None else self.definition
		definition = definition.strip().lower()							
		while definition != "":											# process definition.
			definition = self.generateOne(definition).strip()
	#
	#		Generate one note.
	#
	def generateOne(self,d):
		#
		if d.startswith("*"):											# * single note.
			s = self.strings[self.pos]
			if s is not None:
				self.insertNote(s,self.fretting[s-1])				
			self.pos += 1
			return d[1:]
		#
		if d.startswith("&"):											# & advance to next beat
			self.pos += 1	 											# (used in Erbsen music)
			if self.pos % 2 != 0:
				self.pos += 1
			return d[1:]
		#
		if d.startswith("."):											# . one byte rest
			self.pos += 1
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
			self.pos += 1 												# forward half beat
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
				self.pos += 1
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
			print(self.strings)
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
		if string > 5:
			raise MusicException("Bad String")
		if self.pos >= self.beats * 2:
			raise MusicException("Bar overflow")
		self.notes[self.pos][string-1] = Note(fretPosition,string)
		self.noteCount[self.pos] += 1
	#
	#		Get note to modify - the last note before current position
	#		must be only *one* note.
	#
	def getNoteToModify(self):
		p = self.pos 
		while self.noteCount[p] == 0:
			if p == 0:
				raise MusicException("No note to modify")
			p = p - 1
		if self.noteCount[p] != 1:
			raise MusicException("Cannot modify multiple notes")
		for i in range(0,5):
			if self.notes[p][i] is not None:
				return self.notes[p][i]
		assert False
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

	print("===========================================")

	b = Bar(2,"#6789t $12345.23 ********",4,{})
	b.convert([])
	print(b.toString())
	print(b.getPostStrings())
	print(b.getPostFretting())

