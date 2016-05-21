@ECHO ON
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmAbout.ui -o ui/Ui_frmAbout.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmHelp.ui -o ui/Ui_frmHelp.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmMain.ui -o ui/Ui_frmMain.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmSettings.ui -o ui/Ui_frmSettings.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmAccess.ui -o ui/Ui_frmAccess.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmDocumentsIBM.ui -o ui/Ui_frmDocumentsIBM.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmGroupsIBM.ui -o ui/Ui_frmGroupsIBM.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/frmUsersIBM.ui -o ui/Ui_frmUsersIBM.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/wdgYear.ui -o ui/Ui_wdgYear.py
call c:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ui/wdgYearMonth.ui -o ui/Ui_wdgYearMonth.py
call c:\Python34\Lib\site-packages\PyQt5\pyrcc5.exe  images/didyoureadme.qrc -o images/didyoureadme_rc.py
call c:\Python34\Lib\site-packages\PyQt5\pylupdate5.exe -noobsolete didyoureadme.pro
call c:\Python34\Lib\site-packages\PyQt5\lrelease.exe didyoureadme.pro

