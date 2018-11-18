What is Xulpymoney
==================
Desktop app to manage personal and financial contability

License
=======
GPL-3

Links
=====
Doxygen documentation:
  * http://turulomio.users.sourceforge.net/doxygen/xulpymoney/

Main developer web page:
  * https://github.com/Turulomio 

Pypi web page:
  * https://pypi.org/project/xulpymoney/

Install in Linux
================
If you use Gentoo you can find a ebuild in https://github.com/Turulomio/myportage/tree/master/app-office/xulpymoney

If you use other distribution compatible con pip, you need to install PyQtChart and xulpymoney with the following commands:

`pip install PyQtChart`

`pip install xulpymoney`

You need to install PyQtChart first, because is not in Linux setup.py dependencies due to PyQt5 doesn't use standard setup tools. So for compatibility reasons with distributions like Gentoo, we use this additional step.

Install in Windows as a python module
=====================================
You need to install Python from https://www.python.org and add it to the PATH

You must open a console with Administrator privileges and type:

`pip install xulpymoney`

If you want to create a Desktop shortcut to launch Xulpymoney you must write:

`xulpymoney.exe --shortcuts-create`

If you want to delete that Desktop shortcut you can write:

`xulpymoney.exe --shortcuts-remove`

Install in Windows as a standalone application
==============================================
You need to download xulpymoney-X.X.X.exe from github release

Just execute it

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.
* http://initd.org/psycopg/, to access PostgreSQL database.
* https://pypi.org/project/PyQt5/, as the main library.
* https://pypi.org/project/pytz/, to work with timezones.
* https://pypi.org/project/officegenerator/, to work with LibreOffice and Microsoft Office documents.
* https://pypi.org/project/PyQtChart/, to work with charts.
* https://pypi.org/project/pywin32/, to create shortcuts.

Changelog
=========
0.5.0
  * Solved several bugs
  * Added setup.py pyinstaller to generate one standalone exe to distribute in Windows

0.4.0
  * Xulpymoney is now a gui_script.
  * You can create shortcuts with xulpymoney --shortcuts-create
  * Removed old installation system in Windows. Added Windows installation instructions in README

0.3.0
  * Added platform dependent dependencies

0.2.0
  * Fixed a lot of bugs
  * Now products update is made from products.xlsx on internet
  * Create product.needStatus to load necessary quotes automatically
  * Added python-stdnum dependency to validate ISIN code
  * Updated and added several products

0.1.1
  * Added missing files to MANIFEST.in

0.1.0
*  * Migration from Sourceforge
  * Changed code to python package
Depends
=======

DidYouReadMe has the following dependences:
  - PyQt5
  - python3
  - psycopg
  - pytz





Installation from linux sources
===============================

Uncompress the file
Change to directory where Makefile is and type
  # make all

If you use Gentoo, you can download the ebuild from 
https://xulpymoney.svn.sourceforge.net/svnroot/xulpymoney/myportage/games-board/didyoureadme/

To uninstall use the next command to make a clean uninstall
  # make uninstall

Create a postgresql database:
  # createdb -U postgres didyoureadme
  # psql -U postgres didyoureadme < sql/didyoureadme.sql

Run didyoureadme and configure settings

You must grant didyoureadme_user or didyoureadme_admin to your database user
If you use postgres user, DidYouReadMe gives him both roles


Recomendations
==============
- If you have problems with data base, you should see database posmaster.log file
- Sever time and Client time must be updated
- Antivirus and Firewall could avoid web server comunications and mail sends
Idea and development
--------------------
Mariano Muñoz <turulomio@yahoo.es> 

Translations
------------
English: Mariano Muñoz <turulomio@yahoo.es>
XXXXXXXX
========
- Added more images
- Improved web page output

20160521
========
- Windows versions
- A lot of changes

20150128
========
- Added expiration for documents
- Documents are now inside database
- Improved code reutilization
- Add admin mode
- You can delete documents in admin mode

20140128
========
- Solved bug with mail dates.
- Added autoupdate tables in frmSettings
- Report shows document internal id

20130711
========
- Solved bug with weekday in mail date

20130710
========
- Solved bug when changing web server port
- Mail shows datetime in interantional format
- Closed docs can be searched by month and year
- Datetime view doesn't cut 00 seconds
- members is now a set, not a list

20130208
========
- User and Group combos changed to lists, improving user interface.
- frmMain now update tables automatically.
- Bottle.py remove from project, you must use the bottle.py distribution.
- Adding new document checks if the file selected is really a file.
- Improved user interface

20130116
========
- Script added to make backups. It can be launched from console and from UI.
- Bug solved when sending mail without comment

20130114
========
- Documents are now generated in /tmp/didyoureadme
- Open documents and reports have been improved
- You can add several lines in document comment
- The title of the document is now mandatory


20130108
========
- First version, full functional.
