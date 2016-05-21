DESTDIR ?= /usr


PREFIXBIN=$(DESTDIR)/bin
PREFIXLIB=$(DESTDIR)/lib/didyoureadme
PREFIXSHARE=$(DESTDIR)/share/didyoureadme
PREFIXPIXMAPS=$(DESTDIR)/share/pixmaps
PREFIXAPPLICATIONS=$(DESTDIR)/share/applications
PREFIXSQL=$(PREFIXSHARE)/sql

all: compile install
compile:
	pyuic5 ui/frmAbout.ui > ui/Ui_frmAbout.py &
	pyuic5 ui/frmAccess.ui > ui/Ui_frmAccess.py &
	pyuic5 ui/frmHelp.ui > ui/Ui_frmHelp.py &
	pyuic5 ui/frmMain.ui > ui/Ui_frmMain.py &
	pyuic5 ui/frmSettings.ui > ui/Ui_frmSettings.py &
	pyuic5 ui/frmDocumentsIBM.ui > ui/Ui_frmDocumentsIBM.py &
	pyuic5 ui/frmGroupsIBM.ui > ui/Ui_frmGroupsIBM.py &
	pyuic5 ui/frmUsersIBM.ui > ui/Ui_frmUsersIBM.py &
	pyuic5 ui/wdgYearMonth.ui > ui/Ui_wdgYearMonth.py &
	pyuic5 ui/wdgYear.ui > ui/Ui_wdgYear.py &
	pyrcc5 images/didyoureadme.qrc > images/didyoureadme_rc.py &
	sleep 1
	wait
	pylupdate5 -noobsolete didyoureadme.pro
	lrelease didyoureadme.pro

install:
	install -o root -d $(PREFIXBIN)
	install -o root -d $(PREFIXLIB)
	install -o root -d $(PREFIXSHARE)
	install -o root -d $(PREFIXPIXMAPS)
	install -o root -d $(PREFIXAPPLICATIONS)
	install -o root -d $(PREFIXSQL)

	install -m 755 -o root didyoureadme.py $(PREFIXBIN)/didyoureadme
	install -m 644 -o root libdidyoureadme.py libdbupdates.py $(PREFIXLIB)
	install -m 644 -o root ui/*.py $(PREFIXLIB)
	install -m 644 -o root images/*.py $(PREFIXLIB)
	install -m 644 -o root images/didyoureadme.png $(PREFIXPIXMAPS)/didyoureadme.png
	install -m 644 -o root didyoureadme.desktop $(PREFIXAPPLICATIONS)
	install -m 644 -o root i18n/*.qm $(PREFIXSHARE)
	install -m 644 -o root sql/* $(PREFIXSQL)
	install -m 644 -o root AUTHORS.txt CHANGELOG.txt GPL-3.txt INSTALL.txt RELEASES.txt $(PREFIXSHARE)
	install -m 644 -o root images/didyoureadme.ico $(PREFIXSHARE)

uninstall:
	rm $(PREFIXBIN)/didyoureadme
	rm -Rf $(PREFIXLIB)
	rm -Rf $(PREFIXSHARE)
	rm -fr $(PREFIXPIXMAPS)/didyoureadme.png
	rm -fr $(PREFIXAPPLICATIONS)/didyoureadme.desktop



