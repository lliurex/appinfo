#!/usr/bin/env python3
import sys
import os
from PySide6.QtWidgets import QApplication
from QtExtraWidgets import QStackedWindow
import gettext
gettext.textdomain('appinfo')
_ = gettext.gettext
app=QApplication(["appInfo"])
config=QStackedWindow()
if os.path.islink(__file__)==True:
	abspath=os.path.join(os.path.dirname(__file__),os.path.dirname(os.readlink(__file__)))
else:
	abspath=os.path.dirname(__file__)
config.addStacksFromFolder(os.path.join(abspath,"stacks"))
config.setBanner("/usr/share/appinfo/rsrc/appinfo.png")
config.setIcon("appinfo")
config.show()
app.exec()
