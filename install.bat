mecab\mecab-0.996.exe

rem MeCabのインストール先を調べる

if exist "C:\Program Files (x86)\MeCab" (
	setx MECAB_PATH "C:\Program Files (x86)\MeCab"
) else if exist "C:\Program Files\MeCab" (
	setx MECAB_PATH "C:\Program Files\MeCab"
) else if exist "C:\MeCab" (
	setx MECAB_PATH "C:\MeCab"
) else (
	echo "MeCabが見つかりませんでした"
	echo "手動で環境変数MECAB_PATHを設定してください"
	pause
	exit
)

echo "MMD HumanIK.xmlの移動"
set HIK_PATH=%USERPROFILE%\AppData\Roaming\Autodesk\HIKCharacterizationTool4\template
if exist %HIK_PATH% (
	rem 何もしなくていいよ
) else (
	mkdir %HIK_PATH%
	copy /Y "MMD HumanIK.xml" %HIK_PATH%
)


echo "インストールが完了しました"
pause