// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		bar.agc
//		Purpose:	Bar class
//		Date:		4th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

#constant BAR_DONTPLAY		(-1)								// Fretting value for not playing

// ***************************************************************************************************
//											  Note structure
// ***************************************************************************************************

type Note
	isPlayed as integer 										// Non zero if actually plucked this time.
	fretting as integer[5]										// Fretting for strings 1..5
endtype

// ***************************************************************************************************
//												 Bar class
// ***************************************************************************************************

type Bar
	barNumber as integer 										// Bar number (from 0)
	beats as integer 											// Beats in a bar
	notes as Note[1]											// Notes in the bar (from 0)
endtype

// ***************************************************************************************************
//											  Initialise a bar
// ***************************************************************************************************

function Bar_Initialise(this ref as Bar,barNumber as integer,beats as integer)
	this.barNumber = barNumber									// Copy information in.
	this.beats = beats
	this.notes.length = beats * 2 - 1							// Assume 2 beats per note
	for i = 0 to this.notes.length								// Clear all fretting
		for s = 1 to 5
			this.notes[i].fretting[s] = BAR_DONTPLAY
			if Random(1,4) > 1 then this.notes[i].fretting[s] = Random(0,5) 
		next s
		this.notes[i].isPlayed = 0 
	next i
endfunction

