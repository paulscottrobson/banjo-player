// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		bardisplay.agc
//		Purpose:	Bar Display Information structure
//		Date:		4th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type BarDisplayInfo
	baseID as integer 											// Base ID of this bar
	isDrawn as integer											// True if is already drawn.
	x as integer 												// Currently displayed position in whole units
	y as integer 												// (if drawn)
endtype

#constant 	CMD_INITIALISE		(0)								// Commands to 'display driver'
#constant 	CMD_CREATE			(1)
#constant 	CMD_DESTROY			(2)
#constant 	CMD_VISIBLE			(3)
#constant 	CMD_SHOW			(4)
#constant	CMD_HIDE			(5)

#constant 	CMD_ID				(9000)							// Base Sprite ID for background stuff

type BarParameters												// Structure used to pass information to messages.
	x as integer
	y as integer
	count as integer
endtype

// ***************************************************************************************************
//								Initialise a bar display info object
// ***************************************************************************************************

function BarDisplayInfo_Initialise(this ref as BarDisplayInfo,barNumber as integer)
	this.baseID = 10000 + barNumber * 200						// Allocate object IDs
	this.isDrawn = 0 											// Not currently drawn
	this.x = 0:this.y = 0
endfunction
