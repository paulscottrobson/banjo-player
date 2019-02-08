// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		readfile.agc
//		Purpose:	Platform independent file reader
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

// ***************************************************************************************************
//				Read a file in, return without comments, lines seperated by ~
// ***************************************************************************************************

function File_Read(sourceFile as string)
	SetFolder("")												// root folder
	SetFolder("music")											// music folder
	contents$ = ""
	OpenToRead(1,sourceFile)
	while not FileEOF(1)
		line$ = ReadLine(1)
		if left(line$,2) <> "//" then contents$ = contents$ + line$ +"~"
	endwhile
	CloseFile(1)
	SetFolder("")
	SetFolder("media")
endfunction contents$
