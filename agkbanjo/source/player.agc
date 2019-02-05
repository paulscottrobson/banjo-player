// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		player.agc
//		Purpose:	Tune player
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type PlayerGlobals
	tuning as integer[6]
	baseID as integer
	metronome as integer
endtype

global plg as PlayerGlobals

// ***************************************************************************************************
//								Load required notes for this trune
// ***************************************************************************************************

function Player_Initialise(music ref as Music)	
	
	plg.baseID = 100
	
	plg.tuning[5] = 20 					// G4
	plg.tuning[4] = 3					// D3
	plg.tuning[3] = 8					// G3
	plg.tuning[2] = 12					// B3
	plg.tuning[1] =	15					// D4
	
	for bar = 0 to music.barCount
		for note = 0 to music.bars[bar].beats * 2 - 1
			for strn = 1 to 5
				fret = music.bars[bar].notes[note].fretting[strn]
				noteid = plg.tuning[strn] + fret
				if GetSoundExists(noteid + plg.baseID) = 0 
					LoadSoundOGG(noteid + plg.baseID,str(noteid)+".ogg")
				endif
			next strn
		next note
	next bar

	plg.metronome = LoadSoundOGG("metronome.ogg")
	
endfunction

// ***************************************************************************************************
//									Play the metronome sound
// ***************************************************************************************************

function Player_PlayMetronome()
	PlaySound(plg.metronome)
endfunction

// ***************************************************************************************************
//						Play a note which can be up to 5 strings at once
// ***************************************************************************************************

function Player_PlayNote(note ref as Note)
	if note.isPlayed <> 0
		for s = 1 to 5
			if note.fretting[s] <> BAR_DONTPLAY
				//debug = debug + "S"+str(s)+"."+str(note.fretting[s])+" "
				PlaySound(plg.tuning[s] + note.fretting[s] + plg.baseID)
			endif
		next s
	endif
endfunction
