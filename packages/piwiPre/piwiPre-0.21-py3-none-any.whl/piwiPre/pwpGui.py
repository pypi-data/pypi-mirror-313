# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import os
import tkinter
from tkinter import ttk
import tkinter.font

from piwiPre.pwpLogoSmall import pwpLogo_png
from piwiPre.pwpErrors import LOGGER
from piwiPre.pwpActor import ACTOR


class PwpGui:
    tk = None
    label_font = None
    font_pixels = None
    VERY_LIGHT_GREEN = "#eeeFFFeee"
    LIGHT_GREEN = "#aaaEEEaaa"
    GREEN = "green"
    GREY = "#eeeEEEeee"
    GREY2 = "#cccCCCccc"
    LIGHT_GREY = "#e00e00e00"
    WHITE = "white"
    ORANGE = "#ff7700"
    LIGHT_BLUE = "#dddDDDeee"
    BUTTON_WIDTH = 12
    RADIO_WIDTH = 8
    VALUE_WIDTH = 60
    language = "fr"
    inside_main_loop = False
    # we do not want to have 2 nested main-loops
    # this would happen mainly when GuiError is called

    # TODO: en_name and fr_name instead of name
    def __init__(self, name, language="fr"):
        self.root = None
        self.frm = None
        PwpGui.language = language
        self.widgets = []  # record all items to be able to change the language
        self.column_sizes = []

        try:
            if PwpGui.tk is None:
                PwpGui.tk = tkinter.Tk()
                self.root = PwpGui.tk
                # GuiStringEditor.running_editor = None
                GuiExpandable.info_window = None
            else:
                self.root = tkinter.Toplevel()
            self.root.title(name)

            self.frm = ttk.Frame(self.root, padding=10)
            self.frm.grid()
        except tkinter.TclError:
            LOGGER.error("Unable to start Tk")

        self.feedback = None  # displayer of messages
        if PwpGui.label_font is None:
            PwpGui.label_font = tkinter.font.Font(size=9, family="Helvetica", weight="bold")
            PwpGui.font_pixels = PwpGui.label_font.measure("n")

    def record_widget(self, widget):
        self.widgets.append(widget)

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
        else:
            raise OSError

    def set_language(self, language):
        if PwpGui.language == language:
            return
        PwpGui.language = language
        for widget in self.widgets:
            widget.set_language(language)

    @staticmethod
    def delete():
        # LOGGER.add_gui(None)
        PwpGui.tk = None
        PwpGui.label_font = None
        PwpGui.font_pixels = None
        PwpGui.root = None
        PwpGui.frm = None

    def set_column_sizes(self, sizes):
        self.column_sizes = sizes
        for i in range(0, len(sizes)):
            self.frm.columnconfigure(i, minsize=PwpGui.font_pixels * sizes[i])

    def mainloop(self):
        if self.root and not PwpGui.inside_main_loop:
            PwpGui.inside_main_loop = True
            self.root.mainloop()
            PwpGui.inside_main_loop = False

    def exit(self):
        LOGGER.debug("Exiting from GUI thread")
        PwpGui.feedback = None
        # self.root.withdraw()
        # self.root.quit()  # Do NOT do this, it kills TK !
        self.root.destroy()
        if self.root == PwpGui.tk:
            LOGGER.add_gui(None)
            LOGGER.msg("Exiting from Tk main program")
            PwpGui.delete()

    # ---------------------------------------------------------------------------------------------
    # graphical elements

    def add_messager(self, row, title, fr_title, height, width=1400):
        if not self.feedback:
            self.feedback = GuiMessager(root_gui=self, frm=self.frm, row=row,
                                        title=title, fr_title=fr_title, height=height, width=width)

    def gui_msg(self, line, tag=None, level="msg"):
        if self.feedback:
            if tag is None:
                self.feedback.insert(tkinter.END, line + "\n")
            else:
                self.feedback.insert(tkinter.END, line + "\n", tag)
            self.feedback.yview(tkinter.END)

        if level in ["Warning", "ERROR"] and self.root:
            GuiError(line, line, level == "Warning")

    def gui_warning(self, line):
        self.gui_msg("WARNING: " + line, "orange")

    def gui_error(self, line):
        self.gui_msg("ERROR  : " + line, "red")


class GuiMessager:
    def __init__(self, root_gui: PwpGui, frm, row, title, fr_title, height=5,
                 width=1400,  # width is in pixel !
                 nb_chars=400):
        self.frm = frm
        self.width = width
        font = tkinter.font.Font(size=10, family="Courier")
        nb_chars = nb_chars or (int(self.width / font.measure("n")) - 1)

        self.separator = GuiSeparator(root_gui, frm=frm, row=row, text=title, fr_text=fr_title, width=width)

        # -------------- Feedback
        row += 1

        self.scroller = GuiScrollable(root_gui, frm, row=row, column_sizes=[], name="messenger",
                                      width=self.width, horizontal_scroll=True,
                                      height=height * font.measure("n") * 2)
        # CAVEAT: height in pixels
        #         * 2 because character width != height.

        self.feedback = tkinter.Text(self.scroller.frm, background=PwpGui.LIGHT_GREY,
                                     padx=3, pady=3,
                                     font=font,
                                     #  height=height,
                                     width=nb_chars, )
        self.feedback.pack()
        self.feedback.tag_config('orange', foreground=PwpGui.ORANGE)
        self.feedback.tag_config('red', foreground="red")
        self.feedback.tag_config('blue', foreground="blue")

    def insert(self, where, line, tag=None):
        self.feedback.insert(where, line, tag)

    def yview(self, d):
        self.feedback.yview(d)


# ====================================================================================
# GuiButton
# ====================================================================================


class GuiButton(tkinter.Button):
    def __init__(self, root_gui: PwpGui, frm, column, row, text, fr_text, command,
                 background=PwpGui.GREEN, sticky="W",
                 width=PwpGui.BUTTON_WIDTH):
        super().__init__(frm, text=fr_text if PwpGui.language == 'fr' else text,
                         width=width, command=command,
                         background=background, foreground="white",
                         activebackground="white", activeforeground=background,
                         )
        self.grid(column=column, row=row, sticky=sticky)
        self.back_ground = background
        self.column = column
        self.row = row
        self.text = text
        self.fr_text = fr_text
        self.root_gui = root_gui
        root_gui.record_widget(self)

    def get_xy(self):
        return super().winfo_rootx(), super().winfo_rooty()

    def set_language(self, lan):
        self["text"] = self.fr_text if lan == "fr" else self.text

    def disable(self):
        self.configure(background=PwpGui.GREY2)
        self["state"] = 'disabled'

    def enable(self):
        self.configure(background=self.back_ground)
        self["state"] = 'normal'

    def show_at_row(self, row):
        self.grid(column=self.column, row=row, sticky="W")

    def show(self):
        self.grid(column=self.column, row=self.row, sticky="W")

    def hide(self):
        self.grid_forget()


# ====================================================================================
# GuiEntry
# ====================================================================================


class GuiEntry(tkinter.Entry):
    def __init__(self, frm, width, textvariable, column, row, columnspan):  # noqa
        super().__init__(frm, width=width, textvariable=textvariable, state=tkinter.DISABLED)
        self.column = column
        self.row = row
        self.columnspan = columnspan  # noqa
        self.show()

    def show(self):
        self.grid(column=self.column, row=self.row, sticky="W", columnspan=self.columnspan)

    def hide(self):
        self.grid_forget()


# ================================================================================
# GuiLabel
# ================================================================================


class GuiLabel(ttk.Label):
    def __init__(self, root_gui: PwpGui, frm, column, row, text, fr_text,
                 col_span=1, background=None, width=10, bold=None, relief=False):
        super().__init__(frm, text=fr_text if PwpGui.language == "fr" else text,
                         background=background, anchor="w", padding=2,
                         width=width,
                         font=PwpGui.label_font if bold else None, border=0, borderwidth=0,
                         relief='sunken' if relief else 'flat',
                         foreground="grey" if relief else None, )

        self.grid(column=column, row=row, sticky="W", columnspan=col_span, padx=1, pady=1)
        self.back_ground = background
        self.column = column
        self.row = row
        self.text = text
        self.fr_text = fr_text
        self.root_gui = root_gui
        self.col_span = col_span
        root_gui.record_widget(self)

    def set(self, text, fr_text):
        lan = PwpGui.language
        self["text"] = fr_text if lan == "fr" else text

    def set_language(self, lan):
        self["text"] = self.fr_text if lan == "fr" else self.text

    def show_at_row(self, row):
        self.grid(column=self.column, row=row, sticky="W", columnspan=self.col_span)

    def show(self):
        self.grid(column=self.column, row=self.row, sticky="W", columnspan=self.col_span)

    def hide(self):
        self.grid_forget()


# ====================================================================================
# DirChooser
# ====================================================================================


class _DirChooserField:
    def __init__(self, root_gui: 'GuiDirChooser', frm, path, abspath, row, max_width1, max_width2):
        self.root_gui = root_gui
        self.frm = frm
        self.label = GuiLabel(root_gui, frm,
                              text=path, fr_text=path,
                              column=0, row=row, width=max_width1)

        enter = not path.startswith('--') and not path.startswith('<')
        choice = not path.startswith('[') and not path.startswith('--') and not path.startswith('<')

        self.abspath = GuiLabel(root_gui, frm,
                                text=abspath, fr_text=abspath,
                                column=1, row=row, width=max_width2, relief=enter)

        self.choose_button = None
        self.enter_button = None

        if enter:
            self.enter_button = GuiButton(root_gui, frm, text="Enter", fr_text="Entrer",
                                          command=lambda: self.root_gui.enter(path), sticky="N",
                                          background=PwpGui.GREEN, column=2, row=row)
        if choice:
            self.choose_button = GuiButton(root_gui, frm, text="Choose", fr_text="Choisir",
                                           command=lambda: self.root_gui.select(path), sticky="N",
                                           background=PwpGui.GREEN, column=3, row=row)

    def prompt_new_dir(self):
        x, y = self.enter_button.get_xy()
        GuiStringEditor(father=self,
                        name="nouveau dossier" if PwpGui.language == "fr" else "new directory",
                        initial="", root_gui=self.root_gui,
                        x=x + 10,
                        y=y + 10)

    def delete(self):
        if self.enter_button:
            self.enter_button.destroy()
        if self.choose_button:
            self.choose_button.destroy()
        self.label.destroy()
        self.abspath.destroy()


# --------------------------------------------------------
# Trying to use win32net to get access to network shares :
# --------------------------------------------------------
# The target is to be able to list, on WINDOWS, all directories starting from /
#
# the list of network drives (C: etc...) is easy
#   e.g. os.isdir("D:") etc.
#
# 1) install pywin32
# venv> python -m pip install pywin32  # -> Success
# import win32                         # -> Success
#
# 2) use win32net
# from win32 import win32net           # -> ImportError: DLL load failed while importing win32net
#
# 3) install pywin32 with administrator rights
# from a console with administrative rights,using the appropriate python
# venv> python -m pip uninstall pywin32  # -> Success
# venv> python -m pip install pywin32  # -> Success
#
# found the following :
#       "note however that COM objects cannot be installed without administrative privileges"
# the previous experiment seems to prove that this is right.
#
# 4) use win32net from a NON administrator python:
# from win32 import win32net           # -> Success
# win32net.NetShareEnum("NAS",0)
# ([{'netname': 'documents'}, ... , {'netname': 'home'}], 12, 0)  --> OK !                              # noqa
#
# entries, total, resume = win32net.NetServerEnum(server, level, serverTypes=
#                                                 win32netcon.SV_TYPE_ALL, resume = 0, len=4096)        # noqa

# (wrk_list2, total, res2) = win32net.NetServerEnum(None, 100, win32netcon.SV_TYPE_LOCAL_LIST_ONLY)     # noqa
# -> pywintypes.error: (384, 'NetServerEnum', "Vous ne pouvez pas vous connecter au partage de fichier",
#
# import win32net, win32netcon                                                                          # noqa
# def getall_boxes(domain='', server=''):                                                               # noqa
#     res = 1
#     wrk_lst = []
#     try:
#         while res:
#             # loop until res2
#             (wrk_list2, total, res2) = win32net.NetServerEnum('', 100, win32netcon.SV_TYPE_ALL,       # noqa
#                                                               server, res,
#                                                               win32netcon.MAX_PREFERRED_LENGTH)       # noqa
#             wrk_lst.extend(wrk_list2)
#             res = res2
#     except win32net.error:
#         print traceback.format_tb(sys.exc_info()[2]), '\n', sys.exc_type, '\n', sys.exc_value
#
#     final_lst = []
#     for i in wrk_lst: final_lst.append(str(i['name']))
# return final_lst
#
# print getall_boxes('bedrock', r'\\rubble')                                                            # noqa
#
# Conclusions
# -----------
#   1) Installing win32net is not easy in an automated way for the average python developer
#   2) There is no cool way to get all potential network shares
#   3) Probably .exe generation would be a problem
#   ==> Solution is worse than pain
#   ==> We stick to  "Enter an EXISTING absolute path"
#

class _DirChooserString:
    """Special class to enter the name of the dir"""
    def __init__(self, root_gui: 'GuiDirChooser', frm, row,
                 text, fr_text,
                 b_text, b_fr_text,
                 initial, max_width1,
                 action):
        self.root_gui = root_gui
        self.frm = frm
        self.action = action
        self.variable = tkinter.StringVar()
        self.variable.set(initial)

        self.label = GuiLabel(root_gui, frm,
                              text=text, fr_text=fr_text,
                              column=0, row=row, width=max_width1)

        self.entry = tkinter.Entry(self.frm, background=PwpGui.LIGHT_GREEN, width=65,
                                   textvariable=self.variable, state=tkinter.NORMAL)
        self.entry.grid(column=1, row=row, sticky="W", columnspan=2)

        self.choose_button = GuiButton(root_gui, frm, text=b_text, fr_text=b_fr_text,
                                       command=self.execute_action, sticky="N",
                                       background=PwpGui.GREEN, column=2, row=row)

    def execute_action(self):
        path = self.variable.get()
        self.action(path)

    def delete(self):
        self.label.destroy()
        self.entry.destroy()
        self.choose_button.destroy()
        # TODO: Add a destroy method for self.variable
        # self.variable.destroy()

# ------------------------------------------------------------------------------------------------
# class GuiDirChooser(PwpGui):
# ------------------------------------------------------------------------------------------------
#


class GuiDirChooser(PwpGui):
    """
    Class to choose a directory
    All paths are internally relative to BASE
    """
    running_chooser = None

    def __init__(self, root_gui, initial_dir, name,
                 home, base,
                 called,
                 x=None, y=None):
        """
        class PwpDirChooser(PwpGui):
        :param root_gui:  calling objet. must implement called(path)
        :param initial_dir: initial value of the directory
        :param name: display name of the directory, can be BASE, HOME, OTHER...
        :param home: HOME, as a potential value
        :param base: BASE, as a potential value
        :param called: method from the father, called upon success
        """
        super().__init__("Choisir un dossier" if PwpGui.language == "fr" else "Directory chooser")
        self.dir_name = initial_dir
        self.father = root_gui
        self.home = home
        self.base = base
        self.called = called
        if x is not None and y is not None:
            self.root.geometry(f"+{int(x + 10)}+{y + 10}")
        self.columns = [22, 33, 15, 15, ]
        self.set_column_sizes(self.columns)
        self.do_dirs = tkinter.StringVar()
        self.folders = []
        self.scrollable = None

        row = 0
        # ----------------------- Logo and banner

        self.logo = pwpLogo_png.tk_photo()
        tkinter.Label(self.frm, image=self.logo).grid(column=0, row=row, sticky="W")

        title_font = tkinter.font.Font(size=14, family="Helvetica", weight="bold")
        title = f"Change '{name}'"

        lab = ttk.Label(self.frm, font=title_font, text=title)
        lab.grid(column=1, row=row, columnspan=8, sticky="W")

        # ----------------------- Current value + abort
        row += 1
        GuiLabel(self, self.frm,
                 text=f"Current {name}",
                 fr_text=f"{name} courant",
                 column=0, row=row, width="")

        val = ACTOR.normalise_path(self.dir_name)
        abs_val = ACTOR.normalise_path(self.dir_name, absolute=True)
        self.cur_dir = GuiLabel(self, self.frm,
                                text=val,
                                fr_text=val,
                                relief=False,
                                width="",
                                column=1, row=row, col_span=2)

        self.abort = GuiButton(self, self.frm, column=3, row=row, sticky="N",
                               text="Cancel", fr_text="Annuler",
                               background='red',
                               command=self.exit)

        # ----------------------- sub directories
        row += 1
        self.sep1 = GuiSeparator(self, self.frm, row=row,
                                 text=f"Directories to choose in {abs_val}",
                                 fr_text=f"Choisir un dossier dans {abs_val}",
                                 width=800)

        # -----------------------

        row += 1
        GuiLabel(self, self.frm, column=0,
                 row=row, text="Directory", fr_text="Dossier", bold=True, width="")

        GuiLabel(self, self.frm, column=1, row=row,
                 text="path of directory",
                 fr_text="chemin du dossier",
                 bold=True,  relief=False,
                 width="", col_span=4, background=PwpGui.GREY)

        row += 1
        self.first_row = row
        self.build_list()
        self.frm.focus_set()
        if GuiDirChooser.running_chooser is not None:
            GuiDirChooser.running_chooser.exit()
        GuiDirChooser.running_chooser = self
        self.mainloop()

    def build_list(self):
        row = self.first_row
        for item in self.folders:
            item.delete()
        if self.scrollable:
            self.scrollable.suicide()

        father = ACTOR.normalise_path(os.path.dirname(self.dir_name))

        self.dir_name = ACTOR.normalise_path(self.dir_name, absolute=True)
        self.sep1.set(text=f"Directories to choose in    {self.dir_name}",
                      fr_text=f"Choisir un dossier dans    {self.dir_name}")

        all_lines = [
            ("[HOME]", ACTOR.linux_path(self.home)),
            ('[BASE]', ACTOR.linux_path(self.base)),
            ("[..] = père" if PwpGui.language == "fr" else "[..] = father",
             ACTOR.normalise_path(father, absolute=True)),
            ("-------------",
             " '.' et sous-dossiers" if PwpGui.language == "fr" else " '.' and sub directories "),
            ("'.'  = ce dossier" if PwpGui.language == "fr" else "'.'  = this directory",
             self.dir_name),
            ("[NEW]", "Special value"),
        ]

        all_dirs = os.listdir(self.dir_name) if os.path.isdir(self.dir_name) else []
        all_lines += [(f, ACTOR.normalise_path(self.dir_name + '/' + f, absolute=True))
                      for f in all_dirs if os.path.isdir(self.dir_name + '/' + f)]

        max_width1 = 30
        max_width2 = PwpGui.VALUE_WIDTH

        for line in all_lines:
            max_width1 = max(max_width1, len(line[0]))
            max_width2 = max(max_width2, len(line[1]))

        self.folders = []

        row += 1

        self.scrollable = GuiScrollable(self.father, self.frm, row=row, name="multilevel",
                                        height=int(min(20, len(all_lines) + 1) * PwpGui.font_pixels * 3.8),
                                        width=(max_width1 + max_width2 + 30) * PwpGui.font_pixels)
        self.scrollable.column_sizes(self.columns)
        cur_frame = self.scrollable.frm
        row = 0
        self.folders.append(_DirChooserString(self, cur_frame, row=row,
                                              text="An ABSOLUTE path",
                                              fr_text="Un path ABSOLU",
                                              b_text="Enter",
                                              b_fr_text="Entrer",
                                              initial="Entrer un chemin EXISTANT" if PwpGui.language == "fr"
                                              else "Enter EXISTING path",
                                              max_width1=max_width1,
                                              action=self.check_and_enter))
        row += 1
        for line in all_lines:
            if line[0] == "[NEW]":
                self.folders.append(_DirChooserString(self, cur_frame, row=row,
                                                      text="New directory",
                                                      fr_text="Nouveau dossier",
                                                      b_text="Create",
                                                      b_fr_text="Créer",
                                                      initial="Entrer un NOUVEAU nom" if PwpGui.language == "fr"
                                                      else "Enter a NEW name",
                                                      max_width1=max_width1,
                                                      action=self.create))
            else:
                self.folders.append(_DirChooserField(self, cur_frame, path=line[0], abspath=line[1], row=row,
                                                     max_width1=max_width1, max_width2=max_width2))
            row += 1

    def create(self, path):
        if (path.startswith("./") or
                path.startswith("../") or
                path.startswith(".\\") or
                path.startswith("..\\")):  # pragma: no cover: defensive code
            LOGGER.warning("Illegal path", f"'{path}' starts with ./ or ../")
            return

        full_path = self.dir_name + '/' + path
        if os.path.isdir(path):  # pragma: no cover: defensive code
            LOGGER.warning("Trying to create an existing dir", path)
            return
        os.makedirs(full_path)
        LOGGER.msg(f"Created dir {full_path}")
        self.build_list()

    def check_and_enter(self, path):
        self.enter(path, check=True)

    def select(self, path: str):
        if path.startswith("'.'"):
            path = self.dir_name
        elif path.startswith("[..]"):
            path = self.dir_name + '/..'
        elif path.startswith("[HOME]"):
            path = self.home
        elif path.startswith("[BASE]"):
            path = self.base
        else:
            path = self.dir_name + '/' + path

        full_path = ACTOR.normalise_path(path, error_if_not_included=False)

        if self.father and self.called:
            self.called(full_path)
        LOGGER.msg(f"Chose directory '{full_path}'")
        self.exit()

    def enter(self, path, check=False):
        if path.startswith("'.'"):
            path = self.dir_name
        elif path.startswith("[..]"):
            path = self.dir_name + '/..'
        elif path.startswith("[HOME]"):
            path = self.home
        elif path.startswith("[BASE]"):
            path = self.base
        else:
            path = self.dir_name + '/' + path

        if check and not os.path.isdir(path):
            LOGGER.warning(f"Chosen directory '{path}' does not exist")
            return

        full_path = ACTOR.normalise_path(path, error_if_not_included=False)

        LOGGER.msg(f"Enter directory '{full_path}'")
        self.dir_name = full_path
        self.build_list()

    def exit(self):
        self.scrollable.suicide()
        super().exit()
        GuiDirChooser.running_chooser = None


# ================================================================================
# GuiStringEditor
# ================================================================================


class GuiStringEditor(PwpGui):
    """
    Class to edit a string
    """
    # running_editor = None

    def __init__(self, root_gui: PwpGui, father, name, initial, x=None, y=None):
        """
        class PwpStringEditor(PwpGui):
        :param father:  calling objet. must implement select_dir(path)
        :param initial: initial value
        """
        super().__init__("String Editor")
        self.initial = initial
        self.father = father
        self.root_gui = root_gui

        # we do NOT record a String editor to its root GUI,
        # because string editors are dynamically built with the right language
        # and are destroyed after usage
        # root_gui.record_item(self)

        self.variable = tkinter.StringVar()
        self.variable.set(initial)

        if x is not None and y is not None:
            self.root.geometry(f"+{int(x + 10)}+{y + 10}")

        self.set_column_sizes([15, 55, 18, 18])

        # ----------------------- Logo and banner
        row = 0

        self.logo = pwpLogo_png.tk_photo()
        tkinter.Label(self.frm, image=self.logo).grid(column=0, row=row, sticky="W")

        # ----------------------- Title
        row += 1
        GuiLabel(self, self.frm, column=0, row=row, text="Change", fr_text="Changer", bold=True)
        GuiLabel(self, self.frm, column=1, row=row, text=name, fr_text=name, bold=True, width="")

        row += 1
        GuiLabel(self, self.frm, column=0, row=row, bold=True, width="",
                 text="Current value", fr_text="Valeur courante")
        GuiLabel(self, self.frm, column=1, row=row, text=initial, fr_text=initial, width="")

        # ----------------------- Abort
        row += 1

        val = self.variable.get()
        length = len(val) if val else 0

        entry = tkinter.Entry(self.frm, background=PwpGui.LIGHT_GREEN, width=max(70, length),
                              textvariable=self.variable, state=tkinter.NORMAL)
        entry.grid(column=0, row=row, sticky="W", columnspan=2)

        GuiButton(self, self.frm, column=2, row=row, text="Ok", fr_text="Ok", command=self.choose)
        GuiButton(self, self.frm, column=3, row=row, text="Cancel", fr_text="Annuler", command=self.exit,
                  background="red")

        self.frm.focus_set()
        # if GuiStringEditor.running_editor is not None:
        #     GuiStringEditor.running_editor.exit()
        # GuiStringEditor.running_editor = self

    def choose(self):
        ret_val = self.variable.get()
        if self.father:
            self.father.set_value_and_refresh(ret_val, "GUI", "modify")
        LOGGER.msg(f"Chose '{ret_val}'")
        self.exit()
        # GuiStringEditor.running_editor = None

# ================================================================================
# GuiError
# ================================================================================


class GuiError(PwpGui):
    globalError = None

    def __init__(self, en_txt: str, fr_txt: str, warning=False):
        super().__init__("ERROR")
        if GuiError.globalError:
            GuiError.globalError.dismiss()

        self.label = GuiLabel(self, self.frm, 1, 1,
                              en_txt,
                              fr_txt,
                              background="orange" if warning else "red",
                              width="",
                              bold=True)
        self.button = GuiButton(self, self.frm, 1, 2, "OK", "OK", self.dismiss,
                                background=PwpGui.GREEN, sticky="S",
                                width=PwpGui.BUTTON_WIDTH)

        # self.root.geometry(f"+{int(x + 10)}+{y + 10}")

        self.root.deiconify()
        self.root.lift()

    def dismiss(self):
        if GuiError.globalError:
            GuiError.globalError = None
        self.exit()

    @staticmethod
    def global_dismiss():
        if GuiError.globalError:
            GuiError.globalError.dismiss()


# ================================================================================
# GuiInfo
# ================================================================================


class GuiInfo(PwpGui):
    def __init__(self):
        super().__init__("info")
        self.logo = pwpLogo_png.tk_photo()
        tkinter.Label(self.frm, image=self.logo).grid(column=0, row=0, sticky="W")

        self.title = ttk.Label(self.frm, text="info", padding=4, width=100, font=self.label_font)
        self.title.grid(column=0, row=1, sticky="N")

        self.label = ttk.Label(self.frm, text="info", anchor="w", padding=4, width=100)
        self.label.grid(column=0, row=2, sticky="W")

        self.hide()

    def show_at_row(self, title, info, x, y):
        self.title['text'] = title
        self.label['text'] = info
        self.root.deiconify()
        self.root.lift()

        self.root.geometry(f"+{int(x + 10)}+{y + 10}")

    def hide(self):
        self.root.withdraw()


# ================================================================================
# GuiLevelSeparator
# ================================================================================


class GuiLevelSeparator:
    def __init__(self, root_gui, frm, row, label, fr_label):
        self.frm = frm
        self.frame = tkinter.Frame(frm, width=1300, height=4, background="#aaaCCCaaa", )
        self.frame.grid(column=0, row=row, columnspan=9, sticky="W")
        self.label = GuiLabel(root_gui, frm, column=1, row=row, bold=True, col_span=3, width="",
                              text=label, fr_text=fr_label)
        self.root_gui = root_gui
        self.root_gui.record_widget(self)

    def set_language(self, _lang):
        pass

    def suicide(self):
        self.root_gui.remove_widget(self)
        self.root_gui.remove_widget(self.label)


class GuiSeparator:
    def __init__(self, root_gui, frm, row, text, fr_text, width=1300):
        self.frm = frm
        self.row = row
        self.frame = tkinter.Frame(self.frm, width=width, height=10, background=PwpGui.LIGHT_BLUE)
        self.frame.grid(column=0, row=row, columnspan=9, sticky="W")  # noqa
        self.label = GuiLabel(root_gui, frm, column=0, row=row, background=PwpGui.LIGHT_BLUE,
                              text=text, fr_text=fr_text, bold=True, col_span=5, width="")

    def set(self, text, fr_text):
        self.label.set(text, fr_text)

    def hide(self):
        self.frame.grid_forget()
        self.label.hide()

    def show(self):
        self.frame.grid(column=0, row=self.row, columnspan=9, sticky="W")
        self.label.show()


# ================================================================================
# GuiLevelButton
# ================================================================================


class GuiLevelButton(GuiButton):    # pragma: no cover: This Gui element is not used yet
    def __init__(self, root_gui, frm, row, command, label, fr_label, value: str,
                 column=0,
                 text_on='[-]', text_off='[+]', width=3):

        super().__init__(root_gui, frm, column=column, row=row, text=text_on, fr_text=text_on,
                         command=lambda: command(self.value),
                         background=PwpGui.GREEN, width=width)
        self.frame = tkinter.Frame(frm, width=900, height=10, background="#aaaCCCaaa", )
        self.frame.grid(column=0, row=row, columnspan=8, sticky="W")
        self.frame.lower(self)
        self.label = GuiLabel(root_gui, frm, column=1, row=row, text=label, fr_text=fr_label,
                              bold=True, col_span=3, width="")
        self.value = value
        self.command = command
        self.text_on = text_on
        self.text_off = text_off
        self.column = column

    def refresh(self, level: str):
        if level == self.value:
            self["text"] = self.text_on
        else:
            self["text"] = self.text_off

    def show_at_row(self, row):
        self.grid(column=self.column, row=row, sticky="W")
        self.frame.grid(column=0, row=row, columnspan=8, sticky="W")
        self.frame.lower(self)
        self.label.show_at_row(row)

    def hide(self):
        self.grid_forget()
        self.label.hide()


# ================================================================================
# GuiFrame
# ================================================================================


class GuiFrame(ttk.Frame):
    def __init__(self, frm, row, column=0, width=100, height=100, columnspan=9, column_sizes=None):  # noqa
        super().__init__(frm, width=width, height=height)
        self.column = column
        self.row = row
        self.columnspan = columnspan  # noqa
        super().grid(column=column, row=row, columnspan=columnspan, sticky="W")

        self.row = row
        column_sizes = column_sizes or []
        for i in range(0, len(column_sizes)):
            self.columnconfigure(i, minsize=PwpGui.font_pixels * column_sizes[i])

    def hide(self):
        super().grid_forget()

    def show(self):
        super().grid(column=self.column, row=self.row, columnspan=self.columnspan, sticky="W")


# ================================================================================
# GuiScrollable
# ================================================================================


class GuiScrollable(ttk.Frame):
    canvases = []

    def __init__(self, root_gui: PwpGui, frm, row, height=400, width=1400, column_sizes=None, name="",
                 horizontal_scroll=False):
        super().__init__(frm)
        super().grid(column=0, row=row, columnspan=9, sticky="W")
        self.root_gui = root_gui
        self.name = name
        self.levels = []
        self.all_lines = {}  # all_lines[name] = item
        self.variable = tkinter.StringVar()
        self.variable.set(str(0))
        self.row = row

        self.canvas = tkinter.Canvas(self, width=width, height=height)
        GuiScrollable.canvases.append(self.canvas)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.frm = ttk.Frame(self.canvas)
        self.frm.grid(column=0, row=row, columnspan=9, sticky="W")

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        self.column_sizes(column_sizes if column_sizes else [])

        self.canvas.create_window((0, 0), window=self.frm, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        if horizontal_scroll:
            scroll_h = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            scroll_h.pack(side="bottom", fill="x")
            self.canvas.configure(xscrollcommand=scroll_h.set)

        self.canvas.pack(side="left", fill="both", expand=True)

    def suicide(self):
        pass
        for level in self.levels:
            level.suicide()
            del level
        for name in self.all_lines:
            self.all_lines[name].suicide()
        del self.all_lines
        if self.canvas in GuiScrollable.canvases:
            GuiScrollable.canvases.remove(self.canvas)
        self.destroy()

    def column_sizes(self, sizes):
        for i in range(0, len(sizes)):
            self.frm.columnconfigure(i, minsize=PwpGui.font_pixels * sizes[i])

    @staticmethod
    def on_mouse_wheel(event):
        # O ---> x
        # |
        # v
        # Y
        if GuiScrollable.canvases is not None:
            for canvas in reversed(GuiScrollable.canvases):
                try:
                    root_x = canvas.winfo_rootx()
                    root_y = canvas.winfo_rooty()
                    height = canvas.winfo_height()
                    width = canvas.winfo_width()
                    if (root_x <= event.x_root <= root_x + width) and (root_y <= event.y_root <= root_y + height):
                        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        return
                except tkinter.TclError:
                    LOGGER.error("Wrong canvas in Scrollable")
                    # This was BUG 3132
                    # Steps to reproduce:
                    # PwpConfigurator / Parameters / Choose subdirectory / New subdirectory / Cancel  # noqa
                    # Scroll
                    # the scrollable for String editor is still in the scrollable list

        # else, out of my window, do nothing

    def add_level(self, row, label, fr_label):
        level = GuiLevelSeparator(self.root_gui, self.frm, row=row, label=label, fr_label=fr_label)
        self.levels.append(level)

    def add_item(self, item, name):
        if name is not None:
            self.all_lines[name] = item


# class GuiMultiLevels(tkinter.Frame):
#     def __init__(self, root, frm, row, column_sizes):
#         super().__init__(frm)
#         self.root = root
#         self.frm = self
#         self.levels = []
#         self.lines = {}                 # lines[cur_level][name] = item
#         self.all_lines = {}             # all_lines[name] = item
#         self.variable = tkinter.StringVar()
#         self.variable.set(str(0))
#         self.row = row
#         super().grid(column=0, row=row, columnspan=9, sticky="W")   # noqa
#         self.column_sizes(column_sizes)
#
#     def suicide(self):
#         for level in self.levels:
#             self.root.remove_widget(level)
#             del level
#         self.destroy()
#
#     def column_sizes(self, sizes):
#         for i in range(0, len(sizes)):
#             self.frm.columnconfigure(i, minsize=PwpGui.font_pixels * sizes[i])
#
#     def add_level(self, row, label, fr_label):
#         cur_level = str(len(self.levels))
#         new_level = GuiLevelButton(self.root, self.frm, row=row, command=self.refresh,
#                                    label=label, fr_label=fr_label,
#                                    value=cur_level)
#         self.levels.append(new_level)
#         self.lines[cur_level] = {}
#
#     def add_item(self, item, name):
#         cur_level = str(len(self.levels)-1)
#         if len(self.levels) > 0:
#             self.lines[cur_level][name] = item
#             self.all_lines[name] = item
#
#     def refresh(self, level_number: str = "0"):
#         row = self.row
#         for i in range(0, len(self.levels)):
#             cur_level = str(i)
#             self.levels[i].refresh(level_number)
#             self.levels[i].show_at_row(row=row)
#             row += 1
#             for _k, item in self.lines[cur_level].current_constraints():
#                 if cur_level == level_number:
#                     item.show_at_row(row=row)
#                     row += 1
#                 else:
#                     item.hide()
#


# ================================================================================
# GuiExpandable
# ================================================================================

class GuiExpandable(ttk.Label):
    info_window = None
    width = 15

    def __init__(self, frm, column, row, name, text, long_text):
        super().__init__(frm, text="ESSAI",
                         background=PwpGui.VERY_LIGHT_GREEN,
                         foreground="dark green",
                         anchor="w", padding=2, width=GuiExpandable.width)
        self.name = name
        self.actual_text = None
        self.mini = None
        self.set(text, long_text)
        self.grid(column=column, row=row, sticky="W")
        self.bind("<Button-1>", self.show_info)
        self.bind("<ButtonRelease-1>", self.hide_info)
        self.column = column

        if GuiExpandable.info_window is None:
            GuiExpandable.info_window = GuiInfo()

    def show_at_row(self, row):
        self.grid(column=self.column, row=row, sticky="W")

    def hide(self):
        self.grid_forget()

    def show_info(self, event, x=None, y=None):
        x = event.x_root if event else x  # hack for test
        y = event.y_root if event else y
        GuiExpandable.info_window.show_at_row(self.name, self.actual_text, x, y)

    @staticmethod
    def hide_info(_event=None):
        if GuiExpandable.info_window:
            GuiExpandable.info_window.hide()

    def set(self, text: str, long_text: str):
        self.actual_text = long_text
        self.mini = text[-GuiExpandable.width:]
        self['text'] = self.mini

    def get(self):
        if self.mini == "GUI":
            return "GUI"
        if self.mini == "DEFAULT":
            return "DEFAULT"
        # in all other cases, the filename actual_text, and we want this
        return self.actual_text


# ================================================================================
# GuiValue
# ================================================================================

class GuiValue:
    def __init__(self, root_gui: PwpGui, frm, row: int,
                 dico: dict, fr_dico: dict,
                 column: int = 0, columnspan=1,  # noqa
                 width: int = PwpGui.VALUE_WIDTH):

        self.root_gui = root_gui
        root_gui.record_widget(self)
        self.internal = tkinter.StringVar()
        self.dico = dico
        self.fr_dico = fr_dico
        self.value = None
        self.column = column
        self.columnspan = columnspan        # noqa
        self.row = row
        self.internal.set("???")
        self.entry = tkinter.Entry(frm, width=width,
                                   textvariable=self.internal, state=tkinter.DISABLED,
                                   )
        self.entry.grid(column=column, row=row, sticky="W", columnspan=columnspan)

    def get(self):
        return self.value

    def set(self, val):
        self.value = val
        translated = "???"
        if val in self.dico:
            translated = self.dico[val] if PwpGui.language == "en" else self.fr_dico[val]
        self.internal.set(translated)

    def set_language(self, lang):
        val = self.value
        translated = "???"
        if val in self.dico:
            translated = self.dico[val] if lang == "en" else self.fr_dico[val]
        self.internal.set(translated)

    def hide(self):
        self.entry.grid_forget()

    def show(self):
        self.entry.grid(column=self.column, row=self.row, sticky="W", columnspan=self.columnspan)


# ------------------------------------------------------------------------------
# GuiRadios
# ------------------------------------------------------------------------------


class GuiRadios:
    def __init__(self, root_gui: PwpGui, frm, name: str or None, fr_name: str or None,
                 row: int, dico: dict, fr_dico: dict,
                 variable, command, column: int = 0, width: int = 10):
        # dico and fr_dico are dict[value] = displayed text
        self.row = row
        self.column = column
        self.label = None
        self.variable = variable

        if name is not None:
            self.label = GuiLabel(root_gui=root_gui, frm=frm, text=name, fr_text=fr_name,
                                  column=column, row=row, bold=True, width=width, )
            column += 1

        self.dico = dico
        self.fr_dico = fr_dico
        self.radios = {}
        self.columns = {}

        root_gui.record_widget(self)
        for val, text in fr_dico.items():
            # see https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/radiobutton.html
            style = ttk.Style()
            style.configure('TRadiobutton', focuscolor='green')
            # TODO: change the focus color of Radiobuttons from blue to green.
            # foreground="yellow" : OK
            # background='red'   : OK
            # focus="green"             : KO
            # indicatorcolor = 'orange' : KO                # noqa
            # focuscolor = 'orange'     : KO                # noqa
            # selectcolor='orange'      : KO                # noqa
            # highlightbackground='orange'  : KO            # noqa
            # highlightcolor='orange'   : KO                # noqa

            rad = ttk.Radiobutton(frm, value=val, text=text if PwpGui.language == "fr" else dico[val],
                                  command=command,
                                  style='TRadiobutton',     # the style is found, but not applied .
                                  # width=PwpGui.RADIO_WIDTH,
                                  variable=variable)

            rad.grid(column=column, row=row, sticky="W")
            self.radios[val] = rad
            self.columns[val] = column
            column += 1

    def show(self):
        if self.label is not None:
            self.label.show()
        for val in self.fr_dico.keys():
            rad = self.radios[val]
            column = self.columns[val]
            rad.grid(column=column, row=self.row, sticky="W")

    def hide(self):
        if self.label is not None:
            self.label.hide()
        for val in self.fr_dico.keys():
            rad = self.radios[val]
            rad.grid_forget()

    def get_xy(self):
        for val in self.radios:
            return self.radios[val].winfo_rootx(), self.radios[val].winfo_rooty()

    def set_language(self, lang):
        for val in self.radios:
            rad = self.radios[val]
            rad['text'] = self.fr_dico[val] if lang == "fr" else self.dico[val]

    def disable(self):
        for val in self.radios:
            self.radios[val]["state"] = 'disabled'

    def enable(self):
        for val in self.radios:
            self.radios[val]["state"] = 'normal'


# -------------------------------------------------------------------------
# GuiGroup
# -------------------------------------------------------------------------
# hide or show as a whole


class GuiGroup:
    def __init__(self):
        self.on = False
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        item.hide()

    def hide(self):
        self.on = False
        for item in self.items:
            item.hide()

    def show(self):
        self.on = True
        for item in self.items:
            item.show()

    def refresh(self):
        if self.on:
            self.show()
        else:
            self.hide()


# -------------------------------------------------------------------------
# GuiFolded
# -------------------------------------------------------------------------

# TODO: Quelle difference entre GuiFolded et GuiGroup ?

class GuiFolded(GuiFrame):
    def __init__(self, father_frm, width: int, height: int, row: int, column_sizes, columnspan): # noqa
        # noqa
        super().__init__(father_frm, row=row, width=width, height=height, columnspan=columnspan,
                         column_sizes=column_sizes)
        self.on = False
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def delete_all(self):
        for item in self.items:
            item.destroy()
        self.items = []

    def refresh(self):
        if self.on:
            self.show()
        else:
            self.hide()

    def show(self):
        self.on = True
        super().show()

    def hide(self):
        self.on = False
        super().hide()


class GuiVerticalRadio(PwpGui):
    """Class to choose among several values, vertically presented, in a window"""

    def __init__(self, root_gui, en_text, fr_text, lines,  x=None, y=None):
        super().__init__(fr_text if PwpGui.language == "fr" else en_text, PwpGui.language)
        self.father = root_gui
        self.lines = lines
        self.values = []
        self.buttons = []
        if x is not None and y is not None:
            self.root.geometry(f"+{int(x + 10)}+{y + 10}")

        # ----------------------- Logo and banner
        row = 0
        self.logo = pwpLogo_png.tk_photo()
        tkinter.Label(self.frm, image=self.logo).grid(column=0, row=row, sticky="W")

        row += 1
        self.lab = GuiLabel(self, self.frm, column=0, row=row, fr_text=fr_text, text=en_text,
                            width="", bold=True)

        row += 1
        GuiLabel(self, self.frm, column=0, row=row, fr_text="Annuler le choix", text="Cancel choice", width="")

        self.abort_button = GuiButton(self, self.frm,
                                      column=1, row=row, text="Abort", fr_text="Annuler",
                                      background=PwpGui.ORANGE,
                                      command=self.exit)

        for item in lines:
            row += 1
            value = item[0]
            action = item[1]
            self.values.append(value)
            GuiLabel(self, self.frm, column=0, row=row, fr_text=value, text=value, relief=True, width="")
            button = GuiButton(self, self.frm,
                               column=1, row=row, text="Choose", fr_text="Choisir",
                               command=action)
            self.buttons.append(button)
