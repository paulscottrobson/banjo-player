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

# ***************************************************************************************************
#
#											Base class
#
# ***************************************************************************************************

class BaseMusicEntity(object):
	def __init__(self):
		self.chord = None 												# chord that can override
	#
	#		Set the chord for this entity object
	#
	def setChord(self,chord):
		self.chord = chord.strip().lower()
	#
	#		Render the chord, returns None if no chord or the final render as a half beat
	#
	def getRenderedChord(self,keys):
		if self.chord is None:											# no chord here.
			return None
		if "chord_"+self.chord not in keys:								# check chord defined
			raise MusicException("Unknown chord "+self.chord)
		play = self.textToChordArray(keys["chord_"+self.chord])			# get notes to play here.
		play[4] = None 													# do not strum string 5
		return play
	#
	#		Convert a string of frets with x prefixes to a note list with None,0-
	#
	def textToChordArray(self,definition):
		notes = [ None ] * 5											# output notes
		currentString = 0 												# current position
		definition = definition.lower().strip()							# preprocess
		for d in definition:
			if d == 'x':												# skip a string.
				currentString += 1
			else:														# fret position as text
				fret = self.getFretting().find(d)						# find it
				if fret < 0 or currentString >= 5:						# validate.
					raise MusicException("Chord {0} is ill defined".format(self.chord))
				notes[currentString] = fret 							# store it
				currentString += 1
		return notes
	#
	#		render an array of notes.
	#
	def noteArrayRender(self,notes):
		render = ""
		for string in range(0,5):
			render += self.noteRender(string+1,notes[string])
		return render
	#
	#		Get the fretting search string.
	#
	def getFretting(self):
		return BaseMusicEntity.FRETTING
	#
	#		Default modifier, which doesn't work.
	#
	def modify(self,modifier,count):
		raise MusicException("Modifier unsupported on entity")
	#
	#		Dummies as this class is abstract
	#
	def getNoteSize(self):
		assert False,"Abstract method"
	def get(self):
		assert False,"Abstract method"

BaseMusicEntity.FRETTING = "0123456789tlwhufsve"				

# ***************************************************************************************************
#
#					Single note - can be a single pluck or collection thereof
#					can be modified using pulloffs or hammerons or slides.
#
# ***************************************************************************************************

class Note(BaseMusicEntity):
	def __init__(self,noteDefinition):
		BaseMusicEntity.__init__(self)
		self.notes = self.textToChordArray(noteDefinition)				# original state
		self.modifier = Note.NORMAL 									# modifier
		self.modifierOffset = 1
		self.modifierLength = 0
	#
	#		Get note information
	#
	def get(self):
		info = [x for x in self.notes]
		info.append(1 if self.modifier == Note.NORMAL else self.modifierLength)
		info.append(" +-/"[self.modifier])
		info.append(self.modifierOffset)
		return info
	#
	#		Length of note in half beats. Extended if hammer off/pull on to 2.
	#
	def getNoteSize(self):
		return 1 if self.modifier is Note.NORMAL else self.modifierLength
	#
	#		Modify the note to be a slide, hammeron or pull off over two. The count is 
	#		an absolute value up or down, direction defined by the type.
	#
	def modify(self,modifier,count):
		self.modifier = modifier
		self.modifierOffset = count
		self.modifierLength = 2
	#
	#		Modify the note to be modified over *one* note.
	#
	def makeFastModifier(self):
		self.modifierLength = 1
	#
	#		Convert to string
	#
	def toString(self):
		s = "-".join(["X" if self.notes[n] is None else str(self.notes[n]) for n in range(0,5)])
		if self.modifier != Note.NORMAL:
			s = s + " " + ("/" if self.modifier == Note.SLIDE else "-")+str(self.modifierOffset)+":"+str(self.modifierLength)
		return "["+s+"]"

Note.NORMAL = 0															# types.
Note.HAMMERON = 1
Note.PULLOFF = 2
Note.SLIDE = 3

# ***************************************************************************************************
#
#											Half Beat Rest
#
# ***************************************************************************************************

class HalfBeatRest(BaseMusicEntity):
	#
	#		Get Half Beat equivalence
	#
	def get(self):
		return [ None,None,None,None,None,1,".",0 ]
	#
	#		Length of note in half beats.
	#
	def getNoteSize(self):
		return 1
	#
	#		String conversion
	#
	def toString(self):
		return "[rest]"

if __name__ == "__main__":
	bs = BaseMusicEntity()
	print(bs.getRenderedChord({"chord_c":"0200"}))
	bs.setChord("C")
	print(bs.getRenderedChord({"chord_c":"0200"}))
	print("--------------------------------------------")
	rs = HalfBeatRest()
	print(rs.get(),rs.getNoteSize())
	print(rs.toString())
	print("--------------------------------------------")
	nt = Note("x34")
	print(nt.get(),nt.getNoteSize())
	print(nt.toString())
	print("--------------------------------------------")
	nt.modify(Note.SLIDE,3)
	print(nt.get(),nt.getNoteSize())	
	print(nt.toString())
	print("--------------------------------------------")
	nt.makeFastModifier()
	print(nt.get(),nt.getNoteSize())	
	print(nt.toString())

