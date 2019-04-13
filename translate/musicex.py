# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		musicex.py
#		Purpose:	Exception class for Music Translation
#		Date:		14th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

# ***************************************************************************************************
#
#										Exception class
#
# ***************************************************************************************************

class MusicException(Exception):
	#
	def __init__(self,msg):
		self.errorMessage = msg
	#
	def getMessage(self):
		return "{0} ({1})".format(self.errorMessage,MusicException.Number)

MusicException.Number = 0

if __name__ == "__main__":
	MusicException.Number = 42
	print(MusicException("Test Error").getMessage())