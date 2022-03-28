set startTime=%time%
pyinstaller --version
pyinstaller main.pyw --exclude-module _bootlocale --exclude-module pandas --exclude-module matplotlib --exclude-module numpy --exclude-module cryptography --exclude-module nltk.corpus.omw --exclude-module PIL -y
copy VERSION.txt dist\main\VERSION.txt
Xcopy HelpText dist\main\HelpText\ /E /H /C /I
mkdir dist\main\Data
"C:\Program Files (x86)\Inno Setup 6\iscc.exe" InnoSetupCompileScript.iss
echo Start: %startTime% End: %time%