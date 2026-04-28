echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 54020 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 7396) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 26116) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 1496) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 17132) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47996) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 25864)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-47996.bat"
