# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar class
#		Date:		12th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re
from note import *
from musicex import *

# ***************************************************************************************************
#
#												Bar Class
#
# ***************************************************************************************************

class Bar(object):
	def __init__(self,barNumber,definition = "",initialFretting = [0,0,0,0,0],maxNotes = 4):
		self.barNumber = barNumber
		self.notes = []
		self.maxNotes = maxNotes
		self.startFretting = initialFretting
		if definition != "":
			self.endFretting = self.loadBar(definition,self.startFretting)
	#
	def loadBar(self,definition,fretting):
		MusicException.Number = self.barNumber
		for p in [x.strip() for x in definition.split(" ") if x.strip() != ""]:
			m = re.match("^\\#(\\d+)$",p)
			if m is not None:
				newFretting = [x for x in (m.group(1)+"00000")[:5]]
				for i in range(0,5):
					fretting[i] = BaseNote.NOTES.find(newFretting[i])
					if fretting[i] < 0:
						raise MusicEx("Bad fretting "+m.group(1))
			else:
				if len(self.notes) == self.maxNotes:
					raise MusicException("Too many notes in bar.")
				self.notes.append(self.noteFactory(p,fretting))
	#
	def noteFactory(self,df,fretting):
		if df == "&":
			return RestNote()
		#
		if re.match("^[1-5]\\.?$",df) is not None:
			note = Note(int(df[0]),fretting[int(df[0])-1])
			if df.endswith("."):
				note.addPluck()
			return note
		#
		if re.match("^\\!\\.?$",df) is not None:
			note = BrushNote(fretting)
			if df.endswith("."):
				note.addPluck()
			return note
		#			
		raise MusicException("Unknown note definition "+df)
	#
	def render(self):
		render = "".join([x.render() for x in self.notes])
		return "." if render == "" else render
	#
	def toString(self):
		return "\n".join(self.__toString(s) for s in range(1,6))
	#
	def __toString(self,stringNumber):
		return "".join(["   {0:6}{1:3}".format(s.toString().split("|")[stringNumber-1],"0" if s.pluck and stringNumber == 5 else ".") for s in self.notes]).replace(" ","-")

if __name__ == "__main__":
	br = Bar(1,"#4561 1 4 & #0 4.")			
	print(br.render())
	print(br.toString())
	print("\n\n")

	br = Bar(2,"#1234 1 4 &  !.")			
	print(br.render())
	print(br.toString())
	print("\n\n")
