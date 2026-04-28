echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 56146 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47956) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 48824) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 3396) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 43836) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 43796) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 36688)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-43796.bat"
