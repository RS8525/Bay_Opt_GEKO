echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 54790 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 46644) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 19696) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 19312) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 39896) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 35088) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 43592)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-35088.bat"
