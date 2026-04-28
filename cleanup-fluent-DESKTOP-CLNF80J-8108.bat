echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 65518 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 23300) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 34156) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 28548) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 46772) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 8108) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 36768)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-8108.bat"
