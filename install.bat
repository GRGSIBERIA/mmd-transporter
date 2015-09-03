mecab\mecab-0.996.exe

rem MeCabのインストール先を調べる
if "%PROCESSOR_ARCHITECTURE%" == "x86" (
    SET REG_UNINSTALL_KEY=HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
) else (
    SET REG_UNINSTALL_KEY=HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall
)
for /f "tokens=1,2*" %%A in ('reg query "%REG_UNINSTALL_KEY%"') do (
    reg query "%%A" /v DisplayName 2>NUL | findstr /c:"MeCab" 2>NUL
    if not errorlevel 1 (
    	for /f "usebackq tokens=1,2,3*" %%a in (`reg query "%%A" /v InstallLocation`) do (
    		set MECAB_PATH=%%c
    	)
        goto OUT
    )
)

:OUT
cd %MECAB_PATH%
setx MECAB_PATH %MECAB_PATH%

echo "インストールが完了しました"
pause