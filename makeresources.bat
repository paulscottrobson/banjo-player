@echo off
rem
rem		Builds resources where required and copies them into applications media directory.
rem
copy resources\fonts\*.ttf agkbanjo\media
copy resources\notes\sounds\*.ogg agkbanjo\media\sounds
cd resources\graphics
python makeatlas.py
cd ..\..
copy resources\graphics\sprites* agkbanjo\media
echo "Built resources"
