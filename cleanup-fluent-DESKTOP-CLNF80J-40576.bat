echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\tell.exe" DESKTOP-CLNF80J 49993 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v261\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 35764) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 25140) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 37496) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 36648) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 40576) 
if /i "%LOCALHOST%"=="DESKTOP-CLNF80J" (%KILL_CMD% 41880)
del "C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO\cleanup-fluent-DESKTOP-CLNF80J-40576.bat"
