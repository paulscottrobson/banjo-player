// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		program.agc
//		Purpose:	Main Program
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

global debug as string = "DBG:"

SetWindowTitle( "Banjo Trainer" )
SetWindowSize( SCWIDTH, SCHEIGHT, 0 )
SetWindowAllowResize( 1 ) // allow the user to resize the window
SetVirtualResolution( SCWIDTH, SCHEIGHT ) // doesn't have to match the window
SetOrientationAllowed( 1, 1, 1, 1 ) // allow both portrait and landscape on mobile devices
SetSyncRate( 60, 0 ) // 30fps instead of 60 to save battery
//SetScissor( 0,0,0,0 ) // use the maximum available screen space, no black borders
UseNewDefaultFonts( 1 ) // since version 2.0.22 we can use nicer default fonts

background = CreateSprite(LoadSubImage(LoadImage("sprites.png"),"background"))
SetSpritePosition(background,0,0)
SetSpriteSize(background,SCWIDTH,SCHEIGHT)
SetSpriteDepth(background,9999)

txt = CreateText("Written by Paul Robson (paul@robsons.org.uk) 2019 v"+VERSION)
SetTextFont(txt,LoadFont("rocko.ttf"))
SetTextSize(txt,SCWIDTH/60)
SetTextPosition(txt,SCWIDTH/2-GetTextTotalWidth(txt)/2,SCHEIGHT-GetTextTotalHeight(txt))

tune as Music
Music_Initialise(tune)
Music_AddFile(tune,"cripple.plux")
Manager_Initialise(tune)
Manager_SwitchRenderer(1)
Player_Initialise(tune)

//Manager_SwitchRenderer(0)

pos# = 0
lastTime = GetMilliseconds()

while not GetRawKeyState(27)
	// Elapsed time in milliseconds
	elapsed = GetMilliseconds() - lastTime						// Track time between frames.
	lastTime = GetMilliseconds()
	// Convert to a time in bars.
	elapsed# = elapsed / 1000.0 								// Actual elapsed time in seconds.
	beatsPerMin# = 60.0 										// Beats per minute
	beatsPerSec# = beatsPerMin# / 60.0 							// Beats per second
	beatsPerBar# = tune.bars[trunc(pos#)].beats 				// Beats per bar
	barsPerSec# = beatsPerSec# / beatsPerBar#					// Bars per second
	
	lastpos# = pos#												// Last position
	pos# = pos# + barsPerSec# * elapsed#						// New position
	if pos# >= tune.barCount 									// Off right hand end ?
		pos# = 0:lastpos# = 0									// Reset to start
	endif
	beats = tune.bars[trunc(pos#)].beats 						// How many beats in bar
	qb1 = trunc(lastpos# * beats * 2)							// Work out quarterbeat position
	qb2 = trunc(pos# * beats * 2)
	if qb1 <> qb2 or lastpos# = 0  								// Time for a note ?
		if mod(qb2,2) = 0 then Player_PlayMetronome()			// Play metronome
		Player_PlayNote(tune.bars[trunc(pos#)].notes[mod(qb2,beats*2)])
	endif
    Manager_MoveRenderTo(pos#)									// Update display position

    print(debug)
    print(pos#)
    Sync()
endwhile
