@ECHO OFF
:: Getting current user
for /f %%i in ('whoami') do set CurrentUserClient=%%i
echo The current username is %CurrentUserClient%

:: Setting at User Variables
setx EV_User "%CurrentUserClient%"
echo Enviroment variable setted.