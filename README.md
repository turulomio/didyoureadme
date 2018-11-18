Links
=====
Doxygen documentation:
  * http://turulomio.users.sourceforge.net/doxygen/didyoureadme/

Main developer web page:
  * https://github.com/Turulomio 

Pypi web page:
  * https://pypi.org/project/didyoureadme/

Install in Linux
================
If you use Gentoo you can find a ebuild in https://github.com/Turulomio/myportage/tree/master/app-office/didyoureadme

If you use other distribution compatible con pip, you need to install PyQt5 and didyoureadme with the following commands:

`pip install PyQt5`

`pip install didyoureadme`

You need to install PyQt5 first, because is not in Linux setup.py dependencies due to it doesn't use standard setup tools. So for compatibility reasons with distributions like Gentoo, we use this additional step.

Install in Windows as a python module
=====================================
You need to install Python from https://www.python.org and add it to the PATH

You must open a console with Administrator privileges and type:

`pip install didyoureadme`

If you want to create a Desktop shortcut to launch didyoureadme you must write:

`didyoureadme.exe --shortcuts-create`

If you want to delete that Desktop shortcut you can write:

`didyoureadme.exe --shortcuts-remove`

Install in Windows as a standalone application
==============================================
You need to download didyoureadme-X.X.X.exe from github release

Just execute it

To create DidYouReadmeDatabase
==============================
Create a postgresql database:

`createdb -U postgres didyoureadme`

`psql -U postgres didyoureadme < sql/didyoureadme.sql`

Run didyoureadme and configure settings

You must grant didyoureadme_user or didyoureadme_admin to your database user
If you use postgres user, DidYouReadMe gives him both roles

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.
* http://initd.org/psycopg/, to access PostgreSQL database.
* https://pypi.org/project/PyQt5/, as the main library.
* https://pypi.org/project/pytz/, to work with timezones.
* https://pypi.org/project/pywin32/, to create shortcuts.


Workarounds
===========
- If you have problems with data base, you should see database posmaster.log file
- Sever time and Client time must be updated
- Antivirus and Firewall could avoid web server comunications and mail sends

Authors
=======
Turulomio. Idea and Spanish translation


Changelog
=========

20181118
--------
- Added more images
- Improved web page output
- Migrated to GitHub
- Migrated to setuptools. Now DidYouReadMe is a package

20160521
--------
- Windows versions
- A lot of changes

20150128
--------
- Added expiration for documents
- Documents are now inside database
- Improved code reutilization
- Add admin mode
- You can delete documents in admin mode

20140128
--------
- Solved bug with mail dates.
- Added autoupdate tables in frmSettings
- Report shows document internal id

20130711
--------
- Solved bug with weekday in mail date

20130710
--------
- Solved bug when changing web server port
- Mail shows datetime in interantional format
- Closed docs can be searched by month and year
- Datetime view doesn't cut 00 seconds
- members is now a set, not a list

20130208
--------
- User and Group combos changed to lists, improving user interface.
- frmMain now update tables automatically.
- Bottle.py remove from project, you must use the bottle.py distribution.
- Adding new document checks if the file selected is really a file.
- Improved user interface

20130116
--------
- Script added to make backups. It can be launched from console and from UI.
- Bug solved when sending mail without comment

20130114
--------
- Documents are now generated in /tmp/didyoureadme
- Open documents and reports have been improved
- You can add several lines in document comment
- The title of the document is now mandatory

20130108
--------
- First version, full functional.
