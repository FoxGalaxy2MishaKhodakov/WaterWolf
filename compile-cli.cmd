@echo off
color 2

call "%~dp0compile1.cmd"
call "%~dp0compile2.cmd"
call "%~dp0compile3.cmd"

echo WaterWolf was compiled successfully
pause
