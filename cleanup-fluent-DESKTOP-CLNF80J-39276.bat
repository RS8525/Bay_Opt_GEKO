echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 51351 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 32260) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 24496) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 12648) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 40756) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 39276) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 40416)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-39276.bat"
