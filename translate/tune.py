# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		tune.py
#		Purpose:	Class representing a tune.
#		Date:		14th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,re,sys
from musicex import *
from bar import *

# ***************************************************************************************************
#
#										The basic tune class
#
# ***************************************************************************************************

class BaseTune(object):
	#
	#		Constructor loads in tune, decoding it using the superclass
	#
	def __init__(self,sourceFile):
		src = [x for x in open(sourceFile).readlines()]							# read source in.
		src = [x if x.find("#") < 0 else x[:x.find("#")] for x in src]			# remove comments
		src = [x.replace("\t"," ").strip().lower() for x in src]				# tidy up.
		self.equates = { "beats":"4","tempo":"80","step":"4" }					# default values.
		for equ in [x.replace(" ","") for x in src if x.find(":=") >= 0]:		# process equates
			equp = equ.split(":=")												# split up and verify
			if len(equp) != 2 or equp[0] == "":
				raise MusicException("Bad equate "+equp)
			self.equates[equp[0]] = equp[1]				
		src = [x if x.find(":=") < 0 else "" for x in src]						# remove all but music data
		self.barList = [] 														# bars in the tune.
		self.initialiseTranslation()											# initialise the translation
		for i in range(0,len(src)):												# scan through source.
			MusicException.Number = i + 1										# set line number.
			exp = self.expandMacros(src[i])										# expand the macros
			barSource = [x.strip() for x in exp.split("|") if x.strip()!=""]	# split up into bars
			for barSrc in barSource:											# for each bar
				self.barList.append(self.createBar(barSrc))						# convert it
				print("****"+barSrc+"****\n"+self.barList[-1].toString()+"\n\n")
	#
	#		Expand all the macros in a line.
	#
	def expandMacros(self,l):
		completed = False														# keep going while more
		while not completed and l != "":
			l = re.split("(\{.*?\})",l)											# split it up.
			completed = True
			for i in range(0,len(l)):											# look at all parts
				if l[i].startswith("{") and l[i].endswith("}"):					# found a macro
					if l[i][1:-1] not in self.equates:							# check it exists.
						raise MusicException("Cannot expand "+l[i])
					l[i] = self.equates[l[i][1:-1]]								# expand the macro.
					completed = False 											# may need one more pass
			l = "".join(l)														# back together.
		return l
	#
	#		Initialise anything needed for translation
	#
	def initialiseTranslation(self):
		pass
	#
	#		Create bar from a format specification.
	#
	def createBar(self,definition):
		return Bar()
	#
	#		Strip bar of information till empty.
	#
	def decodeBar(self,definition):
		definition = definition.strip()											# remove spaces
		bar = Bar()																# empty bar
		while definition != "":													# while more to do
			definition = self.decode(bar,definition).strip()					# take some definition off
		return bar

if __name__ == "__main__":
	src = """
#
#		test script
#
beats := 4
tempo := 100
step := 4
demo := abc

1 {demo} 2 {demo}
""".strip()
	h = open("__test.banjo","w")
	h.write(src)
	h.close()
	BaseTune("__test.banjo")







