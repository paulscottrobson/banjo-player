@echo off
rem
rem		Builds resources where required and copies them into applications media directory.
rem
copy fonts\*.ttf agkbanjo\media
copy notes\sounds\*.ogg agkbanjo\media
cd graphics
python makeatlas.py
cd ..
copy graphics\sprites* agkbanjo\media
echo "Built resources"
