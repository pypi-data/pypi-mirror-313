# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

# CAVEAT: executes ONLY on windows !


import platform
import argparse
import threading

import termcolor
import requests
import shutil
import re
import sys
import os
import datetime
import webbrowser
import time
import locale
import zipfile
import json
import subprocess

import tkinter
from tkinter import ttk
import tkinter.font

# be sure that the piwiPre version imported is the latest one...
sys.path = [os.path.dirname(os.path.dirname(os.path.realpath(__file__)))] + sys.path
from piwiPre.pwpVersion import PwpVersion
from piwiPre.pwpLogoSmall import pwpLogo_png
from piwiPre.pwpGui import PwpGui, GuiButton, GuiSeparator, GuiLabel, GuiRadios

if platform.system() == "Windows":
    import winreg
    from ctypes import windll
    from piwiPre.pwpElevate import elevate
    import pylnk3


# DONE: ffmpeg version should be checked only once per install directory, and result of check is cached
# DONE: versions should be checked asynchronously so that the UI is displayed immediately


class PwpInstallerUi(PwpGui):
    def __init__(self, args, installer):
        super().__init__("piwiPre installer", 'fr' if locale.getlocale()[0] == 'fr_FR' else 'en')
        self.installer = installer
        self.args = args
        self.default_base = installer.user_base
        self.set_column_sizes([30, 15, 15, 15, 15, 10])
        self.do_piwipre = tkinter.IntVar()
        self.do_mariadb = tkinter.IntVar()
        self.do_ffmpeg = tkinter.IntVar()
        self.do_mode = tkinter.StringVar()
        self.do_progress = tkinter.IntVar()
        self.en_url = "https://fabien_battini.gitlab.io/piwipre/html/download.html"
        self.fr_url = "https://fabien_battini.gitlab.io/piwipre/html/fr/t%C3%A9l%C3%A9chargement.html"
        # self.piwipre_version = tkinter.StringVar()

        row = 0
        # CAVEAT: logo MUST be stored in an attribute, otherwise it is garbage collected !
        self.logo = pwpLogo_png.tk_photo()
        tkinter.Label(self.frm, image=self.logo).grid(column=0, row=row, sticky="W")

        title_font = tkinter.font.Font(size=15, family="Helvetica", weight="bold")
        lab = ttk.Label(self.frm, font=title_font,
                        text=f"piwiPre installer for Windows version {PwpVersion.spec}\n")
        lab.grid(column=0, row=row, columnspan=5)

        row += 1
        GuiLabel(self, self.frm, text="Elevation enabled",
                 fr_text="Mode administrateur autorisé",
                 column=0, row=row, bold=True, width="")
        GuiLabel(self, self.frm, text=str(self.installer.args.elevation),
                 fr_text="oui" if self.installer.args.elevation == 'true' else "non",
                 column=1, row=row, width="")

        GuiButton(self, self.frm, text="Help", fr_text="Aide",
                  command=lambda: webbrowser.open(self.en_url if self.language == 'en' else self.fr_url),
                  background="blue", column=4, row=row, )

        GuiButton(self, self.frm, text="Quit", fr_text="Abandonner", command=self.exit,
                  background="red", column=3, row=row)

        row += 1

        GuiLabel(self, self.frm, text="Latest piwiPre version",
                 fr_text="Dernière version de piwiPre",
                 column=0, row=row, bold=True, width="")
        self.piwipre_target_label = GuiLabel(self, self.frm, text=installer.piwipre_target_version,
                                             fr_text=installer.piwipre_target_version,
                                             column=1, row=row, width="", col_span=4)

        row += 1
        GuiLabel(self, self.frm, text="Installed piwiPre.exe",
                 fr_text="piwiPre.exe installée",
                 column=0, row=row, bold=True, width="")
        self.piwipre_version_label = GuiLabel(self, self.frm,
                                              text=installer.piwipre_version,
                                              fr_text=installer.piwipre_version,
                                              column=1, row=row, width="", col_span=4)

        row += 1
        GuiLabel(self, self.frm, text="installed ffmpeg",
                 fr_text="ffmpeg installé",
                 column=0, row=row, bold=True, width="")
        self.ffmpeg_version_label = ttk.Label(self.frm, text=installer.ffmpeg_version, padding=4, )
        self.ffmpeg_version_label.grid(column=1, row=row, columnspan=4, sticky="W")

        row += 1
        self.separator = GuiSeparator(self, self.frm, text="Actions", fr_text="Actions", row=row, width=1000)

        row += 1
        ttk.Label(self.frm, text="piwiPre exe", anchor="w", padding=4, font=PwpGui.label_font,
                  ).grid(column=0, row=row, sticky="W")
        self.pwp_button = ttk.Checkbutton(self.frm, text="install", width=10,
                                          variable=self.do_piwipre)
        self.pwp_button.grid(column=1, row=row, sticky="W")

        self.pwp_path = ttk.Label(self.frm, text="",
                                  padding=4, width=90,  # background="light grey",
                                  anchor="w")
        self.pwp_path.grid(column=2, row=row, columnspan=3, sticky="W")

        row += 1
        ttk.Label(self.frm, text="ffmpeg exe", anchor="w", padding=4, font=PwpGui.label_font,
                  ).grid(column=0, row=row, sticky="W")
        self.ffmpeg_button = ttk.Checkbutton(self.frm, text="install", width=10,
                                             variable=self.do_ffmpeg)
        self.ffmpeg_button.grid(column=1, row=row, sticky="W")

        self.ffmpeg_path = ttk.Label(self.frm, text="",
                                     padding=4, width=90,  # background="light grey",
                                     anchor="w")
        self.ffmpeg_path.grid(column=2, row=row, sticky="W", columnspan=3, )

        row += 1
        ttk.Label(self.frm, text="MariaDB CC", anchor="w", padding=4, font=PwpGui.label_font,
                  ).grid(column=0, row=row, sticky="W")
        self.maria_button = ttk.Checkbutton(self.frm, text="install", width=10,
                                            variable=self.do_mariadb)
        self.maria_button.grid(column=1, row=row, sticky="W")

        # ------------------- separator
        row += 1
        tkinter.Frame(self.frm, width=850, height=10, ).grid(column=0, row=row, columnspan=9)

        row += 1

        GuiRadios(self, self.frm,
                  name="Installation type",
                  fr_name="Type d'installation",
                  dico={"test": "for test", "install": "for usage"},
                  fr_dico={"test": "pour test", "install": "pour utilisation"},
                  command=self.reset_and_refresh_default_values,
                  variable=self.do_mode,
                  width=25,
                  column=0, row=row, )

        self.install_button = GuiButton(self, self.frm, text="Install", fr_text="Installer", command=self.run,
                                        background="green", column=4, row=row)
        self.install_button.disable()

        row += 1
        GuiLabel(self, self.frm, text="Configure piwiPre after install",
                 fr_text="Configurer piwiPre après installation",
                 column=0, row=row, bold=True, width="")

        self.configure_button = GuiButton(self, self.frm, text="Configure", fr_text="Configurer",
                                          command=self.configure,
                                          background="green", column=4, row=row)

        # ------------------- separator
        row += 1
        tkinter.Frame(self.frm, width=850, height=10, ).grid(column=0, row=row, columnspan=9)

        row += 1
        self.action = ttk.Label(self.frm, text="Downloader: idle", width=50, anchor="w", padding=2, )
        self.action.grid(column=0, row=row, columnspan=2, sticky="W")

        row += 1
        self.action2 = ttk.Label(self.frm, text="------ KB/ ------ KB", width=50, anchor="w", padding=2, )
        self.action2.grid(column=0, row=row, columnspan=2, sticky="W")

        self.progress = ttk.Progressbar(self.frm, orient="horizontal", variable=self.do_progress,
                                        mode="determinate", length=700, maximum=100)
        self.progress.grid(column=1, row=row, sticky="W", columnspan=8, )

        # ------------------- separator
        row += 1
        tkinter.Frame(self.frm, width=850, height=20, ).grid(column=0, row=row, columnspan=9)

        row += 1
        self.add_messager(title="Feedback from the installer",
                          fr_title="Messages de l'installateur",
                          row=row, height=20, width=1000)

        self.from_python_to_ui()
        if self.installer.async_piwipre is not None:
            self.installer.async_piwipre.run(self)
        if self.installer.async_ffmpeg is not None:
            self.installer.async_ffmpeg.run(self)
        if self.installer.async_packages is not None:
            self.installer.async_packages.run(self)

        if installer.args.mode == "test":
            self.root.after(2 * 1000, self.test_scenario)

    def activate_buttons(self):
        self.install_button.enable()

    def test_scenario(self):
        self.do_piwipre.set(1)
        self.do_mariadb.set(0)
        self.do_ffmpeg.set(0)
        self.do_mode.set("test")
        self.installer.run_min_test(system_dir=False)
        self.refresh_default_values()
        self.installer.run()
        time.sleep(4.0)
        self.exit()

    def reset_and_refresh_default_values(self):
        # called when we change the installation type
        self.installer.piwipre_version = None
        self.installer.ffmpeg_version = None
        self.refresh_default_values()

    def refresh_default_values(self):
        self.from_ui_to_python()
        self.installer.compute_default_values()
        self.from_python_to_ui()

    def from_python_to_ui(self):

        self.do_piwipre.set(1 if self.installer.args.piwipre else 0)
        self.do_mariadb.set(1 if self.installer.args.mariadb else 0)
        self.do_ffmpeg.set(1 if self.installer.args.ffmpeg else 0)
        self.do_mode.set(self.installer.args.mode)

        self.pwp_button['text'] = "re install" if self.installer.piwipre_exists else "install"

        self.piwipre_version_label['text'] = self.installer.piwipre_version or '----'
        self.pwp_path['text'] = self.installer.piwipre_path
        if os.path.isfile(self.installer.piwipre_path + '/piwiPre.exe'):
            self.configure_button.enable()
        else:
            self.configure_button.disable()

        if self.installer.ffmpeg_exists:
            self.ffmpeg_button['text'] = "re install"
        else:
            self.ffmpeg_button['text'] = "install"
        self.ffmpeg_version_label['text'] = self.installer.ffmpeg_version or '----'
        self.ffmpeg_path['text'] = self.installer.ffmpeg_path
        self.do_progress.set(0)
        self.set_action("Downloader idle")

        # New
        if self.installer.piwipre_version is None:
            return
        self.installer.action("", "")

        m = re.match(r"([\d.]*)", self.installer.piwipre_version)
        self.installer.piwipre_exists = m.group(1) >= self.installer.piwipre_target_version
        self.pwp_button['text'] = "re install" if self.installer.piwipre_exists else "install"

    def from_ui_to_python(self):
        self.args.piwipre = self.do_piwipre.get() == 1
        self.args.ffmpeg = self.do_ffmpeg.get() == 1
        self.args.mariadb = self.do_mariadb.get() == 1
        self.args.mode = self.do_mode.get()
        pass

    def run(self):
        self.from_ui_to_python()
        self.installer.run()

    def set_action(self, line1, line2="------ KB/ ------ KB"):
        self.action["text"] = line1
        self.action2["text"] = line2

    def set_progress(self, val):
        self.do_progress.set(int(val))
        self.root.update()
        self.root.update_idletasks()

    def configure(self):
        self.installer.launch_piwi_pre()


# =====================================================================
# Asynchronous calls
# =====================================================================


class AsyncObject:
    nb = 0
    method = None

    def __init__(self):
        AsyncObject.nb += 1

    @staticmethod
    def ended():
        AsyncObject.nb -= 1
        if AsyncObject.nb == 0:
            if AsyncObject.method is not None:
                AsyncObject.method()

    @staticmethod
    def add_method(method):
        AsyncObject.method = method


class AsyncRequest(AsyncObject):
    def __init__(self, asynchronous: bool, url: str, method, is_json: bool):
        super().__init__()
        self.asynchronous = asynchronous
        self.url = url
        self.ui = None
        self.root = None
        self.method = method
        self.result = None
        self.thread = None
        self.is_json = is_json
        if not asynchronous:
            self.worker(None)

    def run(self, ui: "PwpInstallerUi" or None):
        # will be called when the UI is available
        self.ui = ui
        if ui is not None:
            self.root = ui.root

        self.thread = threading.Thread(target=self.worker, args=[ui], daemon=True)
        self.thread.start()
        self.check()

    def worker(self, _ui):
        response = requests.get(self.url)
        if response.status_code == 200:
            print(f"get answer from {self.url}")
            if self.is_json:
                self.result = json.loads(response.content)
            else:
                strings = response.content.decode('utf-8')
                self.result = strings.split('\n')
            if not self.asynchronous:
                self.postprocess()
            return
        print(f"Failed to download '{self.url}'")
        if self.ui:
            self.ui.error(f"Failed to download '{self.url}'")

    def postprocess(self):
        print(f"postprocess {self.url}")
        self.method(self.result)
        self.ended()

    def check(self, _foo=None):
        if self.thread.is_alive():
            self.root.after(200, self.check, [None])
        else:
            # process is ended
            self.postprocess()
            self.ui.refresh_default_values()


class AsyncPopen(AsyncObject):
    # Do a synchronous or asynchronous Popen, depending on flag
    def __init__(self, asynchronous: bool, args, installer: "Installer", expr, installer_name, ui_name):
        super().__init__()
        self.process = None
        self.args = args
        self.installer = installer
        self.ui = None
        self.root = None
        self.expr = expr
        self.installer_name = installer_name
        self.ui_name = ui_name
        if not asynchronous:
            self.run(None)

    def run(self, ui: "PwpInstallerUi" or None):
        # will be called when the UI is available
        self.ui = ui
        if ui is not None:
            self.root = ui.root
        # HACK:
        # Do NOT ask me why!
        # when the exe is in "Program Files (x86)"
        # it is mandatory to have shell=True if we have stdout=subprocess.PIPE
        # otherwise run fails.
        # but, shell=True is NOT mandatory
        #   - if we do NOT have   stdout=subprocess.PIPE
        #   - OR if the exe is in a user directory
        # rather strange, and not so much documented.

        try:
            self.process = subprocess.Popen(self.args, shell=True,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # noqa
        except OSError as e:
            print(f"Error {e} while subprocess({self.args}")
            return
        if self.ui is None:
            self.process.wait()
            self.postprocess()
        else:
            self.check()

    def postprocess(self):
        (results, errors) = self.process.communicate()
        # print(f"ended [{results}]\n")
        s = results.decode('utf-8')
        m = re.match(self.expr, s)
        if m:
            val = m.group(1)
            print(f"{self.installer_name} = '{val}'")
            setattr(self.installer, self.installer_name, val)
            if self.ui is not None:
                label = getattr(self.ui, self.ui_name)
                label["text"] = val
                self.ui.refresh_default_values()
        self.ended()

    def check(self, _foo=None):
        if self.process.poll() is None:
            self.root.after(200, self.check, [None])
        else:
            # process is ended
            self.postprocess()


class Installer:
    def __init__(self, arguments=None):
        self.progress_status = 0
        self.ui = None
        self.async_ffmpeg: AsyncPopen or None = None
        self.async_piwipre: AsyncPopen or None = None
        self.async_packages: AsyncRequest or None = None

        if platform.system() != "Windows":
            self.warning("--install-exe can be used only on Windows!")
            exit(-1)

        print("Installer  : starting piwiPre Installer")

        arguments = arguments or []

        parser = argparse.ArgumentParser(description='install piwiPre on computer')
        parser.add_argument('--gui',
                            help="display the graphical UI",
                            action='store',
                            choices=['true', 'false'],
                            default="true")
        parser.add_argument('--elevation',
                            help="elevate privileges to be able to write in system files",
                            action='store',
                            choices=['true', 'false'],
                            default="true")
        parser.add_argument('--version',
                            help="prints help and exits",
                            action='store_true')

        parser.add_argument('--user',
                            help="Install for user. This is for internal use only, not to be used by humans")
        parser.add_argument('--program-files',
                            help="Install in that directory. This is for internal use only, not to be used by humans")
        parser.add_argument('--home',
                            help="User home. This is for internal use only, not to be used by humans")
        parser.add_argument('--appdata',
                            help="User appdata directory. This is for internal use only, not to be used by humans")

        parser.add_argument('--ffmpeg',
                            help="Install ffmpeg.exe",
                            action='store_true')
        parser.add_argument('--piwipre',
                            help="Install piwiPre.exe",
                            action='store_true')
        parser.add_argument('--mariadb',
                            help="Install mariaDb connector",
                            action='store_true')

        parser.add_argument('--force',
                            help="forces a new install of up to date packages (only for command-line)",
                            action='store_true')

        parser.add_argument('--mode',
                            help="test: run in separate dir, install: normal install",
                            action='store',
                            choices=['test', 'install'],
                            default="install")

        parser.add_argument('--chdir',
                            help="new directory to change to",
                            action='store')
        parser.add_argument('--base',
                            help="base directory for piwiPre",
                            action='store')

        self.args = parser.parse_args(arguments)

        if self.args.version:
            print(f"Installer  : pwpInstaller version {PwpVersion.spec}")
            exit(0)

        # when we call elevation(), the program is started again,
        # BUT, we can modify self.args.user, and this modification is remembered.
        # HOWEVER, other args are not !

        if self.args.user:
            self.msg(f"get user {self.args.user} from cmdline ")
        else:
            self.args.user = os.getlogin()
            self.msg(f"get user {self.args.user} from environment ")

        self.user_key = None  # will be computed by compute_default_values()
        self.user_home = None
        self.user_base = None
        self.user_program_files = None
        self.user_appdata = None

        if self.args.elevation == "true":
            try:
                elevate(show_console=self.args.gui == "false")  # noqa
                # elevate(show_console=True)  # noqa
                print("Elevated OK")
            except Exception as exx:
                print(f"Exception '{exx}' in elevate()")

        self.cur_dir = os.path.abspath(self.args.chdir or
                                       (os.path.expanduser('~' + self.args.user) + r'\Downloads'))
        self.makedirs(self.cur_dir)
        os.chdir(self.cur_dir)

        self.ffmpeg_path = None
        self.ffmpeg_exists = False
        self.ffmpeg_version = None

        self.piwipre_version = None
        self.piwipre_target_version = None
        self.piwipre_path = None
        self.piwipre_exists = False
        self.waiting = None

        self.compute_default_values()

        if self.args.gui == "false":
            self.run()
        else:
            print("StartingPwpInstallerUI")
            self.ui = PwpInstallerUi(self.args, installer=self)

            AsyncPopen.add_method(self.ui.activate_buttons)
            self.ui.mainloop()
            pass

    def launch_piwi_pre(self):
        self.action("Launching piwiPre", "ongoing")
        target = f"{self.piwipre_path}\\piwiPre.exe"

        if not os.path.isfile(target):
            self.warning("Launching piwiPre FAILED")
            return
        try:
            print(f"Installer  : starting {target} --gui true --home {self.user_home} --base {self.user_base}")
            args = [target,
                    "--gui", "true",
                    "--home", self.user_home,
                    "--base", self.user_base,
                    "--enable-create-base", "true"]
            self.msg(f'starting {args}')
            subprocess.Popen(args,  # non blocking call.
                             shell=True,
                             # check=True,
                             # text=True,
                             )  # noqa
        except OSError as e:
            self.warning(f"Error {e} while piwiPre --version")
            return False

    def compute_default_values(self):
        self.user_key = self.get_user_key(self.args.user)

        self.user_home = (self.cur_dir if self.args.mode == "test"
                          else self.args.home if self.args.home
                          else os.path.expanduser(f"~{self.args.user}"))

        self.user_base = (self.args.base if self.args.base
                          else os.path.abspath(self.user_home + r'/Pictures/BASE'))

        self.user_appdata = (self.cur_dir if self.args.mode == "test"
                             else self.args.appdata if self.args.appdata
                             else self.user_home + r"\AppData\Roaming")  # os.environ['APPDATA']

        self.user_program_files = (self.cur_dir if self.args.mode == "test"
                                   else self.args.program_files if self.args.program_files
        else os.environ['PROGRAMFILES(X86)'])  # noqa

        self.msg(f"USER = {self.args.user}")
        self.msg(f"KEY  = {self.user_key}")
        self.msg(f"HOME = {self.user_home}")
        self.msg(f"BASE = {self.user_base}")
        self.msg(f"DATA = {self.user_appdata}")
        self.msg(f"PRGF = {self.user_program_files}")  # noqa

        self.ffmpeg_path = self.user_program_files + '\\ffmpeg'  # noqa

        self.ffmpeg_exists = (os.path.isfile(f"{self.ffmpeg_path}\\bin\\ffmpeg.exe") and
                              os.path.isfile(f"{self.ffmpeg_path}\\bin\\ffprobe.exe"))

        asynchronous = (self.args.gui == "true")

        if self.ffmpeg_exists:
            self.msg(f"ffmpeg {self.ffmpeg_version} is already installed in '{self.ffmpeg_path}' ")
            if self.ffmpeg_version is None and self.async_ffmpeg is None:
                self.msg("Checking FFMPEG version")
                self.action("Checking FFMPEG version", "ongoing")
                target = f"{self.ffmpeg_path}/bin/ffmpeg.exe"
                self.async_ffmpeg = AsyncPopen(asynchronous,
                                               [target, "-version"],
                                               self,
                                               r".*ffmpeg version (.*) Copyright .*",
                                               "ffmpeg_version",
                                               "ffmpeg_version_label")

            if not asynchronous:
                # the AsyncObject MUST have returned
                self.msg(f"FFMPEG version = {self.ffmpeg_version}")
                if self.args.mode != "test":
                    self.msg("use --force to force new install")
                    self.args.ffmpeg = False
            self.action("Downloader idle", "------ KB/ ------ KB")

        self.piwipre_path = self.user_program_files + '\\piwiPre'  # noqa
        self.piwipre_exists = False

        if self.piwipre_target_version is None and self.async_packages is None:
            self.msg("getting piwiPre latest packages name from server")
            self.async_packages = AsyncRequest(asynchronous,
                                               "https://gitlab.com/api/v4/projects/48915444/packages",
                                               self.postprocess_packages,
                                               is_json=True)

        target = f"{self.piwipre_path}\\piwiPre.exe"

        if not os.path.isfile(target):
            self.msg("piwiPre is NOT installed, need to install it")
            return

        if self.piwipre_version is None and self.async_piwipre is None:
            self.action("Checking PiwiPre installed version", "ongoing")
            # current version: '0.17 at 03/30/2024 18:32:06'
            self.async_piwipre = AsyncPopen(asynchronous,
                                            [target, "--version"],
                                            self,
                                            r"current version: '(.*)'",
                                            "piwipre_version",
                                            "piwipre_version_label")

    def action(self, line1, line2="------ KB/ ------ KB"):
        if self.ui:
            self.ui.set_action(line1, line2)

    def warning(self, line):
        if self.ui:
            self.ui.gui_warning(line)

        print(termcolor.colored("WARNING: " + line, color='red', force_color=True))

    def error(self, line):
        if self.ui:
            self.ui.gui_error(line)
        else:
            print(termcolor.colored("ERROR  : " + line, color='red', force_color=True))
            # input("Close window after error?")
            exit(-1)

    def msg(self, line):
        if self.ui:
            self.ui.gui_msg(line)
        print("Installer  : " + line)

    @staticmethod
    def makedirs(path):
        if os.path.isdir(path):
            return
        os.makedirs(path)

    def get_html(self, url):
        # No need to make asynchronous, because is done during the installation phase
        response = requests.get(url)
        if response.status_code == 200:
            strings = response.content.decode('utf-8')
            return strings.split('\n')
        self.error(f"Failed to download '{url}'")

    def progress_bar(self, filename, nb_chunk: int, chunk_size: int, total: int):
        fetched_kb = int(nb_chunk * chunk_size / 1024)
        if nb_chunk <= 1:
            self.progress_status = 0

        if self.ui:
            pc = int(100 * 1024 * fetched_kb / total)
            self.action(filename, f"{fetched_kb: 6} KB / {int(total / 1024)} KB")
            self.ui.set_progress(pc)

        pc = int(50 * 1024 * fetched_kb / total)
        print(f"\r[{'#' * pc}{'-' * (49 - pc)}]  {fetched_kb: 6} KB / {int(total / 1024)} KB", end="")

    def download(self, url, dest):
        self.msg(f"Starting to download'{url}' into '{dest}'")
        response = requests.get(url, stream=True)
        size = int(response.headers['Content-Length'])
        self.msg(f"Size = {int(size / 1024)} KB")
        if response.status_code == 200:
            nb_chunk = 0
            self.makedirs(os.path.dirname(dest))
            with open(dest, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    nb_chunk += 1
                    self.progress_bar(os.path.basename(dest), nb_chunk, 1024, size)

            self.progress_bar("", 0, 1024, size)
            self.action(os.path.basename(dest), "downloaded")
            self.msg(f"\ndownloaded successfully '{url}' into '{dest}' in {int(size / 1024)} KB")
        else:
            self.error(f"Failed to download '{url}' into '{dest}'.")

    # -----------------------------------------------------------------------------------------
    # ffmpeg

    def install_ffmpeg(self):
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

        self.msg(f"Downloading latest FFMPEG package version {url}")
        self.download(url, f"{self.ffmpeg_path}/ffmpeg.zip")
        root = None
        with zipfile.ZipFile(f"{self.ffmpeg_path}/ffmpeg.zip") as myzip:
            names = myzip.namelist()
            found_ffmpeg = False
            found_ffprobe = False
            for f in names:
                if root is None or len(f) < len(root):
                    root = f
                if "ffmpeg.exe" in f:
                    myzip.extract(f, self.ffmpeg_path)
                    found_ffmpeg = True
                    self.makedirs(f"{self.ffmpeg_path}/bin")
                    shutil.move(f"{self.ffmpeg_path}/{f}", f"{self.ffmpeg_path}/bin/ffmpeg.exe")
                if "ffprobe.exe" in f:
                    myzip.extract(f, self.ffmpeg_path)
                    found_ffprobe = True
                    self.makedirs(f"{self.ffmpeg_path}/bin")
                    shutil.move(f"{self.ffmpeg_path}/{f}", f"{self.ffmpeg_path}/bin/ffprobe.exe")

        os.remove(f"{self.ffmpeg_path}/ffmpeg.zip")
        shutil.rmtree(f"{self.ffmpeg_path}/{root}")
        if found_ffmpeg and found_ffprobe:
            self.msg(f"ffmpeg installed in '{self.ffmpeg_path}'")
        else:
            self.error('ffmpeg or ffprobe not found in archive')

        # useless: ffmpeg is called from absolute path
        # if not self.args.self_test:
        #     self.add_to_path(ffmpeg_path + '/bin')

    # -----------------------------------------------------------------------------------------
    # auto-install

    def postprocess_packages(self, packages):
        def to_float(des: str):
            my = re.match(r"(\d+)\.(\d+).?(\d*)", des)
            if my:
                a = int(my.group(1))
                b = int(my.group(2))
                c = float(my.group(3) or '0.0')
                return a * 10000 + b + c / 10000.0
            return 0

        latest = None
        latest_float = 0.0
        for pack in packages:
            new_val = to_float(pack['version'])
            if new_val > latest_float:
                latest = pack
                latest_float = new_val
        self.piwipre_target_version = latest["version"]
        if self.ui:
            self.ui.piwipre_target_label["text"] = latest["version"]

        # CAVEAT: piwipre_version and piwipre_target_version are computed asynchronously
        # so we do not know which one is known before the other.
        # this is managed by python_to_ui

        if self.args.piwipre and self.ui is None:
            self.msg(f"piwiPre is already installed in '{self.piwipre_path}' " +
                     f" with version {self.piwipre_version}")
            if self.args.mode != "test":
                self.msg("use --force to force new install")
                self.args.piwipre = False

    def install_piwipre(self):
        def build_lnk(source, dst, arguments: str):
            if os.path.isfile(dst):
                os.remove(dst)
            pylnk3.for_file(source, dst, arguments=arguments, window_mode="Minimized")
            self.msg(f"built '{dst}'")

        self.makedirs(self.piwipre_path)
        target = self.piwipre_target_version

        base_url = "https://gitlab.com/api/v4/projects/48915444/packages/generic/piwiPre"

        piwipre_abs = os.path.abspath(f"{self.piwipre_path}/piwiPre.exe")
        piwipre_vers = os.path.abspath(f"{self.piwipre_path}/piwiPre-{target}.exe")
        piwipre_lnk = os.path.abspath(f"{self.piwipre_path}/piwiPreGui.lnk")

        self.download(f"{base_url}/{target}/piwiPre-{target}.exe", piwipre_vers)
        build_lnk(piwipre_abs, piwipre_lnk, '--gui true --base-last true')
        shutil.copy2(piwipre_vers, piwipre_abs)

        src = f"{base_url}/{target}/pwpInstaller-{target}.exe"
        today = time.strftime("%Y-%m-%d-%Hh%M-%S")
        installer_abs = os.path.abspath(f"{self.piwipre_path}/pwpInstaller.exe")
        installer_vers = os.path.abspath(f"{self.piwipre_path}/pwpInstaller-{target}-{today}.exe")
        installer_lnk = os.path.abspath(f"{self.piwipre_path}/pwpInstallerGui.lnk")

        myself = os.path.abspath(sys.orig_argv[0] if sys.orig_argv else sys.argv[0])

        build_lnk(installer_abs, installer_lnk, '--gui true')

        if myself == installer_abs:
            self.download(src, installer_vers)
            self.warning(f"Latest package version '{target}' installed as '{installer_vers}'")
            self.warning(f"You can copy it: copy  {installer_vers}  {installer_abs}")
        # elif myself == installer_vers:
        #     This will never happen, because we are now using the date-time
        #     self.download(src, installer_abs)
        #     self.warning(f"Latest package version '{target}' installed as '{installer_abs}'")
        #     self.warning(f"You can copy it: copy  {installer_abs}  {installer_vers}")
        else:
            self.download(src, installer_vers)
            shutil.copy2(installer_vers, installer_abs)
            self.warning(f"Latest package version '{target}' installed as '{installer_abs}' and '{installer_vers}' ")

        if not self.args.mode == "test":
            self.add_to_path(self.user_program_files + '\\piwiPre')  # noqa

        menu = self.user_appdata + r"\Microsoft\Windows\Start Menu\Programs\piwiPre"

        if not os.path.isdir(menu):
            self.makedirs(menu)
            self.msg(f"build menu directory '{menu}'")
        else:
            self.msg(f"existing menu directory '{menu}'")

        build_lnk(piwipre_abs, menu + '/piwiPre.lnk',
                  arguments=f' --gui true --home "{self.user_home}" --base-last true')
        build_lnk(installer_abs, menu + '/pwpInstaller.lnk',
                  arguments=f' --gui true  --user "{self.args.user}"')
        if self.ui:
            self.ui.configure_button.enable()

    def find_maria_db_url(self, bits: str):
        # code below is an attempt to find the latest MariaDB CC version
        # however, as of 2024/10/24, there is NO Windows version in MariaDB 3.4
        # but there is one in 3.3.11 !
        # So we just return the latest known version in case of error
        all_versions = self.get_html("https://dlm.mariadb.com/browse/c_connector/")
        url = None
        version = None
        for line in all_versions:
            #             <td><a href="/browse/c_connector/201/">C connector 3.3</a></td>
            #             <td><a href="/browse/c_connector/169/">C connector 3.2 (EOL)</a></td>
            m = re.match(r'\s*<td><a href="(.*)">C connector (.*)</a></td>', line)
            if m and m.group(2) and 'EOL' not in m.group(2):
                if version is None or m.group(2) > version:
                    version = m.group(2)
                    url = m.group(1)
        if url is None:
            self.error('Unable to find URL of current version in "https://dlm.mariadb.com/browse/c_connector/"')

        all_sub_versions = self.get_html("https://dlm.mariadb.com" + url)
        sub_url = None
        sub_version = None
        for line in all_sub_versions:
            #             <td><a href="/browse/c_connector/201/1294/">C connector 3.3.0</a></td>
            m = re.match(r'\s*<td><a href="(.*)">C connector (.*)</a></td>', line)
            if m and 'EOL' not in m.group(2):
                if sub_version is None or m.group(2) > sub_version:
                    sub_version = m.group(2)
                    sub_url = m.group(1)

        if sub_url is None:
            self.error(f'Unable to find current version in "https://dlm.mariadb.com/browse/c_connector{url}"')

        all_bins = self.get_html("https://dlm.mariadb.com" + sub_url)
        for line in all_bins:
            # <td><a href="https://dlm.mariadb.com/3677107/Connectors/c/connector-c-3.3.8/
            # mariadb-connector-c-3.3.8-win32.msi">connector-c-3.3.8/mariadb-connector-c-3.3.8-win32.msi</a></td>
            m = re.match(r'\s*<td><a href="(.*)">.*\.msi</a></td>', line)
            if m and bits in m.group(1):
                return m.group(1)
        self.msg(f'Unable to find {bits} version in "https://dlm.mariadb.com{sub_url}"')
        # default to last known version
        return "https://dlm.mariadb.com/3907090/Connectors/c/connector-c-3.3.11/mariadb-connector-c-3.3.11-win64.msi"

    def install_maria_db(self):
        archi = "64" if "64" in os.environ['PROCESSOR_ARCHITECTURE'] else '32'
        url = self.find_maria_db_url(archi)
        dest = f"{os.getcwd()}/mariadb.msi"
        self.download(url, dest)
        self.warning(f"maria_db for {archi} bits architecture is downloaded as '{dest}'")

        if self.args.mode == "test":
            self.warning("You should running it AS AN ADMINISTRATOR")
            #  os.system(dest)
        else:
            self.warning("test: NOT running it ")

    def install_for_python(self):
        """
        Used in a PYTHON context, for windows architectures
        helps the installation of ffmpeg and mariaDb
        :return:
        """
        if platform.system() != "Windows":
            self.error("--install-tools can be used only on Windows!")

        self.install_ffmpeg()
        self.install_maria_db()

    @staticmethod
    def get_user_from_key(key):
        try:
            with winreg.ConnectRegistry(None, winreg.HKEY_USERS) as registry:
                with winreg.OpenKey(registry, key) as key2:
                    with winreg.OpenKey(key2, "Volatile Environment") as key3:
                        return winreg.QueryValueEx(key3, "USERNAME")[0]
        except OSError:
            return None

    @staticmethod
    def get_value(key, fid):
        try:
            return winreg.QueryValueEx(key, fid)[0]
        except OSError:
            return None

    def get_user_key(self, username):
        # How to find user registry ID?
        # look at all HKEY-USERS/key/Volatile Environmemt/USERNAME      # noqa
        with winreg.ConnectRegistry(None, winreg.HKEY_USERS) as registry:
            index = 0
            while True:
                try:
                    key = winreg.EnumKey(registry, index)
                    val = self.get_user_from_key(key)
                    if val == username:
                        return key
                    index += 1
                except OSError:
                    return None

    def add_to_path(self, value, master_key="Path"):
        if not windll.shell32.IsUserAnAdmin():
            self.error("INTERNAL ERROR: Not an admin")

        try:
            with winreg.ConnectRegistry(None, winreg.HKEY_USERS) as registry:  # pragma: no cover
                # requires administrator privileges, which is difficult in automated tests
                with winreg.OpenKey(registry, self.user_key) as key2:
                    with winreg.CreateKey(key2, "Environment") as key3:  #
                        current = self.get_value(key3, master_key)
                        if current is None:
                            current = value + ";"
                            winreg.SetValueEx(key3, master_key, 0, winreg.REG_EXPAND_SZ, current)
                            winreg.FlushKey(key3)
                            self.msg(f"Created '{value}' to {master_key} environment variable")
                        elif value not in current:
                            if current[-1:] != ';':
                                current += ';'
                            current += value + ";"
                            winreg.SetValueEx(key3, master_key, 0, winreg.REG_EXPAND_SZ, current)
                            winreg.FlushKey(key3)
                            self.msg(f"Added '{value}' to {master_key} environment variable")
                        else:
                            self.msg(f"{master_key} already get '{value}' ")
        except Exception as e:
            self.error(f"Exception '{e}' in registry write")

    def run_min_test(self, system_dir=True):
        self.action("Minimal test", "Starting")
        test_dir = (self.user_program_files if system_dir else '.') + '\\piwiPreTmp'  # noqa
        if os.path.isdir(test_dir):
            os.rmdir(test_dir)
            self.msg(f"Removed {test_dir}")
        else:
            os.makedirs(test_dir)
            self.msg(f"Created {test_dir}")
        self.add_to_path(str(datetime.datetime.now()), "PiwiPrePath")
        self.action("Minimal test", "OK")

    def run(self):
        self.action("Installation", "Start")

        # if not self.args.piwipre and not self.args.ffmpeg and not self.args.mariadb and self.args.mode == "test":
        #     self.run_min_test()
        if self.args.piwipre:
            self.install_piwipre()
        if self.args.ffmpeg:
            self.install_ffmpeg()
        if self.args.mariadb:
            self.install_maria_db()
        self.action("Installation", "OK")


def run_installer(arguments):
    if platform.system() != "Windows":  # pragma: no cover
        print("Installer  : runs only on windows")
        return
    try:
        Installer(arguments)
    except OSError as e:
        print(f"Installer  :OS Error {e}")
    except Exception as f:
        print(f"Installer  : Run Error {f}")


def installer_console():  # pragma: no cover
    if '--gui' in sys.argv:
        run_installer(sys.argv[1:])
    else:
        run_installer(sys.argv[1:] + ['--gui', 'false'])


def installer_gui():  # pragma: no cover
    if '--gui' in sys.argv:
        run_installer(sys.argv[1:])
    else:
        run_installer(sys.argv[1:] + ['--gui', 'true'])


if __name__ == "__main__":
    # NB --gui default is true, so pwpInstaller runs in GUI mode.
    run_installer(sys.argv[1:])
