mecab\mecab-0.996.exe

rem MeCab�̃C���X�g�[����𒲂ׂ�

if exist "C:\Program Files (x86)\MeCab" (
	setx MECAB_PATH "C:\Program Files (x86)\MeCab"
) else if exist "C:\Program Files\MeCab" (
	setx MECAB_PATH "C:\Program Files\MeCab"
) else if exist "C:\MeCab" (
	setx MECAB_PATH "C:\MeCab"
) else (
	echo "MeCab��������܂���ł���"
	echo "�蓮�Ŋ��ϐ�MECAB_PATH��ݒ肵�Ă�������"
	pause
	exit
)

echo "MMD HumanIK.xml�̈ړ�"
set HIK_PATH=%USERPROFILE%\AppData\Roaming\Autodesk\HIKCharacterizationTool4\template
if exist %HIK_PATH% (
	rem �������Ȃ��Ă�����
) else (
	mkdir %HIK_PATH%
	copy /Y "MMD HumanIK.xml" %HIK_PATH%
)


echo "�C���X�g�[�����������܂���"
pause