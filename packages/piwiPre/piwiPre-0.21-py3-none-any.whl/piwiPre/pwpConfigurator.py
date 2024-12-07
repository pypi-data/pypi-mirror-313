# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import sys
import os
import tkinter
import platform
import shutil
import threading
import webbrowser
import time
from tkinter import ttk
import tkinter.font

from piwiPre.pwpActor import ACTOR

if platform.system() == "Windows":
    import pylnk3

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from piwiPre.pwpVersion import PwpVersion
from piwiPre.pwpParser import PwpParser
from piwiPre.pwpArgsIni import ConstraintHow, ServerSetup, CVS, PwpConstraint, PwpArgType
from piwiPre.pwpGui import GuiLabel, GuiExpandable, PwpGui, GuiStringEditor, GuiDirChooser, GuiButton, GuiRadios, \
    GuiScrollable, GuiFrame, GuiSeparator, GuiValue, GuiGroup, GuiEntry, GuiFolded, GuiVerticalRadio, GuiError
from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpLogoSmall import pwpLogo_png
from piwiPre.pwpErrors import LOGGER


# REQ 6001: Configurator edits piwiPre.ini files, in text or GUI mode
# REQ 6002: piwiPre has a GUI, that allows to modify args arguments and show the current config file

# REQ 6020: depending on the setup, some configuration items are useless. They are not displayed.
# REQ 6050: String values background is meaningful
#       grey if the unmodified value fromconfig file (aka undo),
#       white if clear
#       green when modified

# REQ 6101: Need to check 'modify' to change values
# REQ 6102: 'directory' fields have a directory chooser UI
# REQ 6103: There is only 1 directory chooser, shared by all usages
# REQ 6104: Need to select 'modify' to modify a value.
# REQ 6105: origin has a button, press to view complete value
# REQ 6106: items are fold-able by category
# REQ 6107: directories are displayed as relative path to CWD
# REQ 6108: when at least 1 item has been modified, "SAVE" and "UNDO" are available, and "Change dir" and "HOME" are not
# REQ 6109: when all items are not modified, "SAVE" and "UNDO" are not available, and "Change dir" and "HOME" are
# REQ 6110 : all widgets have 2 texts: en... , with a global change event.
# REQ 6111: config items window is scrollable with scroll bar and mouse wheel
# REQ 6112:  create piwiPre.bat/sh in the configured directory, with --base and --home
# REQ 6113: verbose/short version of the .ini, depending on --verbose
# REQ 6114: Only 1 setup editor
# REQ 6115: BUG When Configurator is started twice by the test harness, the 2nd time, bold font is bad + an extra window
# REQ 6116: in piwiPre mode, RUN is active even with modification of parameters, but inactive if used once
# REQ 6117: DirChooser: has a "create dir" button
# REQ 6118: DirChooser long directories are managed  with a vertical scrollbar
# REQ 6119: GuiScrollable: has an horizontal scrollbar
# REQ 6120: in piwiPre mode, the cmdline arguments are at the start of screen
# TODO REQ 6121: StringEditor: SHOW/HIDE for passwords
# REQ 6122: the scrollable areas can be scrolled with mouse button when the mouse is over their window
#
# REQ 6124: MINOR bug: messenger is not completely readable through scroll-bar & mouse events
# REQ 6125: when piwiPre is running: run a spinner, disable SAVE, RUN, CANCEL, UNDO

# REQ 6126: Installer can be stopped after launch of Configurator.
# REQ 6127: piwiPre should remember last BASE when config writen (configurator) or piwiPre run
#           When started from main program menu, (or with option --base-last)
#           change dir to that last BASE, otherwise to HOME if BASE does not exist
# REQ 6128: Configurator has an HTML help
# REQ 6129: Backup() use the date (rather than increment numbers).
# TODO REQ 6130: Multiline string editor allows to change authors, dates etc.
# DONE, by hand: test Configurator and piwiPre GUI without HOME/.piwiPre.ini
# DONE, by hand: test  "pwpInstaller --gui false --mode install --piwipre --ffmpeg "
# REQ 6131: BUG: if 'names' is changed by the GUI, the display is still the OLD value, but config file is OK


# --------------------------------------------- GUI Main --------------------------------------------


def equal_path(p1, p2):
    # CAVEAT ! abspath does NOT normalize the character case !
    # so we need to normcase because of WINDOWS, which does normcase.
    if platform.system() == 'Windows':
        return os.path.normcase(os.path.abspath(p1)) == os.path.normcase(os.path.abspath(p2))
    else:
        return os.path.abspath(p1) == os.path.abspath(p2)


class Field:
    def __init__(self, root_gui: 'PwpEditorUI', frm, name: str, constraint: PwpConstraint, row: int,
                 config: PwpConfig, allow_modification: bool):
        self.name = name
        self.frm = frm
        self.root_gui = root_gui
        self.config = config
        self.constraint = constraint
        self.allow_modification = allow_modification

        self.label = GuiLabel(root_gui=root_gui, frm=self.frm, text=name, fr_text=name, column=0, row=row, width=25)

        self.variable = tkinter.StringVar()
        self.change_var = tkinter.StringVar()

        self.how = constraint.how

        self.origin = GuiExpandable(self.frm, column=4, row=row, name=f"Origin of {name}", text="void",
                                    long_text="a longer explanation")

        self.first_value = self.config[self.name]
        self.first_origin = self.config.get_origin(self.name)

        self.prev_value = self.config.get_previous_value(self.name)
        self.prev_origin = self.config.get_previous_origin(self.name)

        if allow_modification:
            self.action_radio = GuiRadios(root_gui=root_gui, frm=self.frm, name=None, fr_name=None,
                                          dico={"undo": "Un-modified", "clear": "Inherit", "modify": "Modify"},
                                          fr_dico={"undo": "Sans modif", "clear": "Hériter", "modify": "Modifier"},
                                          variable=self.change_var, command=self.refresh_value,
                                          column=5, row=row, )
        else:
            self.action_radio = None

        self.help_label = GuiLabel(root_gui=root_gui, frm=self.frm,
                                   text=constraint.helps, fr_text=constraint.fr_helps,
                                   column=8, row=row, width=self.root_gui.VALUE_WIDTH)

    def suicide(self):
        self.root_gui.remove_widget(self.label)
        if self.action_radio:
            self.root_gui.remove_widget(self.action_radio)
        self.root_gui.remove_widget(self.help_label)

    # def show(self, row):
    #     self.label.show(row)
    #     self.origin.show(row)
    #     self.undo_radio.grid(column=5, row=row, sticky="W")
    #     self.clear_radio.grid(column=6, row=row, sticky="W")
    #     self.modify_radio.grid(column=7, row=row, sticky="W")
    #     self.help_label.grid(column=8, row=row, sticky="W")

    @staticmethod
    def create_field(root: 'PwpEditorUI', frm, name: str, row: int,
                     constraint: PwpConstraint,
                     config: PwpConfig,
                     allow_modification: bool):
        if constraint.pwp_type == PwpArgType.BOOL or constraint.pwp_type == PwpArgType.PRESENT:
            res = BoolField(name, row, root, frm, constraint, config, allow_modification)
        elif constraint.pwp_type == PwpArgType.PASSWORD:
            res = PasswordField(root, frm, name, row, constraint, config, allow_modification)
        elif constraint.pwp_type in [PwpArgType.STR, PwpArgType.INT]:  # TODO: add IntField
            res = StringField(name, row, root, frm, constraint, config, allow_modification)
        elif constraint.pwp_type == PwpArgType.DIR:
            res = DirField(name, row, root, frm, constraint, config, allow_modification)
        else:
            raise OSError
        # We cannot undo() here, because
        # if the server settings have been modified,
        # then the initial values are NOT coming from the file,
        #
        res.first_display()
        return res

    def first_display(self):
        """
        Display the item for the first time after creation is complete
        :return: None
        """
        if self.constraint.origin == 'GUI':
            self.set_value_and_refresh(self.constraint.value, 'GUI', 'modify', refresh=False)
        else:
            self.undo(refresh=False)

    def get_value(self):
        return self.variable.get()

    def get_origin(self):
        return self.origin.get()

    def set_value_and_refresh(self, value, origin, change, refresh=True):
        """This method is automatically called by the GUI element in charge of the modification,
           e.g. GuiStringEditor
        """
        self.variable.set("true" if value is True else "false" if value is False else str(value))
        if origin == "DEFAULT":
            longer = "Built-in default value" if PwpGui.language == "en" else "Valeur par défaut, par construction"
        elif origin == "GUI":
            longer = "Set by the Graphical User Interface" if PwpGui.language == "en" else \
                "En provenance de l'interface graphique"
        elif equal_path(os.path.dirname(origin), self.config['home']):
            longer = origin
            origin = "HOME"
        elif equal_path(os.path.dirname(origin), self.config['base']):
            longer = origin
            origin = "BASE"
        else:
            longer = origin
            origin = "SUB DIRECTORY"

        self.origin.set(origin, longer)
        self.change_var.set(change)
        if refresh:
            self.root_gui.refresh_main_buttons()

    def undo(self, refresh=True):
        self.set_value_and_refresh(self.first_value, self.first_origin, 'undo', refresh=refresh)

    def clear(self):
        self.set_value_and_refresh(self.prev_value, self.prev_origin, 'clear', refresh=True)

    def modify(self):
        # self.set_value(self.first_value)  # let's keep the existing value, so that we can modify twice
        self.set_value_and_refresh(self.get_value(), "GUI", change='modify', refresh=True)
        # self.origin.set("GUI")
        # self.change_var.set('modify')
        # self.root_gui.refresh_main_buttons()

    def refresh_value(self):
        new_mode = self.change_var.get()
        if new_mode == "undo":
            self.undo()
        elif new_mode == "clear":
            self.clear()
        else:
            self.modify()

    # def delete(self):
    #     self.label.destroy()
    #     del self.variable
    #     self.origin.destroy()
    #     if self.change_var:
    #         del self.change_var
    #         self.undo_radio.destroy()
    #         self.clear_radio.destroy()
    #         self.modify_radio.destroy()
    #     self.help_label.destroy()

    # def hide(self):
    #     self.label.grid_forget()
    #     self.origin.grid_forget()
    #     if self.change_var:
    #         self.undo_radio.grid_forget()
    #         self.clear_radio.grid_forget()
    #         self.modify_radio.grid_forget()
    #     self.help_label.grid_forget()


class BoolField(Field):
    def __init__(self, name: str, row: int, root_gui: 'PwpEditorUI', frm, constraint,
                 config: PwpConfig, allow_modification: bool):
        super().__init__(root_gui, frm, name, constraint, row, config, allow_modification)

        if constraint.how == ConstraintHow.CMDLINE:
            self.first_value = constraint.initial == 'true'
            self.prev_value = constraint.initial == 'true'
        # else, the init was correctly done

        self.on_radio = ttk.Radiobutton(self.frm, value="true", text="true", width=self.root_gui.RADIO_WIDTH,
                                        variable=self.variable)
        self.on_radio.grid(column=1, row=row, sticky="W")
        self.off_radio = ttk.Radiobutton(self.frm, value="false", text="false", width=self.root_gui.RADIO_WIDTH,
                                         variable=self.variable)
        self.off_radio.grid(column=2, row=row, sticky="W")

    # def show(self, row):
    #     super().show(row)
    #     self.on_radio.grid(column=1, row=row, sticky="W")
    #     self.off_radio.grid(column=2, row=row, sticky="W")

    # def delete(self):
    #     super().delete()
    #     self.on_radio.destroy()
    #     self.off_radio.destroy()

    # def hide(self):
    #     super().hide()
    #     self.on_radio.grid_forget()
    #     self.off_radio.grid_forget()

    def set_value_and_refresh(self, value, origin, change, refresh=True):
        new_value = "true" if (value is True or value == "true") else "false"
        super().set_value_and_refresh(new_value, origin, change, refresh=refresh)

    def undo(self, refresh=True):
        super().undo(refresh)
        self.on_radio.state(['disabled'])
        self.off_radio.state(['disabled'])

    def modify(self):
        super().modify()
        self.on_radio.state(['!disabled'])
        self.off_radio.state(['!disabled'])

    def clear(self):
        super().clear()
        self.on_radio.state(['disabled'])
        self.off_radio.state(['disabled'])


class StringField(Field):
    def __init__(self, name: str, row: int, root_gui: 'PwpEditorUI', frm, constraint,
                 config: PwpConfig, allow_modification: bool):
        super().__init__(root_gui, frm, name, constraint, row, config, allow_modification)

        # The 'validate' method to set actually the value is not clear to average users:
        # validation is done only when the widget comes out of focus, which is confusing.
        # a traditional box with OK/Cancel is better.
        # self.validate_cmd = frm.register(self.validate)

        self.item = tkinter.Entry(self.frm, background=PwpGui.LIGHT_GREEN, width=self.root_gui.VALUE_WIDTH,
                                  # validate='focusout',
                                  # validate command=self.validate_cmd,
                                  textvariable=self.variable, state=tkinter.DISABLED)
        self.item.grid(column=1, row=row, sticky="W", columnspan=3)
        self.editor = None

    # def validate(self):
    #     self.father.add_msg(f"'{self.name}' new value = {self.get_value()}\n")
    #     return True

    # def show(self, row):
    #     super().show(row)
    #     self.item.grid(column=1, row=row, sticky="W", columnspan=3)   # noqa

    # def delete(self):
    #     super().delete()
    #     self.item.destroy()

    # def hide(self):
    #     super().hide()
    #     self.item.grid_forget()

    def undo(self, refresh=True):
        super().undo(refresh)
        self.item.configure(disabledbackground=PwpGui.GREY)

    def modify(self, gui=True, x=None, y=None):
        super().modify()
        self.item.configure(disabledbackground=PwpGui.GREY2)  # do this before Editor, otherwise code not reached
        if gui:
            if x is None and y is None:  # x and y are specified while we test
                x, y = self.action_radio.get_xy()
            self.editor = GuiStringEditor(father=self, name=self.name,
                                          initial=self.get_value(), root_gui=self.root_gui,
                                          x=x + 10,
                                          y=y + 10)
            # self.editor.run() this is useless, because the mainloop() is already running

    def clear(self):
        super().clear()
        self.item.configure(disabledbackground=PwpGui.WHITE)


class DirField(StringField):
    def __init__(self, name: str, row: int, root_gui: 'PwpEditorUI', frm, constraint,
                 config: PwpConfig, allow_modification: bool):
        super().__init__(name, row, root_gui, frm, constraint, config, allow_modification)

    def modify(self, gui=True, x=None, y=None):
        # CAVEAT: we MUST bypass the STRING.modify(), otherwise we end-up in the string editor
        super().modify(gui=False)  # if PwpDirChooser is cancelled, we keep the existing value
        if x is None and y is None:
            x, y = self.action_radio.get_xy()
        GuiDirChooser(self, ACTOR.normalise_path(self.variable.get()),
                      self.name, called=self.select_one_dir,
                      home=self.root_gui.do_home.get(),
                      base=self.root_gui.do_base.get(),
                      x=x + 10, y=y + 10)
        return

    def select_one_dir(self, path):
        self.set_value_and_refresh(path, "GUI", 'modify')


class PasswordField(StringField):
    def __init__(self, root_gui: 'PwpEditorUI', frm, name: str, row: int, constraint,
                 config: PwpConfig, allow_modification: bool):
        super().__init__(name, row, root_gui, frm, constraint, config, allow_modification)

        self.item.configure(width=self.root_gui.VALUE_WIDTH - 15, show='*')
        self.item.grid(column=1, row=row, sticky="W", columnspan=3)

        self.show_var = GuiButton(root_gui, self.frm,
                                  text="Show" if self.item['show'] == '*' else "Hide",
                                  fr_text="Voir" if self.item['show'] == '*' else "Cacher",
                                  command=lambda: self.show_password(),
                                  column=3, row=row)

    def suicide(self):
        super().suicide()
        self.root_gui.remove_widget(self.show_var)

    # def show(self, row):
    #     super().show(row)
    #     self.item.grid(column=1, row=row, sticky="W", columnspan=3)     # noqa
    #     self.show_var.grid(column=3, row=row, sticky="W")

    # def delete(self):
    #     super().delete()
    #     self.item.destroy()
    #     self.show_var.destroy()

    # def hide(self):
    #     super().hide()
    #     self.item.grid_forget()
    #     self.show_var.grid_forget()

    def show_password(self):
        self.item['show'] = "*" if self.item['show'] == '' else ''
        self.show_var["text"] = " Show " if self.item['show'] == '*' else " Hide "


# ---------------------------------------------  SettingsUi


class PwpSettingsUi(PwpGui):
    instance = None

    def __init__(self, root_gui: "PwpEditorUI", language, x=None, y=None):
        super().__init__("Server settings", language=language)
        if PwpSettingsUi.instance is not None:
            PwpSettingsUi.instance.exit()
            PwpSettingsUi.instance = None
        PwpSettingsUi.instance = self

        self.father = root_gui
        if x is not None and y is not None:
            self.root.geometry(f"+{int(x + 10)}+{y + 10}")

        self.do_album = tkinter.StringVar()
        self.do_thumbnails = tkinter.StringVar()

        self.do_album.set(self.father.album_value.get())
        self.do_thumbnails.set(self.father.thumbnails_value.get())

        row = 0

        self.set_column_sizes([15, 15, 15, 15, 15])
        self.logo = pwpLogo_png.tk_photo()

        self.logo_label = tkinter.Label(self.frm, image=self.logo)
        self.logo_label.grid(column=0, row=row, sticky="W")

        row += 1

        GuiLabel(self, self.frm, column=0, row=row, text=" Action", fr_text="Action", bold=True)

        GuiButton(self, self.frm, column=1, row=row, text="OK", fr_text="OK", command=self.choose)

        GuiButton(self, self.frm, column=2, row=row, text="Undo", fr_text="Annuler", command=self.undo,
                  background=PwpGui.ORANGE)

        GuiButton(self, self.frm, column=3, row=row, text="Exit", fr_text="Abandonner", command=self.exit,
                  background="red")

        # -------------- album
        row += 1
        self.album_radio = GuiRadios(self, self.frm, row=row, column=0,
                                     name="album",
                                     fr_name="album",
                                     variable=self.do_album,
                                     command=self.set_values_from_setup,
                                     dico={"local": "local", "remote": "remote"},
                                     fr_dico={"local": "local", "remote": "distant"},
                                     width=20)
        GuiLabel(self, self.frm, column=6, row=row,
                 text="pictures/video folder after handling",
                 fr_text="dossier des photos/vidéos après traitement",
                 width="", )

        # -------------- thumbnails

        row += 1
        self.thumbnails_radio = GuiRadios(self, self.frm, row=row, column=0,
                                          name="thumbnails",
                                          fr_name="miniatures",
                                          variable=self.do_thumbnails,
                                          command=self.set_values_from_setup,
                                          dico={"local": "local", "remote": "remote", "unused": "unused"},
                                          fr_dico={"local": "local", "remote": "distant", "unused": "inutile"},
                                          width=20)

        GuiLabel(self, self.frm, column=6, row=row,
                 text="thumbnails specific to piwigo server",
                 fr_text="miniatures spécifiques du serveur piwigo",
                 width="", )

    def choose(self):
        album = self.do_album.get()
        thumbnails = self.do_thumbnails.get()

        if self.father:
            self.father.gui_set_album_thumbnails(album, thumbnails)

        LOGGER.msg(f"Chose album='{album}', thumbnails='{thumbnails}'")
        self.exit()

    def undo(self):
        album = self.father.initial_album
        thumbnails = self.father.initial_thumbnails
        self.do_album.set(album)
        self.do_thumbnails.set(thumbnails)
        LOGGER.msg(f"Reset to album='{album}', thumbnails='{thumbnails}'")
        if self.father:
            self.father.gui_set_album_thumbnails(album, thumbnails)
        # self.exit()

    def set_values_from_setup(self):
        pass


# ---------------------------------------------  PwpEditorUI


class PwpEditorUI(PwpGui):

    def __init__(self, father: "PwpConfigurator", config: PwpConfig):
        super().__init__("piwiPre", father.language)

        self.en_url = "https://fabien_battini.gitlab.io/piwipre/html/usage/How-to-configure.html"
        self.fr_url = "https://fabien_battini.gitlab.io/piwipre/html/fr/configurer.html"

        self.configurator: PwpConfigurator = father
        self.config = config
        self.change_parameters_on = False
        # will be set to True when the change parameters submenu is on.

        self.vertical_radio = None

        config.save_base_history()

        self.do_language = tkinter.StringVar()
        self.do_dir_to_configure = tkinter.StringVar()

        self.do_home = tkinter.StringVar()
        self.do_home_configured = tkinter.StringVar()

        self.do_base = tkinter.StringVar()
        self.do_base_configured = tkinter.StringVar()

        # self.do_bat = tkinter.StringVar()

        self.do_verbosity = tkinter.StringVar()

        self.password = None
        self.off_var = None
        self.label_font = tkinter.font.Font(size=9, family="Helvetica", weight="bold")
        row = 0
        PwpSettingsUi.instance = None

        self.initial_home = str(self.configurator.home)
        self.initial_base = str(self.configurator.base)
        self.initial_album = str(self.configurator.album_cvs)
        self.initial_thumbnails = str(self.configurator.thumbnails_cvs)
        # self.setup_different_from_initial = False   # if True, we need to save the current configuration

        self.set_column_sizes([29, 29, 15, 15, 15, 15, 15, ])

        # CAVEAT: logo MUST be stored in an attribute, otherwise it is garbage collected !
        self.logo = pwpLogo_png.tk_photo()

        self.logo_label = tkinter.Label(self.frm, image=self.logo)
        self.logo_label.grid(column=0, row=row, sticky="W")

        title_font = tkinter.font.Font(size=14, family="Helvetica", weight="bold")

        lab = ttk.Label(self.frm, font=title_font,
                        text=f" piwiPre  version {PwpVersion.spec} \n")
        lab.grid(column=3, row=row, columnspan=8, sticky="W")

        # -------------- language
        row += 1
        self.language_radio = GuiRadios(self, self.frm, name="Language", fr_name="Langue",
                                        dico={"en": "en", "fr": "fr"},
                                        fr_dico={"en": "en", "fr": "fr"},
                                        command=self.__gui_set_language,
                                        variable=self.do_language,
                                        column=0, row=row)

        self.help_button = GuiButton(self, self.frm, column=5, row=row, text="Help", fr_text="Aide",
                                     background="blue",
                                     command=lambda: webbrowser.open(self.en_url if self.language == "en"
                                                                     else self.fr_url), )

        GuiLabel(self, self.frm, column=6, row=row,
                 text="Online Help",
                 fr_text="Aide en ligne",
                 width=55)

        # -------------- BASE
        row += 1
        GuiLabel(self, self.frm, column=0, row=row, text="BASE", fr_text="BASE", bold=True)

        self.do_base.set(ACTOR.normalise_path(self.configurator.base, absolute=True))

        self.base_entry = tkinter.Entry(self.frm, width=PwpGui.VALUE_WIDTH,
                                        textvariable=self.do_base, state=tkinter.DISABLED)
        self.base_entry.grid(column=1, row=row, sticky="W", columnspan=3)

        # -------------- Configure

        # row += 1
        # GuiLabel(self, self.frm, text="Change parameters", fr_text="Changer les paramètres",
        #          bold=True, column=0, row=row, width="")

        self.configure_params_button = GuiButton(self, self.frm, row=row, column=5,
                                                 text="Change Params",
                                                 fr_text="Changer Params", command=self.__gui_change_parameters)

        GuiLabel(self, self.frm, column=6, row=row,
                 text="Change the configuration temporarily or definitely",
                 fr_text="Changer la configuration de façon temporaire ou définitive",
                 width=55)

        # -------------- Execute

        row += 1
        GuiLabel(self, self.frm, text="Run piwiPre in BASE", fr_text="Exécuter piwiPre dans BASE",
                 bold=True, column=0, row=row, width="")

        # The default increment is 1, every N m=millSec, specified by start(N)
        self.spinner = ttk.Progressbar(self.frm, orient="horizontal", maximum=40,
                                       mode="indeterminate", length=300)
        self.spinner.grid(column=1, row=row, sticky="W", columnspan=3, )

        self.run_button = GuiButton(self, self.frm, column=4, row=row,
                                    text="Run", fr_text="Exécuter",
                                    command=self.__run)

        GuiButton(self, self.frm, column=5, row=row, text="Quit", fr_text="Quit",
                  command=self.exit, background="red")

        GuiLabel(self, self.frm, column=6, row=row,
                 text="If BASE is not configured, Run is not possible",
                 fr_text="si BASE n'est pas configuré, Exécuter est impossible",
                 width=55)

        # --------------------------------------------------------------------
        # -------------- Separator    : Choose Menu

        row += 1
        self.parameters_menu = GuiFolded(self.frm, width=1440, height=0, row=row,
                                         column_sizes=[29, 45, 15, 15, 15],
                                         columnspan=9)
        self.parameters_dico = {}

        sub_row = 0

        self.sep0 = GuiSeparator(self, self.parameters_menu, row=sub_row,
                                 text="Choose directory to configure",
                                 fr_text="Choisir le dossier à configurer")

        sub_row += 1
        GuiLabel(self, self.parameters_menu, column=0, row=sub_row, text="Cancel",
                 fr_text="Annuler", bold=True, width="")

        self.undo_button = GuiButton(self, self.parameters_menu, row=sub_row, column=3,
                                     text="Cancel params",
                                     fr_text="Annuler params",
                                     command=self.launch_cancel_params,
                                     background=PwpGui.ORANGE)

        sub_row += 1
        GuiLabel(self, self.parameters_menu, column=0, row=sub_row, text="Change BASE",
                 fr_text="Changer BASE", bold=True, width="")

        self.choose_base_button = GuiButton(self, self.parameters_menu, row=sub_row, column=3,
                                            text="Choose BASE",
                                            fr_text="Choisir BASE", command=self.launch_choose_base)

        GuiLabel(self, self.parameters_menu, column=4, row=sub_row,
                 text="Choose an existing BASE in history or create a new BASE to configure",
                 fr_text="Choisir BASE dans historique ou créer une nouvelle BASE à configurer",
                 width="")

        # CAVEAT: The parameters_menu is DYNAMICALLY built.
        #         in __gui_change_parameters

        # --------------------------------------------------------------------------------
        # -------------- Separator    : Configure Menu
        # Configure Menu starts hidden

        self.configure_menu = GuiGroup()

        row += 1
        self.sep1 = GuiSeparator(self, self.frm, row=row,
                                 text="Configure a directory",  # CAVEAT: text will be dynamically changed
                                 fr_text="Configurer un dossier")
        self.configure_menu.add_item(self.sep1)

        # -------------- Dir to configure

        row += 1
        self.directory_label = GuiLabel(self, self.frm, column=0, row=row, bold=True,
                                        text="Directory",
                                        fr_text="dossier")
        self.configure_menu.add_item(self.directory_label)
        self.do_dir_to_configure.set(ACTOR.normalise_path(self.configurator.dir_to_configure, absolute=True))

        self.directory_entry = GuiEntry(self.frm, width=PwpGui.VALUE_WIDTH,
                                        textvariable=self.do_dir_to_configure, column=1, row=row, columnspan=3)
        self.configure_menu.add_item(self.directory_entry)

        self.directory_save_button = GuiButton(self, self.frm, column=4, row=row, text="Write config",
                                               fr_text='Écrit config',
                                               command=self.__save)
        self.configure_menu.add_item(self.directory_save_button)

        # self.exec_no_save_button = GuiButton(self, self.frm, column=5, row=row,
        #                                      text="Exec no save", fr_text="Exec sans sauve",
        #                                      command=self.__run_unsaved_config)
        # self.configure_menu.add_item(self.exec_no_save_button)

        # ---------------------------------------------------------- Build local shortcuts
        row += 1

        self.bat_label = GuiLabel(self, self.frm, column=0, row=row,
                                  text="Build local shortcuts",
                                  fr_text="Créer raccourcis locaux",
                                  bold=True,
                                  width=30)
        self.configure_menu.add_item(self.bat_label)

        self.bat_button = GuiButton(self, self.frm, text="Create", fr_text="Créer",
                                    command=self.__create_bat,
                                    column=4, row=row)
        self.configure_menu.add_item(self.bat_button)

        self.bat_radio_help = GuiLabel(self, self.frm, column=5, row=row, col_span=2,
                                       text="Allows to start piwiPre from the file explorer",
                                       fr_text="Permet de démarrer piwiPre depuis l'explorateur de fichiers",
                                       width=55)
        self.configure_menu.add_item(self.bat_radio_help)

        # ---------------------------------------------------------- Verbosity of ini file
        row += 1

        self.verbosity_radio = GuiRadios(self, self.frm,
                                         name="Verbosity of ini file",
                                         fr_name="Verbosité du fichier .ini",
                                         row=row,
                                         dico={'true': "on", "false": "off"},
                                         fr_dico={'true': "oui", "false": "non"},
                                         command=lambda: True,
                                         # self.set_values_from_setup,  # no need to compute again the setup
                                         variable=self.do_verbosity,
                                         width=20)
        self.configure_menu.add_item(self.verbosity_radio)

        self.verbosity_label = GuiLabel(self, self.frm, column=5, row=row, col_span=2,
                                        text="if true, .ini is really self documented, else minimal doc",
                                        fr_text="si 'oui', le fichier .ini est très documenté, sinon minimal",
                                        width=55)
        self.configure_menu.add_item(self.verbosity_label)

        # -------------- Album settings

        row += 1
        self.album_label = GuiLabel(self, self.frm, text="Album", fr_text="Album",
                                    column=0, row=row, bold=True, width="")
        self.configure_menu.add_item(self.album_label)

        self.album_value = GuiValue(self, self.frm, column=1, row=row, width=10,
                                    dico={"local": "local", "remote": "remote"},
                                    fr_dico={"local": "local", "remote": "distant"})
        self.configure_menu.add_item(self.album_value)

        self.thumbnails_label = GuiLabel(self, self.frm, text="Thumbnails", fr_text="Miniatures",
                                         column=2, row=row, bold=True, width="")
        self.configure_menu.add_item(self.thumbnails_label)

        self.thumbnails_value = GuiValue(self, self.frm, column=3, row=row, width=10,
                                         dico={"local": "local", "remote": "remote", "unused": "unused"},
                                         fr_dico={"local": "local", "remote": "distant", "unused": "inutile"})
        self.configure_menu.add_item(self.thumbnails_value)

        self.settings_ui = None
        self.modify_button = GuiButton(self, self.frm, text="Modify", fr_text="Modifier",
                                       command=self.__run_settings,
                                       column=4, row=row)
        self.configure_menu.add_item(self.modify_button)

        self.modify_label = GuiLabel(self, self.frm, column=5, row=row, col_span=2,
                                     text="Usage and location of album and thumbnail",
                                     fr_text="Utilisation et localisation de album et miniatures",
                                     width=55)
        self.configure_menu.add_item(self.modify_label)

        # -------------- Separator
        # row += 1
        # self.sep3 = GuiSeparator(frm=self.frm, row=row, text="Change settings")

        # -------------- Variable items
        row += 1
        self.max_common_row = row
        self.multi_level = None
        self.enclosing = None

        sizes = [25, 21, 18, 13, 35, 20, 10, 10, ]
        all_sizes = sizes + [200 - sum(sizes)]

        self.enclosing = GuiFrame(self.frm, width=1410, height=220, row=row, column=0,
                                  column_sizes=all_sizes,
                                  columnspan=9)
        self.configure_menu.add_item(self.enclosing)

        # caveat: columns in multilevel are managed in multilevel, NOT here !

        GuiLabel(self, self.enclosing, column=0, row=0, text="item", fr_text="item", bold=True, width="")
        GuiLabel(self, self.enclosing, column=1, row=0, text="value", fr_text="valeur", bold=True, width="")
        GuiLabel(self, self.enclosing, column=4, row=0, text="origin", fr_text="origine", bold=True, width="")
        GuiLabel(self, self.enclosing, column=5, row=0, text="action", fr_text="action", bold=True, width="")
        GuiLabel(self, self.enclosing, column=6, row=0, text="help", fr_text="aide", bold=True, width="")
        # -------------- messages
        row += 1
        self.add_messager(row=row, title="Messages", fr_title="Messages", height=8)

        # ======================================= Self Test

        if father.test_scenario:
            # look for gui_starter:
            for index in range(len(father.test_scenario)):
                k = father.test_scenario[index][0]
                if k == "start GUI test":
                    self.start_spinner()
                    self.root.after(1000, lambda: self.__execute_gui_scenario_n(index+1))
                    break  # HACK! MUST break here, so that index value is NOT modified when lambda is started

        self.__from_python_to_ui()

    def __execute_gui_scenario_n(self, n):

        def __scenario_choose_multilevel(myvalues):
            field = myvalues[0]
            val_field: StringField = self.multi_level.all_lines[field]
            editor: GuiStringEditor = val_field.editor
            editor.choose()

        def __scenario_set_multilevel(myvalues):
            field = myvalues[0]
            value = myvalues[1]
            val_field: BoolField = self.multi_level.all_lines[field]
            val_field.variable.set(value)

        def __scenario_show_hide_field(myvalues):
            field = myvalues[0]
            val_field = self.multi_level.all_lines[field]
            origin: GuiExpandable = val_field.origin
            origin.show_info(event=None, x=10, y=10)
            self.root.after(1 * 500, origin.hide_info)

        def __scenario_settings_set(myvalues):
            album = myvalues[0]
            thumbnails = myvalues[1]
            self.settings_ui.do_album.set(album)
            self.settings_ui.do_thumbnails.set(thumbnails)
            self.settings_ui.choose()

        def __scenario_exit():
            if not self.configurator.pwp_main.working:
                # working is set to False when piwiPre is finished
                self.exit()
            else:
                self.root.after(200, __scenario_exit)

        actions = {
            "gui error dismiss": lambda _v: GuiError.global_dismiss(),
            "gui change parameters": lambda _v: self.__gui_change_parameters(),
            "gui config": lambda vals: self.__launch_configure(vals[0]),
            "gui save": lambda _v: self.__save(),
            "gui execute": lambda vals: vals[0](),   # run an external hook
            "gui modify multilevel string": lambda vals: self.multi_level.all_lines[vals[0]].modify(x=50, y=50),
            "gui modify multilevel bool": lambda vals: self.multi_level.all_lines[vals[0]].modify(),
            "gui choose base": lambda _v: self.launch_choose_base(),
            "gui select base": lambda vals: self.launch_select_base(vals[0]),
            "gui choose multilevel": __scenario_choose_multilevel,
            "gui set multilevel bool": __scenario_set_multilevel,
            "gui modify_settings invoke": lambda _v: self.modify_button.invoke(),
            "gui settings_ui undo": lambda _v: self.settings_ui.undo(),
            "gui settings_ui set": __scenario_settings_set,
            "gui show-hide info": __scenario_show_hide_field,
            "gui dir-chooser enter": lambda vals: GuiDirChooser.running_chooser.check_and_enter(vals[0]),
            "gui dir-chooser select": lambda vals: GuiDirChooser.running_chooser.select(vals[0]),
            "gui dir-chooser create": lambda vals: GuiDirChooser.running_chooser.create(vals[0]),
            "gui run": lambda _v: self.__run(),
            "gui exit": lambda _v: __scenario_exit(),
            "gui pause": lambda _v: True,
        }

        key, *values = self.configurator.test_scenario[n]
        if key != "gui exit":
            self.root.after(1000, lambda: self.__execute_gui_scenario_n(n+1))
            # we MUST do this ahead, because the action may be blocking

        if key in actions:
            LOGGER.trace(f"GUI scenario '{key}' {values}")
            actions[key](values)
        else:
            LOGGER.internal_error(f"wrong GUI test action '{key}'")

    def start_spinner(self):
        if self.configurator.pwp_main is None or self.spinner is None:
            return
        self.spinner.start(10)
        self.root.after(100, self.stop_spinner_if_done)

    def stop_spinner_if_done(self):
        if self.configurator.pwp_main is None or self.spinner is None:
            return
        if self.configurator.pwp_main.working:
            self.root.after(100, self.stop_spinner_if_done)
        else:
            self.spinner.stop()

    def exit(self):
        if self.spinner:
            self.spinner.stop()
            self.spinner.destroy()
        super().exit()

    def launch_cancel_params(self):
        self.__gui_set_base(self.initial_base)
        self.__gui_hide_parameters_menu()

    def launch_choose_base(self):
        def _build_lambda(val):
            return lambda: self.__gui_set_base(val)

        lines = self.config.get_base_history()
        items_and_action = []
        for item in lines:
            items_and_action.append((item, _build_lambda(item)))
        items_and_action.append(("Create a new Base" if PwpGui.language == "en" else "Créer nouvelle base",
                                self.launch_create_base))

        self.vertical_radio = GuiVerticalRadio(self.root, "Choose a new BASE",
                                               "Choisir une nouvelle BASE",
                                               lines=items_and_action)

    def launch_select_base(self, new_base):
        if new_base is True:
            # means create
            self.launch_create_base()
            return
        self.__gui_set_base(new_base)

    def launch_create_base(self):
        GuiDirChooser(self.root, ACTOR.normalise_path(self.initial_base + '/..', absolute=True),
                      "BASE",
                      self.initial_home, self.initial_base,
                      called=self.__gui_set_base)

    def __gui_set_base(self, new_base):
        new_base = ACTOR.normalise_path(new_base, absolute=True)
        ACTOR.mkdirs(new_base)
        os.chdir(new_base)
        self.configurator.base = new_base
        self.do_base.set(new_base)
        self.do_dir_to_configure.set(new_base)
        if self.vertical_radio:
            self.vertical_radio.exit()
            self.vertical_radio = None
        self.__from_ui_to_python_to_ui()

    def __gui_hide_parameters_menu(self):
        self.change_parameters_on = False
        self.parameters_menu.hide()
        self.configure_menu.hide()

    def __get_full_hierarchy(self):
        hierarchy = self.config.get_hierarchy()
        home = self.configurator.home + '\\.piwiPre.ini'
        if home not in hierarchy:
            # CAVEAT: if HOME is not configured, it will not be in hierarchy, and we want it
            hierarchy.insert(1, home)  # Should be just after DEFAULT

        base = self.configurator.base + '\\piwiPre.ini'
        if base not in hierarchy:
            # CAVEAT: if BASE is not configured, it will not be in hierarchy, and we want it
            hierarchy.insert(2, base)

        cmd_line = "[CMD LINE]"
        if cmd_line not in hierarchy:
            # CAVEAT: if CMD-LINE is not configured, it will not be in hierarchy, and we want it
            hierarchy.insert(3, cmd_line)

        return hierarchy

    def __gui_update_change_parameters(self):
        if not self.change_parameters_on:
            return
        self.__gui_change_parameters()

    def __gui_change_parameters(self):
        self.change_parameters_on = True

        hierarchy = self.__get_full_hierarchy()
        # hierarchy it the list of configuration FILES not directories.

        row = 4

        self.parameters_menu.delete_all()
        self.parameters_dico = {}
        #
        self.scale = 2.0
        nb = 0
        for item in hierarchy:
            if item == 'DEFAULT':
                pass
            else:
                if item == self.configurator.home + '\\.piwiPre.ini':
                    txt = 'HOME'
                elif item == self.configurator.base + '\\piwiPre.ini':
                    txt = "BASE"
                elif item == '[CMD LINE]':
                    txt = "[CMD LINE]"
                else:
                    txt = "BASE sub-dir"

                label = GuiLabel(self, self.parameters_menu, column=0, row=row,
                                 text=txt, fr_text=txt,
                                 width="", bold=True)
                self.parameters_menu.add_item(label)

                nb += 1

                if item == '[CMD LINE]':
                    value3 = GuiLabel(self, self.parameters_menu, column=1, row=row,
                                      text="cmd line flags (--XXX)",
                                      fr_text="les drapeaux sur la ligne de commande (--XXX)",
                                      width="", relief=False)
                    self.parameters_menu.add_item(value3)

                    action3 = GuiButton(self, self.parameters_menu, column=3, row=row,
                                        text="Set cmdline",
                                        fr_text="Ligne de Cmd",
                                        command=self.__launch_set_cmdline)
                    self.parameters_menu.add_item(action3)
                else:
                    path = os.path.dirname(item)
                    value = GuiLabel(self, self.parameters_menu, column=1, row=row,
                                     text=path, fr_text=path,
                                     width="", relief=True)
                    self.parameters_menu.add_item(value)

                    if os.path.isfile(item):
                        conf_val_fr = "Configuré"
                        conf_val_gb = "Configured"
                    else:
                        conf_val_fr = "NON Configuré"
                        conf_val_gb = "NOT Configured"

                    conf = GuiLabel(self, self.parameters_menu, column=2, row=row,
                                    text=conf_val_gb, fr_text=conf_val_fr,
                                    width=16, relief=True)
                    self.parameters_menu.add_item(conf)
                    self.parameters_dico[item] = conf

                    # hack as a correction of BUG 3131:
                    # we cannot write directly command=lambda: self.__launch_configure(path)
                    # because the value of path is read from the environment of the calling function
                    # (here __gui_change_parameters)
                    # and therefore path has always the same LAST value,
                    # for all iterations of the loop.
                    #
                    # but build_lambda creates a different lambda for each loop,
                    # with a parameter which is not read from the environment variables

                    def _build_lambda(val):
                        return lambda: self.__launch_configure(val)

                    action = GuiButton(self, self.parameters_menu, column=3, row=row,
                                       text="Config " + txt, fr_text="Config " + txt,
                                       command=_build_lambda(path))
                    self.parameters_menu.add_item(action)
                row += 1

        # -------------------------------
        #  Sub directories of BASE

        label2 = GuiLabel(self, self.parameters_menu, column=0, row=row,
                          fr_text="Sous-dossier de BASE",
                          text="BASE Sub-directory",
                          width="", bold=True)
        self.parameters_menu.add_item(label2)

        conf2 = GuiLabel(self, self.parameters_menu, column=1, row=row,
                         text="value to choose", fr_text="Valeur à choisir",
                         width="")
        self.parameters_menu.add_item(conf2)

        action2 = GuiButton(self, self.parameters_menu, column=3, row=row,
                            text="Chose", fr_text="Choisir",
                            command=lambda: self.__launch_configure_other(action2))
        self.parameters_menu.add_item(action2)
        self.parameters_dico["Choose other button"] = action2

        help2 = GuiLabel(self, self.parameters_menu, column=4, row=row,
                         text="CAVEAT: BASE must be configured before its sub-dirs",
                         fr_text="ATTENTION: il faut configurer BASE avant ses sous-dossiers éventuels",
                         width="")
        self.parameters_menu.add_item(help2)

        # -------------------------------
        # end

        if not os.path.isfile(self.configurator.base + '/piwiPre.ini'):
            action2.disable()
            # cannot configure a subdirectory unless BASE is configured

        self.parameters_menu.show()  # un-hide the change parameters menu

    def __run_settings(self):
        self.settings_ui = PwpSettingsUi(self, language=self.language,
                                         x=self.modify_button.winfo_rootx(),
                                         y=self.modify_button.winfo_rooty())

    def __display_multilevel(self, start_row):
        if self.multi_level is not None:
            self.multi_level.suicide()
            del self.multi_level

        self.multi_level = GuiScrollable(self, self.enclosing, row=start_row + 1, name="multilevel", height=250,
                                         column_sizes=[25, 20, 18, 12, 18, 10, 10, 10])
        row = 0
        level_0_shown = False
        level_1_shown = False
        level_2_shown = False
        level_3_shown = False

        # Stage 0: constraint.how == ConstraintHow.CMDLINE
        # Stage 1: constraint.how != FORCED, CMDLINE location = args or both
        # Stage 2: constraint.how != FORCED, CMDLINE location = config
        # Stage 3: constraint.how == FORCED

        if self.do_dir_to_configure.get() == "[CMD LINE]":
            my_range = range(0, 4)
        else:
            my_range = range(1, 4)

        for stage in my_range:
            row += 1

            for name in self.configurator.current_constraints:
                father: 'PwpConfigurator' = self.configurator
                constraint: PwpConstraint = father.get_constraint(name)

                if constraint.how == ConstraintHow.HIDDEN:
                    continue

                # Stage 0: constraint.how == ConstraintHow.CMDLINE
                if stage == 0:
                    if constraint.how != ConstraintHow.CMDLINE:
                        continue
                if stage == 0 and not level_0_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items only on cmdline, cannot be saved in .ini",
                                               fr_label="Items seulement sur ligne de commande, pas en .ini")
                    level_0_shown = True
                    row += 1

                # Stage 1: constraint.how != FORCED, CMDLINE location = args or both
                if stage == 1:
                    if constraint.how == ConstraintHow.FORCED or constraint.how == ConstraintHow.CMDLINE:
                        continue
                    if constraint.location != "both" and constraint.location != "args":
                        continue
                if stage == 1 and not level_1_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items that can be saved in .ini OR in cmdLine",
                                               fr_label="Items qui peuvent être dans .ini "
                                                        "ou sur la ligne de commande")
                    row += 1
                    level_1_shown = True

                # Stage 2: constraint.how != FORCED, CMDLINE location = config
                if stage == 2:
                    if constraint.how == ConstraintHow.FORCED or constraint.how == ConstraintHow.CMDLINE:
                        continue
                    if constraint.location != "config":
                        continue

                if stage == 2 and not level_2_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items that can be set only in .ini",
                                               fr_label="Items seulement en fichier .ini ")
                    row += 1
                    level_2_shown = True

                # Stage 3: constraint.how == FORCED
                if stage == 3:
                    if constraint.how != ConstraintHow.FORCED:
                        continue

                if stage == 3 and not level_3_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items forced by the server setup",
                                               fr_label="Items forcés par le setup du serveur")
                    row += 1
                    level_3_shown = True

                allow_modification = (self.do_dir_to_configure.get() != "[CMD LINE]") or (stage in [0, 1])
                self.multi_level.add_item(Field.create_field(root=self, frm=self.multi_level.frm,
                                                             name=name, row=row,
                                                             constraint=constraint, config=self.config,
                                                             allow_modification=allow_modification),
                                          name)
                row += 1

    def __create_bat(self):
        self.configurator.build_shortcuts()
        self.__from_ui_to_python_to_ui()

    def gui_set_album_thumbnails(self, album, thumbnails):
        self.album_value.set(album)
        self.thumbnails_value.set(thumbnails)
        self.__from_ui_to_python_to_ui()

    def refresh_main_buttons(self):
        self.parameters_menu.refresh()

        modified = False
        for field in self.multi_level.all_lines.values():
            st = field.change_var.get()
            if st != "undo":
                modified = True
                break
            # NB: here, we are paranoid.
            #     we say modified as soon as status != undo
            #     so that it is clear to the user that "UNDO" or "SAVE"
            #     must be explicitly used to exit from the edition mode

        # run_button
        if ((self.do_dir_to_configure.get() == "[CMD LINE]" or not modified) and
                os.path.isfile(self.configurator.base + "/piwiPre.ini")):
            self.run_button.enable()
            # we allow to execute ONLY in [CMD LINE] else changes must have been saved
        else:
            self.run_button.disable()

        # This was BUG 01312
        # but, if no secrets are used, there is NO reason to have HOME configured.
        #
        # if equal_path(self.do_dir_to_configure.get(), self.configurator.base) and self.configure_menu.on:
        #     self.bat_radio.show()
        #     self.bat_radio_label.show()
        #     self.exec_no_save_button.show()
        # else:
        #     self.bat_radio.hide()
        #     self.bat_radio_label.hide()
        #     self.exec_no_save_button.hide()

        LOGGER.msg(f"HOME               : '{self.configurator.home}' "
                   f"configured : '{os.path.isfile(self.configurator.home + '/.piwiPre.ini')}'")
        LOGGER.msg(f"BASE               : '{self.configurator.base}' "
                   f"configured : '{os.path.isfile(self.configurator.base + '/piwiPre.ini')}'")

        self.do_dir_to_configure.set(ACTOR.normalise_path(self.configurator.dir_to_configure, absolute=True))
        self.__gui_update_change_parameters()

    def show_configure_menu(self):
        self.configure_menu.show()
        # labels
        directory_on = False
        bat_on = False
        verbose_on = False
        server_on = False

        if equal_path(self.do_dir_to_configure.get(), self.configurator.home):
            self.sep1.set(text="Configure a directory : [HOME]",
                          fr_text="Configurer un dossier : [HOME]")
            directory_on = True
            verbose_on = True

        elif equal_path(self.do_dir_to_configure.get(), self.configurator.base):
            self.sep1.set(text="Configure a directory : [BASE]",
                          fr_text="Configurer un dossier : [BASE]")
            directory_on = True
            verbose_on = True
            bat_on = True
            server_on = True

        elif self.do_dir_to_configure.get() == "[CMD LINE]":
            self.sep1.set(text="Configure the command line",
                          fr_text="Configurer la ligne de commande")
        else:
            self.sep1.set(text="Configure a sub-directory of BASE",
                          fr_text="Configurer un sous-dossier de BASE")
            directory_on = True
            verbose_on = True
            server_on = True

        if self.change_parameters_on and directory_on:
            self.directory_save_button.show()
            self.directory_label.show()
            self.directory_entry.show()
        else:
            self.directory_save_button.hide()
            self.directory_label.hide()
            self.directory_entry.hide()

        if self.change_parameters_on and bat_on:
            self.bat_label.show()
            self.bat_button.show()
            self.bat_radio_help.show()
        else:
            self.bat_label.hide()
            self.bat_button.hide()
            self.bat_radio_help.hide()

        if self.change_parameters_on and verbose_on:
            self.verbosity_label.show()
            self.verbosity_radio.show()
        else:
            self.verbosity_label.hide()
            self.verbosity_radio.hide()

        if self.change_parameters_on and server_on:
            self.album_label.show()
            self.album_value.show()
            self.thumbnails_label.show()
            self.thumbnails_value.show()
            self.modify_button.show()
        else:
            self.album_label.hide()
            self.album_value.hide()
            self.thumbnails_label.hide()
            self.thumbnails_value.hide()
            self.modify_button.hide()

    def __gui_set_dir(self, path):
        if path == "[CMD LINE]":
            self.do_dir_to_configure.set("[CMD LINE]")
        else:
            self.do_dir_to_configure.set(ACTOR.normalise_path(path, absolute=True))
        self.__from_ui_to_python_to_ui()

    def __launch_set_cmdline(self):
        """Change the cmdline parameters"""
        self.__gui_set_dir("[CMD LINE]")
        self.show_configure_menu()

    def __launch_configure_other(self, button):
        """
        Here, we change the directory being configured, but we do not change HOME or BASE
        First, select the directory to be configured, starting from BASE
        then, configure it
        """
        self.__gui_set_dir(self.do_base.get())
        x = button.winfo_rootx()
        y = button.winfo_rooty()
        GuiDirChooser(self, ACTOR.normalise_path(self.do_dir_to_configure.get()),
                      "Other directory",
                      home=self.do_home.get(),
                      base=self.do_base.get(),
                      called=self.__continue_configure_other,
                      x=x + 10, y=y + 10)

    def __continue_configure_other(self, path):
        # Restrict path to be relative to BASE
        abs_path = ACTOR.normalise_path(path, self.configurator.base, error_if_not_included=True,
                                        caller="Configure BASE sub dir")
        if abs_path is None:
            # ERROR has already been generated
            return
        self.__gui_set_dir(abs_path)
        self.show_configure_menu()

    def __launch_configure(self, path):
        self.__gui_set_dir(path)
        self.show_configure_menu()

    def __gui_set_language(self):
        self.set_language(self.do_language.get())

    def set_language(self, language):
        self.configurator.language = language
        super().set_language(language)

    def __from_ui_to_python_to_ui(self):
        self.__from_ui_to_python()
        self.__from_python_to_ui()

    def __from_ui_to_python(self):
        new_language = self.do_language.get() or 'en'
        new_album: CVS = CVS.from_str(self.album_value.get())  # LOCAL, REMOTE
        new_thumbnails: CVS = CVS.from_str(self.thumbnails_value.get())  # LOCAL, REMOTE, UNUSED
        new_home = self.do_home.get()
        new_base = self.do_base.get()
        new_dir_to_configure = self.do_dir_to_configure.get()

        if self.configurator.language != new_language:
            self.configurator.language = new_language
            self.set_language(new_language)

        config_has_changed = (not equal_path(self.configurator.dir_to_configure, new_dir_to_configure) or
                              not equal_path(self.configurator.home, new_home) or
                              not equal_path(self.configurator.base, new_base))
        # if config_has_changed, we need to read again the config

        self.configurator.setup_has_changed = (
                not equal_path(self.configurator.dir_to_configure, new_dir_to_configure) or
                self.configurator.album_cvs != new_album or
                self.configurator.thumbnails_cvs != new_thumbnails or
                not equal_path(self.configurator.home, new_home) or
                not equal_path(self.configurator.base, new_base))
        # if setup_has_changed, we will compute again the constraints
        # in from python_to_ui

        self.configurator.dir_to_configure = new_dir_to_configure
        self.configurator.album_cvs = new_album
        self.configurator.thumbnails_cvs = new_thumbnails
        self.configurator.home = new_home
        self.configurator.base = new_base

        # We want to force to configure directories in a logical order: HOME - BASE - CMD-LINE - SUB-DIRS
        # BUT we do not do it at this level,
        # because this cannot be understood by the user
        # instead, we do it at the UI level.

        self.configurator.verbose = self.do_verbosity.get() == "true"

        # copy the values from the multi_level in the GUI to python
        for name, field in self.multi_level.all_lines.items():
            self.configurator.set_value(name, field.get_value(), field.get_origin())

        if config_has_changed:
            self.configurator.set_dir_and_config(self.configurator.dir_to_configure, None)
        self.configurator.compute_constraints()

    def __from_python_to_ui(self):
        self.set_language(self.configurator.language)

        self.do_language.set(self.configurator.language)
        self.album_value.set(str(self.configurator.album_cvs))
        self.thumbnails_value.set(str(self.configurator.thumbnails_cvs))
        # self.do_bat.set("true" if self.configurator.bat else 'false')
        self.do_verbosity.set("true" if self.configurator.verbose else 'false')

        self.do_home.set(self.configurator.home)

        self.do_base.set(self.configurator.base)

        self.do_dir_to_configure.set(ACTOR.normalise_path(self.configurator.dir_to_configure, absolute=True))
        self.config = self.configurator.config

        self.__display_multilevel(self.max_common_row)
        self.refresh_main_buttons()

    def undo(self):
        #  Go back to all previous values for the dir to configure
        self.album_value.set(self.initial_album)
        self.thumbnails_value.set(self.initial_thumbnails)
        # self.do_home.set(self.initial_home)
        # self.do_cwd.set(self.initial_cwd)

        for name, field in self.multi_level.all_lines.items():
            field.undo()
        self.__from_ui_to_python_to_ui()

    def __run(self):
        # DONE: Verify that we take into account unsaved arguments, see program_909
        self.__from_ui_to_python()
        self.configurator.run(with_gui_config=True)

    def __save(self):
        self.__from_ui_to_python()
        self.configurator.save()
        self.__from_python_to_ui()

# ------------------------------------------------------------------------------------------
# class PwpConfigurator
# ------------------------------------------------------------------------------------------


class PwpConfigurator:
    def __init__(self,
                 config: PwpConfig or None = None,
                 pwp_main=None,
                 logger=None,
                 action=None,
                 test_scenario=None):

        self.ui: PwpEditorUI or None = None
        self.pwp_main = pwp_main
        self.logger = logger
        self.action = action
        self.config = config
        self.language = config['language']

        self.dir_to_configure = None

        self.home = ACTOR.normalise_path(config['home'] or os.path.expanduser("~"))
        self.base = ACTOR.linux_path(os.getcwd())  # initially, piwiPre has done a chdir, so BASE is always os.getcwd()  # noqa

        self.build_for_home = None  # means dir_to_configure == HOME

        self.album_cvs: CVS = CVS.LOCAL        # will be set by set_dir_and_config
        self.thumbnails_cvs: CVS = CVS.UNUSED  # will be set by set_dir_and_config

        self.do_gui = config["gui"]
        self.do_run = True

        self.verbose = False
        self.setup_has_changed = False
        target = '.'

        # We do not want to do this here, it is not understandable by users
        # if os.path.isfile(self.home + '/.piwiPre.ini'):
        #     if not os.path.isfile(self.base + '/piwiPre.ini'):
        #         target = self.base
        # else:
        #     target = self.home

        # Previously, this was in set_dir_and_config
        self.album_cvs = CVS.REMOTE if self.config['enable-remote-album'] else CVS.LOCAL
        self.thumbnails_cvs = (CVS.UNUSED if self.config['enable-thumbnails'] is False
                               else CVS.REMOTE if self.config['enable-remote-thumbnails']
                               else CVS.LOCAL)

        self.test_scenario = test_scenario
        if test_scenario:
            for k, *v in test_scenario:
                if k == "album-setup":
                    self.album_cvs = CVS.from_str(v[0])
                if k == "thumbnails-setup":
                    self.thumbnails_cvs = CVS.from_str(v[0])

        self.current_constraints: dict[str, PwpConstraint] = {}
        self.parser = PwpParser(program="piwiPre", parse_args=False, with_config=False,
                                arguments=pwp_main.parser.cmd_line_args)
        self.set_dir_and_config(target, config)

    def start_spinner(self):
        if self.ui:
            self.ui.start_spinner()
        # will stop by itself when processing is done

    def file_to_configure(self):
        if self.dir_to_configure == self.home:
            return self.dir_to_configure + '/.piwiPre.ini'
        return self.dir_to_configure + '/piwiPre.ini'

    def run_or_display(self):
        if self.test_scenario:
            self.start_spinner()
            self.setup_has_changed = True
            self.compute_constraints()

            test_actors = {
                "choose dir": lambda values: self.set_dir_and_config(values[0], None),
                "set album": lambda values: self.set_value("album", values[0], "GUI"),
                "set thumbnails": lambda values: self.set_value('thumbnails', values[0], "GUI"),
                "set enable-remote-album": lambda values: self.set_value('enable-remote-album', values[0],
                                                                         "GUI"),
                "set ssh-user": lambda values: self.set_value('ssh-user', values[0], "GUI"),
                "set ssh-host": lambda values: self.set_value('ssh-host', values[0], "GUI"),
                "set piwigo-user": lambda values: self.set_value('piwigo-user', values[0], "GUI"),
                "set copyright": lambda values: self.set_value('copyright', values[0], "GUI"),
                "shortcuts": lambda _: self.build_shortcuts(),
                "save": lambda _: self.save(),
                "run": lambda _: self.run(),
                "run-with-gui-config": lambda _: self.run(with_gui_config=True),
                "exit": lambda _: self.exit(),
                # next ones are already managed
                "album-setup": lambda _: True,      # managed in __init__
                "thumbnails-setup": lambda _: True,      # managed in __init__
            }

            for (k, *v) in self.test_scenario:
                if k in test_actors:
                    test_actors[k](v)
                elif k == "start GUI test":
                    break
                else:
                    LOGGER.internal_error(f"test scenario : item '{k}' unknown")

            if self.ui:
                self.ui.spinner.stop()

        if self.do_gui:
            self.setup_has_changed = True
            self.compute_constraints()
            self.ui = PwpEditorUI(self, self.config)
            if self.logger:
                self.logger.add_gui(self.ui)
            if self.ui.root is None:  # pragma: no cover : defensive code
                self.ui = None
                LOGGER.warning("unable to start TK")
                return
            self.ui.mainloop()

            if self.logger:
                self.logger.add_gui(None)

        elif self.do_run:
            self.run()

    def exit(self):
        if self.ui:
            self.ui.exit()
        if self.logger:
            self.logger.add_gui(None)
        self.do_run = False

    def set_dir_and_config(self, path, config):
        if path == "[CMD LINE]":
            self.build_for_home = False
            self.dir_to_configure = path
            LOGGER.msg("target           : 'cmd line items'")
            path = self.base
            # This is aligned with the doc in PwpParser:
            # 4. in BASE.
            # 5. on command-line
        else:
            path = ACTOR.normalise_path(path)
            self.build_for_home = equal_path(path, self.home)
            self.dir_to_configure = path

            LOGGER.msg(f"target directory   : '{ACTOR.normalise_path(self.dir_to_configure, absolute=True)}'")
            if self.build_for_home:
                LOGGER.msg("target file          : HOME/.piwiPre.ini ")
            else:
                LOGGER.msg(f"target file        : '{self.file_to_configure()}' ")

        # if config is set, then we do not need to parse the configuration file again
        self.config = config or self.parser.parse_for_dir(path, self.home, self.base, self.language,
                                                          self.parser.cmd_line_args)

    def get_constraint(self, name) -> PwpConstraint:
        """
        get_values(self, name):
        :param name:
        :return: PwpConstraint
        """
        return self.current_constraints[name]

    def set_value(self, name: str, value: str, origin: str):
        self.current_constraints[name].value = value
        self.current_constraints[name].origin = origin

    def compute_constraints(self):
        if not self.setup_has_changed:
            return

        LOGGER.msg("Applying constraints from album/thumbnail setup ")
        LOGGER.msg(f"HOME       : {str(self.home)}")
        LOGGER.msg(f"BASE       : {str(self.base)}")
        LOGGER.msg(f"ALBUM      : {str(self.album_cvs)}")
        LOGGER.msg(f"THUMBNAILS : {str(self.thumbnails_cvs)}")
        setup = ServerSetup(album=self.album_cvs, thumbnails=self.thumbnails_cvs)

        self.current_constraints = self.parser.get_constraints_for_setup(setup=setup,
                                                                         config=self.config)
        self.setup_has_changed = False

    @staticmethod
    def copy(src, dst):
        """
        copy src to dst, unless dryrun is True
        :param src: file to copy
        :param dst: destination filename
        :return: None
        """
        base = os.path.dirname(dst)
        if not os.path.isdir(base):
            os.makedirs(base, exist_ok=True)

        if not os.path.isfile(src):
            LOGGER.warning(f"FAILED copy '{src}' ->  '{dst}' : non existing source")

        shutil.copy2(src, dst)  # preserve metadata

        if os.path.isfile(dst):
            LOGGER.msg(f"copy '{src}' ->  '{dst}'")
        else:
            LOGGER.warning(f"FAILED copy '{src}' ->  '{dst}' : file not copied")

    @staticmethod
    def backup(filename):
        if not os.path.isfile(filename):
            return

        bak = filename + time.strftime("-%Y-%m-%d-%Hh%M-%S.bak")
        PwpConfigurator.copy(filename, bak)

    def compute_config_delta(self, for_save):
        """
        computes the new configuration out of the GUI,
        CAVEAT: this is NOT the full configuration merged with previous in hierarchy,
                this is only the specific part that can be written
        either to write in ini file or run the program without saving
        :param for_save:
            if True, the new configuration will REPLACE the current one, and will be SAVED in the same file
            if False, the new configuration will be used to run without saving,
                      so we keep origin = GUI,
                      and we need the cmdline arguments
        :return: the new configuration
        """
        dico = {}
        # let's compute the value of config parameters we want to write in the config file
        #
        # CAVEAT: We want to keep the values from the current config file that have NOT been modified
        #         by the GUI. For instance the 'names' item.
        #
        # CAVEAT: when the parameter is inherited from a previous config
        #   - in the GUI, we display the previous value (and the previous origin)
        #   - in the saved config file, we want to not set the value,
        #     so that, in the case we change the previous config file, that new value will be inherited.
        #     The alternative would be to write again the previous value,
        #     in this case, any change of the previous file is NOT inherited,
        #     which is something that we do not want.
        #
        # CAVEAT: when there is NO configuration file in the directory where we will write the config
        #    (e.g. we are writing BASE config, but BASE was empty)
        #    then self.config is inherited from the hierarchy, for instance from HOME

        for name in self.config:
            if name in self.current_constraints:
                cc: PwpConstraint = self.current_constraints[name]
                uv = cc.value

                if for_save and cc.how == ConstraintHow.CMDLINE:
                    # we do not put CMDLINE items in the config files.
                    continue

                if cc.origin == "GUI":  # NB: "GUI" is always higher case.
                    if for_save:
                        cc.origin = self.file_to_configure()
                    else:
                        pass  # keep origin == GUI
                    # we will write  it in the config file
                elif uv is None or not equal_path(cc.origin, self.file_to_configure()):
                    # it means that the value is inherited from a previous config
                    # so, we will NOT write the value in the config file
                    continue

                val = (uv if uv in ["", 'true', 'false', 'TRIAGE', 'BACKUP', 'ALBUM', 'THUMBNAILS', 'fr', 'en']
                       else int(uv) if cc.pwp_type == PwpArgType.INT
                       else ACTOR.normalise_path(uv) if cc.pwp_type == PwpArgType.DIR
                       else f'{uv}')
                dico[name] = val
            else:
                # this is a config item not managed by the GUI
                if equal_path(self.config.origin[name], self.file_to_configure()):
                    # it was set on THIS config file, we keep its value,
                    dico[name] = self.config[name]
                else:
                    pass
                    # otherwise we keep it unset in order to enable inheritance
        if for_save:
            new_config = PwpConfig(filename=self.file_to_configure(), dico=dico, previous=self.config.previous)
        else:
            new_config = PwpConfig(filename="GUI", dico=dico, previous=self.file_to_configure())
        return new_config

    def run(self, with_gui_config=False):
        # run piwiPre in BASE
        if self.ui:
            self.ui.directory_save_button.disable()
            self.ui.start_spinner()

        if with_gui_config:
            # let's take into account items in the GUI, not saved
            new_config = self.compute_config_delta(for_save=False)
            self.pwp_main.parser_config = new_config.merge_ini(self.pwp_main.parser_config)
            # TODO: Investigate the previous line. Here, we clobber parser_config with no mean to go back
        self.action()       # spawn piwiPre in a separate thread
        # if self.ui:
        #     self.ui.spinner.stop()
        #     print("SPINNER STOP")
        return

    def build_shortcuts(self):
        if not equal_path(self.dir_to_configure, self.base):
            LOGGER.msg("Configured directory is not BASE: Not creating shortcuts")
            return

        piwipre_path = (os.environ['PROGRAMFILES(X86)'] + '\\piwiPre\\'  # noqa
                        if platform.system() == "Windows" else "")

        base = os.path.dirname(self.file_to_configure())
        if not os.path.isdir(base):
            os.makedirs(base, exist_ok=True)

        def build_file(file_name, program, gui_flag):
            if platform.system() == "Windows" and gui_flag:
                pylnk3.for_file(f'{piwipre_path}{program}.exe',
                                file_name, arguments='--gui true', window_mode="Minimized")
                LOGGER.msg(f"Generated  '{file_name}' ")
                return

            with open(file_name, "w", encoding="utf8") as f:
                if platform.system() != "Windows":
                    f.write("#!/bin/sh \n")

                cur_dir = self.base
                home = os.path.relpath(self.home, cur_dir)
                f.write("# file generated by pwpConfigurator\n")
                f.write("#\n")
                f.write(f"# file       =  '{self.file_to_configure()}'\n")
                f.write("#\n")
                f.write(f"# album      =  '{self.album_cvs}'\n")
                f.write(f"# thumbnails =  '{self.thumbnails_cvs}'\n")
                f.write("#\n")
                flag = "true" if gui_flag else "false"
                if platform.system() == "Windows":
                    f.write(f'"{piwipre_path}{program}.exe" --gui {flag} --base "{cur_dir}" --home "{home}" %*\n')
                else:
                    f.write(f'{program} --gui {flag} --base "{cur_dir}" --home "{home}"  &\n')
                f.write("\n")
                LOGGER.msg(f"Generated  '{file_name}' ")

        filename = base + ("\\piwiPreCmd.bat" if platform.system() == "Windows" else '/piwiPreCmd.sh')
        build_file(filename, "piwiPre", False)

        filename = base + ("\\piwiPreGui.lnk" if platform.system() == "Windows" else '/piwiPreGui.sh')
        build_file(filename, "piwiPre", True)

    def save(self):
        # save config file being edited
        config_delta = self.compute_config_delta(for_save=True)

        self.backup(self.file_to_configure())
        configured_dir = os.path.dirname(self.file_to_configure())

        if not os.path.isdir(configured_dir):
            os.makedirs(configured_dir, exist_ok=True)

        if configured_dir == self.base:
            triage = configured_dir + '/' + self.config['triage']
            if not os.path.isdir(triage):
                os.makedirs(triage, exist_ok=True)

        prologue = f"""
# file generated by piwiPre Configurator
#
# file       :  '{self.file_to_configure()}'
#
# album      :  '{self.album_cvs}'
# thumbnails :  '{self.thumbnails_cvs}'
# language   :  '{self.language}'
#
"""

        self.parser.write_ini_file(self.file_to_configure(), lang=self.language, config=config_delta,
                                   verbose=self.verbose, prologue=prologue)

        LOGGER.msg(f"Generated  '{self.file_to_configure()}' ")

        # OPTIMISATION:
        # if config.previous is None, it means that self.config is the default configuration
        # (which is possible, if there is no ini file in HOME, and we are modifying HOME,
        # or in HOME and BASE, and we are modifying BASE)
        # so, in this case, we can merge with self.config, instead of creating again the default config
        self.config = config_delta.merge_ini(self.config.previous or self.config)

        # introduce again home and base, but with data coming from the GUI, NOT from the cmdline
        # these were not in config_delta, because are not written in files.
        self.config['home'] = self.home
        self.config['base'] = self.base

        self.pwp_main.parser_config = self.config

        # save_base_history() saved the current base, not the current dir, so this is OK
        # at worst, we save a BASE that will never be used
        self.config.save_base_history()

    def msg(self, line):
        if self.ui:
            self.ui.gui_msg(line)
        print(f"msg     {line}")


class ThreadConfigurator:

    def __init__(self,
                 config: PwpConfig,
                 pwp_main,
                 logger,
                 worker,
                 test_scenario=None):
        self.worker = worker
        self.son = None
        self.configurator = PwpConfigurator(config=config, pwp_main=pwp_main,
                                            logger=logger, action=self.spawn_worker,
                                            test_scenario=test_scenario)
        pwp_main.configurator = self.configurator
        self.configurator.run_or_display()

    def spawn_worker(self):
        # we have to create a thread each time we want to start
        self.son = threading.Thread(target=self.run_worker, args=[], daemon=True)
        self.son.start()

    def run_worker(self):
        self.worker()
