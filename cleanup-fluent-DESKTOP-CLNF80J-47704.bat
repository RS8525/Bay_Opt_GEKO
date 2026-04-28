echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 51538 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 19644) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 45172) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 30676) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47544) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47704) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 31468)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-47704.bat"
