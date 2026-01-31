@echo off
echo Installing LavaScript Environment...
assoc .ls=LavaScriptFile
ftype LavaScriptFile=python.exe "%1" %*
echo Done!
pause
