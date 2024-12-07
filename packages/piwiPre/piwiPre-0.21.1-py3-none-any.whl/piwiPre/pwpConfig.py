# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import os
import datetime
import re
import socket
import time

# pip install pyyaml
import yaml
import yaml.parser

from piwiPre.pwpActor import ACTOR
from piwiPre.pwpErrors import LOGGER

# DONE: specifications are imported from code, not from doc
# DONE: parse also the list of possible values, so that we can do a verification


class PwpConfig(dict):
    format_dico = {
        'author': '{author}',
        'radical': '{radical}',
        'Y': '{Y:04}',
        'm': '{m:02}',
        'd': '{d:02}',
        'H': '{H:02}',
        'M': '{M:02}',
        'S': '{S:02}',
        'month_name': '{month_name}',
        'count': '{count:03}',
        'suffix': '{suffix}',
    }
    legal_items = None

    def __init__(self, content_str: str = None, filename: str = None,
                 dico=None,
                 previous: "PwpConfig" or None = None):
        super().__init__()
        LOGGER.msg(f"Reading configuration from '{filename}'")
        self.filename = filename
        self.previous = previous
        self.format_cached = {}
        self.origin = {}
        if content_str is not None:
            try:
                dico = yaml.safe_load(content_str)
            except yaml.parser.ParserError as error:
                error: yaml.parser.ParserError
                context = f"in file {filename}: line : {error.problem_mark.line}"
                msg = "Yaml parsing error : " + error.args[0] + ' ' + error.args[2]
                LOGGER.config_error(msg, context=context)

            # CAVEAT:
            # - when dico has been read from a string, (i.e. from a file)
            #   None means "", there was a declaration of the item, no value = empty
            # in other cases, None means None
            if dico is None:
                # This happens if there is a file, but empty, or just comments.
                dico = {}
            for key, value in dico.items():
                dico[key] = "" if value is None else value

        elif type(dico) is not dict:
            LOGGER.internal_error("illegal PwpConfig(dico) not a dict")

        if dico is None:
            dico = {}                 # pragma: no cover: defensive code

        dico['ini-filename-parsed'] = filename
        # postprocessing

        for key, value in dico.items():
            k = PwpConfig.normalize(key)
            self[k] = PwpConfig.normalize(value)
            self.origin[k] = filename

        if PwpConfig.legal_items is None:
            PwpConfig.legal_items = list(self.keys())   # better to do an explicit copy here

    def get_origin(self, name):
        if name not in self:
            return None
        return self.origin[name]

    def get_previous(self):
        return self.previous or self  # previous is None when self is for default values

    def get_previous_value(self, name):
        prev = self.get_previous()
        return prev[name] if name in prev else None

    def get_previous_origin(self, name):
        prev = self.get_previous()
        return prev.get_origin(name)

    def get_hierarchy(self):
        res = [] if self.previous is None else self.previous.get_hierarchy()
        res.append(self.filename)
        # CAVEAT: if HOME or BASE is not configured, it will not be in hierarchy, and we want it
        #         this will be done by the caller of get_hierarchy
        return res

    @staticmethod
    def normalize(val):
        if val == 'True' or val == 'true':
            return True
        if val == 'False' or val == 'false':
            return False
        if val == 'None' or val == 'none' or val is None:
            # the management of None -> "" is done before, only for parsed strings.
            return None

        if val is True or val is False:
            return val
        if val == '':
            return val
        if isinstance(val, str) and ((val[0] == "'" and val[-1] == "'") or (val[0] == '"' and val[-1] == '"')):
            return PwpConfig.normalize(val[1:-1])
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            if val[-1:] == '/':  # remove trailing / for ALL items.
                return PwpConfig.normalize(val[:-1])
            else:
                return val
        if isinstance(val, list):
            nl = [PwpConfig.normalize(x) for x in val]
            return nl
        if isinstance(val, dict):
            nd = {}
            for k, v in val.items():
                nd[PwpConfig.normalize(k)] = PwpConfig.normalize(v)
            return nd
        LOGGER.internal_error("Normalize illegal type")

    @staticmethod
    def parse_ini_file(filename, previous):
        filename = ACTOR.linux_path(filename)
        if not ACTOR.isfile(filename):
            return PwpConfig(content_str="", filename=filename, previous=previous)    # pragma: no cover: defensive code

        with ACTOR.open(filename, "r") as ini:
            content = ini.readlines()
        content_str = "".join(content)
        conf = PwpConfig(content_str=content_str, filename=ACTOR.linux_path(filename), previous=previous)
        legals = PwpConfig.legal_items
        for key, value in conf.items():
            if key not in legals:
                LOGGER.config_error(f"Illegal configuration item '{key} : {value}' in '{filename}'")
            conf[key] = None if value == 'None' else value
            conf.origin[key] = filename
        return conf

    def merge_ini(self, old, with_cmdline=False):
        LOGGER.debug(f"merging ini files '{old['ini-filename-parsed']}' and '{self['ini-filename-parsed']}'")
        for key in self.keys():
            if key not in old:
                if with_cmdline:
                    # argsparse has already filtered the arguments, so they are valid    # noqa
                    pass
                else:
                    # the old is the default, so it has all the keys.
                    LOGGER.config_error(f"ERROR: illegal key '{key}'")

        for key, value in old.items():
            if key not in self or self[key] is None:
                self[key] = value
                self.origin[key] = old.origin[key] if key in old.origin else "Internal"
                # Internal happens for tmp_dir
            # otherwise, we keep the new value.
        self.previous = old
        return self

    @staticmethod
    def args_to_dict(args):
        args_dict = vars(args)
        for key, value in args_dict.items():
            args_dict[key] = PwpConfig.normalize(value)
        return args_dict

    @staticmethod
    def args_to_dict_for_config(args):
        args_dict = vars(args)
        res = {}
        for key, value in args_dict.items():
            new_key = key.replace('_', '-')
            res[new_key] = PwpConfig.normalize(value)
        return res

    def merge_ini_args(self, args, arguments: list):
        """
        merges self and args
        :param args: arguments after parsing by argparse, takes default value into account
        :param arguments: argument list BEFORE parsing by argparse
        :return: self
        """
        LOGGER.debug("merging ini with cmdline args")

        args_dict = self.args_to_dict(args)

        for key, value in self.items():
            flag = key.replace('-', '_')
            expected = '--' + key
            if flag in args_dict and expected in arguments:
                # if key not in arguments, then args contains the default value
                # so the .ini file has higher priority
                self[key] = args_dict[flag]  # or value
                self.origin[key] = "cmdline"

        # manage items that are in args but not in config (aka self)
        for flag in args_dict.keys():
            key = flag.replace('_', '-')
            if key not in self:
                self[key] = args_dict[flag]
                self.origin[key] = "cmdline"
        return self

    def push_local_ini(self, filename):
        if ACTOR.isfile(filename):
            new_ini = PwpConfig.parse_ini_file(filename, previous=self)
            new_ini.merge_ini(self)
            return new_ini
        return self

    def author(self, apn, _date):
        author = 'Photographer'
        authors = self['authors']
        if apn in authors:
            author = authors[apn]
        elif 'DEFAULT' in authors:
            author = authors['DEFAULT']
        LOGGER.trace(f"apn '{apn}'  => author '{author}'")
        return author

    @staticmethod
    def absolute_date(photo_date: datetime, absolute: dict):

        absolute['hour'] = photo_date.hour if 'hour' not in absolute and photo_date else 0
        absolute['minute'] = photo_date.minute if 'minute' not in absolute and photo_date else 0
        absolute['second'] = photo_date.second if 'second' not in absolute and photo_date else 0

        LOGGER.debug(f"absolute-date {absolute}")
        abs_datetime = datetime.datetime(**absolute)
        return abs_datetime

    def fix_date(self, filename, photo_date, apn):
        all_dates = self['dates']
        if not isinstance(all_dates, dict):
            all_dates = {}                 # pragma: no cover: defensive code

        if photo_date is None:
            if 'NO-DATE' in all_dates:
                nd = all_dates['NO-DATE']
                if 'forced' in nd:
                    return self.absolute_date(photo_date, nd['forced'])
                LOGGER.config_error(f"'{filename}' NO-DATE statement without a 'forced: date'")

            LOGGER.debug(f"'{filename}' without a date and without a correction: "
                         "no NO-DATE valid statement")  # pragma: no cover: defensive code
            return None

        for key, descr in all_dates.items():
            if key == 'NO-DATE':
                continue
            start = datetime.datetime(**descr['start']) if 'start' in descr else None
            end = datetime.datetime(**descr['end']) if 'end' in descr else None

            found_apn = apn if apn in descr else 'default' if 'default' in descr else None
            if found_apn and (key == 'ALL' or (start and end and start <= photo_date <= end)):
                update = descr[found_apn]
                if 'delta' in update:
                    new_date = photo_date + datetime.timedelta(**update['delta'])
                    LOGGER.msg(f"DATE correction: {filename}:{apn} (delta) {photo_date} -> {new_date}")
                    return new_date
                if 'forced' in update:
                    nd = update['forced'].copy()
                    new_date = self.absolute_date(photo_date, nd)
                    LOGGER.msg(f"DATE correction: {filename}:{apn} (forced) {photo_date} -> {new_date}")
                    return new_date

                LOGGER.warning(f"date correction start:{start} end:{end} camera:{apn} " +
                               "without a delta or forced statement")  # pragma: no cover: defensive code

        return photo_date

    def format(self, field):
        if field not in self.format_cached:
            self.format_cached[field] = self[field].format(**self.format_dico)
        return self.format_cached[field]

    def format_dict(self, date, author, radical='', count=1, suffix='.jpg'):
        """
        :param date: inherited from the IPTC date of the picture.
        :param author: picture author from IPTC data
        :param radical: is the name of the TRIAGE folder where the picture was originally found.
        :param count:
        :param suffix: file suffix
        :return: the dictionary used to format a file or document
        """
        month = self['month-name']
        month_name = month[date.month-1]
        dico = {
            'author': author,
            'radical': radical,
            'Y': date.year,
            'm': date.month,
            'd': date.day,
            'H': date.hour,
            'M': date.minute,
            'S': date.second,
            'month_name': month_name,
            'count': count,
            'suffix': suffix,
        }
        return dico

    @staticmethod
    def guess_base_history(home: str):
        current_host = socket.gethostname()
        current_host = re.sub(r'\W+', "-", current_host)
        filename = f"{home}/.piwiPre.last.{current_host}"

        if ACTOR.isfile(filename):
            with open(filename, 'r', encoding='utf8') as f:
                history = f.readlines()
            stripped = []
            for line in history:
                stripped.append(line.rstrip())
            return stripped
        return []

    def get_base_history(self):
        home = ACTOR.normalise_path(self['home'])
        return PwpConfig.guess_base_history(home)

    @staticmethod
    def guess_latest_base(home: str):
        if home is None:
            home = os.path.expanduser('~')
        history = PwpConfig.guess_base_history(home)
        if len(history) > 0:
            return history[0]
        else:
            return None

    def get_latest_base(self):
        history = self.get_base_history()
        if len(history) > 0:
            return history[0]
        else:
            return None

    def save_base_history(self):
        base = ACTOR.linux_path(self['base'])
        home = ACTOR.linux_path(self['home'])
        current_host = socket.gethostname()
        current_host = re.sub(r'\W+', "-", current_host)
        filename = f"{home}/.piwiPre.last.{current_host}"

        olds = self.get_base_history()

        if ACTOR.isfile(filename):
            backup = time.strftime(f"{filename}.bak._%Y_%m_%d_%H-%Mh%S")
            ACTOR.copy(filename, backup)

        with open(filename, 'w', encoding='utf8') as f:
            f.write(f"{base}\n")
            for line in olds:
                if base != line:
                    f.write(f"{line}\n")
        LOGGER.trace(f"Saved last run location in {filename}")
