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

// ***************************************************************************************************
//											Add music
// ***************************************************************************************************

function Music_Add(this ref as Music,tune as string)
	for i = 1 to CountStringTokens(tune,"|")
		bar$ = TruncateString(GetStringToken(tune,"|",i)," "+chr(8))
		if bar$ <> "" then Music_AddNewBar(this,bar$)
	next i
endfunction

// ***************************************************************************************************
//										Add an empty bar to the tune
// ***************************************************************************************************

function Music_AddNewBar(this ref as Music,defn as string)
	id = this.barCount
	inc this.barCount
	if this.barCount > this.bars.length 
		this.bars.length = this.bars.length + 20
	endif
	Bar_Initialise(this.bars[id],id,4)
	Bar_Load(this.bars[id],defn)
endfunction id

// ***************************************************************************************************
//									Load a .plux file in
// ***************************************************************************************************

function Music_AddFile(this ref as Music,sourceFile as string)
	source$ = File_Read(sourceFile)
	for i = 1 to CountStringTokens(source$,"~")
		line$ = GetStringToken(source$,"~",i)
		if left(line$,1) = "|" then Music_Add(this,mid(line$,2,-1))
	next i
endfunction


