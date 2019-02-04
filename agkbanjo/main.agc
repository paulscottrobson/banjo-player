SetErrorMode(2)
#constant SCWIDTH 1024
#constant SCHEIGHT 768
#constant DPHEIGHT 640

#include "source/bar.agc"
#include "source/bardisplay.agc"
#include "source/music.agc"
#include "source/renderers/fretrenderer.agc"


SetWindowTitle( "agkbanjo" )
SetWindowSize( SCWIDTH, SCHEIGHT, 0 )
SetWindowAllowResize( 1 ) // allow the user to resize the window
SetVirtualResolution( SCWIDTH, SCHEIGHT ) // doesn't have to match the window
SetOrientationAllowed( 1, 1, 1, 1 ) // allow both portrait and landscape on mobile devices
SetSyncRate( 30, 0 ) // 30fps instead of 60 to save battery
SetScissor( 0,0,0,0 ) // use the maximum available screen space, no black borders
UseNewDefaultFonts( 1 ) // since version 2.0.22 we can use nicer default fonts

background = CreateSprite(LoadSubImage(LoadImage("sprites.png"),"background"))
SetSpritePosition(background,0,0)
SetSpriteSize(background,SCWIDTH,SCHEIGHT)
SetSpriteDepth(background,9999)

demobar as Bar 
Bar_Initialise(demobar,0,4)
dispInfo as BarDisplayInfo
BarDisplayInfo_Initialise(dispInfo,demoBar.barNumber)
p as BarParameters
p.count = 12
FretRenderer_Command(CMD_INITIALISE,demobar,dispInfo,p)
FretRenderer_Command(CMD_CREATE,demobar,dispInfo,p)
//FretRenderer_Command(CMD_DESTROY,demobar,dispInfo,p)

while not GetRawKeyState(27)
    Print( ScreenFPS() )
    Sync()
endwhile
