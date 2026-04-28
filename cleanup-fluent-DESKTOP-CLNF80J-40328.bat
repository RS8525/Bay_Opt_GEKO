echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 51492 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47968) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 48724) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 21172) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47072) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 40328) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 5588)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-40328.bat"
