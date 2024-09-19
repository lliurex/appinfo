import sys
import os
from PySide2.QtWidgets import QLabel, QPushButton,QGridLayout,QLineEdit,QTextEdit
from PySide2 import QtGui
from PySide2.QtCore import Qt
from QtExtraWidgets import QStackedWindowItem
import subprocess
import gettext
_ = gettext.gettext

i18n={"SEARCH":_("Insert package name")}

class policy:
	def __init__(self):
		appinfo={'id':None,'package':None,'version':None,'arch':None,'origin':None,'policy':None}
	#def __init__

	def getInfo(self,pkgname):
		appinfo={'package':pkgname,'origin':'unknown'}
		try:
			result=subprocess.run(["apt-cache","show",pkgname],stdout=subprocess.PIPE,universal_newlines=True)
		except Exception as e:
			print(e)
			return
		if len(result.stdout)>0:
			appinfo['policy']=result.stdout
			for line in result.stdout.split("\n"):
				if line.startswith("Version"):
					appinfo['version']=":".join(line.split(":")[1:]).strip()
				if line.startswith("Architecture"):
					appinfo['arch']=":".join(line.split(":")[1:]).strip()
			result=subprocess.run(["apt-cache","policy",pkgname],stdout=subprocess.PIPE,universal_newlines=True)
			if len(result.stdout)>0:
				appinfo['policy']="{}\n=====\n{}".format(appinfo['policy'],result.stdout)
		return appinfo
	#def getInfo


class main(QStackedWindowItem):
	def __init_stack__(self):
		self.dbg=False
		self.enabled=True
		self.index=1
		self.hideControlButtons()
		self.policy=policy()
		self.clipboard=QtGui.QClipboard()
		self.menu_description=i18n.get('MENUDESCRIPTION')
		self.description=i18n.get('DESCRIPTION')
		self.icon=('application-x-desktop')
		self.show()

	def __initScreen__(self):
		lay=QGridLayout()
		lay.setHorizontalSpacing(0)
		self.setLayout(lay)
		self.inpSearch=QLineEdit()
		self.inpSearch.setPlaceholderText(i18n.get("SEARCH"))
		self.inpSearch.returnPressed.connect(self._searchPkg)
		lay.addWidget(self.inpSearch,0,0,1,1)
		icn=QtGui.QIcon.fromTheme("search")
		btnSearch=QPushButton()
		btnSearch.setIcon(icn)
		btnSearch.clicked.connect(self._searchPkg)
		lay.addWidget(btnSearch,0,1,1,1,Qt.Alignment(-1))
		self.txtEdit=QTextEdit()
		self.txtEdit.setReadOnly(True)
		lay.addWidget(self.txtEdit,1,0,1,2)
		btnCopy=QPushButton()
		icn=QtGui.QIcon.fromTheme("edit-copy")
		btnCopy.setIcon(icn)
		btnCopy.clicked.connect(self._copyToClipboard)
		lay.addWidget(btnCopy,2,1,1,1)
	#def __initScreen__
		
	def _searchPkg(self):
		self.txtEdit.setText("")
		pkg=self.policy.getInfo(self.inpSearch.text())
		self.txtEdit.setText(pkg.get("policy",""))
	#def _searchPkg

	def _copyToClipboard(self):
		self.clipboard.setText(self.txtEdit.toPlainText())
	#def _copyToClipboard
	
	def updateScreen(self):
		pass
