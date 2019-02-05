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
		this.notes[i].isPlayed = 0 
		for s = 1 to 5
			this.notes[i].fretting[s] = BAR_DONTPLAY
		next s
	next i
endfunction

// ***************************************************************************************************
//								Load a definition into the bar.
// ***************************************************************************************************

function Bar_Load(this ref as Bar,barDesc as string)
	currentString = 0
	currentNote = 0
	for c = 1 to len(barDesc)
		d$ = mid(barDesc,c,1)
		if d$ >= "1" and d$ <= "5" then currentString = Val(d$)
		if d$ >= "A" and d$ <= "Z"
			this.notes[currentNote].fretting[currentString] = asc(d$) - asc("A")
			this.notes[currentNote].isPlayed = 1
			inc currentNote
		endif
	next c
endfunction
