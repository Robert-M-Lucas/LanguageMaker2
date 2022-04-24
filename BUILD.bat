set startTime=%time%

python BuildUtil\prebuild.py

pyinstaller --version
pyinstaller main.pyw --icon=BuildUtil\icon.ico --version-file BuildUtil\file_version_info.txt --exclude-module _bootlocale --exclude-module pandas --exclude-module matplotlib --exclude-module numpy --exclude-module cryptography -y

attrib +h build

del dist\main\nltk_data\corpora\omw-1.4.zip
del dist\main\nltk_data\corpora\wordnet.zip

copy VERSION.txt dist\main\VERSION.txt
mkdir dist\main\GUI
copy GUI\icon.ico dist\main\GUI\icon.ico
Xcopy HelpText dist\main\HelpText\ /E /H /C /I
mkdir dist\main\Data
copy Data\TestLanguage.lang dist\main\Data\TestLanguage.lang

ren dist\main\main.exe LanguageMaker2.exe

"C:\Program Files (x86)\Inno Setup 6\iscc.exe" BuildUtil\InnoSetupCompileScript.iss

echo Start: %startTime% End: %time%

dist\LanguageMakerSetup.exe