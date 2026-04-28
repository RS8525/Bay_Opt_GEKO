echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 50466 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 43348) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 11884) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 44644) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 45792) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 43524) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 25620)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-43524.bat"
