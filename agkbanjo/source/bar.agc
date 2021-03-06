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
	modifier as integer 										// Normal or hammer on/pull off etc.
	modifierString as integer 									// String to which this applies.
	modifierAdjust as integer 									// Amount by which modifier adjusts
	modifierLength as integer 									// one or two note length modifier ?
	chordLabel as string 										// Chord Label, if any.
endtype

// ***************************************************************************************************
//												 Bar class
// ***************************************************************************************************

type Bar
	barNumber as integer 										// Bar number (from 0)
	beatsInBar as integer 										// Beats in a bar
	notesInBar as integer 										// Notes in a bar
	notes as Note[1]											// Notes in the bar (from 0),.
endtype

// ***************************************************************************************************
//											  Initialise a bar
// ***************************************************************************************************

function Bar_Initialise(this ref as Bar,barNumber as integer,beats as integer)
	this.barNumber = barNumber									// Copy information in.
	this.beatsInBar = beats 									// Number of beats
	this.notesInBar = 8											// Number of notes
	if beats = 3 then this.notesInBar = 6
	this.notes.length = this.notesInBar							
	for i = 0 to this.notes.length								// Clear all fretting
		this.notes[i].isPlayed = 0 								// Not played yet
		this.notes[i].modifier = NOTE_NORMAL					// Normal type of note
		this.notes[i].modifierString = 0	
		this.notes[i].modifierAdjust = 0 
		this.notes[i].modifierLength = 2
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
			this.notes[currentNote].modifierAdjust = 0
			this.notes[currentNote].modifierLength = 2
			this.notes[currentNote].modifier = NOTE_NORMAL
			this.notes[currentNote].isPlayed = 1
		endif
		if d$ = "." then inc currentNote
		if d$ = "+" or d$ = "-" or d$ = "/"
			this.notes[currentNote].modifierString = currentString
			inc this.notes[currentNote].modifierAdjust 
			if d$ = "+" then this.notes[currentNote].modifier = NOTE_HAMMERON
			if d$ = "-" then this.notes[currentNote].modifier = NOTE_PULLOFF
			if d$ = "/" then this.notes[currentNote].modifier = NOTE_SLIDE
		endif
		if d$ = "=" then this.notes[currentNote].modifierLength = 1
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
		select this.notes[note].modifier
			case NOTE_PULLOFF:
				note$ = note$+"-"+str(this.notes[note].fretting[strn]-this.notes[note].modifierAdjust)
			endcase
			case NOTE_SLIDE:
				note$ = note$+"/"+str(this.notes[note].fretting[strn]+this.notes[note].modifierAdjust)
			endcase
			case NOTE_HAMMERON:
				note$ = note$+"-"+str(this.notes[note].fretting[strn]+this.notes[note].modifierAdjust)
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
		m = this.notes[note].modifier
		isWide = (m = NOTE_PULLOFF or m = NOTE_SLIDE or m = NOTE_HAMMERON) and (this.notes[note].modifierLength = 2)
	endif
endfunction isWide
