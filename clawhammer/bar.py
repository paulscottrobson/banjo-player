# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar class.
#		Date:		17th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re
from musicex import *
from entity import *

# ***************************************************************************************************
#
#											Bar class
#
# ***************************************************************************************************

class Bar(object):
	def __init__(self,definition,keys,barNumber,beats):
		self.barNumber = barNumber
		self.keys = keys
		if barNumber <= 1:
			Bar.currentFretting = [0,0,0,0,0]
		self.beats = beats
		MusicException.Number = barNumber
		self.entities = []
		self.pendingChordDisplay = None
		definition = definition.strip().lower()
		while definition != "":
			definition = self.processElement(definition.strip()).strip()
		if len(self.entities) > self.beats:
			raise MusicException("Bar too large")
	#
	#		Process a single element off the definition
	#
	def processElement(self,d):
		m = re.match("^([\\-\\/])(["+BaseMusicEntity.ENCODE+"])(.*)$",d)
		if m is not None:
			if len(self.entities) == 0:
				raise MusicException("No note to modify")
			endFret = BaseMusicEntity.ENCODE.find(m.group(2))
			lastNote = self.entities[-1]
			lastNote.modify(m.group(1),endFret)
			if self.isFingeringChange(lastNote.getFretting(),Bar.currentFretting):
				Bar.currentFretting = lastNote.getFretting()
			return m.group(3)
		#
		m = re.match("^(x*)(["+BaseMusicEntity.ENCODE+"]+)(.*)$",d)
		if m is not None:
			newNote = Note(m.group(1)+m.group(2))
			if self.pendingChordDisplay:
				newNote.setChord(self.pendingChordDisplay)
				self.pendingChordDisplay = None
			self.entities.append(newNote)
			if self.isFingeringChange(newNote.getFretting(),Bar.currentFretting):
				Bar.currentFretting = newNote.getFretting()
			return m.group(3)
		#
		m = re.match("^\\((.*?)\\)(.*)$",d)
		if m is not None:
			self.pendingChordDisplay = m.group(1).lower()
			if "chord_"+self.pendingChordDisplay not in self.keys:
				raise MusicException("Chord "+self.pendingChordDisplay+" unknown")
			chord =(self.keys["chord_"+self.pendingChordDisplay]+"0000")[:4]
			if re.match("^["+BaseMusicEntity.ENCODE+"]+$",chord) is None:
				raise MusicException("Bad chord definition "+chord)
			for i in range(0,len(chord)):
				Bar.currentFretting[i] = BaseMusicEntity.ENCODE.find(chord[i])
			return m.group(2)
		#
		if d.startswith("."):
			if len(self.entities) == 0:
				raise MusicException("No note to pluck")
			self.entities[-1].setPluck()
			return d[1:]
		#
		elif d.startswith("&"):
			self.entities.append(BeatRest())
			return d[1:]
		#
		elif d.startswith("!"):
			self.entities.append(Brush(Bar.currentFretting))
			if self.pendingChordDisplay:
				self.entities[-1].setChord(self.pendingChordDisplay)
				self.pendingChordDisplay = None
			return d[1:]
		else:
			raise MusicException("Cannot understand "+d)
	#
	#		Does a new fretting require a fingering change
	#
	def isFingeringChange(self,newFret,oldFret):
		changed = False
		for i in range(0,5):
			if oldFret[i] != newFret[i]:
				changed = True
		return changed
	#
	#		Convert to string
	#
	def toString(self):
		return "[{0}]:".format(self.barNumber)+",".join([x.toString() for x in self.entities])
	#
	#		Render a bar
	#
	def render(self):
		return "".join([x.render() for x in self.entities])

Bar.currentFretting = [0,0,0,0,0]

if __name__ == "__main__":
	b = Bar("5 x3 7 x2.",{ "chord_c":"2000" },1,4)
	print(b.toString(),b.render())
	print("=====================================")
	b = Bar("! & !. &",{ "chord_c":"2000" },2,4)
	print(b.toString(),b.render())
	print("=====================================")
	b = Bar("5-7 x3-1 7/9 !.",{ "chord_c":"2000" },3,4)
	print(b.toString(),b.render())
	print("=====================================")
	b = Bar("5!. (c)!.",{ "chord_c":"2135" },4,4)
	print(b.toString(),b.render())
	print("=====================================")
