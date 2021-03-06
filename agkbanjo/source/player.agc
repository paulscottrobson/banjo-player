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
	pendingNote as integer
	pendingCount as integer
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
	
	if music.tuning = "gcgcd"
		plg.tuning[4] = 1 				// C3
		plg.tuning[2] = 13 				// C4
	endif
	
	for bar = 0 to music.barCount
		for note = 0 to music.bars[bar].notesInBar
			for strn = 1 to 5
				fret = music.bars[bar].notes[note].fretting[strn]
				if fret <> BAR_DONTPLAY
					noteid = plg.tuning[strn] + fret
					if GetSoundExists(noteid + plg.baseID) = 0 
						LoadSoundOGG(noteid + plg.baseID,"sounds/"+str(noteid)+".ogg")
					endif
				endif
			next strn
			ntype = music.bars[bar].notes[note].modifier
			if ntype = NOTE_HAMMERON or ntype = NOTE_PULLOFF or ntype = NOTE_SLIDE
				if ntype = NOTE_PULLOFF then notedir = -1 else notedir = 1
					s = music.bars[bar].notes[note].modifierString
					noteid = plg.tuning[s]+music.bars[bar].notes[note].fretting[s] + music.bars[bar].notes[note].modifierAdjust * notedir
					if GetSoundExists(noteid + plg.baseID) = 0 
						LoadSoundOGG(noteid + plg.baseID,"sounds/"+str(noteid)+".ogg")
					endif
			endif
		next note
	next bar

	plg.metronome = LoadSoundOGG("sounds/metronome.ogg")
	plg.pendingNote = -1
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

function Player_PlayNote(note ref as Note,fullNote as integer)
	if plg.pendingNote >= 0
		dec plg.pendingCount
		if plg.pendingCount = 0
			PlaySound(plg.pendingNote)
			plg.pendingNote = -1
		endif
	endif
	if fullNote <> 0 
		if note.isPlayed <> 0
			for s = 1 to 5
				if note.fretting[s] <> BAR_DONTPLAY
					rem debug = debug + str(note.fretting[s]+plg.tuning[s])+"."+str(s)+" "
					PlaySound(plg.tuning[s] + note.fretting[s] + plg.baseID)
				endif
			next s
		endif
		ntype = note.modifier
		if ntype = NOTE_HAMMERON or ntype = NOTE_PULLOFF or ntype = NOTE_SLIDE
			if ntype = NOTE_PULLOFF then notedir = -1 else notedir = 1
			plg.pendingNote = plg.baseID + plg.tuning[note.modifierstring]+note.fretting[note.modifierstring] + notedir * note.modifierAdjust
			plg.pendingCount = note.modifierLength
		endif
	endif
endfunction
