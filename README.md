# Language maker 2
This is an updated version of a previous language maker to track my improvement in python
programming

The initial startup may take longer as it converts the Markdown text files to HTML if they
haven't been cached in advance

Press F1 on most screens for help - there isn't much explanation for how the program works
here as I am trying to make it self-explanatory

### Translation Errors
- [NT for {word name}] - No translation for this word; add a translation by editing the word's 
English synonyms

Using 'stepped' translation allows you to resolve errors as they come up

### Dependencies
```pip install *library name*```
- requests
- tkhtmlview
- nltk
- markdown

Building this app with pyinstaller (see BUILD.bat) requires the dev version which can be
installed with 
```shell
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
```