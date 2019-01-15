
***********************************************************
************************READ ME****************************
***********************************************************

This folder is the default folder with all templates used
throughout the project. All HTML files will extend these
in some way shape or form.

__data__.html is a default template for all HTML files
that extend these files.

form_template.html is used to generate the default state
of forms.

FOLDERS:
1. includes - this folder contains little snippets of
code added throughout the pages such as footers and
certain CSS styles
2. regular HTML -  this folder contains a quick template
of regular html. There is no Jinja in this code, just raw
HTML and CSS
3.  registered - this folder contains all HTML files that
are accessible by the user once logged in. All HTML files
in this folder will extend base.html
4. unregistered - this folder contains all HTML files
that are only accessible by an unregistered user. All
HTML files in this folder will extend base_unregistered.html