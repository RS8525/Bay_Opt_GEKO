echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 60953 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 24444) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 41028) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 41208) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 46716) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 37468) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 31520)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-37468.bat"
