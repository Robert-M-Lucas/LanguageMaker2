### This project is marked as complete
# Language maker 2

This is an updated version of a previous language maker to track my improvement in python
programming.

The initial startup may take longer as it converts the Markdown text files to HTML if they
haven't been cached in advance.

Press F1 on most screens for help - there isn't much explanation for how the program works
here as I am trying to make it self-explanatory.

You will have to heavily modify build files to make them work on your machine. To build you
will need pyinstaller and Inno Setup Compiler.

Building this app with pyinstaller (see BUILD.bat) requires the dev version which can be
installed with.

```pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip```

You can find a build version in the 'dist' folder

### Dependencies
```pip install *library name*```
- requests
- tkhtmlview
- nltk
- markdown
