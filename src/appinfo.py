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
				desc_md=_("<small>Package:</small> %s %s %s\n<small>Origin:</small> %s\n<span color='blue'><sub><span underline='single'>More details</span>...</sub></span>")%(info['package'],info['version'],info['arch'],info['origin'])
				desc_txt=_("Package: %s %s %s\nOrigin: %s")%(info['package'],info['version'],info['arch'],info['origin'])
				lbl_result.set_markup(desc_md)
				btn_result.set_tooltip_text(desc_txt)
				lbl_policy.set_markup("%s"%info['policy'])
			else:
				lbl_result.set_label(_("Package not found/not installed"))
				lbl_policy.set_markup("")
			box_btn_result.set_no_show_all(False)
			btn_result.set_no_show_all(False)
			btn_result.show_all()
			if rvl_result.get_reveal_child():
				_toggle_reveal()

	def _toggle_reveal(*args):
		rvl_result.set_reveal_child(not(rvl_result.get_reveal_child()))
		global size
		if size==0:
			size=window.get_size()
		if rvl_result.get_reveal_child():
			rvl_result.set_visible(True)
			btn_result.set_size_request(size.width,-1)
		else:
			rvl_result.set_visible(False)
			window.resize(size.width,size.height)

	def _copy_clipboard(*args):
		clipboard.set_text(lbl_policy.get_text(),-1)

	_set_css_info()
	window=Gtk.Window()
	window.set_position(Gtk.WindowPosition.CENTER)
	window.set_resizable(False)
	window.set_title("appinfo")
	window.connect("destroy",Gtk.main_quit)
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
	btn_result.set_margin_top(MARGIN)
	btn_result.set_margin_left(MARGIN)
	btn_result.set_margin_right(MARGIN)
	btn_result.set_margin_bottom(MARGIN)
	btn_result.set_name("BTN_ITEM")
	btn_result.connect("clicked",_toggle_reveal)
	btn_result.set_valign(Gtk.Align.START)
	btn_result.set_no_show_all(True)
	box_btn_result=Gtk.Box()
	lbl_result=Gtk.Label()
	lbl_result.set_hexpand(False)
	lbl_result.set_halign(Gtk.Align.START)
	lbl_result.set_ellipsize(Pango.EllipsizeMode.END)
#	lbl_result.set_line_wrap(True)
	lbl_result.set_max_width_chars(35)
	box_btn_result.add(lbl_result)
	btn_result.add(box_btn_result)
	box_btn_result.set_no_show_all(True)
	box.add(btn_result)

	#Container for label
	box_scroll_result=Gtk.ScrolledWindow()
	box_scroll_result.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.NEVER)
	rvl_result=Gtk.Revealer()
	box_result=Gtk.VBox()
	box_result.set_valign(Gtk.Align.START)
	lbl_policy=Gtk.Label()
	lbl_policy.set_single_line_mode(False)
	lbl_policy.set_margin_left(MARGIN)
	lbl_policy.set_margin_right(MARGIN)
	lbl_policy.set_selectable(True)
	box_scroll_result.add(lbl_policy)
	box_result.add(box_scroll_result)
	#Copy button
	btn_copy=Gtk.Button.new_from_icon_name(Gtk.STOCK_COPY,Gtk.IconSize.BUTTON)
	btn_copy.set_tooltip_text(_("Copy to clipboard"))
	btn_copy.connect("clicked",_copy_clipboard)
	box_result.add(btn_copy)
	rvl_result.add(box_result)
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



	#ENTRY_LABEL{
		color:grey;
		padding:6px;
		padding-bottom:0px;
	}


	#BLUE_FONT {
		color: #3366cc;
		font: Roboto Bold 11;
		
	}	
	
	#BTN_ITEM {
		padding: 6px;
		margin:6px;
		font: 12px Roboto;
		background-image:-gtk-gradient(linear, left top, left bottom, from (#7ea8f2),to (#7ea8f2));
		box-shadow: -0.5px 3px 2px #aaaaaa;
		background:white;
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
	
