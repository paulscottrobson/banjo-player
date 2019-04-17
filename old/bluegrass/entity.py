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
		if self.chord not in keys:										# check chord defined
			raise MusicException("Unknown chord "+self.chord)
		play = self.textToChordArray(keys[self.chord])					# get notes to play here.
		play[4] = None 													# do not strum string 5
		return self.noteArrayRender(play)								# and render it.
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
	#		render a single note
	#
	def noteRender(self,string,fret):
		if string is None or fret is None:
			return ""
		else:
			return str(string)+chr(fret+97)
	#
	#		Get the fretting search string.
	#
	def getFretting(self):
		return "0123456789tlwhufsve"				
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
	def render(self):
		assert False,"Abstract method"

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
	#
	#		Convert note to final format, at one half beat
	#
	def render(self):
		render = self.noteArrayRender(self.notes)						# "normal" note
		if self.modifier != Note.NORMAL:								# modify it.
			render += (" +-/"[self.modifier]) * self.modifierOffset
		return render + ("." * self.getNoteSize())						# pad out to length
	#
	#		Length of note in half beats. Extended if hammer off/pull on to 2.
	#
	def getNoteSize(self):
		return 1 if self.modifier is Note.NORMAL else 2
	#
	#		Modify the note to be a slide, hammeron or pull off.
	#
	def modify(self,modifier,count):
		self.modifier = modifier
		self.modifierOffset = count


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
	#		Convert note to final format, at one half beat
	#
	def render(self):
		return "."
	#
	#		Length of note in half beats.
	#
	def getNoteSize(self):
		return 1

if __name__ == "__main__":
	bs = BaseMusicEntity()
	print(bs.getRenderedChord({"c":"0200"}))
	bs.setChord("C")
	print(bs.getRenderedChord({"c":"0200"}))
	print("--------------------------------------------")
	rs = HalfBeatRest()
	print(rs.render(),rs.getNoteSize())
	print("--------------------------------------------")
	nt = Note("x34")
	print(nt.render(),nt.getNoteSize())
	print("--------------------------------------------")
	nt.modify(Note.SLIDE,3)
	print(nt.render(),nt.getNoteSize())
	