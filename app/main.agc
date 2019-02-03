#constant DEBUG 1
SetErrorMode(2)
SetWindowTitle( "agkbanjo" )
SetWindowSize( 1024, 768, 0 )
SetWindowAllowResize( 1 ) // allow the user to resize the window
SetVirtualResolution( 1024, 768 ) // doesn't have to match the window
SetOrientationAllowed( 1, 1, 0, 0 ) // allow both portrait and landscape on mobile devices
SetSyncRate( 30, 0 ) // 30fps instead of 60 to save battery
SetScissor( 0,0,0,0 ) // use the maximum available screen space, no black borders
UseNewDefaultFonts( 1 ) // since version 2.0.22 we can use nicer default fonts
SetClearColor(255,255,255)

#include "source/bar.agc"

bDemo as Bar
Bar_Initialise(bDemo,330,100,500,300)
bDemo.notes[0].fretting[5] = 1
Bar_Draw(bDemo)

bDemo2 as Bar
Bar_Initialise(bDemo2,10,110,250,125)
Bar_Draw(bDemo2)

while not GetRawKeyState(27) 
    Print( ScreenFPS() )
    Sync()
endwhile
