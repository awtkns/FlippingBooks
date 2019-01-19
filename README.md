************************************
INSTALLATION
************************************
1. Instal Python 3.6.x
https://www.python.org/downloads/
We recommend Python 3.6.x.
NOTE: Python 2 and Python 3 are not the same.
Do not install Python 2
Please see link below for more details.
https://wiki.python.org/moin/Python2orPython3

2. Instal pip
Instructions as follows
https://pip.pypa.io/en/stable/installing/

3. Instal Django 1.11.x
https://www.djangoproject.com/download/
You can use pip to install Django or
manually install it.


************************************
RUNNING THE SERVER
************************************

WINDOWS
1. Open up a command prompt, change the directory to
/FlippingBooks-v1.0.0
eg: D:\Python\FlippingBooks-v1.0.0
In this folder, there should be a manage.py file.
2. To run the server, type python manage.py runserver
3. If no errors occur, you can visit the website by going
to 127.0.0.1:8000


************************************
HOW DJANGO WORKS
************************************

Django is a python web frameowrk built on a few simple concepts.
1. The project has a settings.py where you apply all your apps
and major settings of the project.
2. The project has a urls.py which matches the url using regular
expressions to determine which page to load. This also applies to
url.py inside our application (main/urls.py)
3. Everything involving our app is under the main folder. Inside there
is models.py. Models is a class definition of your tables in your database.
Each class represents a table and each attribute represents a column in 
the corresponding table.
4. views.py are the ways that Django generates the web pages. This includes
your business logic, as well as where to obtain the html files for the user.
4. inside main, there is a templates folder. This folder contains all html
pages. See readme.txt in templates/main/ for more information.
5. the main/static/ folder contains our css and other static files such as images.
6. main/forms.py is used to generate user input forms for retreviing data from user.
7. sql.py contains all raw SQL queires.
8. map.py contains all tuples for mapping key to value for dropdown lists.

************************************
OUR SQL STATEMENTS
************************************

All our sql statments are located within ./main/sql.py
All the sql was done using raw sql using SqlLite.

For the detailed querys visit ./main/sql.py

************************************
HELP
************************************

If for some reason you cannot set up django correctly
please contact us so we can set up webhosting for you to be able to view our site.

