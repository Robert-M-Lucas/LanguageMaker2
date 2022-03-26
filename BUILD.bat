pyinstaller --version
pyinstaller main.pyw --exclude-module _bootlocale -y
copy VERSION.txt dist\main\VERSION.txt
Xcopy HelpText dist\main\HelpText\ /E /H /C /I
mkdir dist\main\Data