set startTime=%time%

python BuildUtil\prebuild.py

pyinstaller --version
pyinstaller main.pyw --icon=BuildUtil\icon.ico --version-file BuildUtil\file_version_info.txt --exclude-module _bootlocale --exclude-module pandas --exclude-module matplotlib --exclude-module numpy --exclude-module cryptography --exclude-module nltk.corpus.omw -y

attrib +h build

del dist\main\nltk_data\corpora\omw-1.4.zip
del dist\main\nltk_data\corpora\wordnet.zip
del dist\main\nltk_data\corpora\omw-1.4\*.* /q /s
del dist\main\nltk_data\corpora\omw-1.4 /q /s

copy VERSION.txt dist\main\VERSION.txt
Xcopy HelpText dist\main\HelpText\ /E /H /C /I
mkdir dist\main\Data

ren dist\main\main.exe LanguageMaker2.exe

"C:\Program Files (x86)\Inno Setup 6\iscc.exe" BuildUtil\InnoSetupCompileScript.iss

echo Start: %startTime% End: %time%