# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import argparse
import re
import sys
import os
import pprint
import datetime
import locale
import platform
from enum import Enum

from piwiPre.pwpActor import ACTOR

from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpErrors import LOGGER
from piwiPre.pwpGui import GuiError
from piwiPre.pwpVersion import PwpVersion
from piwiPre.pwpLicence import PwpLicence
# NB: cannot import PwpConfigurator here, would be a circular import...


class ArgHeader:
    def __init__(self, helps: str, lang='en'):
        self.helps = helps
        self.lang = lang
        self.setups = []
        self.location = "header"  # can be used to differentiate with cmdline arguments
        # following lines are just to shut up the syntax checker
        self.name = "header"
        self.default = "header"
        self.fr_default = "header"

    @staticmethod
    def is_in_config():
        return False

    def write_rst(self, stream, lang='en'):
        if lang != self.lang:
            return
        stream.write("\n")
        for line in self.helps.splitlines():
            stream.write(line + '\n')
        stream.write("\n")

    def write_ini_file(self, stream, lang='en', config=None, verbose=True):
        del config
        if lang != self.lang:
            return
        if not verbose:
            return
        stream.write("\n")
        for line in self.helps.splitlines():
            stream.write('# ' + line + '\n')
        stream.write("\n")

    # following lines are just to shut up the syntax checker
    def get_setup_constraint(self,
                             setup: "ServerSetup",
                             config: PwpConfig):
        LOGGER.internal_error("ArgHeader.get_setup_constraint()")
        return PwpConstraint("", ConstraintHow.HIDDEN, "", "", "", PwpArgType.STR,
                             "", "", location="")


class PwpArgType(Enum):
    """
    Describes the kind of UI that should be used to change the value, and the typing verifications
    """

    BOOL = 'BOOL'
    STR = 'STR'
    PASSWORD = 'PASSWORD'
    DIR = 'DIR'
    INT = "INT"
    DICT = "DICT"
    LIST = 'LIST'
    PRESENT = 'PRESENT'     # present (=true) or absent (=None)

    def has_instance(self, value):
        if self == PwpArgType.BOOL:
            return isinstance(value, str) and value.lower() in ['true', 'false'] or isinstance(value, bool)
        if self == PwpArgType.STR:
            return isinstance(value, str)
        if self == PwpArgType.PASSWORD:
            return isinstance(value, str)
        if self == PwpArgType.DIR:
            return isinstance(value, str)
        if self == PwpArgType.INT:
            return isinstance(value, int)
        if self == PwpArgType.DICT:
            return isinstance(value, dict)
        if self == PwpArgType.LIST:
            return isinstance(value, list) or value is None
        if self == PwpArgType.PRESENT:
            return isinstance(value, str) and value == ''

        return False


class ConstraintHow(Enum):
    """
        Explains 'HOW' the constraint should be set to the configuration parameter

        CMDLINE:  can be changed by user, but from the cmdline only
        DEFAULT:  can be changed by user, default to the default value, no need to specify value on the arg list.
        VALUE:    can be changed by user, default to a different value set in 'value', it is NOT the default value
        SILENT:   CANNOT be changed by user, the value is mandatory for this setup
        HIDDEN:   CANNOT be changed with a GUI, must be done within a config file
    """

    # Rules for setting correctly the fields of server setup
    # each configuration item has a list of ServerSetups that is evaluated sequentially
    # as soon as 1 setup matches, the corresponding constraint is returned
    # when the setup is unknown, it is set to None, None, None
    #
    # the setups should be ordered as follows:
    # - If no setup,       e.g --help
    #   the item is not displayed on the UI.
    # - If how == HIDDEN,  e.g. --gui
    #   the item is not displayed on the UI AND the value is set
    # - If how == CMDLINE, e.g. --quiet
    #   the item is shown in piwiPre,
    #   and NOT shown in configurator
    #
    # - If an item is sensitive to the values of the setup, e.g. to piwigo TRUE/FALSE
    #   The value for TRUE, ALL, ALL should be set
    #       with how == FORCED when the value is mandatory
    #       with how == DEFAULT if the default value can be used, but other values are possible
    #       with how == VALUE is the corresponding value is better than the default
    #   The value for FALSE, ALL, ALL should also be set, with the same rules
    #       e.g. --enable-verify-sub-album, with a value for true, false, None
    #   the default should be set when the setup is unknown
    #       the corresponding value should NOT be FORCED, otherwise we force a value in unknown cases
    #       that last item can be merged with one of the previous if the values, and how are the same
    #            e.g. --enable-thumbnails-delete

    # NB:
    # DEFAULT *could* be replaced by VALUE
    # But it is easier to use it, because we do not need to pass the default_value while creating the ServerSetup

    CMDLINE = "CMDLINE"
    DEFAULT = 'DEFAULT'
    VALUE = 'VALUE'
    FORCED = 'FORCED'
    HIDDEN = 'HIDDEN'       # This ConstraintHow is currently unused by the code

    def __str__(self):
        return self.value.lower()

    @staticmethod
    def from_str(rep: str):
        for item in ConstraintHow:
            if item.value.lower() == rep.lower():
                return item
        LOGGER.internal_error(f"Illegal ConstraintHow '{rep}'")


class CVS(Enum):
    """potential values for the piwigo, album and thumbnails conditions
    """
    LOCAL = 'LOCAL'
    REMOTE = 'REMOTE'
    UNUSED = 'UNUSED'
    ALL = 'ALL'

    def __str__(self):
        return self.value.lower()

    @staticmethod
    def from_str(rep: str):
        for item in CVS:
            if item.value.lower() == rep.lower():
                return item
        LOGGER.internal_error(f"Illegal CVS {rep}")


class PwpConstraint:

    def __init__(self, name: str, how: ConstraintHow, value: str, helps: str, fr_helps: str,
                 pwp_type: PwpArgType, origin: str, initial: str, location: str):
        """
        A constraint set on a configuration parameter
        :param name: name of the parameter
        :param how:  ConstraintHow
        :param value: new value
        :param helps: help string
        :param fr_helps: in French
        :param pwp_type: str etc...
        :param origin: origin of the value: gui, config file, default...
        :param initial: initial value found in the config file (or inherited from predecessors)
        :param location: args/config/both
        """

        self.name = name
        self.how: ConstraintHow = how
        self.value = value
        self.helps = helps
        self.fr_helps = fr_helps
        self.pwp_type: PwpArgType = pwp_type
        self.origin = origin
        self.initial = initial
        self.location = location


class ServerSetup:
    def __init__(self,
                 album: CVS = CVS.ALL,
                 thumbnails: CVS = CVS.ALL,
                 how: ConstraintHow = ConstraintHow.DEFAULT,
                 pwp_type: PwpArgType = PwpArgType.STR,
                 value=None,
                 en_help=None,
                 fr_help=None,
                 location="both"):
        """
        ServerSetup : One specific setup = (piwigo, album, thumbnails) and associated value for a field
        :param album:       Conditions for this value
        :param thumbnails:  Conditions for this value
        :param how:         How to get the value for this case
        :param value:       value if condition is met
        :param en_help:     help if condition is met
        :param fr_help:     help if condition is met
        :param location:    where the parameter is set
        """

        self.album = album
        self.thumbnails = thumbnails
        # values when condition is True
        self.how = how
        self.value = value
        self.pwp_type = pwp_type
        self.en_help = en_help
        self.fr_help = fr_help
        self.location = location

    def match(self, cond: 'ServerSetup'):

        if self.album == cond.album or self.album == CVS.ALL or cond.album == CVS.ALL:
            pass
        else:
            return False
        if self.thumbnails == cond.thumbnails or self.thumbnails == CVS.ALL or cond.thumbnails == CVS.ALL:
            pass
        else:
            return False
        return True

    def is_default(self):
        return self.how == ConstraintHow.DEFAULT

    def get_value_from_constraint(self, initial_value, initial_origin):
        value = self.value or ""
        value = value.lower() == 'true' if self.pwp_type == PwpArgType.BOOL else value

        if self.how == ConstraintHow.FORCED:
            # the value in the constraint is mandatory
            if value == initial_value:
                return initial_value, initial_origin
            else:
                return value, "GUI"

        if self.how == ConstraintHow.HIDDEN:
            # The GUI does not allow to change the value
            return initial_value, initial_origin

        # else, the current value can be used, unless empty/not-empty

        if value != "" and initial_value == "":
            # there is no initial value, propose the default
            return value, "GUI"

        # there is a value,
        return initial_value, initial_origin


class ArgIniItem(ArgHeader):

    def __init__(self,
                 name: str,
                 l_help: str,
                 location: str,
                 helps: str,
                 default,
                 arg,
                 pwp_type: PwpArgType,
                 fr_help: str, fr_l_help: str, fr_default: str or None,
                 setups=None):
        """
        ArgIniItem:        a configuration item in cmdline args or .ini file
        :param name:       name of the parameter
        :param l_help:  english version of the long_help (for the config file)
        :param location:   where the arg may be set: args (aka cmdline), both
        :param helps:    short help
        :param default:    default value
        :param arg:        argparse.arg as managed by argparse
        :param pwp_type:   python type str, int, dict... or 'dir'
        :param fr_help:    French help
        :param fr_l_help:  French long help
        :param fr_default: French default value, if different from the english one
        :param setups:     list of setups where this parameter is valid (pîwigo, album, thumbnails settings)
        """
        super().__init__(helps=helps)
        self.name = name
        self.l_help = l_help
        self.fr_l_help = fr_l_help
        self.location = location
        self.fr_help = fr_help
        self.default = default
        self.fr_default = fr_default
        self.arg = arg
        self.pwp_type = pwp_type
        self.setups: [ServerSetup] = setups or []

        if self.pwp_type == PwpArgType.DICT and self.default == '':
            self.default = {}
        if not self.pwp_type.has_instance(self.default) and self.default is not None:
            LOGGER.internal_error(f"Parameter '{name}' default value {default} should have type {str(pwp_type)} ")

    def get_setup_constraint(self,
                             setup: ServerSetup,
                             config: PwpConfig):
        """
        get_value_for_setup(self, setup, lang):
        :param setup: triage, local or remote
        :param config: the initial configuration, before applying the constraint.
        :return: PwpConstraint or None
        """
        for setup_val in self.setups:
            if setup.match(setup_val):
                value, origin = setup_val.get_value_from_constraint(config[self.name], config.origin[self.name])
                how = ConstraintHow.VALUE if (
                    setup_val.how in [ConstraintHow.FORCED] and value == config[self.name]  # removed HIDDEN from list
                ) else setup_val.how
                # forced items that do not change are not reported as forced
                return PwpConstraint(self.name, how, value,
                                     setup_val.en_help or self.helps,
                                     setup_val.fr_help or self.fr_help,
                                     self.pwp_type,
                                     origin=origin,
                                     initial=config[self.name],
                                     location=setup_val.location)
        # if we reach here, it means that there is no matching setup, in this case we do not want to change the element
        return None

    def print_fr(self, full=False):

        def fit(val, explain):
            if len(val) > 24:
                if explain:
                    return f"{val}\n{'':>26}{explain}"
                else:
                    return f"{val}"
            else:
                return f"{val:<24}{explain}"

        def right(val):
            if val == '':
                return ''
            res = ""
            cur_line = ""
            sp = val.split(" ")
            for elem in sp:
                if len(cur_line) + len(elem) > 50:
                    res += f"{cur_line}\n{'':>26}"
                    cur_line = ""
                cur_line += elem + " "
            res += cur_line
            return res

        if not self.arg:
            # this is not a cmd-line arg
            return

        name = '--' + self.name + " "
        if not self.arg.const:
            sep = ''
            if self.arg.choices:
                name += '{'
                for item in getattr(self.arg, 'choices'):
                    name += f"{sep}'{item}'"
                    sep = ', '
                name += '}'
            else:
                name += getattr(self.arg, 'dest').upper()  # noqa

        print(f"  {fit(name, right(self.fr_help))}")
        if full and self.fr_l_help:
            for line in self.fr_l_help.split('\n'):
                print("                  |  " + line)

    def is_in_config(self):
        return self.location != 'args'

    def write_rst(self, stream, lang='en'):

        default = self.format_ini_value(self.default, 0, ini_file=False)
        # default = 'false' if default is False else 'true' if default is True else default

        if lang == 'en':
            location = ('configuration files only' if self.location == 'config' else
                        'cmd-line arguments only' if self.location == 'args' else
                        'both configuration files and cmd-line arguments')
        else:  # if lang == 'fr':
            location = ('uniquement dans les fichiers de configuration ' if self.location == 'config' else
                        'uniquement sur la ligne de commande ' if self.location == 'args' else
                        'dans les fichiers de configuration ou sur la ligne de commande')
        default = ("``" + default + "``") if default else ''
        stream.write(f"\n**{self.name}** : {default}\n\n")
        if lang == 'en':
            stream.write(f"  where: {location}\n\n")
            config = self.l_help
            helps = self.helps
        else:
            stream.write(f"   où: {location}\n\n")
            config = self.fr_l_help
            helps = self.fr_help
        stream.write(f"   {helps}\n")
        for line in config.splitlines():
            stream.write(f"   {line}\n")
        stream.write("\n")

    def format_ini_value(self, item, level=0, ini_file=True):
        if item is False:
            return 'false'
        if item is True:
            return 'true'
        if item is None:
            # Output 'None' is NOT an issue,
            # because 'None' will be parsed afterward as None
            return 'None'
        if isinstance(item, str):
            if re.search(r'\W', item):
                return "'" + item + "'"
            return item

        if type(item) is dict:
            if len(item.keys()) == 0:
                return ""
            if level == 0:
                if ini_file:
                    res = '\n'
                else:
                    res = '\n ::\n\n'
            else:
                res = '\n'
            for key, value in item.items():
                prefix = ""
                prefix += " " * ((level + 1)*(4 if ini_file else 3))
                k = self.format_ini_value(key, level=level + 1, ini_file=ini_file)
                val = self.format_ini_value(value, level=level + 1, ini_file=ini_file)
                res += f"{prefix}{k}: {val}\n"
            if level == 0:
                if not ini_file:
                    res += "\n\n#  *(end of the structure)*\n"
            return res

        return str(item)

    def write_ini_file(self, stream, lang='en', config=None, verbose=True):
        """
        Writes the .ini file for the ArgIniItem
        if config is None, writes the default value for the parser
        else, writes the value for config
        :param stream:
        :param lang:
        :param config:
        :param verbose: if true, print every info
        :return:
        """
        do_print_value = True
        if config is None:
            # means that we are printing the default configuration, always print the default value
            val = self.default
        elif self.name not in config:
            # means that the item is NOT in the configuration, we do not print it
            do_print_value = False
            val = ""
        elif config[self.name] is None:
            # None means inherit from previous file
            # so, we do not print it
            do_print_value = False
            val = ""
        else:
            val = config[self.name]

        if self.pwp_type == PwpArgType.DIR:
            val = val or ''     # None -> ""
            val = val.replace('\\', '/')

        val = self.format_ini_value(val, 0, ini_file=True)

        if lang == 'en':
            location = ('configration files only' if self.location == 'config' else
                        'cmd-line arguments only' if self.location == 'args' else
                        'both configuration files and cmd-line arguments')
        else:  # if lang == 'fr':
            location = ('uniquement dans les fichiers de configuration ' if self.location == 'config' else
                        'uniquement sur la ligne de commande ' if self.location == 'args' else
                        'dans les fichiers de configuration ou sur la ligne de commande')

        if self.location == 'args':
            if not verbose:
                return
            header = '# '
            name = '--' + self.name
        elif not do_print_value:
            if not verbose:
                return
            header = '# '
            name = self.name
        else:
            header = ''
            name = self.name

        doc = f"{header}{name} : {val} "
        str_help = self.helps if lang == 'en' else self.fr_help

        stream.write(f"{doc} {' '*(max(0, 60-len(doc)))} # {str_help}\n")
        if not do_print_value:
            if not verbose:
                pass
            elif lang == 'en':
                stream.write("#   This item is absent from this config file, and will be inherited from previous\n")
            else:
                stream.write("#   Cet élément est absent de ce fichier de configuration et sera hérité du précédent\n")
        if not verbose:
            pass
        elif lang == 'en':
            stream.write(f"#   where: {location}\n\n")
            # stream.write(f"#   {self.helps}\n")
            for line in self.l_help.splitlines():
                stream.write(f"#   {line}\n")
        else:
            stream.write(f"#   où: {location}\n\n")
            # stream.write(f"#   {self.fr_help}\n")
            for line in self.fr_l_help.splitlines():
                stream.write(f"#   {line}\n")

        # stream.write("\n")


class PwpArgsIni(argparse.ArgumentParser):

    def __init__(self, **_kwargs):
        super().__init__(prog='piwiPre', allow_abbrev=False, exit_on_error=False)
        self.args_dico = {}
        self.items_list: list[ArgHeader] = []  # a list of ArgHeader or ArgIniItem
        self.home_config = None
        self.home = os.path.expanduser("~")

    def add_header(self, prologue: str, lang='en'):
        item = ArgHeader(prologue, lang=lang)
        self.items_list.append(item)

    def add_item(self, name_or_flags: str, **kwargs):
        # location should be 'config' or 'args'. any other value = 'both'. default = 'both'

        location = kwargs.pop('location') if 'location' in kwargs else 'both'

        config = kwargs.pop('config') if 'config' in kwargs else ""

        fr_config = kwargs.pop('fr_config') if 'fr_config' in kwargs else ''

        help_str = '' if 'help' not in kwargs else kwargs['help']

        fr_help_str = kwargs.pop('fr_help') if 'fr_help' in kwargs else ''

        fr_default_str = kwargs.pop('fr_default') if 'fr_default' in kwargs else None

        default = '' if 'default' not in kwargs else kwargs['default']

        pwp_type = kwargs.pop('pwp_type') if 'pwp_type' in kwargs else PwpArgType.STR

        setups = kwargs.pop('setups') if "setups" in kwargs else {}

        arg = super().add_argument('--' + name_or_flags, **kwargs) if location != 'config' else None
        item = ArgIniItem(name_or_flags, config, location, help_str, default, arg, pwp_type,
                          fr_help=fr_help_str, fr_l_help=fr_config, fr_default=fr_default_str, setups=setups)
        self.args_dico[name_or_flags] = item
        self.items_list.append(item)

    def print_fr(self, full=False):
        print("")
        print("Les options:")
        for arg in self.args_dico:
            self.args_dico[arg].print_fr(full)
        print("")

    def get_constraints_for_setup(self, setup: ServerSetup, config: PwpConfig)\
            -> dict[str, PwpConstraint]:
        """
        get_constraints_for_setup()
        :param setup: The server setup, or None if no setup
        :param config: configuration before applying the constraints from the server
        :return: a dict of PwpConstraint
        """
        res = {}
        for item in self.items_list:
            if item.location != "header":
                state = item.get_setup_constraint(setup, config)
                if state:
                    res[state.name] = state
        return res

    def build_rst(self, filename: str, lang='en'):
        abs_path = ACTOR.normalise_path(filename)
        LOGGER.debug(f"Build RST file {abs_path} , lang={lang}")
        with open(filename, 'w', encoding="utf-8") as f:
            start = datetime.datetime.now()
            if lang == 'en':
                f.write(f".. comment : CAVEAT: This text is automatically generated by pwpPatcher.py on {start}\n")
                f.write(".. comment :         from the code in pwpParser.py\n")
            else:
                f.write(f".. comment : ATTENTION: Ce fichier est a été généré par pwpPatcher.py le {start}\n")
                f.write(".. comment :             à partir du code dans pwpParser.py\n")

            for item in self.items_list:
                item.write_rst(f, lang)

    def write_ini_file(self, filename: str, lang='en', config=None, verbose=True, prologue=''):
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(prologue)
            for item in self.items_list:
                item.write_ini_file(f, lang=lang, config=config, verbose=verbose)

    def build_initial_config(self, language):
        """
        builds the default configuration.
        some values are computed depending on the language, which may have been set on the cmdline.
        :param language: en etc ...       # noqa
        :return: dict
        """
        dico = {}
        for v in self.items_list:
            if v.location != 'header':
                dico[v.name] = v.default if language == 'en' or v.fr_default is None else v.fr_default
        dico['help'] = None
        res = PwpConfig(content_str=None, filename="DEFAULT", dico=dico, previous=None)
        return res

    @staticmethod
    def stringify(value: str):
        if isinstance(value, str) and '--' in value[1:]:  # pragma: no cover
            LOGGER.warning(f"argument '{value}' contains '--', this is probably an error with 2 flags concatenated")
        if value is True or isinstance(value, str) and value.lower() == 'true':
            return 'true'
        if value is False or isinstance(value, str) and value.lower() == 'false':
            return 'false'
        if value is None or isinstance(value, str) and value.lower() == 'none':
            return 'none'
        if isinstance(value, int):
            return int(value)

        return value

    @staticmethod
    def get_val_from_cmdline(flag: str, cmdline):
        if flag in cmdline:
            index = cmdline.index(flag)
            if index > len(cmdline):
                LOGGER.config_error(f"--{flag} without a value")
            else:
                return cmdline[index + 1]
        return None

    @staticmethod
    def get_val_from_cmdline_lower(flag, cmdline):
        val = PwpArgsIni.get_val_from_cmdline(flag, cmdline)
        return None if val is None else val.lower()

    def check_cmd_line(self, program: str, real_args):

        LOGGER.msg(f"{program}: reading configuration from cmd-line arguments")
        string_args = [self.stringify(a) for a in real_args]
        args = None
        unknowns = []
        try:
            args, unknowns = super().parse_known_args(args=string_args)
        except argparse.ArgumentError as e:
            super().print_help()
            LOGGER.internal_error(f"configuration error {e}")
        except SystemExit as e:  # pragma: no cover
            super().print_help()
            # return None
            LOGGER.internal_error(f"Error on arguments {e}")

        if args is None:
            LOGGER.config_error("Unknown Error on arguments")
            return None

        if unknowns:
            super().print_help()
            en_msg = f"\n\ncmd-line : Unknown arguments {unknowns} \n *** Please change configuration ***\n"
            fr_msg = f"\n\ncmd-line : Arguments inconnus {unknowns}\n *** Changer la configuration ***  \n"

            if hasattr(args, 'gui') and args.gui == 'true':
                # When we have a GUI, we want to show the error
                # SOMETIMES, the main UI is not yet created: the initial check_cmd_line
                # SOMETIMES, the main UI is created, if we check_cmd_line while changing BASE, for instance
                # so, we rely on PwpGui.inside_main_loop to avoid nested loops
                # which ensures that mainloop() is started ONLY if not started inside a mainloop()
                # see program_907, 908 and program_1006

                LOGGER.msg(en_msg)
                gui = GuiError(en_msg, fr_msg)
                if hasattr(args, 'test_gui_dismiss_errors') and args.test_gui_dismiss_errors == 'true':
                    gui.root.after(1 * 1000, lambda: gui.dismiss())
                gui.mainloop()
            else:
                LOGGER.config_error(f"Unknown arguments {unknowns} *** Please change configuration ***")

        return args

    def parse_args_and_ini(self, program: str, ini_to_parse: str, arguments, with_config=True,):
        """
        parse_args_and_ini()
        :param program: str       = the program name, for debug messages
        :param ini_to_parse: str  = the name of the .ini file to be parsed, changed by test harness
        :param arguments:         = List of cmdline args (NOT a dico)
        :param with_config:       = if True, builds the initial config
        :return:
        """
        initial_config = None
        real_args = arguments if arguments is not None else []

        # check if actual arguments prevent from using the default .ini

        if self.get_val_from_cmdline_lower("--language", real_args) == 'fr':
            language = 'fr'
        elif self.get_val_from_cmdline_lower("--language", real_args) == 'en':
            language = "en"
        else:
            loc, _ = locale.getlocale()
            language = 'fr' if loc == 'fr_FR' else 'en'

        old_dir = os.getcwd()
        new_base = self.get_val_from_cmdline('--base', real_args)
        base_last = self.get_val_from_cmdline('--base-last', real_args)
        if new_base:
            if not os.path.isdir(new_base):
                if self.get_val_from_cmdline_lower('--enable-create-base', real_args) == 'true':
                    ACTOR.mkdirs(new_base, forced=True)
                else:
                    LOGGER.config_error(f"--base '{new_base}' : non existing dir and --enable-create-base false")
            LOGGER.msg(f"base '{new_base}'")
            os.chdir(new_base)
        elif base_last == "true":
            new_base = PwpConfig.guess_latest_base(self.get_val_from_cmdline('--home', real_args))
            if os.path.isdir(new_base):
                LOGGER.msg(f"base-last '{new_base}'")
                os.chdir(new_base)
            else:
                LOGGER.config_error(f"--base-last : last dir '{new_base}' does not exist ")

        new_home = self.get_val_from_cmdline('--home', real_args)
        if new_home:
            if not os.path.isdir(new_home):
                LOGGER.config_error(f"--home '{new_home}' : non existing directory")
                ACTOR.mkdirs(new_home)      # we get there ONLY if GUI, otherwise exit with error
            self.home = new_home
            LOGGER.msg(f"new home '{new_home}'")

        exit_after = False
        if '--help' in real_args:
            if language == 'en':
                self.print_help()
                # if we do exit(0) or raisePwpConfigError, (on program_3) on test 400, Paramiko exits on error!
                # msg is:  'ValueError: I/O operation on closed file'
                # this seems to be an issue with stdin, probably closed before Paramiko ends
                # Trick: We return None, so that the program is ended gracefully
                return None
            self.print_usage()
            self.print_fr()
            exit_after = True

        if '--full-help' in real_args:
            if language == 'en':
                self.print_usage()
                return None
            self.print_fr(full=True)
            exit_after = True

        if '--version' in real_args:
            version = PwpVersion()
            # LOGGER.msg(f"current version: '{version.help}' ")
            print(f"current version: '{version.help}'")
            exit_after = True

        if '--licence' in real_args:
            licence = PwpLicence()
            licence.print()
            exit_after = True

        if exit_after:
            os.chdir(old_dir)
            return None

        if '--quiet' not in real_args:
            LOGGER.start()

        if with_config:
            initial_config = self.build_initial_config(language=language)

        home_ini_path = ACTOR.normalise_path(self.home + '/.' + ini_to_parse)
        config = initial_config

        if with_config and os.path.isfile(home_ini_path):
            LOGGER.msg(f"{program}: reading configuration from HOME = {home_ini_path}")
            home_ini = PwpConfig.parse_ini_file(home_ini_path, previous=config)
            # if not ACTOR.is_mode_protected(home_ini_path):
            #    LOGGER.error(f"HOME ini file {home_ini_path} MUST be protected by chmod 0x600 o 0x400")
            # chmod has limited meaning in windows universe
            config = home_ini.merge_ini(initial_config)

        self.home_config = config

        if with_config and os.path.isfile(ini_to_parse):
            LOGGER.msg(f"{program}: reading configuration from BASE = {ini_to_parse}")
            first_ini = PwpConfig.parse_ini_file(ini_to_parse, previous=config)
            config = first_ini.merge_ini(config)

        checked_args = self.check_cmd_line(program, real_args)

        if with_config:
            config = config.merge_ini_args(checked_args, real_args)
        else:
            config = PwpConfig.args_to_dict(checked_args)

        return config

    def manage_cmdline_specials(self, new_config, real_args):
        new_base = self.get_val_from_cmdline('--base', real_args)
        if new_base:
            new_config['base'] = new_base

        new_home = self.get_val_from_cmdline('--home', real_args)
        if new_home:
            new_config['home'] = new_home
        return new_config

    def parse_for_dir(self, path, home: str, base: str, language, real_args):
        """
        gets the final config for this directory,
        taking into account defaults, HOME, BASE and cmdline options.

        read: default, HOME/.piwiPre.ini, BASE/piwiPre.ini, CMD-LINE, ... path/piwiPre.ini
        path MUST be a subdir of BASE (this must have been checked before)
        all paths are abspath()

        :param path:  where we may find a piwiPre.ini
        :param home: home, maybe changed with --home
        :param base: maybe changed with --base
        :param language:  en, etc.
        :param real_args: list of cmdline arguments
        :return: PwpConfig
        """
        # CAVEAT: This is mainly a re-write of parse_args_and_ini()
        #         which SHOULD be factorised in a shared code

        # ------------- DEFAULT
        initial_config = self.build_initial_config(language=language)
        ini_to_parse = 'piwiPre.ini'

        home_ini_path = ACTOR.normalise_path(home + '/.' + ini_to_parse)
        config = initial_config

        # ------------- HOME
        if os.path.isfile(home_ini_path):
            LOGGER.msg(f"GUI: reading configuration from HOME = {home_ini_path}")
            first_ini = PwpConfig.parse_ini_file(home_ini_path, previous=config)
            config = first_ini.merge_ini(config)

        config = self.manage_cmdline_specials(config, real_args)
        if path == home:
            return config

        # ------------- BASE
        base_ini_path = ACTOR.normalise_path(base + '/' + ini_to_parse)
        if os.path.isfile(base_ini_path):
            LOGGER.msg(f"GUI: reading configuration from BASE = {ini_to_parse}")
            base_ini = PwpConfig.parse_ini_file(base_ini_path, previous=config)
            config = base_ini.merge_ini(config)

        config = self.manage_cmdline_specials(config, real_args)
        if path == base:
            return config

        # ------------- CMD-LINE

        checked_args = self.check_cmd_line("GUI", real_args)
        config = config.merge_ini_args(checked_args, real_args)

        # ------------- Sub-Dirs
        # let's compute the route between base and path
        space = path[len(base):]
        way = space.split('\\' if platform.system() == "Windows" else '/')

        cp = base + '/'
        for inter in way:
            if inter != "":
                cp += inter
                base_ini_path = ACTOR.normalise_path(cp + '/' + ini_to_parse)
                if os.path.isfile(base_ini_path):
                    target_ini = PwpConfig.parse_ini_file(base_ini_path, previous=config)
                    config = target_ini.merge_ini(config)
                    config = self.manage_cmdline_specials(config, real_args)

        return config

# end of class PwpArgsIni


def args_ini_main(arguments):
    parser = PwpArgsIni()
    parser.add_header('Unified parser for .ini files and cmdline flags')
    parser.add_header('===============================================')
    parser.add_header('\nParameters when executing pwpArgsIni as a program\n')
    parser.add_item('build-ini-file',
                    help='builds the ini-file argument',
                    action='store_true',
                    location='args')
    parser.add_item('ini-file',
                    help='sets the ini-file to build',
                    action='store',
                    default="test.ini")
    parser.add_item('build-rst-file',
                    help='builds the rst-file argument',
                    action='store_true',
                    location='args')
    parser.add_item('rst-file',
                    help='sets the rst-file to build',
                    action='store',
                    default="test.rst")
    parser.add_item('dump-config',
                    help='dumps the configuration and exits',
                    action='store_true',
                    location='args')
    parser.add_item('auto-test',
                    help='performs the auto-test and exits',
                    action='store_true',
                    location='args')
    parser.add_item('full-help',
                    help='prints the help',
                    action='store_true',
                    location='args')

    # check if actual arguments ask for new configuration items just for test

    if '--auto-test' in arguments:
        # The following data is fake, just to test if args-ini works OK
        parser.add_header("""
#######################
Flags and configuration
#######################""")
        parser.add_header("""
File usage
==========

This file is the default configuration of piwiPre.

Unless stated otherwise, the  configuration items have a command line argument counterpart, 
with the same name, starting with -- .

The default value is given as an argument.

The configuration file uses the yaml syntax,
and uses pyYaml  to read/write the configuration file""")
        parser.add_item('version', help="Prints piwiPre version number and exits.",
                        action='store_true', location='args')

        parser.add_header("""
Management of directories
=========================""")

        parser.add_item('triage',
                        help='Sets the root directory for TRIAGE pictures to manage.',
                        action='store',
                        default='TRIAGE',
                        config="""
- value = 'directory': Sets the root directory for TRIAGE pictures to manage
- value = None: renaming  has already been done, so the TRIAGE directory is not processed
""")

        parser.add_item('month-name',
                        help='The name for each month, used to compute month_name.',
                        action='store',
                        pwp_type=PwpArgType.LIST,
                        default=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        location='config')

        parser.add_item('piwigo-thumbnails',
                        help='A dictionary if thumbnail specifications',
                        pwp_type=PwpArgType.DICT,
                        default={
                            "{f}-sq.jpg": {'width': 120, 'height': 120, 'crop': True},
                            "{f}-th.jpg": {'width': 144, 'height': 144, 'crop': False},
                            "{f}-me.jpg": {'width': 792, 'height': 594, 'crop': False},
                            "{f}-cu_e250.jpg": {'width': 250, 'height': 250, 'crop': True},
                        },
                        location='config')
        parser.add_item('dates',
                        help='A dictionary of dates corrections',
                        action='store',
                        pwp_type=PwpArgType.DICT,
                        default={},
                        location='config')
        parser.add_item('verify-album',
                        help='true/false/list of directories in ALBUMS to be processed ',
                        action='store',
                        pwp_type=PwpArgType.DIR,
                        default="")
        parser.add_item('process-rename',  # is used to test ambiguous arguments
                        help='Enables files renaming',
                        action='store',
                        choices=['true', 'false'],
                        default='false')
    # end of auto-test case
    config = parser.parse_args_and_ini("autotest", "test.ini", arguments)
    if config is None:
        # cmdline arguments say 'exit'
        return

    if config['build-rst-file'] or config['auto-test']:
        parser.build_rst(config['rst-file'] or "../results/test-result.rst")
    if config['build-ini-file'] or config['auto-test']:
        parser.write_ini_file("../results/test-result.ini")
    if config['auto-test']:
        pprint.pprint(config)
        pprint.pprint(config)
        parser.print_help()
        return
    if config['help']:
        parser.print_help()


# by default, --auto-test is launched from the tests/argsini directory  # noqa

if __name__ == "__main__":
    sys.exit(args_ini_main(sys.argv[1:]))
