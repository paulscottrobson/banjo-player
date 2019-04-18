# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar class
#		Date:		18th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from entity import *
from musicex import *
import re

# ***************************************************************************************************
#
#											Bar Class
#
# ***************************************************************************************************

class Bar(object):
	def __init__(self,barNumber,beats,definition,entryFretting = [0,0,0,0,0],entryStrings = None):
		MusicException.Number = barNumber								# set error info
		self.barNumber = barNumber										# save info
		self.beats = beats
		self.currentFretting = [x for x in entryFretting]				# copy current fretting
		self.currentStrings = entryStrings
		if self.currentStrings is None:
			self.currentStrings = [ None ] * (beats * 2)				# current strings.
		self.entities = []												# entities in this bar
		definition = definition.lower().strip()
		while definition != "":
			definition = self.processOne(definition).strip()
	#
	#		Process one 'command'.
	#			
	def processOne(self,d):
		if d.startswith("."):											# . half beat rest
			self.entities.append(HalfBeatRest())
			return d[1:]
		#
		if d.startswith("*"):											# * note from fretting		
			pos = self.getPosition()									# where are we in the bar
			if pos >= self.beats * 2:									# overflow
				raise MusicException("Bar overflow")
			string = self.currentStrings[pos]							# Get string then fretting
			fretting = None if string is None else self.currentFretting[string-1]
			if string is None or fretting is None:						# No fretting/string
				self.entities.append(HalfBeatRest())
			else:														# note built to be played
				self.entities.append(Note(("x")*(string-1)+BaseMusicEntity.FRETTING[fretting]))
			return d[1:]
		#
		m = re.match("^(x*["+BaseMusicEntity.FRETTING+"]+)(.*)",d)		# xxnnnn set note.
		if m is not None:
			self.entities.append(Note(m.group(1)))						# add note using definition
			self.currentFretting = [x for x in self.entities[-1].get()[:5]] # reset current fretting
			return m.group(2)
		#
		m = re.match("^\\<([1-5\\.]+)\\>(.*)$",d)						# <ssssssss> set strings.
		if m is not None:
			if len(m.group(1)) != self.beats * 2:						# check length
				raise MusicException("String set length should be {0}".format(self.beats*2))
			self.currentStrings = [None if x == "." else int(x) for x in m.group(1)]
			return m.group(2)			
		#			
		m = re.match("^\\#(["+BaseMusicEntity.FRETTING+"\\.]+)(.*)$",d)	# #<frets> set fretting
		if m is not None:
			newFrets = (m.group(1)+"0000")[:5]
			self.currentFretting = [None if x == "." else BaseMusicEntity.FRETTING.find(x) for x in newFrets]
			return m.group(2)
		#		
		raise MusicException("Unknown element "+d)
	#
	#		Get position
	#
	def getPosition(self):
		pos = 0
		for e in self.entities:
			pos += e.get()[5]
		return pos
	#
	#		Convert to string
	#
	def toString(self):
		return "< "+(",".join([x.toString() for x in self.entities]))+" >"

if __name__ == "__main__":
	bar = Bar(1,4,"<1234.243> #6.89 ****** 	2345 *")
	print(bar.toString())
	bar = Bar(2,4,"<12341432> #6789 ********")
	print(bar.toString())

# / ^ v = modifiers
