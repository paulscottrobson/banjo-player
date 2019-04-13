# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Class representing a bar of music
#		Date:		14th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from musicex import *

# ***************************************************************************************************
#
#									Class representing a single bar
#
# ***************************************************************************************************

class Bar(object):
	#
	def __init__(self,size = 8):
		self.fretting = [] 							 							# fretting each note
		for i in range(0,size):
			self.fretting.append(["."] * 5)
		self.modifiers = [ None ] * size 										# modifier
		self.modifierCount = [ 0 ] * size 										# modifier count.		
		self.chords = [ "" ] * size 											# display chord
		self.pos = 0 															# position in bar
		self.lastNote = None													# last note set.
	#
	#		Get and Update position in bar
	#
	def getPos(self):
		return self.pos
	def movePos(self,offset):
		self.pos += offset
	#
	#		Set Note/Notes at current position.
	#
	def setNotes(self,fretting,string = 1):
		fretting = fretting.lower().strip()
		if self.pos < 0 or self.pos >= len(self.fretting):						# validate position
			raise MusicException("Bar position out of range "+str(self.pos))
		for f in fretting:														# for each given character.
			if f != "." and Bar.FRETTING.find(f) < 0:							# validate fretting value
				raise MusicException("Bad fretting '{0}'".format(f))
			if string < 1 or string > 5:										# validate string.
				raise MusicException("Bad string "+str(string))
			self.fretting[self.pos][string-1] = f 								# update fretting.
			string += 1															# next string
		self.lastNote = self.pos 												# remember last note.
	#
	#		Set a Pinch at current position.
	#
	def setPinch(self):
		self.setNotes("0...0")
	#
	#		Set display chord
	#
	def setDisplayChord(self,display):
		if self.pos < 0 or self.pos >= len(self.fretting):						# validate position
			raise MusicException("Bar position out of range "+str(self.pos))
		self.chords[self.pos] = display
	#
	#		Apply a modifier to the current position.
	#
	def modify(self,modifier):
		if self.lastNote is None:												# something to modify ?
			raise MusicException("No note defined to modify")
		if modifier != "+" and modifier != "-" and modifier != "/":				# validate modification
			raise MusicException("Bad modifier '{0}'".format(modifier))
		if self.modifiers[self.lastNote] is not None:							# can only do one !
			if self.modifiers[self.lastNote] != modifier:
				raise MusicException("Modifier changed")
		self.modifiers[self.lastNote] = modifier 								# update modification.
		self.modifierCount[self.lastNote] += 1
	#
	#		Render in ASCII .... poorly
	#
	def toString(self):
		l = ""
		for s in range(0,5):													
			l = l + "|----"
			for i in range(0,8):
				l = l + (self.fretting[i][s] if self.fretting[i][s] != "." else ".")
				if self.modifiers[i] is None or self.fretting[i][s] == ".":
					l = l + "----"
				else:
					l = l + (self.modifiers[i]*self.modifierCount[i])+("-"*(4-self.modifierCount[i]))
			l = l + "|\n"
		return l.strip()
	#
	#		Render the bar in .plux format.
	#
	def render(self):
		return "|"+".".join([self.__renderNote(n) for n in range(0,len(self.fretting))])
	#
	def __renderNote(self,n):
		notes = "".join([str(i+1)+chr(Bar.FRETTING.find(self.fretting[n][i])+97) for i in range(0,5) if self.fretting[n][i] != "."])
		if self.modifiers[n] is not None:
			notes += (self.modifiers[n]*self.modifierCount[n])
		if self.chords[n] != "":
			notes = "("+self.chords[n]+")"+notes
		return notes

Bar.FRETTING = "0123456789tewhufs"												# fretting values.

if __name__ == "__main__":
	b = Bar()
	b.setNotes("t",4)
	b.movePos(2)
	b.setPinch()
	b.movePos(2)
	b.setNotes("1",3)
	b.setNotes("2",2)
	b.modify("+")
	b.modify("+")

	print()
	print(b.fretting)
	print()
	print(b.toString())
	print()
	print(b.render())