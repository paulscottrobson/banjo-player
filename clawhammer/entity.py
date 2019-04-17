# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		entity.py
#		Purpose:	Entities that form part of a bar.
#		Date:		17th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from musicex import *

# ***************************************************************************************************
#
#											Base class
#
# ***************************************************************************************************

class BaseMusicEntity(object):
	def __init__(self):
		self.chord = None 												# chord that can override
		self.pluck = None
	#
	#		Set the chord for this entity object
	#
	def setChord(self,chord):
		self.chord = chord.strip().lower()
	#
	#		Get chord Rendering
	#
	def getChordRendering(self):
		return "" if self.chord is None else "("+self.chord+")"
	#
	#		Make this a 'pluck'
	#
	def setPluck(self):
		self.pluck = True
	#
	#		Get the rendering for the second half note (if not a modified note)
	#	
	def getPluckRendering(self):
		return self.noteToRender(5,0)+"." if self.pluck else "."
	#
	#		Get pluck "toString"
	#
	def getPluckToString(self):
		return "." if self.pluck else ""
	#
	#		Get the fretting search string.
	#
	def getFrettingEncode(self):
		return BaseMusicEntity.ENCODE
	#
	#		Convert a string/fret pair to a note.
	#
	def noteToRender(self,string,fretting):
		return chr(string+48)+chr(fretting+97)
	#
	#		Dummies as this class is abstract
	#
	def render(self):
		assert False,"Abstract method"
	def modify(self,modifier,count):
		assert False,"Abstract method"

BaseMusicEntity.ENCODE = "0123456789tlwhufsve"				

# ***************************************************************************************************
#
#											Beat Rest
#
# ***************************************************************************************************

class BeatRest(BaseMusicEntity):
	#
	#		Convert note to final format, at one half beat
	#
	def render(self):
		return self.getChordRendering()+"."+self.getPluckRendering()
	def toString(self):
		return "&"+self.getPluckToString()

# ***************************************************************************************************
#
#					Single note - can be a single pluck or chord
#					can be modified using pulloffs or hammerons or slides.
#
# ***************************************************************************************************

class Note(BaseMusicEntity):
	def __init__(self,definition):
		BaseMusicEntity.__init__(self)
		self.modifier = Note.NORMAL 									# no slides/pulloff/hammers
		self.modifierOffset = 0											# how it changes numerically.
		self.setFretting(definition)
	#
	#		Get current fretting (copy)
	#	
	def getFretting(self):
		return [x if x is None else x + self.modifierOffset for x in self.fretting]
	#
	#		Set fretting in the xxxxffff format.
	#
	def setFretting(self,definition):
		self.fretting = [ None ] * 5 									# default fretting
		currentString = 0
		for d in definition.strip().lower():							# scan definition string
			if d == "x":												# don't play
				currentString += 1
			else:
				if currentString >= 5:									# pluck string check and do
					raise MusicException("Bad note definition "+definition)
				self.fretting[currentString] = self.getFrettingEncode().find(d)
				if self.fretting[currentString] < 0:
					raise MusicException("Unknown fret position "+d)
				currentString += 1
	#
	#		Render note.
	#
	def render(self):
		render = self.getChordRendering()								# chord display
		for string in range(0,5):										# build played notes.
			if self.fretting[string] is not None:
				render += self.noteToRender(string+1,self.fretting[string])
		if self.modifier == Note.NORMAL:								# if not modified add pluck if any
			return render + "." + self.getPluckRendering()
		return render + (" +-/"[self.modifier]) * abs(self.modifierOffset) + "."+self.getPluckRendering()
	#
	#		Modify current note
	#
	def modify(self,modifier,newPosition):
		currentPos = None 												# figure out note adjusting
		for i in range(0,5):
			if self.fretting[i] is not None:
				if currentPos is not None:
					raise MusicException("Can only modify a single note")
				currentPos = self.fretting[i]
		if currentPos is None:
			raise MusicException("No note to modify")
		self.modifierOffset = newPosition - currentPos
		self.modifier = Note.SLIDE 
		if modifier == "-":
			self.modifier = Note.HAMMERON if self.modifierOffset >= 0 else Note.PULLOFF
	#
	#		Convert to string
	#
	def toString(self):
		return "".join([self._toString(x) if x is not None else "x" for x in self.fretting])+self.getPluckToString()
	#
	def _toString(self,fret):
		if self.modifier == Note.NORMAL:
			return str(fret) 
		return str(fret)+("/" if self.modifier == Note.SLIDE else "-")+str(fret+self.modifierOffset)

Note.NORMAL = 0															# types.
Note.HAMMERON = 1
Note.PULLOFF = 2
Note.SLIDE = 3

# ***************************************************************************************************
#
#								Brush, derived from current fretting
#
# ***************************************************************************************************

class Brush(Note):
	def __init__(self,currentFretting,brushStrings = 3):
		newDef = "".join(["0" if x is None else self.getFrettingEncode()[x] for x in currentFretting[:brushStrings]])		
		Note.__init__(self,newDef)

if __name__ == "__main__":
	rs = BeatRest()
	print(rs.render())
	rs.setPluck()
	print(rs.render())
	print("--------------------------------------------")
	nt = Note("x34")
	print(nt.render(),nt.getFretting())
	nt.setPluck()
	print(nt.render(),nt.getFretting())
	print("--------------------------------------------")
	nt = Note("x1")
	print(nt.render(),nt.getFretting())
	nt.modify("-",5)
	print(nt.render(),nt.getFretting())
	nt.setPluck()
	print(nt.render(),nt.getFretting())
	nt.setChord("c#m")
	print(nt.render(),nt.getFretting())
	print("--------------------------------------------")
	br = Brush(Note("x42").getFretting())
	print(br.render(),br.getFretting())
