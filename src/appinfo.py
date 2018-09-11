#!/usr/bin/env python3
import os
import subprocess
from lliurexstore.plugins import debManager

import gi
gi.require_version('Gtk','3.0')
gi.require_version('PangoCairo','1.0')
from gi.repository import Gtk, Gdk, GObject, GLib, PangoCairo, Pango, GdkPixbuf

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import gettext
gettext.textdomain('appinfo')
_ = gettext.gettext

SPACING=6
MARGIN=6
RSRC_DIR='/usr/share/appinfo/rsrc'

class policy:
	def __init__(self):
		self.debman=debManager.debmanager()
		appinfo={'id':None,'package':None,'version':None,'arch':None,'origin':None,'policy':None}
	def _get_info(self,pkgname):
		appinfo={'package':pkgname}
		res=self.debman.execute_action('policy',[appinfo],2)
		if res['status']['status']==0:
			try:
				for app in res['data']:
					info_array=app['id'].split(';')
					appinfo['package']=info_array[0]
					appinfo['version']=info_array[1]
					appinfo['arch']=info_array[2]
					appinfo['origin']=info_array[3]
			except:
				pass
			try:
				result=subprocess.run(["apt-cache","policy",info_array[0]],stdout=subprocess.PIPE,universal_newlines=True)
				appinfo['policy']=result.stdout
			except Exception as e:
				print(e)
				pass
		else:
			appinfo=None
		return appinfo


def _render_gui():
	def _begin_search_app(*args):
			info=_search_app(inp_input.get_text())
			if info:
				lbl_result.set_markup(_("Package: %s %s %s\nOrigin: %s\n<span color='blue'><span underline='single'>More details</span>...</span>")%(info['package'],info['version'],info['arch'],info['origin']))
				lbl_policy.set_markup("%s"%info['policy'])
			else:
				lbl_result.set_label(_("Package not found/not installed"))
				lbl_policy.set_markup("")
			box_btn_result.set_no_show_all(False)
			btn_result.show_all()

	def _toggle_reveal(*args):
		rvl_result.set_reveal_child(not(rvl_result.get_reveal_child()))
		global size
		if size==0:
			size=window.get_size()
		if rvl_result.get_reveal_child():
			rvl_result.set_visible(True)
		else:
			rvl_result.set_visible(False)
			window.resize(size.width,size.height)

	def _copy_clipboard(*args):
		clipboard.set_text(lbl_policy.get_text(),-1)

	_set_css_info()
	window=Gtk.Window()
	window.connect("destroy",Gtk.main_quit)
	window.set_resizable(False)
	window.set_title("appinfo")
	clipboard=Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
	box=Gtk.VBox()
	pb=GdkPixbuf.Pixbuf.new_from_file("%s/appinfo.png"%RSRC_DIR)
	img_banner=Gtk.Image.new_from_pixbuf(pb)
	img_banner.props.halign=Gtk.Align.CENTER
	img_banner.set_margin_left(MARGIN*2)
	img_banner.set_valign(Gtk.Align.START)
	box.add(img_banner)
	box_search=Gtk.Box(spacing=SPACING)
	box_search.set_margin_top(SPACING*2)
	box_search.set_margin_left(SPACING*2)
	box_search.set_margin_right(SPACING*2)
	box_search.set_margin_bottom(SPACING*2)
	box_search.set_vexpand=False
	box_search.set_hexpand=True
	box_search.set_valign(Gtk.Align.START)
	box_input=Gtk.VBox(spacing=SPACING)
	box_input.set_valign(Gtk.Align.START)
	lbl_input=Gtk.Label()
	lbl_input.set_name("ENTRY_LABEL")
	lbl_input.set_halign(Gtk.Align.START)
	lbl_input.set_markup("<sup>%s</sup>"%_("Package's name"))
	box_input.add(lbl_input)
	inp_input=Gtk.Entry()
	inp_input.connect("activate",_begin_search_app)
	inp_input.set_hexpand=True
	inp_input.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,Gtk.STOCK_FIND)
	inp_input.set_placeholder_text(_("Package name"))
	box_input.add(inp_input)
	box_search.add(box_input)
	btn_search=Gtk.Button.new_from_icon_name(Gtk.STOCK_FIND,Gtk.IconSize.BUTTON)
	btn_search.set_vexpand(False)
	btn_search.set_valign(Gtk.Align.END)
	btn_search.connect("clicked",_begin_search_app)
	box_search.add(btn_search)
	box.add(box_search)
	btn_result=Gtk.Button()
	btn_result.connect("clicked",_toggle_reveal)
	btn_result.set_valign(Gtk.Align.START)
	box_btn_result=Gtk.Box()
	lbl_result=Gtk.Label()
	box_btn_result.add(lbl_result)
	btn_result.add(box_btn_result)
	box_btn_result.set_no_show_all(True)
	box.add(btn_result)


	rvl_result=Gtk.Revealer()
	box_result=Gtk.VBox()
	box_result.set_valign(Gtk.Align.START)
	rvl_result.add(box_result)
	lbl_policy=Gtk.Label()
	lbl_policy.set_single_line_mode(False)
	lbl_policy.set_margin_left(MARGIN)
	lbl_policy.set_margin_right(MARGIN)
	lbl_policy.set_line_wrap(True)
	lbl_policy.set_selectable(True)
	box_result.add(lbl_policy)
	btn_copy=Gtk.Button.new_from_icon_name(Gtk.STOCK_COPY,Gtk.IconSize.BUTTON)
	btn_copy.set_tooltip_text(_("Copy to clipboard"))
	btn_copy.connect("clicked",_copy_clipboard)
	box_result.add(btn_copy)
	box.add(rvl_result)
	window.add(box)
	window.show_all()
	Gtk.main()

def _search_app(pkgname):
	appinfo=app_policy._get_info(pkgname)
	return(appinfo)

def _set_css_info():

	css = b"""

	GtkEntry{
		font-family: Roboto;
		border:0px;
		border-bottom:1px grey solid;
		margin-top:0px;
		padding-top:0px;
	}

	GtkLabel {
		font-family: Roboto;
	}

	#NOTIF_LABEL{
		background-color: #3366cc;
		font: 11px Roboto;
		color:white;
		border: dashed 1px silver;
		padding:6px;
	}

	#ERROR_LABEL{
		background-color: red;
		font: 11px Roboto;
		color:white;
		border: dashed 1px silver;
		padding:6px;
	}

	#ENTRY_LABEL{
		color:grey;
		padding:6px;
		padding-bottom:0px;
	}

	#PLAIN_BTN,#PLAIN_BTN:active{
		border:0px;
		padding:0px;
		background:white;
	}
	
	#PLAIN_BTN_DISABLED,#PLAIN_BTN_DISABLED:active{
		border:0px;
		padding:0px;
		background:white;
		font:grey;
	}

	#COMPONENT{
		padding:3px;
		border: dashed 1px silver;

	}

	#WHITE_BACKGROUND {
		background-color:rgba(255,255,255,1);
	
	}

	#BLUE_FONT {
		color: #3366cc;
		font: Roboto Bold 11;
		
	}	
	

	#TASKGRID_FONT {
		color: #3366cc;
		font: Roboto 11;
		
	}

	#LABEL #LABEL_INSTALL{
		padding: 6px;
		margin:6px;
		font: 12px Roboto;
	}

	#LABEL_OPTION{
	
		font: 48px Roboto;
		padding: 6px;
		margin:6px;
		font-weight:bold;
	}

	#ERROR_FONT {
		color: #CC0000;
		font: Roboto Bold 11; 
	}

	#MENUITEM {
		padding: 12px;
		margin:6px;
		font: 24px Roboto;
		background:white;
	}

	#BLUEBUTTON {
		background-color: #3366cc;
		color:white;
		font: 11px Roboto Bold;
	}

	"""
	style_provider=Gtk.CssProvider()
	style_provider.load_from_data(css)
	Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
#def set_css_info	
size=0
app_policy=policy()
_render_gui()
#appinfo=appinfo._get_info("firefox")
#if appinfo:
#	print(appinfo)
	
