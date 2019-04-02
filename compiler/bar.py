# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar representation
#		Date:		1st April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

from musicex import *
import re

# ***************************************************************************************************
#
#											BAR Base Class
#
# ***************************************************************************************************

class Bar(object):
	#
	#		Initialise.
	#
	def __init__(self,barNumber,description,beats = 4,entryFretting = None):
		self.barNumber = barNumber
		self.description = description
		self.beats = beats
		self.initialFretting = entryFretting if entryFretting is not None else [ 0 ] * 5
		self.processDescription()
	#
	#		Convert the initial fretting/strings and the descriptor into a set of notes played
	#		at each half beat.
	#
	def processDescription(self):
		self.notes = [] 														# create empty note structure
		self.isUsed = [ False ] * 8												# checks if note played any 1/2 beat		
		for b in range(0,self.beats * 2):
			self.notes.append([None] * 5)										# note, modifier, count
		self.position = 0 														# 1/2 beat position
		self.fretting = [x for x in self.initialFretting]						# fretting.and strings
		self.lastNote = None 													# last note created
		desc = self.description.strip().lower() 								# preprocess.
		while desc != "":														# while something left
			desc = self.processOne(desc).strip()								# keep going
		self.finalFretting = [x for x in self.fretting] 						# remember final fretting/strings
	#
	#		Get end fretting
	#
	def getEndFretting(self):
		return self.finalFretting
	#
	#		Pluck one string.
	#
	def setPluck(self,pos,string):
		self.notes[pos][string-1] = [self.fretting[string-1],None,0]
		self.isUsed[pos] = True 	
		self.lastNote = pos
		return string
	#
	#		Set a fretting
	#
	def setFretting(self,string,fretPos):
		self.fretting[string-1] = fretPos
	#
	#		Convert to string
	#
	def toString(self):
		s = "Bar:{0} Beats:{1} Descriptor:\"{2}\" Output:\"{3}\"\n".format(self.barNumber,self.beats,self.description,self.toOutput())
		s = s + "Start Fretting:"+",".join([str(x) for x in self.initialFretting])
		s = s + " End Fretting:"+",".join([str(x) for x in self.finalFretting])+"\n"
		for st in range(0,5):
			s = s + "|"
			for be in range(0,self.beats * 2):
				pluck = self.notes[be][st]
				s = s + ("---.---" if pluck is None else ("---"+str(pluck[0])+"---")[:7])
			s = s + "|\n"
		return s
	#
	#		Convert to output format.
	#
	def toOutput(self):
		return ".".join([self.__renderNote(n) for n in range(0,len(self.notes))])
	#
	def __renderNote(self,pos):
		return "".join(["" if self.notes[pos][i] is None else self.__renderPluck(pos,i) for i in range(0,5)])
	#
	def __renderPluck(self,pos,strn):
		return str(strn+1)+chr(self.notes[pos][strn][0]+97)		


# ***************************************************************************************************
#
#										Bar that decodes BlueGrass
#
# ***************************************************************************************************

class BluegrassBar(Bar):
	#
	#		Process a single "command"
	#
	def processOne(self,d):
		#
		if d.startswith("."):													# skip 
			self.position += 1
			return d[1:]
		#
		if d.startswith("&"):													# & advance to next beat
			self.position = int((self.position+2)/2) * 2
			return d[1:]
		#
		if d[0] >= '1' and d[0] <= '5':											# 1-5 pluck string/advance
			self.setPluck(self.position,int(d[0]))
			self.position += 1
			return d[1:]
		#
		m = re.match("^\\#(["+Bar.FRETS+"]*)(.*)$",d)							# reset fretting.
		if m is not None:														# padded right with 0s.
			newFretting = [Bar.FRETS.find(x) for x in (m.group(1)+"00000")[:5]]
			for i in range(0,len(newFretting)):
				self.setFretting(i+1,newFretting[i])
			return m.group(2)
		#		
		raise MusicException("Cannot process '{0}'".format(d),self.barNumber)	# give up.

Bar.FRETS = "0123456789tlwhufxv"

if __name__ == "__main__":
	# So bluegrass stuff can be done like this
	b = BluegrassBar(1,"123 #56789 12345",4)
	print(b.toString())
	# and Wayne Erbsen's tunes like this.
	b1 = BluegrassBar(1,"#00370 3 && 4 &&")	
	print(b1.toString())
