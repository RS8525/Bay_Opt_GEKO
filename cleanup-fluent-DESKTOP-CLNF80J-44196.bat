echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 51215 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 43880) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 31620) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 41416) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 40568) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 44196) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 37260)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-44196.bat"
