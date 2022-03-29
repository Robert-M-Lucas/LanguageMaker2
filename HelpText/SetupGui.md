# Language Selector Help

NLTK is required for finding synonyms to words and this program relies on it to
give predictions for synonyms you may want to add.

If you are running into crashes, re-downloading NLTK may help

Languages are stored in /Data/***language_name***.db
The only allowed characters in language names are alphanumerics, '-' and '_'

Two languages aren't permitted to have the same name

### Deleting a language
To prevent accidental deletion of a language, languages can't be deleted from inside the app.
To delete a language go to the **Data** folder in the root of where this app is stored
and delete **language_name**.db