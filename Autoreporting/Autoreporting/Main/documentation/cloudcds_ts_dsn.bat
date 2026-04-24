@echo off
cls

echo Configure Data Sources for CloudCDS Top Secret
echo.

set dsn_name=CloudCDS_ts
set config_dsn=configdsn "SQL Server" "DSN=%dsn_name%|Description=CloudCDS TS Connection|Server=sql2407-fm1s-in.amr.corp.intel.com,3181|Database=cloudcds_ts|Trusted_Connection=yes"

%windir%\system32\odbcconf %config_dsn%
%windir%\syswow64\odbcconf %config_dsn%

echo Data Source "%dsn_name%" has been configured.
echo.

echo Done.
echo.
pause
