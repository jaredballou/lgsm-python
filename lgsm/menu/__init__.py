import curses
from curses import panel

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
                # Handle exit from menu
                if self.position == len(self.items)-1 or str(self.items[self.position][1]) == "exit":
                    break
                else:
                    if self.rootmenu.set_selection(self.items[self.position][1]):
                        break

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

class CursesMenu(object):
    def __init__(self, stdscreen, menudata=None):
        self.selection = None
        self.submenus = {}
        self.screen = stdscreen
        curses.curs_set(0)
	if menudata is not None:
		self.menu = iter_menu(menudata=menudata, rootmenu=self)
	else:
	        self.menu = self.default_menu()
        self.menu.display()

    def default_menu(self):
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
	return main_menu

    def set_selection(self, selection=None):
        if selection.__class__.__name__ == "CursesMenuPanel":
            self.selection = selection
            self.selection.display()
            return False
        elif hasattr(selection, '__call__'):
            self.selection = selection()
            return True
        else:
            self.selection = selection
            return True

    def get_selection(self):
        return self.selection

def iter_menu(menudata,rootmenu,path=""):
	menu_items = []
	for key, val in menudata.iteritems():
		if hasattr(val, "__call__"):
			menu_items.append([key,val])
		elif isinstance(val, dict):
			submenu_name = "/".join(path,key)
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
	def __init__(self, type="curses", menudata=None):
		if type == "curses":
			self.menu = curses.wrapper(CursesMenu,menudata=menudata)

	def get_selection(self):
		if not self.menu is None:
			return self.menu.get_selection()
