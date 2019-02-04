// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		manager.agc
//		Purpose:	Render Manager
//		Date:		4th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type Manager_Global_Info
	music as Music
	renderID as integer
	displayInfo as BarDisplayInfo[1]
endtype

global mgr as Manager_Global_Info

// ***************************************************************************************************
//								Initialise Rendering Manager
// ***************************************************************************************************

function Manager_Initialise(music ref as Music)
	mgr.music = music
	mgr.renderID = -1
	mgr.displayInfo.length = music.barCount
endfunction

// ***************************************************************************************************
//									Switch to a new renderer
// ***************************************************************************************************

function Manager_SwitchRenderer(newID as integer)
	if mgr.renderID >= 0 										// If already one being displayed
		for i = 0 to mgr.music.barCount-1						// Hide any visible displays
			if mgr.displayInfo[i].isDrawn <> 0 
				Manager_Command(CMD_HIDE,mgr.music.bars[0],mgr.displayInfo[0],p)
				mgr.displayInfo[i].isDrawn = 0
			endif
		next i
																// Remove the background.
		Manager_Command(CMD_DESTROY,mgr.music.bars[0],mgr.displayInfo[0],p)
	endif
	mgr.renderID = newID										// Update ID
	for i = 0 to mgr.music.barCount-1							// Initialise all the displayinfo structures.
		BarDisplayInfo_Initialise(mgr.displayInfo[i],i)
	next i
	p as BarParameters 											// Set up parameters
	p.count = mgr.music.barCount 								// And then initialise and draw backgrounds
	Manager_Command(CMD_INITIALISE,mgr.music.bars[0],mgr.displayInfo[0],p)
	Manager_Command(CMD_CREATE,mgr.music.bars[0],mgr.displayInfo[0],p)
	Manager_MoveRenderTo(0)										// Move the rendering position to the origin.
endfunction

// ***************************************************************************************************
//									Move all rendered objects
// ***************************************************************************************************

function Manager_MoveRenderTo(pos as integer)
	p as BarParameters
	p.pos = pos
	for i = 0 to mgr.music.barCount-1
		if Manager_Command(CMD_VISIBLE,mgr.music.bars[i],mgr.displayInfo[i],p) <> 0
			Manager_Command(CMD_SHOW,mgr.music.bars[i],mgr.displayInfo[i],p)
		else
			Manager_Command(CMD_HIDE,mgr.music.bars[i],mgr.displayInfo[i],p)
		endif
	next i
endfunction

// ***************************************************************************************************
//									Dispatch rendering command
// ***************************************************************************************************

function Manager_Command(command as integer,bar ref as Bar,displayInfo ref as BarDisplayInfo,params ref as BarParameters)
	r = FretRenderer_Command(command,bar,displayInfo,params)
endfunction r
