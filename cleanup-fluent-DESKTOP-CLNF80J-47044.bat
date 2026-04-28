echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 64416 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 22992) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 45508) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 29616) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 22768) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 47044) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 24060)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-47044.bat"
