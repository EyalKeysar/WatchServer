@echo off

start cmd /k "cd /d C:\Dev\WatchServer\src && py worker.py"
start cmd /k "cd /d C:\Dev\Watchapp && py app.py"

exit
