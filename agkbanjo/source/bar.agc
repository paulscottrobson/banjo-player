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

#constant NOTE_NORMAL 		(0)									// Normal note
#constant NOTE_HAMMERON		(1)									// Modifiers
#constant NOTE_PULLOFF 		(2)
#constant NOTE_SLIDE		(3)

// ***************************************************************************************************
//											  Note structure
// ***************************************************************************************************

type Note
	isPlayed as integer 										// Non zero if actually plucked this time.
	fretting as integer[5]										// Fretting for strings 1..5
	modifer as integer 											// Normal or hammer on/pull off etc.
	modifierString as integer 									// String to which this applies.
	newFretting as integer 										// New fretting for hammer on or slide.
	chordLabel as string 										// Chord Label, if any.
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
		this.notes[i].isPlayed = 0 								// Not played yet
		this.notes[i].modifer = NOTE_NORMAL						// Normal type of note
		this.notes[i].modifierString = 0	
		this.notes[i].newFretting = 0
		this.notes[i].chordLabel = ""
		for s = 1 to 5											// Not playing any strings, yet.
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
	barDesc = Upper(barDesc)
	while barDesc <> ""
		d$ = left(barDesc,1)
		barDesc = mid(barDesc,2,-1)
		if d$ >= "1" and d$ <= "5"
			currentString = Val(d$)
		endif
		if d$ >= "A" and d$ <= "Z"
			this.notes[currentNote].fretting[currentString] = asc(d$) - asc("A")
			this.notes[currentNote].newFretting = this.notes[currentNote].fretting[currentString]
			this.notes[currentNote].modifer = NOTE_NORMAL
			this.notes[currentNote].isPlayed = 1
		endif
		if d$ = "/" then inc currentNote
		if d$ = "+" or d$ = "-" or d$ = ">"
			this.notes[currentNote].modifierString = currentString
			if d$ = "+" or d$ = ">" then inc this.notes[currentNote].newFretting
			if d$ = "-" then dec this.notes[currentNote].newFretting
			if d$ = "+" then this.notes[currentNote].modifer = NOTE_HAMMERON
			if d$ = "-" then this.notes[currentNote].modifer = NOTE_PULLOFF
			if d$ = ">" then this.notes[currentNote].modifer = NOTE_SLIDE
		endif
		if d$ = "("
			p = FindString(barDesc,")")
			chord$ = left(barDesc,p-1)
			this.notes[currentNote].chordLabel = upper(left(chord$,1))+lower(mid(chord$,2,-1))
			barDesc = mid(barDesc,p+1,-1)
		endif
	endwhile
endfunction

// ***************************************************************************************************
//								Get note representation as a string
// ***************************************************************************************************

function Bar_GetNoteText(this ref as bar,note as integer,strn as integer)
	note$ = str(this.notes[note].fretting[strn])
	if strn = this.notes[note].modifierString
		select this.notes[note].modifer
			case NOTE_PULLOFF:
				note$ = note$+"-"+str(this.notes[note].newFretting)
			endcase
			case NOTE_SLIDE:
				note$ = note$+"/"+str(this.notes[note].newFretting)
			endcase
			case NOTE_HAMMERON:
				note$ = note$+"-"+str(this.notes[note].newFretting)
			endcase
		endselect
	endif
endfunction note$

// ***************************************************************************************************
//										Use double width note
// ***************************************************************************************************

function Bar_IsNoteDoubleWidth(this ref as bar,note as integer,strn as integer)
	isWide = 0
	if strn = this.notes[note].modifierString
		m = this.notes[note].modifer
		isWide = m = NOTE_PULLOFF or m = NOTE_SLIDE or m = NOTE_HAMMERON
	endif
endfunction isWide
