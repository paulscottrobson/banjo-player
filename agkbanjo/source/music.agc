// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		music.agc
//		Purpose:	Class representing one tune.
//		Date:		4th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type Music
	defaultBPM as integer 										// Standard play rate
	barCount as integer 										// Number of bars
	bars as Bar[1]												// Bars
endtype

// ***************************************************************************************************
//											Initialise Music
// ***************************************************************************************************

function Music_Initialise(this ref as Music)
	this.defaultBPM = 40 										// Playing speed
	this.barCount = 0 											// Number of bars in tune
	this.bars.length = 20 										// Bar array is added in chunks
endfunction

