import curses
import os
from curses import panel
from pprint import pprint

class CursesMenuPanel(object):

    def __init__(self, items, rootmenu):
        self.rootmenu = rootmenu
        self.window = rootmenu.screen.subwin(0,0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(('exit','exit'))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = '%d. %s' % (index, item[0])
                self.window.addstr(1+index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items)-1:
                    break
                else:
                    self.rootmenu.set_selection(self.items[self.position][1])

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

class CursesMenu(object):
    selection = None
    submenus = {}
    def __init__(self, stdscreen, menudata=None):
        self.screen = stdscreen
        curses.curs_set(0)
        self.process_menudata()
        self.menu.display()

    def process_menudata(self):
        submenu_items = [
                ('beep', curses.beep),
                ('flash', curses.flash),
                ('stringy', "stringgggg"),
                ]
        submenu = CursesMenuPanel(items=submenu_items, rootmenu=self)
	#return submenu
        main_menu_items = [
                ('beep', curses.beep),
                ('flash', curses.flash),
                ('submenu', submenu),
                ('submenutype', submenu.__class__.__name__),
                ('stringy', "stringgggg")
                ]
        main_menu = CursesMenuPanel(items=main_menu_items, rootmenu=self)
        self.menu = main_menu

    def set_selection(self, selection=None):
        if selection.__class__.__name__ == "CursesMenuPanel":
            self.selection = selection
            self.selection.display()
        elif hasattr(selection, '__call__'):
            self.selection = selection()
        else:
            self.selection = selection

    def get_selection(self):
        return self.selection
#self.selection

menudata = {
	"Main Menu": {
		"beep": curses.beep,
		"flash": curses.flash,
		"print": ("print","some string"),
		"Item One": "",
		"Item Two": "item2",
		"Submenu One": {
			"Item One": "something",
			"Item Two": ""
		}
	}
}
pprint(menudata)
def iter_menu(menudata,rootmenu,path=""):
	menu_items = []
	for key, val in menudata.iteritems():
		if hasattr(val, "__call__"):
			menu_items.append([key,val])
		elif isinstance(val, dict):
			submenu_name = os.path.join(path,key)
			rootmenu.submenus[submenu_name] = iter_menu(menudata=val, rootmenu=rootmenu, path=submenu_name)
			menu_items.append([key,rootmenu.submenus[submenu_name]])
		elif isinstance(val, list) or isinstance(val, tuple):
			menu_items.append([key,", ".join(val)])
		elif isinstance(val, basestring):
			menu_items.append([key,val])
		else:
			menu_items.append([key,val])
	return CursesMenuPanel(items=menu_items, rootmenu=rootmenu)


class Menu(object):
	def __init__(self, type="curses"):
		print "Menu"
		print type
		if type == "curses":
			self.menu = curses.wrapper(CursesMenu)
			pprint(dir(self.menu))
			self.new_menu = iter_menu(menudata=menudata, rootmenu=self.menu)
			self.new_menu.display()

	def get_selection(self):
		if not self.menu is None:
			return self.menu.get_selection()

if __name__ == '__main__':
	print "main"
	menu = Menu()
	print menu.get_selection()
