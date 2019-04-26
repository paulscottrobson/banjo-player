@echo off
sh buildall.sh
echo 0 >..\agkbanjo\media\showmenu.txt
..\agkbanjo\agkbanjo
echo 1 >..\agkbanjo\media\showmenu.txt
