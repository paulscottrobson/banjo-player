# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		note.py
#		Purpose:	Note class
#		Date:		12th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from musicex import *

# ***************************************************************************************************
#
#										Base Note Class
#
# ***************************************************************************************************

class BaseNote(object):
	def __init__(self):
		self.pluck = False
	#
	def render(self):
		ending = "." if not self.pluck else self.note(5,0)
		return self.renderNote()+"."+ending
	#
	def addPluck(self):
		self.pluck = True
	#
	def note(self,stringNumber,fretting):
		self.validate(stringNumber,fretting)
		return chr(stringNumber+48)+chr(fretting+97)
	#
	def validate(self,stringNumber,fretting):
		if stringNumber < 1 or stringNumber > 5:
			raise MusicException("Bad string "+str(stringNumber))
		if fretting < 0 or fretting > 20:
			raise MusicException("Bad fretting "+str(fretting))

BaseNote.NOTES = "0123456789tewhuvxsgn"

# ***************************************************************************************************
#
#										Single Rest Class
#
# ***************************************************************************************************

class RestNote(BaseNote):
	def renderNote(self):
		return "."
	#
	def toString(self):
		return ".|.|.|.|."

# ***************************************************************************************************
#
#											Single Note
#
# ***************************************************************************************************

class Note(BaseNote):
	def __init__(self,stringNumber,fretting):
		self.validate(stringNumber,fretting)
		self.stringNumber = stringNumber
		self.fretting = fretting
		BaseNote.__init__(self)
	#
	def renderNote(self):
		return self.note(self.stringNumber,self.fretting)
	#
	def toString(self):
		result = [ "." ] * 5
		result[self.stringNumber-1] = str(self.fretting)
		return "|".join(result)

# ***************************************************************************************************
#
#											Brush Note
#
# ***************************************************************************************************

class BrushNote(BaseNote):
	def __init__(self,fretting,brushCount = 3):
		self.fretting = [x for x in fretting][:brushCount]
		BaseNote.__init__(self)
	#
	def renderNote(self):
		return "".join([self.note(stringNumber,self.fretting[stringNumber-1]) for stringNumber in range(1,1+len(self.fretting))])
	#		
	def toString(self):
		notes = [str(x) for x in self.fretting]
		while len(notes) < 5:
			notes.append(".")
		return "|".join(notes)

if __name__ == "__main__":
	rn = RestNote()
	print(rn.render(),rn.toString())
	nt = Note(2,4)
	print(nt.render(),nt.toString())
	bn = BrushNote([11,12,13,14,15],3)
	print(bn.render(),bn.toString())

