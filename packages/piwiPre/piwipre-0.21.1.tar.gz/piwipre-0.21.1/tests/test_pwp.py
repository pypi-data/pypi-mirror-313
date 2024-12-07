# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------
import socket
# ---------------------------------------------------------------------------------------------------------------
# test_pwp.py
# ---------------------------------------------------------------------------------------------------------------
# This test is intended to be run from piwiPre directory by invoking pytest,
# which will run all files of the form test_*.py or *_test.py in the current directory and its subdirectories.
#
# is called by tox
#
# can be called directly by running, from piwiPre root directory (where tox.ini is):
# prompt> python -I tests/test_pwp.py -n 0 # or other number...

# =============================================================================================================
# CAVEAT:
# =============================================================================================================
#         tox has issues with comodo antivirus when run from PyCharm Terminal window
#         To avoid this, run tox from a native terminal, not within PyCharm
#
#         The origin seems to be that PyCharm creates a temp script which is not assess correctly by comodo
# =============================================================================================================

import sys
import os
import argparse
import inspect
import re
import datetime
import getpass
import subprocess
import platform

from piwiPre.pwpGui import PwpGui

# be sure that the piwiPre version imported is the latest one...
sys.path = [os.path.dirname(os.path.dirname(os.path.realpath(__file__)))] + sys.path

from piwiPre.pwpActor import ACTOR
from piwiPre.pwpMain import pwp_main, pwp_run, pwp_init
from piwiPre.pwpErrors import LOGGER, PwpConfigException
from piwiPre.pwpArgsIni import args_ini_main
from piwiPre.pwpParser import pwp_parser_main
from piwiPre.pwpData import PwpJpg, PwpMp4
from piwiPre.pwpParser import PwpParser

from piwiPre.pwpInstaller import run_installer

from source.parse_requirements import run_requirements
from patcher import patcher_main


# --------------------------------------------------------------------------------
# test vectors
# --------------------------------------------------------------------------------


class PwpPattern:
    first_id = 0

    # Typical pattern:
    #  source "tests/sources/PICTURES/Armor-cup/20230617_110544-bis.jpg"
    #  in-source = "PICTURES/Armor-cup/20230617_110544-bis.jpg"
    #  triage "tests/results/TRIAGE/Armor-cup/Armor01.jpg"
    #  in-triage = "Armor-cup/Armor01.jpg"
    #  album

    def __init__(self, data: dict, cmdline: dict):
        """
        Builds a new pattern based on the data and config
        :param data:
            if in-triage is set, gives the triage location
            if no-auto-id is not set (which is the default), in-triage is computed

            in-album: path of the resulting file on the album
                if starts with /, is an absolute path and is kept
                else, is a path relative to config['album']

            in-thumbnails: likewise, for thumbnails

            may also hold jpg data: orientation, copyright, special

        :param cmdline: current cmdline for process, as a hash.
            holds:
            --album, --remote-album, --enable-remote-album,
            --thumbnails, --remote-thumbnails, --enable-remote-thumbnails
            extra data: piwigo-thumbnails, offset
        """

        self.in_source = ("tests/sources/" + data['in-source']) if 'in-source' in data else None
        self.in_triage = ("tests/results/TRIAGE/" + data['in-triage']) if 'in-triage' in data else None
        self.in_album = None
        self.in_database = None
        self.data = data
        self.thumbs = []
        self.remote_thumbs = []
        self.triage_info = f"TRIAGE/{data['in-triage']}" if 'in-triage' in data else None

        album = cmdline['--album'] if "--album" in cmdline else None
        remote_album = cmdline['--remote-album'] if "--remote-album" in cmdline else None
        thumbnails = cmdline['--thumbnails'] if '--thumbnails' in cmdline else None
        remote_thumbnails = cmdline['--remote-thumbnails'] if '--remote-thumbnails' in cmdline else None
        enable_remote_thumbnails = (cmdline['--enable-remote-thumbnails'] == 'true') if (
                '--enable-remote-thumbnails' in cmdline) else None

        offset = cmdline['offset'] if 'offset' in cmdline else ''
        if offset:
            album = (album + '/' + offset) if album else None
            remote_album = (remote_album + '/' + offset) if remote_album else None
            thumbnails = (thumbnails + '/' + offset) if thumbnails else None
            remote_thumbnails = (remote_thumbnails + '/' + offset) if remote_thumbnails else None

        enable_database = cmdline['--enable-database'] if '--enable-database' in cmdline else False

        do_in_remote = ('--remote-album' in cmdline and '--enable-remote-album' in cmdline
                        and cmdline['--remote-album'] and cmdline['--enable-remote-album'])

        self.album_info = f"{album}/{data['in-album']}" if 'in-album' in data else None

        self.in_remote_album = None

        if self.in_source:
            _, suffix = os.path.splitext(self.in_source)
        else:
            suffix = None

        if suffix == '.ini':
            self.in_triage = "tests/results/" + data['in-results']

        if self.in_triage is None and self.in_source is not None:
            m = re.match(r'tests/sources/[\w-]*/(.*)', self.in_source)
            if m:
                base = os.path.dirname(m.group(1))
                if base:
                    base += '/'
                if base:
                    self.in_triage = f"tests/results/TRIAGE/{base}Pattern-{PwpPattern.first_id}{suffix}"
                    PwpPattern.first_id += 1

        # --------------------------------------------
        if self.in_source and self.in_triage:
            if suffix == '.ini' and offset:
                LOGGER.test_msg(f"Copy {self.in_source} {self.in_triage} , with patch = {offset}")
                with ACTOR.open(self.in_source, 'r') as ins:
                    content = ins.readlines()
                ACTOR.mkdirs(os.path.dirname(self.in_triage))
                with ACTOR.open(self.in_triage, 'w') as outs:
                    for line in content:
                        line = line.replace("names: 'tmp/", f"names: '{offset}/")
                        line = line.replace("names: tmp/", f"names: {offset}/")
                        outs.write(line)
            else:
                LOGGER.test_msg(f"Copy {self.in_source} {self.in_triage}")
                ACTOR.copy(self.in_source, self.in_triage)
        # --------------------------------------------

        in_album = data['in-album'] if 'in-album' in data else None

        if not in_album:
            return

        if enable_database:
            self.in_database = ('/' + offset + '/' if offset else '') + in_album

        # we cannot guess in-album, because it involves renaming,
        assert in_album[0] != '/', "Internal: in_album absolute"
        # this is a relative path vs config['album']
        if album[0] == '/':
            # album is an absolute path, we keep it
            self.in_album = album + '/' + in_album
            if do_in_remote:
                self.in_remote_album = remote_album + '/' + in_album
        else:
            # this is a path relative to cwd, we restore cwd to 'tests/results'
            self.in_album = 'tests/results/' + album + '/' + in_album
            if do_in_remote:
                self.in_remote_album = 'tests/results/' + remote_album + '/' + in_album

        # now, compute the thumbnails:

        if thumbnails and 'piwigo-thumbnails' in cmdline:
            thumbs = cmdline['piwigo-thumbnails']
            if cmdline['--thumbnails'][0] == '/':
                # thumbnails is an absolute path, we keep it
                base = thumbnails + '/' + in_album[:-4]  # remove .jpg
            else:
                # this is a path relative to cwd, we restore cwd to 'tests/results'
                base = 'tests/results/' + thumbnails + '/' + in_album[:-4]

            remote_base = None
            if enable_remote_thumbnails and remote_thumbnails:
                remote_base = remote_thumbnails + '/' + in_album[:-4]

            _, album_suffix = os.path.splitext(in_album)
            if album_suffix == '.mp4':
                base = os.path.dirname(base) + '/pwg_representative/' + os.path.basename(base)
                if remote_base:
                    remote_base = os.path.dirname(remote_base) + '/pwg_representative/' + os.path.basename(remote_base)

            for name, values in thumbs.items():
                thumb_name = name.format(f=base)
                self.thumbs.append(thumb_name)
                if remote_base:
                    remote_thumb_name = name.format(f=remote_base)
                    self.remote_thumbs.append(remote_thumb_name)

            self.thumbs.append(os.path.dirname(base) + '/index.htm')
            if remote_base:
                self.remote_thumbs.append(os.path.dirname(remote_base) + '/index.htm')

    def find(self, dico: dict):
        for k, v in dico.items():
            if not getattr(self, k, None) == v:
                return False
        return True

    def check(self, tester: 'PwpTester', backup_prefix):
        def clamp(s):
            s = s or ''
            return f'{s[-40:]:40}'

        msg = f"check  src:'{clamp(self.in_source)}' triage:'{clamp(self.in_triage)}' album:'{clamp(self.in_album)}' ["

        if self.in_triage:
            tester.assert_file(self.in_triage)
            msg += "triage, "
            if 'TRIAGE' in self.in_triage:
                msg += "backup, "
                backup_path = self.in_triage.replace("TRIAGE", 'BACKUP/' + backup_prefix + "/TRIAGE")
                tester.assert_file(backup_path)

        if self.in_album:
            tester.assert_file(self.in_album)
            # tester.assert_info(f"RENAME: {self.triage_info} : {self.album_info}")  # noqa
            # CANNOT test systematically rename, because in multiple cases, there is a conflict and already present
            msg += "album] "
            _, suffix = os.path.splitext(self.in_album)

            if suffix == '.jpg':
                msg += "meta["
                with PwpJpg(self.in_album, config=tester.home_config) as jpg:
                    tester.assert_jpg_field(jpg, 'orientation', '1')
                    # 'pwg_representative' not in self.in_album:
                    tester.assert_in_jpg_field(jpg, 'copyright', '(C)')
                    # we cannot ALWAYS test 'special', because sometimes it is different
                    # so we will test it wit the loop just bellow
                    # tester.assert_special(jpg, 'No copy allowed unless explicitly approved by')

                    for item in ['author', 'copyright', 'special', 'creation', 'make', 'model',
                                 'size', 'width', 'height']:
                        if item in self.data:
                            if item == 'size':
                                tester.assert_jpg_size(jpg, item, self.data[item])
                            else:
                                tester.assert_jpg_field(jpg, item, self.data[item])
                            msg += f"{item}, "

            elif suffix == ".mp4":
                msg += "meta["
                with PwpMp4(self.in_album, config=tester.home_config) as mp4:
                    for item in ['author', 'copyright', 'special', 'creation', 'width', 'height']:
                        if item in self.data:
                            tester.assert_mp4_field(mp4, item, self.data[item])
                            msg += f"{item}, "

        msg += "] "
        if self.in_database:
            file_info = tester.assert_db_file(self.in_database)
            msg += "db["
            for item in ['width', 'height', 'md5sum', 'author', 'latitude', 'longitude']:
                if item in self.data:
                    tester.assert_db_file_field(self.in_database, file_info, item, self.data[item])
                    msg += f"{item}, "
            msg += "] "

        if self.in_triage and self.in_album and self.triage_info and self.album_info:
            tester.assert_trace_or([f"RENAME: '{self.triage_info}' : '{self.album_info}'",
                                   f"New file '{self.triage_info}' is already in album as '{self.album_info}'"])

        if len(self.remote_thumbs):
            msg += " Rem_Thumbs:["
            for item in self.remote_thumbs:
                tester.assert_remote_file(item)
                suf = item[-6:-4]
                if suf == "50":
                    suf = "cu"
                if suf == "ex":
                    suf = "htm"
                msg += suf + ", "
            msg += "]"
        else:
            if len(self.thumbs):
                msg += "Thumbs:["
            for item in self.thumbs:
                tester.assert_file(item)
                suf = item[-6:-4]
                if suf == "50":
                    suf = "cu"
                if suf == "ex":
                    suf = "htm"
                msg += suf + ", "
            msg += "]"

        LOGGER.test_msg(msg)


class PwpVector:
    def __init__(self, cmdline: dict, items: list[dict]):
        self.items = [PwpPattern(data=item, cmdline=cmdline) for item in items]
        self.cmdline = cmdline

    def add(self, items: list[dict]):
        for item in items:
            self.items.append(PwpPattern(data=item, cmdline=self.cmdline))
        return self

    def check(self, tester: 'PwpTester', backup_prefix):
        for item in self.items:
            item.check(tester, backup_prefix)

    def find(self, dico: dict):
        for item in self.items:
            if item.find(dico):
                return item
        return None


class PwpTester:
    def __init__(self):
        self.programs_done = {'program_0': False}
        self.programs = {'program_0': self.program_0}
        self.program_numbers = []
        self.run_file = "tests/sources/run.txt"
        self.asserts = 0
        self.start_time = datetime.datetime.now()
        self.files_processed = {}
        self.scenario = 0
        self.scenario_OK = 0

        parser = PwpParser(arguments=[], program="test_harness", with_config=True)
        self.home_config = parser.home_config

        self.vectors = {}

        members = inspect.getmembers(self)
        last = 0
        for m in members:
            r = re.match(r"program_\d+", m[0])
            if r and m[0] != 'program_0':
                name = m[0]
                number = int(name[8:])  # because we want them ordered
                last = max(number, last)
                self.programs_done[name] = False
                self.programs[name] = m[1]
                self.program_numbers.append(number)
        self.last = last
        self.program_numbers.sort()

    @staticmethod
    def get_unique_id():
        # chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.$&@~!,;+°()àâäéèêëïîôöùûüÿÀÂÄÉÈÊËÏÎÔÖÙÛÜŸ'  # noqa
        #                10        20        30        40        50        60        70        80
        chars = '-0123456789=@ABCDEFGHIJKLMNOPQRSTUVWXYZ_'  # noqa
        #                10        20        30        40   in ascii order

        # when we run the test,
        #     we generate an (old) directory which is unique during the next year
        # next time we run the test,
        #     we start by erasing that old directory,
        #     and create a new one using get_unique_id()
        # the new will be different from old, unless you run the same test exactly 1 year after, at 1/10 sec accuracy
        # So there is no race condition between the deletion of old and usage of new
        #
        # Why don't we simply read the name of the old directory and create a new one different,
        # for instance by incrementing a counter ?
        #
        # Because:
        # if the previous test was interrupted for some abnormal reason,
        # we may end-up with clean_remote_tmp() not executed
        # and we still have an ald tmp directory
        # if we restart the test, we want to read that old directory name,
        # maybe with a different protocol.
        # and now, we DO have a race condition.
        # e.g. in real-life:
        #   - we created old with sftp
        #   - we read with NFS
        #   - the windows NFS stack has issues: "access forbidden",
        #   - the only way is to reboot the windows client!

        stp = datetime.datetime.now()

        val = (stp.month * 31 * 24 * 60 * 60 * 10 +
               stp.day * 24 * 60 * 60 * 10 +
               stp.hour * 60 * 60 * 10 +
               stp.minute * 60 * 10 +
               stp.second * 10 +
               int(stp.microsecond / 100000))

        # max = 12 * 31 * 24 * 60 * 60 * 10 =  321 408 000
        # 40 * 40 * 40 * 40 * 40 * 40 = 4 096 000 000
        # so we can code the name using 6 chars, which is shorter than writing the traditional year-month etc...
        c1 = val % 40  # changes every  1/10 sec
        c2 = int(val / 40) % 40  # changes every  40/10 = 4 sec
        c3 = int(val / (40 * 40)) % 40  # changes every  (40*40)/(10*60) = 2.6 min
        c4 = int(val / (40 * 40 * 40)) % 40  # changes every  (40*40*40)/(10*60*60) = 1.8 hour
        c5 = int(val / (40 * 40 * 40 * 40)) % 40  # changes every  (40*40*40*40)/(10*60*60*24) = 2.9 day
        c6 = int(val / (40 * 40 * 40 * 40 * 40)) % 40  # changes every  (40*40*40*40*40)/(10*60*60*24) = 118 day

        return f"tmp/{chars[c6]}{chars[c5]}{chars[c4]}{chars[c3]}{chars[c2]}{chars[c1]}"

    def get_vector_uid(self, nb):
        if nb not in self.vectors:
            LOGGER.internal_error(f"wrong nb {nb}")
        offset = self.vectors[nb].cmdline['offset']
        LOGGER.test_msg(f"offset = {offset}")
        return offset

    def check(self, nb: int, backup_prefix, vector=None, after_verify_album=False):
        if vector:
            self.vectors[nb] = vector
        vector = self.vectors[nb]
        if after_verify_album:
            for pattern in vector.items:
                if pattern.triage_info:
                    pattern.triage_info = None
                    # means that we have not copied it from triage, so we will not test for RENAME
        self.vectors[nb].check(self, backup_prefix)

    @staticmethod
    def get_assert_context():
        previous_frame = inspect.currentframe().f_back.f_back
        (filename, line_number, _function_name, _lines, _index) = inspect.getframeinfo(previous_frame)
        context = f"'{filename}':{line_number:03}\n               "
        return context

    def assert_dir(self, dir_path: str):
        msg = f"{self.get_assert_context()} directory {dir_path} should exist"
        self.asserts += 1
        assert os.path.isdir(dir_path), msg

    def assert_no_dir(self, dir_path: str):
        msg = f"{self.get_assert_context()} directory {dir_path} should not exist"
        self.asserts += 1
        assert not os.path.isdir(dir_path), msg

    def assert_file(self, filepath: str):
        msg = f"{self.get_assert_context()} file {filepath} should exist"
        self.asserts += 1
        assert ACTOR.isfile(filepath), msg

    def assert_remote_file(self, filepath: str):
        msg = f"{self.get_assert_context()} remote file {filepath} should exist"
        self.asserts += 1
        assert ACTOR.remote_isfile(filepath, forced=True), msg  # forced = bypass --dryrun

    def assert_thumbnail(self, thumbnails, remote_thumbnails, filepath: str):
        if remote_thumbnails:
            self.assert_remote_file(remote_thumbnails + filepath)
        else:
            self.assert_file(thumbnails + filepath)

    def assert_no_file(self, filepath: str):
        msg = f"{self.get_assert_context()} file {filepath} should not exist"
        self.asserts += 1
        assert not ACTOR.isfile(filepath), msg

    def assert_no_remote_file(self, filepath: str):
        msg = f"{self.get_assert_context()} remote file {filepath} should not exist"
        self.asserts += 1
        assert not ACTOR.remote_isfile(filepath), msg

    def assert_file_contains(self, filepath: str, line: str):
        msg = f"{self.get_assert_context()} file {filepath} should exist"
        self.asserts += 1
        assert ACTOR.isfile(filepath), msg
        with open(filepath, 'r', encoding="utf-8") as f:
            lines = f.readlines()
        msg = f"{self.get_assert_context()} file {filepath} should contain '{line}'"
        for la in lines:
            if line in la:
                return
        assert False, msg

    def assert_file_not_contains(self, filepath: str, line: str):
        msg = f"{self.get_assert_context()} file {filepath} should exist"
        self.asserts += 1
        assert ACTOR.isfile(filepath), msg
        with open(filepath, 'r', encoding="utf-8") as f:
            lines = f.readlines()
        msg = f"{self.get_assert_context()} file {filepath} should not contain '{line}'"
        for la in lines:
            assert line not in la, msg

    def assert_config(self, config, item, value):
        msg = f"{self.get_assert_context()} config['{item}'] should be '{value}' and not '{str(config[item])}'"
        self.asserts += 1
        assert str(config[item]) == str(value), msg

    def assert_not_config(self, config, item, value):
        msg = f"{self.get_assert_context()} config[{item}] should not be '{value}'"
        self.asserts += 1
        assert str(config[item]) != str(value), msg

    def assert_error_number(self, level: str, err_nb: int):
        nb = LOGGER.test_msg_nb(level)
        msg = f"Line:{str(inspect.currentframe().f_lineno)}: {level}[{err_nb}] is not the max[{nb}]"
        self.asserts += 1
        assert nb == err_nb, msg

    def assert_error_contains(self, level: str, err_nb: int, start: str):
        nb = LOGGER.test_msg_nb(level)
        self.asserts += 1
        previous_frame = inspect.currentframe().f_back
        (filename, line_number, _function_name, _lines, _index) = inspect.getframeinfo(previous_frame)
        context = f"{filename}:{line_number:3}"
        msg = f"{context}: Error[{err_nb}] not reached"
        assert nb >= err_nb, msg
        if nb < err_nb:
            return
        err = LOGGER.data[level][err_nb]
        msg = f"{context}: Error[{err_nb}] '{err[:40]}' != '{start[:40]}' "
        assert start in err, msg

    def assert_trace(self, value: str):
        msg = f"{self.get_assert_context()} debug info log should contain <{value}>"
        self.asserts += 1
        all_info = LOGGER.data['trace']
        for err in all_info:
            if value in err:
                return
        assert False, msg

    def assert_trace_or(self, values: [str]):
        msg = f"{self.get_assert_context()} debug info log should contain <{values[0]}> or ..."
        self.asserts += 1
        all_info = LOGGER.data['trace']
        for err in all_info:
            for v in values:
                if v in err:
                    return True
        assert False, msg

    def assert_not_info(self, value: str):
        msg = f"{self.get_assert_context()} debug info log should contain '{value}'"
        self.asserts += 1
        for err in LOGGER.data['trace']:
            assert value not in err, msg

    def assert_jpg_size(self, jpg: PwpJpg, field: str, expected: str):
        # we do compare at 0.5 % to accommodate for small JPEG compression variations,
        # due to different compression algo depending on host , e.g. linux gitlab

        val = int(getattr(jpg, field))
        exp = int(expected)
        msg = f"{self.get_assert_context()} '{field}' of '{jpg.filename}' should be '{expected}' +/- 0.5 % not '{val}' "
        self.asserts += 1
        assert abs(val - exp) / exp < 0.005, msg

    def assert_jpg_field(self, jpg: PwpJpg, field: str, expected: str):
        val = getattr(jpg, field)
        msg = f"{self.get_assert_context()} '{field}' of '{jpg.filename}' should be '{expected}' not '{val}' "
        self.asserts += 1
        if expected is None or expected == "null":
            assert val is None or val == "null", msg
        else:
            assert expected == str(val), msg

    def assert_in_jpg_field(self, jpg: PwpJpg, field: str, expected: str):
        val = getattr(jpg, field)
        msg = f"{self.get_assert_context()} '{field}' of '{jpg.filename}' should contain '{expected}'"
        self.asserts += 1
        assert expected in str(val), msg

    def assert_jpg_no_field(self, jpg: PwpJpg, field: str, expected: str):
        val = getattr(jpg, field)
        msg = f"{self.get_assert_context()} '{field}' of '{jpg.filename}' should not be '{expected}' "
        self.asserts += 1
        if expected is None:
            assert val is not None, msg
        else:
            assert expected != str(val), msg

    def assert_author(self, jpg: PwpJpg, expected: str):
        val = jpg.author
        msg = f"{self.get_assert_context()} author '{val}' should contain '{expected}' "
        self.asserts += 1
        assert expected in str(val), msg

    def assert_picture_field(self, jpg: PwpJpg, field: str, expected: str):
        image = jpg.image
        val = getattr(image, field)
        msg = f"{self.get_assert_context()} '{field}' of '{jpg.filename}' should be '{expected}' not '{val}' "
        self.asserts += 1
        if expected is None or expected == "null":
            assert val is None or val == "null", msg
        else:
            assert expected == str(val), msg

    def assert_mp4_field(self, mp4: PwpMp4, field: str, expected: str):
        val = getattr(mp4, field)
        msg = f"{self.get_assert_context()} '{field}' of '{mp4.filename}' should be '{expected}' not '{val}' "
        self.asserts += 1
        if expected is None or expected == "null":
            assert val is None or val == "null", msg
        else:
            assert expected == str(val), msg

    def assert_no_copyright(self, jpg: PwpJpg, expected: str):
        val = jpg.copyright
        msg = f"{self.get_assert_context()} copyright '{val}' should not contain '{expected}' "
        self.asserts += 1
        assert expected not in str(val), msg

    def assert_special(self, jpg: PwpJpg, expected: str):
        val = jpg.special
        msg = f"{self.get_assert_context()} special instructions '{val}' should contain '{expected}' "
        self.asserts += 1
        assert expected in str(val), msg

    def assert_db_file(self, filename):
        msg = f"{self.get_assert_context()} sql_get_file_info('{filename}') should return a result"
        self.asserts += 1
        sql_file_info = ACTOR.sql_get_file_info(filename)
        assert sql_file_info is not None, msg
        return sql_file_info

    def assert_db_file_field(self, filename: str, sql_file_info, field: str, expected: str):
        msg = f"{self.get_assert_context()} sql_get_file_info('{filename}') should return a result"
        self.asserts += 1
        assert sql_file_info is not None, msg

        val = getattr(sql_file_info, field)
        msg = f"{self.get_assert_context()} '{field}' of '{filename}' should be '{expected}' not '{val}' "
        self.asserts += 1
        if expected is None or expected == "null":
            assert val is None or val == "null", msg
        else:
            assert expected == str(val), msg

    def assert_db_no_file(self, filename):
        sql_file_info = ACTOR.sql_get_file_info(filename)
        msg = f"{self.get_assert_context()} file '{filename}' should not be available in db got {sql_file_info}"
        self.asserts += 1
        assert sql_file_info is None, msg

    def assert_db_dir_field(self, dir_path, field, expected: str):
        sql_dir_info = ACTOR.sql_get_dir_info(dir_path)
        msg = f"{self.get_assert_context()}  dir '{dir_path}' should be in the db"
        self.asserts += 1
        assert sql_dir_info is not None, msg

        val = getattr(sql_dir_info, field)
        msg = f"{self.get_assert_context()} '{field}' of '{dir_path}' should be '{expected}' not '{val}' "
        self.asserts += 1
        if expected is None or expected == "null":
            assert val is None or val == "null", msg
        else:
            assert expected == str(val), msg

    def assert_db_no_dir(self, dir_path):
        sql_dir_info = ACTOR.sql_get_dir_info(dir_path)
        msg = f"{self.get_assert_context()} dir '{dir_path}' should not be available in db got {sql_dir_info}"
        self.asserts += 1
        assert sql_dir_info is None, msg

    def done(self, name, ok=True):
        ACTOR.mkdirs("tests/results")
        ACTOR.create(f"tests/results/{name}_done.txt")
        sys.stdout.flush()
        self.scenario += 1
        if ok:
            self.scenario_OK += 1

    def check_done(self, name: str, vector_nb: int = 0):
        if vector_nb and (vector_nb not in self.vectors or self.vectors[vector_nb] is None):
            return False

        return ACTOR.isfile(f"tests/results/{name}_done.txt")

    @staticmethod
    def reset_done(name: str):
        ACTOR.delete(f"tests/results/{name}_done.txt", forced=True)

    def reset_data(self):
        ACTOR.reset_data()
        old = LOGGER.reset_data()
        for k in old:
            self.files_processed[k] = old[k] + self.files_processed[k] if k in self.files_processed else 0

    @staticmethod
    def merge_dicts(origin, patch):  # noqa
        result = []
        for k in origin:
            result.append(k)
            result.append(patch[k] if k in patch else origin[k])
        for k in patch:
            if k not in origin:
                if k in ['offset', 'database', 'piwigo-thumbnails', 'result-album', 'result-thumbnails',
                         'set-thumbnails', 'result-auto-config', 'set-album', 'enable-database']:
                    pass  # another ugly patch to use the patch to convey the data
                else:
                    result.append(k)
                    result.append(patch[k])

        return result

    # We want to configure the test harness according to 3 types of configurations
    #   home: what is set in HOME, typically thumbnails/album may be mounted or remote
    #   local: force processing to be local
    #   remote: if HOME settings allow it, go remote, else go as HOME says
    #
    # Assumptions for HOME/.piwiPre.ini:
    #   if thumbnails can be mounted/synchronized:
    #       thumbnails : mount point
    #       remote-thumbnails : remote path
    #       enable-remote-thumbnails: false
    #   else:
    #       thumbnails : THUMBNAILS
    #       remote-thumbnails: remote-path
    #       enable-remote-thumbnails: true
    #   So that:
    #       by default, the home configuration occurs
    #       changing thumbnails and enable-remote-item performs a remote operation

    # set                   home                    local        remote             # noqa
    # ---------------------------------------------------------------------------
    # item                  home[item]              ITEM         ITEM
    # remote-item           home[remote-item]       None         home[remote-item]
    # enable-remote-item    home[enable-remote]     False        True

    def build_test_cmdline(self, cmdline: dict,
                           set_thumbnails='local',
                           set_album='local',
                           set_auto_config='local',
                           offset='',
                           enable_database=False):

        LOGGER.test_msg("build_cmdline")
        LOGGER.test_msg(f"{'set_thumbnails':19} : {set_thumbnails}")
        LOGGER.test_msg(f"{'set_album':19} : {set_album}")
        LOGGER.test_msg(f"{'set_auto_config':19} : {set_auto_config}")
        LOGGER.test_msg(f"{'offset':19} : '{offset}'")
        LOGGER.test_msg(f"{'enable_database':19} : {enable_database}")

        thumbnails = 'THUMBNAILS'
        remote_thumbnails = None
        enable_thumbnails = "false"
        if set_thumbnails == 'home':
            thumbnails = self.home_config['thumbnails']
            remote_thumbnails = self.home_config['remote-thumbnails']
            enable_thumbnails = self.home_config['enable-remote-thumbnails']
        elif set_thumbnails == 'local':
            # defaults values are already set
            if enable_database:
                LOGGER.internal_error("Cannot have database and local for thumbnails")
        elif set_thumbnails == 'remote':
            remote_thumbnails = self.home_config['remote-thumbnails']
            enable_thumbnails = "true"
        else:
            LOGGER.internal_error(f"set_thumbnails {set_thumbnails}")

        album = "ALBUM"
        remote_album = None
        enable_album = "false"
        if set_album == 'home':
            album = self.home_config['album']
            remote_album = self.home_config['remote-album']
            enable_album = self.home_config['enable-remote-album']
        elif set_album == 'local':
            # default values are already set
            if enable_database:
                LOGGER.internal_error("cannot have database and local for album")
        elif set_album == 'remote':  # aka remote
            remote_album = self.home_config['remote-album']
            enable_album = "true"
        else:
            LOGGER.internal_error(f"set_album {set_album}")

        auto_config = "AUTO-CONFIG"
        remote_auto_config = None
        enable_auto_config = "false"
        if set_auto_config == 'home':
            auto_config = self.home_config['auto-config']
            remote_auto_config = self.home_config['remote-auto-config']
            enable_auto_config = self.home_config['enable-remote-auto-config']
        elif set_auto_config == 'local':
            # default values are already set
            if enable_database:
                LOGGER.internal_error("cannot have database and local for auto_config")
        elif set_auto_config == 'remote':  # aka remote
            remote_auto_config = self.home_config['remote-auto-config']
            enable_auto_config = "true"
        else:
            LOGGER.internal_error(f"set_auto_config {set_auto_config}")

        if '--gui' not in cmdline:
            cmdline['--gui'] = 'false'
        if '--base' not in cmdline:
            cmdline['--base'] = 'tests/results'
        if '--thumbnails' not in cmdline:
            cmdline['--thumbnails'] = thumbnails
        if '--remote-thumbnails' not in cmdline:
            cmdline['--remote-thumbnails'] = remote_thumbnails
        if '--enable-remote-thumbnails' not in cmdline:
            cmdline['--enable-remote-thumbnails'] = enable_thumbnails
        if '--album' not in cmdline:
            cmdline['--album'] = album
        if '--remote-album' not in cmdline:
            cmdline['--remote-album'] = remote_album
        if '--enable-remote-album' not in cmdline:
            cmdline['--enable-remote-album'] = enable_album
        if '--auto-config' not in cmdline:
            cmdline['--auto-config'] = auto_config
        if '--remote-auto-config' not in cmdline:
            cmdline['--remote-auto-config'] = remote_auto_config
        if '--enable-remote-auto-config' not in cmdline:
            cmdline['--enable-remote-auto-config'] = enable_auto_config

        if enable_database:
            cmdline['--enable-database'] = 'true'

        LOGGER.test_msg("")
        for k, v in cmdline.items():
            LOGGER.test_msg(f"{k:19} : {v}")
        LOGGER.test_msg("")

        # now, items that are not used in the actual command-line of pwpMain,
        # but are used to convey values to build the vectors

        # album is a path relative to BASE, which was changed to 'tests/results'
        cmdline['result-album'] = ('tests/results/' if album[0] != '/' else '') + album
        # thumbnails is a path relative to BASE, which was changed to 'tests/results'
        cmdline['result-thumbnails'] = ('tests/results/' if thumbnails[0] != '/' else '') + thumbnails
        # auto-config is a path relative to BASE, which was changed to 'tests/results'
        cmdline['result-auto-config'] = ('tests/results/' if auto_config[0] != '/' else '') + auto_config

        cmdline['piwigo-thumbnails'] = self.home_config['piwigo-thumbnails']

        cmdline['set-thumbnails'] = set_thumbnails
        cmdline['set-album'] = set_album
        if enable_database:
            cmdline['enable-database'] = enable_database

        if offset:
            cmdline['offset'] = offset  # not --offset, to be sure it is removed before calling process

        return cmdline

    def database_synchronize(self, path):
        # CAVEAT: works ONLY in the configuration of HOME, so with its remote-thumbnails and remote-album config
        #         if a change has been done on these settings, use a different method
        # Do not use build_cmdline to keep it silent
        self.process({'--triage': None,
                      '--album': self.home_config['album'],
                      '--gui': 'false',
                      '--thumbnails': self.home_config['thumbnails'],
                      '--remote-thumbnails': self.home_config['remote-thumbnails'],
                      '--verify-album': path,
                      '--enable-thumbnails-delete': 'true',
                      '--enable-verify-sub-album': 'true',
                      '--enable-database': self.home_config['enable-database'],
                      '--enable-rename': 'false',
                      '--enable-remote-thumbnails': self.home_config['enable-remote-thumbnails'],
                      }, "Database Synchronize")

    @staticmethod
    def verify_local_album(path, enable_rename, time_stamp):
        LOGGER.test_msg(f'Verify local album {path}')
        # Do not use build_cmdline to keep it silent
        cmd_line = ['--triage', 'None',
                    '--gui', 'false',
                    '--base', 'tests/results',
                    '--album', 'ALBUM',
                    '--thumbnails', 'THUMBNAILS',
                    '--backup', 'BACKUP',
                    '--enable-verify-sub-album', 'true',
                    '--enable-database', 'false',  # mandatory, because we are not dealing with the real DB
                    '--enable-rename', enable_rename,
                    '--enable-thumbnails', 'true',
                    '--enable-metadata', 'true',
                    '--remote-thumbnails', None,
                    '--enable-remote-thumbnails', 'false',
                    '--remote-album', None,
                    '--enable-remote-album', 'false',
                    '--backup-test-stamp', time_stamp,
                    '--verify-album', path,
                    # '--debug',
                    # '--trace-malloc'
                    ]
        return pwp_main(cmd_line)

    def process(self, patch: dict, msg=''):
        LOGGER.test_msg(f"Processing {msg} {{")
        for k, v in patch.items():
            if k != 'piwigo-thumbnails':
                LOGGER.test_msg(f"    {k:20} : {v}")
        LOGGER.test_msg("}")
        LOGGER.test_msg("")

        # by default, for Triage
        cmdline = {'--base': 'tests/results',
                   '--triage': 'TRIAGE',
                   '--album': 'ALBUM',
                   '--thumbnails': 'THUMBNAILS',
                   '--backup': 'BACKUP',
                   '--enable-verify-sub-album': 'true',
                   '--enable-database': 'false',  # mandatory, because we are not dealing with the real DB
                   '--enable-rename': 'true',
                   '--enable-thumbnails': 'true',
                   '--enable-thumbnails-delete': 'true',
                   '--enable-metadata': 'true',
                   '--enable-auto-configuration': 'true',
                   '--enable-remote-thumbnails': 'false'}

        res = self.merge_dicts(cmdline, patch)
        main = pwp_main(res)
        return main

        # --------------------------------------------------------------------------------
        # Convention for the test harness:
        # --------------------------------------------------------------------------------
        #       -
        #       1) If thumbnails CAN be mounted AND is also accessible through SSH,
        #           Then :
        #               'remote-thumbnails' is set to the remote location
        #               'thumbnails' is set to the mount point
        #               'enable-remote-thumbnails' is set to false
        #           So, when we want to test SSH in the test harness, we can
        #               set enable-remote-thumbnails to True
        #               set thumbnails to 'thumbnails'
        #           Therefore, depending on tests, we may access to remote directories using NFS or SSH
        #       -
        #       2) If thumbnails CAN NOT be mounted and is accessible ONLY through SSH
        #           Then:
        #               'remote-thumbnails' is set to the remote location
        #               'thumbnails' is set to THUMBNAILS
        #               'enable-remote-thumbnails' is set to true
        #           Therefore, we access remote directories only with SSH
        #       -
        #       3) If thumbnails CAN be mounted and is NOT accessible through SSH
        #           Then:
        #               'remote-thumbnails' is set to None or ''
        #               'thumbnails' is set to the mount point
        #               'enable-remote-thumbnails' is set to false
        #           Therefore, we access to remote directories only with NFS
        #       -
        #       If none of these case is OK,
        #           Then thumbnails is not accessible, and we cannot test...
        #       -
        #       We can have race condition ONLY in the 1st case:
        #           we can use 2 protocols to remove/create files/directories: nfs and ssh
        #           the race condition occurs when we access to the remote directory with one protocol
        #           when it was created with the other protocol:
        #           nfs may be not coherent with the existence of the directory as seen on the remote host over ssh
        #           This leads to various protocol errors:
        #           - we try to erase a directory through NFS,
        #             but NFS is not yet aware of the existence of the directory
        #             so erasing fails : file not found, and the directory is still there
        #           - we try to erase a directory over NFS, but the directory aw already erased over ssh,
        #             and NFS still reports the directory existing
        #             when we erase, the NFS stack is in error, and generates "illegal access errors",
        #             the only known way to restore a stable state is to reboot the NFS client.
        #           - we read the /tmp content over NFS, and the presence of a directory is not known by NFS,
        #             when it does exist. So this directory is not detected and will not be erased
        #       -
        #       There are 3 scenario for race conditions:
        #           a) when the test is complete,
        #              clean by removing the 'old' remote-thumbnails/tmp/offset and remote-album/tmp/offset
        #              -
        #              we can avoid the race condition by deleting the directory with the protocol used to create it.
        #              as we have finished the test, we know the protocol
        #              -
        #           b) after removing the old directory,
        #              we will create again a 'new' directory
        #              and start a new test, that may use a different protocol
        #              -
        #              we can avoid the race condition by insuring that the new directory IS different from the old
        #              this is the purpose of get_unique_id()
        #              -
        #           c) after an abnormal stop of the test, we may have not cleaned, and an old directory may remain
        #              we could want to erase it immediately, leading to potential race condition
        #              -
        #              we can avoid the race condition by :
        #              - launching tests with old still present: there is no risk, since the directories
        #                have different names.
        #              - At the END of the test i.e. with clean_remote_tmp()
        #                read /tmp and delete any remaining directory
        #                We expect that the time between abnormal stop and clean_remote_tmp() is sufficient
        #                to avoid race conditions
        #

    def clean_remote_tmp(self, nb: int, delete=True):
        """
        clean_remote_tmp
            erases album/offset and thumbnails/offset
            the protocol used depends on set_album and set_thumbnails, i.e. on cmdline:
            if local: do nothing, the directory is in tests/results
            if home:
               when enable-remote-thumbnails is set, use ssh
               else use NFS
            if remote: use ssh

            use the protocol defined in home (enable-remote-thumbnails, enable-remote-album)
            If another directory is seen in album/tmp or thumbnails/tmp
            remove it using the protocol.

            if with_db, synchronise /tmp with the database to clean the database

        :param nb: nb of the test to clean
        :param delete: if True, deletes the vector
        :return: None
        """
        cmdline = {}
        if nb in self.vectors:
            cmdline = self.vectors[nb].cmdline
        else:
            LOGGER.internal_error(f"wrong test nb {nb}")

        ACTOR.reset_data()
        set_album = cmdline['set-album']
        set_thumbnails = cmdline['set-thumbnails']
        with_db = cmdline['enable-database'] if 'enable-database' in cmdline else False
        offset = cmdline['offset']
        assert offset != '' and offset is not None, f"illegal offset '{offset}'"

        LOGGER.test_msg("")
        LOGGER.test_msg(f"Clean tmp(set-album={set_album}, set-thumbnails={set_thumbnails}, "
                        f"enable-database={with_db}, offset={offset})")

        if ACTOR.isfile(self.run_file):
            ACTOR.delete(self.run_file)

        ACTOR.rmtree('tests/results')

        def remote_clean(path, off):
            all_items = ACTOR.remote_ls(path)
            for item in all_items.values():
                if item['type'] == 'dir' and item['dir_name'] != off:
                    abs_path = path + '/' + item['dir_name']
                    ACTOR.remote_rmtree(abs_path)
                    LOGGER.test_msg(f"Clean tmp: remote rmtree {abs_path}")

        def local_clean(path, off):
            if not os.path.isdir(path):
                return
            all_items = os.listdir(path)
            for item in all_items:
                abs_path = path + '/' + item
                if os.path.isdir(abs_path) and item != off:
                    ACTOR.rmtree(abs_path)
                    LOGGER.test_msg(f"Clean tmp: rmtree {abs_path} remaining")

        if (self.home_config['remote-thumbnails'] and
                (set_thumbnails == 'remote' or (set_thumbnails == 'home' and
                                                self.home_config['enable-remote-thumbnails']))):
            remote_thumbnails = self.home_config['remote-thumbnails'] + '/' + offset
            ACTOR.remote_rmtree(remote_thumbnails)
            LOGGER.test_msg(f"Clean tmp: remote rmtree {remote_thumbnails} remaining remote_thumbnails")

            remote_clean(self.home_config['remote-thumbnails'] + '/' + os.path.dirname(offset),
                         os.path.basename(offset))

        elif set_thumbnails == 'home':
            thumbnails = self.home_config['thumbnails'] + '/' + offset
            ACTOR.rmtree(thumbnails)
            LOGGER.test_msg(f"Clean tmp: rmtree {thumbnails} as thumbnails")

            local_clean(self.home_config['thumbnails'] + '/' + os.path.dirname(offset), os.path.basename(offset))
        # if local, do nothing

        album = self.home_config['album'] + '/' + offset

        if (self.home_config['remote-album'] and
                (set_album == 'remote' or (set_album == 'home' and self.home_config['enable-remote-album']))):
            remote_album = self.home_config['remote-album'] + '/' + offset
            ACTOR.remote_rmtree(remote_album)
            LOGGER.test_msg(f"Clean tmp: remote rmtree {remote_album} as remote_album")

            remote_clean(self.home_config['remote-album'] + '/' + os.path.dirname(offset), os.path.basename(offset))

        elif set_album == 'home':
            # and self.home_config['enable-remote-album'] is False
            ACTOR.rmtree(album)
            LOGGER.test_msg(f"Clean tmp: rmtree {album} as album")

            local_clean(self.home_config['album'] + '/' + os.path.dirname(offset), os.path.basename(offset))
        # if local, do nothing

        if with_db:
            ACTOR.copy("tests/sources/piwiPre-to-tmp.ini", "tests/results/piwiPre.ini")
            # --------------------------------
            self.database_synchronize(f"{self.home_config['album']}/tmp")
            # --------------------------------
        else:
            LOGGER.test_msg("Clean tmp: Skipping db synchronization")

        if delete:
            del self.vectors[nb]
            LOGGER.test_msg(f"Clean tmp: deleted vector {nb}")
        LOGGER.test_msg("Clean tmp: Done")
        LOGGER.test_msg("")

    @staticmethod
    def copy_armor(vector: PwpVector, name='Armor-cup', for_auto_conf=False):
        if for_auto_conf:
            dst_0 = "2023/06/17/Armor-cup-001.jpg"
            dst_1 = "2023/06/17/Armor-cup-002.jpg"
            copy_right = '(C) for autoconfig 2023'
        else:
            dst_0 = f"2023/2023-06-Juin-17-{name}/2023-06-17-11h05-44-{name}.jpg"  # noqa
            dst_1 = f"2023/2023-06-Juin-17-{name}/2023-06-17-11h05-45-{name}.jpg"  # noqa
            copy_right = "(C) 2023 by Agnes BATTINI, for test"

        return vector.add([
            {'in-source': "PICTURES/Armor-cup/20230617_110544-bis.jpg",
             'in-triage': f"{name}/Armor-0.jpg",
             # same metadata than 20230617_110544, but image is different because has been modified
             'in-album': dst_0,
             'md5sum': 'c5b83eee39ef237ab42a473b1139c540',  # previous: 'aa8fe00349ca160e8bf0f88f45f5cea7',
             'copyright': copy_right,
             'author': "Agnes BATTINI",
             'special': "No copy allowed unless explicitly approved by Agnes BATTINI",
             'creation': '2023-06-17 11:05:44',
             'make': 'samsung',
             'model': 'SM-A336B',
             'size': '830550' if for_auto_conf else '830562',
             },  # noqa
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-triage': f"{name}/Armor-1.jpg",
             'in-album': dst_1,
             'md5sum': '89aade70e5a7b883b3a6b0dfb64eaa8e',  # Previous: 'd181b3d94bb20487d4e9d6faa72b64a8',
             'copyright': copy_right,
             'author': "Agnes BATTINI"},  # noqa
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-triage': f"{name}/Armor-2.jpg",
             'in-album': dst_1,
             'author': "Agnes BATTINI"}])  # noqa

    @staticmethod
    def copy_corsica(vector: PwpVector, standard=True, for_auto_conf=False):
        if for_auto_conf:
            path1 = "2020/05/17/Corse-001.jpg"  # noqa
            path2 = "2021/08/18/Corse-001.jpg"  # noqa
            path3 = "2021/08/19/Corse-001.jpg"  # noqa
            path4 = "2021/08/19/Corse-002.jpg"  # noqa
        elif standard:
            path1 = "2020/2020-05-Mai-17-Corse/2020-05-17-12h00-00-Corse.jpg"  # noqa
            path2 = "2021/2021-08-Août-18-Corse/2021-08-18-12h00-00-Corse.jpg"  # noqa
            path3 = "2021/2021-08-Août-19-Corse/2021-08-19-12h04-00-Corse.jpg"  # noqa
            path4 = "2021/2021-08-Août-19-Corse/2021-08-19-12h04-01-Corse.jpg"  # noqa
        else:  # alternative names
            path1 = "Corsica/2020-05-17-12h00-00-Corsica.jpg"
            path2 = "Corsica/2021-08-18-12h00-00-Corsica.jpg"
            path3 = "Corsica/2021-08-19-12h04-00-Corsica.jpg"
            path4 = "Corsica/2021-08-19-12h04-01-Corsica.jpg"

        return vector.add([
            {'in-source': "PICTURES/Corse/IMG-20200517-WA0000.jpg",  # noqa
             'in-triage': "Corse/IMG-20200517-WA0000.jpg",  # noqa
             'in-album': path1,
             'author': 'Famille BATTINI'},  # noqa

            {'in-source': "PICTURES/Corse/IMG-20210818-WA0000.jpg",  # noqa
             'in-triage': "Corse/IMG-20210818-WA0000.jpg",  # noqa
             'in-album': path2,
             'author': 'Famille BATTINI'},  # noqa

            {'in-source': "PICTURES/Corse/IMG-20210819-WA0004 - Modified.jpg",  # noqa
             'in-triage': "Corse/IMG-20210819-WA0004 - Modified.jpg",  # noqa
             'in-album': path3,
             'author': 'Famille BATTINI'},  # noqa

            {'in-source': "PICTURES/Corse/IMG-20210819-WA0004.jpg",  # noqa
             'in-triage': "Corse/IMG-20210819-WA0004.jpg",  # noqa
             'in-album': path4,
             'author': 'Famille BATTINI'},  # noqa
        ])

    @staticmethod
    def copy_forest(vector: PwpVector):
        return vector.add([
            {'in-source': "PICTURES/Forêt-de-la-Corbière/20230611_162816.jpg",  # noqa
             'in-triage': "Forêt-de-la-Corbière/Foret01.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg",  # noqa
             # noqa
             'orientation': '1',
             'copyright': "(C) 2023 by Agnes BATTINI, for test",  # noqa
             'author': "Agnes BATTINI",
             'special': "No copy allowed unless explicitly approved by Agnes BATTINI",
             "latitude": "48.139922",
             "longitude": "-1.373026"},  # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/2023-06-11-17h02-40-Forêt-de-la-Corbière.png",  # noqa
             'in-triage': "Forêt-de-la-Corbière/2023-06-11-17h02-40-Forêt-de-la-Corbière.png",  # noqa
             # here, we keep the filename to get the information
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-17h02-40-Forêt-de-la-Corbière.jpg",  # noqa
             # noqa
             'author': "Famille BATTINI",
             'special': "No copy allowed unless explicitly approved by Famille BATTINI",
             'orientation': '1',
             'copyright': "(C) 2023 by Famille BATTINI, for test"},

            {'in-source': "PICTURES/Forêt-de-la-Corbière/20230611_170225.jpg",  # noqa
             'in-triage': "Forêt-de-la-Corbière/Foret02.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-17h02-25-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/20230611_162803.jpg",  # noqa
             'in-triage': "Forêt-de-la-Corbière/Foret03.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h28-04-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/20230611_162811.jpg",  # noqa
             'in-triage': "Forêt-de-la-Corbière/Foret04.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h28-11-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/20230611_170215.jpg",  # noqa
             'in-triage': "Forêt-de-la-Corbière/Foret05.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-17h02-16-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/IMG20230611162736.jpg",  # noqa
             'in-triage': "Forêt-de-la-Corbière/Foret06.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa
        ])

    @staticmethod
    def copy_video(vector: PwpVector):
        return vector.add([
            {'in-source': "VIDEO/Opéra-Paris.mp4",
             'in-triage': "test/sample-mp4.mp4",
             'in-album': '2023/2023-01-Janvier-27-test/2023-01-27-17h59-39-test.mp4',  # noqa
             'copyright': "(C) 2023 by Famille BATTINI, for test",  # noqa
             'author': "Famille BATTINI",
             'special': "No copy allowed unless explicitly approved by Famille BATTINI",
             "representative_ext": "jpg",
             "width": "1080",
             "height": "1920",
             'creation': '2023-01-27 17:59:39'},

            {'in-album': "2023/2023-01-Janvier-27-test/pwg_representative/2023-01-27-17h59-39-test.jpg",
             "width": "1080",
             "height": "1920",
             'author': "Famille BATTINI",
             'copyright': "(C) 2023 by Famille BATTINI, for test",  # noqa
             "representative_ext": "NULL"},

            {'in-source': "VIDEO/sample.avi",
             'in-triage': "test/sample-avi.avi",
             'in-album': '2007/2007-04-Avril-03-test/2007-04-03-18h04-24-test.mp4',
             'copyright': "(C) 2007 by Famille BATTINI, for test",  # noqa
             "representative_ext": "jpg",
             'author': "Famille BATTINI",
             'special': "No copy allowed unless explicitly approved by Famille BATTINI",
             'creation': '2007-04-03 18:04:24',
             "width": "320",
             "height": "240"},

            {'in-album': "2007/2007-04-Avril-03-test/pwg_representative/2007-04-03-18h04-24-test.jpg",
             "width": "320",
             "height": "240",
             'author': "Famille BATTINI",
             'copyright': "(C) 2007 by Famille BATTINI, for test",  # noqa
             "representative_ext": "NULL"}])

    # ================================================================================
    # Starting tests
    # ================================================================================

    # --------------------------------------- Testing cmd line flags and configuration

    def program_1(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('testing base, dump-config')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results/home")
        ACTOR.mkdirs("tests/results/TRIAGE/Armor")

        LOGGER.test_msg('')
        LOGGER.test_msg('we want to set up the following hierarchy')
        LOGGER.test_msg('HOME = tests/results/home : .piwiPre.ini = piwiPre-local.ini')
        LOGGER.test_msg('BASE =  tests/results      : piwiPre-fake.ini')
        LOGGER.test_msg('BASE/TRIAGE:                 reset to default')
        LOGGER.test_msg('BASE/TRIAGE/Armor:           piwiPre-alt-Armor.ini')

        # CAVEAT: on Linux, case of directory names is meaningful
        #         So, we better use 'home' rather than 'HOME'

        ACTOR.copy('tests/sources/piwiPre-local.ini', "tests/results/home/.piwiPre.ini")
        ACTOR.copy('tests/sources/piwiPre-fake.ini', "tests/results/piwiPre.ini")
        ACTOR.copy('tests/sources/piwiPre-alt-Armor.ini', "tests/results/TRIAGE/Armor/piwiPre.ini")

        # -----------------------------------------------------------------
        LOGGER.test_msg('')
        LOGGER.test_msg('Step 1: Call Configurator to setup a local setup in tests/results')
        LOGGER.test_msg('')
        cwd = os.getcwd()
        pwp_main(arguments=['--quiet', 'true',
                            '--gui', False,
                            '--home', 'home',  # executed AFTER --base, so should end-up in test/results/HOME
                            '--base', 'tests/results', ],
                 test_scenario=[("album-setup", 'local'),
                                ("thumbnails-setup", 'local'),
                                ("set album", "ALBUM"),
                                ("set thumbnails", 'THUMBNAILS'),
                                ("save", ),
                                ("exit", ), ])
        os.chdir(cwd)

        # -----------------------------------------------------------------

        LOGGER.test_msg('')
        LOGGER.test_msg('Step 2: Use dump-config to verify the generated piwiPre.ini')
        LOGGER.test_msg('')

        main = pwp_init(['--base', 'tests/results',
                         '--triage', 'TRIAGE',
                         '--home', 'home',  # executed AFTER --base, so should end-up in test/results/HOME
                         '--gui', 'false',
                         '--dump-config', 'TRIAGE/Armor'])  # , '--debug'])
        pwp_run(main)

        armor_conf = main.dumped_config

        # album is written by cwd/piwiPre.ini and reset in cwd/TRIAGE
        self.assert_config(armor_conf, 'album', 'ALBUM')
        self.assert_config(armor_conf, 'names', '{Y}/{m}/{d}/{radical}-{count}.{suffix}')

        # sql-user should be set in cwd/TRIAGE, but overwritten by cwd/TRIAGE/Armor
        self.assert_config(armor_conf, 'sql-user', 'unknown-user')
        self.assert_config(armor_conf, 'ssh-user', '')

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_2(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg('testing --licence etc')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')

        ACTOR.rmtree("tests/results")
        ACTOR.copy('tests/sources/piwiPre-local.ini', "tests/results/piwiPre.ini")

        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--licence',
                  '--version',
                  '--language', 'en'])
        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--licence',
                  '--version',
                  '--language', 'fr'])

        # PwpLicence.print()
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        # verify visual output, mainly to get coverage higher
        self.done(mn)

    def program_3(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        ACTOR.mkdirs('tests/results')
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('testing  --help')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')
        LOGGER.test_msg('')
        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--help',
                  '--full-help',
                  '--language', 'en'])

        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--help',
                  '--full-help',
                  '--language', 'fr'])
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_4(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg('')
        LOGGER.test_msg('testing management of piwiPre.ini file and --home')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')

        ACTOR.rmtree("tests/results")

        cmdline = self.build_test_cmdline({'--album': "LOCAL-ALBUM",
                                           '--thumbnails': 'LOCAL-THUMBNAILS',
                                           '--language': 'en'})
        # we use cmdline to set the appropriate destination folders in the vector
        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-alt-Armor.ini", 'in-results': "TRIAGE/Armor-cup/piwiPre.ini"},
            {'in-source': "piwiPre-alt.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "PICTURES/Armor-cup/20230617_110544-bis.jpg",
             'in-album': '2023/2023-08-Aug-30-Armor-cup/2023-08-30-11h05-44-Armor-cup.jpg'},
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-album': "2023/2023-08-Aug-30-Armor-cup/2023-08-30-11h05-45-Armor-cup.jpg"},
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-album': "2023/2023-08-Aug-30-Armor-cup/2023-08-30-11h05-45-Armor-cup.jpg"},
            {'in-source': "PICTURES/Armor-cup/20230617_111349-new.jpg",
             'in-album': "2023/2023-08-Aug-30-Armor-cup/2023-08-30-11h13-50-Armor-cup.jpg"},
            {'in-source': "PICTURES/Armor-cup/20230617_113128-new.jpg",
             'in-album': "2023/2023-08-Aug-30-Armor-cup/2023-08-30-11h31-28-Armor-cup.jpg"},
        ])

        # ----------------------------------------------------------------

        # CAVEAT: we do NOT use cmdline, because
        #  - we want to check that LOCAL-ALBUM and LOCAL-THUMBNAILS are read from .ini
        #  - and we use cmdline ONLY to build the test vector
        main = pwp_main(['--base', 'tests/results',
                         '--gui', 'false',
                         '--home', '.',
                         '--language', 'en',
                         '--triage', 'TRIAGE',
                         '--enable-database', 'false',  # mandatory, because we are not dealing with the real DB
                         '--enable-rename', 'true',
                         '--enable-thumbnails', 'true',
                         '--enable-metadata', 'true',
                         '--enable-remote-thumbnails', 'false'])
        config = main.parser_config

        # Caveat: cannot use triage_local_album, because --album would be on the command line
        # hence not changed by piwiPre-alt.ini
        # ----------------------------------------------------------------

        # let's verify the .ini has been used, even in subdirectories.
        # the album and thumbnails changes are in cwd
        # the date change is in Armor-cup

        vector.check(self, main.start_time)
        self.assert_config(config, 'album', 'LOCAL-ALBUM')
        self.assert_config(config, 'sql-user', 'Foo')
        self.assert_no_file('tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                            '2023-06-11-17h02-26-Forêt-de-la-Corbière.jpg')  # noqa
        self.assert_no_file('tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                            '2023-06-11-17h02-26-Forêt-de-la-Corbière.jpg')  # noqa

        LOGGER.test_msg(f"BASE  = '{os.getcwd()}' ")

        self.assert_dir('tests/results')  # noqa
        self.assert_dir('tests/results/LOCAL-ALBUM')  # noqa
        self.assert_dir('tests/results/LOCAL-ALBUM/2023')  # noqa
        self.assert_dir('tests/results/LOCAL-ALBUM/2023/2023-08-Aug-30-Armor-cup')  # noqa

        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def program_5(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        cwd = os.getcwd()
        ACTOR.mkdirs('tests/results')
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('testing  --help --language fr')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')
        LOGGER.test_msg('')
        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--help',
                  '--language', 'fr'])
        LOGGER.test_msg('')
        LOGGER.test_msg('')
        os.chdir(cwd)
        LOGGER.test_msg('----- full-help:')
        LOGGER.test_msg('')
        pwp_main(['--base', 'tests/results', '--gui', 'false',
                  '--full-help',
                  '--language', 'fr'])
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_6(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function

        # WTF ? 'what' fails on Linux !
        # what = "where" if platform.system() == "Windows" else "what"
        # res = subprocess.run([what, "python"], capture_output=True, text=True)
        # LOGGER.msg(f"Python = '{res}'")

        # HACK.
        # -----
        # For windows, if we do NOT have shell=True in next line,
        # then a different python is started,
        # without mariadb installed and the test fails.
        # BUT, on Linux, adding shell=True makes the test fail on gitlab pipeline
        #
        shell = platform.system() == "Windows"
        res = subprocess.run(["python", "-m", "piwiPre", "--version", ],
                             capture_output=True, text=True, shell=shell)  # noqa
        # current version: '0.17 at 03/30/2024 18:32:06'
        m = re.search(r".*current version: '(.*)'", res.stdout)
        assert m is not None, f"piwiPre --version generated a bad output '{res.stdout}'"
        LOGGER.test_msg(f"Read version = '{m.group(1)}'")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_7(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg('')
        LOGGER.test_msg('Verify --language en is taken into account for months on a french host')
        LOGGER.test_msg('uses a purely local configuration in tests/results, with empty HOME')
        LOGGER.test_msg('')

        initial_cwd = os.getcwd()
        ACTOR.rmtree("tests/results")

        ACTOR.mkdirs("tests/results/HOME")
        ACTOR.mkdirs("tests/results/BASE")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('test RUN from the UI with empty BASE, empty HOME, no thumbnails ')

        cmdline = self.build_test_cmdline({
            '--language': 'en',
            '--gui': 'false',
            '--base': initial_cwd + "/tests/results/BASE",
            '--home': initial_cwd + "/tests/results/HOME",
        })

        # The same test as program_30
        # without any .ini
        # and we change the values on the command-line :
        vector = PwpVector(cmdline, [])
        self.copy_armor(vector)

        # patching vector to get TRIAGE in BASE
        ACTOR.move(initial_cwd + "/tests/results/TRIAGE",
                   initial_cwd + "/tests/results/BASE/TRIAGE")
        for vect in vector.items:
            vect.in_triage = vect.in_triage.replace("TRIAGE", "BASE/TRIAGE")
            vect.in_album = vect.in_album.replace("ALBUM", "BASE/ALBUM")
            vect.in_album = vect.in_album.replace("Juin", "Jun")
            vect.album_info = vect.album_info.replace("Juin", "Jun")
            if "author" in vect.data:
                del vect.data["author"]
            if "copyright" in vect.data:
                del vect.data["copyright"]
            if "special" in vect.data:
                del vect.data["special"]
            if "size" in vect.data:
                del vect.data["size"]
            vect.thumbs = []

        # ----------------------------------------------------
        main = self.process(cmdline)
        # ----------------------------------------------------

        # --------------------------------
        # check will verify the pictures are computed, but we do not do fully the test
        self.check(910, main.start_time, vector)
        self.assert_dir("tests/results/BASE/BACKUP")
        self.assert_dir("tests/results/BASE/THUMBNAILS")     # we said thumbnails = unused

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_10(self):
        initial_cwd = os.getcwd()
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('autotest of ArgsIni')
        LOGGER.test_msg('uses a purely local configuration in tests/argsini')  # noqa
        LOGGER.test_msg('')

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        ACTOR.copy('tests/argsini/tests.ini', "tests/results/test.ini")  # noqa

        os.chdir('tests/results')  # noqa
        args_ini_main(['--auto-test',
                       '--triage', None,
                       '--verify-album', 'ALBUM/toto'])
        args_ini_main(['--auto-test',
                       '--triage', None,
                       '--verify-album', 'ALBUM/fifi'])
        self.assert_file("test.rst")
        self.assert_file("test.ini")

        args_ini_main(['--help', '--full-help'])

        ACTOR.delete("test.ini")
        ACTOR.delete("test.rst")
        os.chdir(initial_cwd)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_11(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('autotest of pwpPatcher')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        # this test must be executed, like pwpPatcher, from piwPre root
        patcher_main(['--autotest'])
        self.assert_file_contains('tests/results/pwpLicence.py', 'EUROPEAN UNION PUBLIC LICENCE')
        self.assert_file_contains('tests/results/pwpVersion.py', 'class PwpVersion:')
        self.assert_file('tests/results/version.txt')
        self.assert_file('tests/results/pwpLogoSmall.py')
        self.assert_file_contains('tests/results/configuration.rst', '**enable-rotation** : ``true``')
        self.assert_file_contains('tests/results/configuration_fr.rst', '**enable-rotation** : ``true``')
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def get_first_album(self, default="2023/2023-01-Janvier-08-Ballade"):  # noqa
        LOGGER.test_msg('')
        LOGGER.test_msg(f'if run by the developer, will verify album {default}')  # noqa
        LOGGER.test_msg("if run in a different context, will run the first sub-album in album")
        LOGGER.test_msg("If no sql connection, will abort")
        LOGGER.test_msg('')

        if ACTOR.sql_connection is None:
            LOGGER.test_msg("No sql connection, aborting")
            return None
        album = self.home_config['album']
        if os.path.isdir(album) and os.path.isdir(album + '/' + default):
            return default  # noqa

        if not os.path.isdir(album):
            return None

        all_files = os.listdir(album)
        for it in all_files:
            if os.path.isdir(album + '/' + it):
                return it
        return None

    def program_12(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('autotest of piwigo database access')
        LOGGER.test_msg('')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('if there are not database access, will generate a message')
        LOGGER.test_msg('relies on database information from HOME/.piwiPre.ini')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        ACTOR.configure(self.home_config)  # enable db access for the test harness

        pwp_main(['--base', 'tests/results', '--gui', 'false',
                  '--enable-database', 'true',
                  '--test-sql'])

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_13(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('autotest of PwpParser')
        LOGGER.test_msg('uses a purely local configuration in tests/argsini')  # noqa
        LOGGER.test_msg('')

        os.chdir('tests/argsini')  # noqa
        pwp_parser_main([])
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        ACTOR.mkdirs('tests/results')
        self.done(mn)

    def program_15(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('Tests Error generation')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')
        seen = False

        try:
            pwp_main(['--gui', 'false',
                      '--base',
                      '--debug', 'true'])
        except PwpConfigException:
            seen = True
        assert seen, f"{mn} should have generated a PwpConfigError"
        LOGGER.test_msg("This program has correctly generated 'ERROR   --base '--debug' : non existing directory'")
        LOGGER.test_msg(f'--------------- end of  {mn}')

        # test if  chdir to --debug has not been done
        cur_dir = os.path.basename(os.getcwd())
        assert cur_dir != "--debug", "'--debug' should not exist"
        self.done(mn)

    def program_16(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('autotest of parse_requirements')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')

        run_requirements([])
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_17(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('tests error generation in parse_requirements')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('')

        ACTOR.copy("tests/sources/piwiPre-error.ini", "tests/results/piwiPre.ini")
        initial_cwd = os.getcwd()

        done = False
        try:
            main = pwp_init(['--base', 'tests/results'])
            pwp_run(main)
        except PwpConfigException:
            done = True
            LOGGER.test_msg("Correctly generated 'ERROR Illegal configuration item'")
            os.chdir(initial_cwd)  # otherwise self.done does not work

        assert done, f"{mn}  should have generated an error"

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_18(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('Tests Error generation with a wrong album-name')
        LOGGER.test_msg('uses a purely local configuration in tests/results')
        LOGGER.test_msg('Requires a database connection, or will abort')

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        # Remainder: we must NOT do this here ACTOR.configure(self.home_config)
        # otherwise ACTOR will not take into account the piwigo-album-name manually added

        seen = False
        # we need to reset ACTOR database connection potentially set by previous tests
        if ACTOR.sql_connection:
            ACTOR.sql_connection.close()
            ACTOR.sql_connection = None
        try:
            pwp_main(['--base', 'tests/results',
                      '--gui', 'false',
                      '--piwigo-album-name', 'This-album-name-is-wrong',
                      '--test-sql'])
        except PwpConfigException:
            seen = True

        if not ACTOR.sql_connection:
            LOGGER.test_msg("No SQL connection available, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        ACTOR.sql_connection.close()
        ACTOR.sql_connection = None  # avoid the propagation of bad sql_connection to other tests
        ACTOR.sql_first_album = None  # avoid the propagation of bad sql_first_album to other tests

        assert seen, f"{mn} should have generated a PwpConfigError"
        LOGGER.test_msg('The following errors have been correctly generated above:')
        LOGGER.test_msg("      ERROR   Cmd-line/configuration")
        LOGGER.test_msg("      ERROR   album-name argument 'This-album-name-is-wrong' is not known in piwigo database")

        LOGGER.test_msg(f'--------------- end of {mn}')
        self.done(mn)

    # =====================================================================================================
    # ==================================  30 : Starting tests for TRIAGE Stage, with local ALBUM

    def program_30(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS')
        LOGGER.test_msg('')
        LOGGER.test_msg('Verifies renaming, copyright, author, special, rotation')
        LOGGER.test_msg('with .jpg, .jpg + GPS, png')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        cmdline = self.build_test_cmdline({'--language': 'fr',
                                           "--backup-test-stamp": "program-30-start-time"})  # purely local

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-local.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "GPS/2023-02-19-11h38-23-Plouhinec.jpg",  # noqa
             'in-triage': "test/picture-with-gps.jpg",
             'in-album': "2023/2023-02-Février-19-test/2023-02-19-11h38-23-test.jpg",  # noqa
             'md5sum': '5021904b830ccca656c32410edc3acc0',
             "latitude": "47.988561",
             "longitude": "-4.478702",
             'orientation': '1'}])

        self.copy_armor(vector)
        self.copy_corsica(vector)
        self.copy_forest(vector)

        # --------------------------------
        self.process(cmdline)
        # --------------------------------

        self.check(30, "program-30-start-time", vector)

        # verifying that the thumbnails also have metadata
        with PwpJpg('tests/results/THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup-me.jpg',
                    # noqa
                    config=self.home_config) as jpg:
            self.assert_jpg_field(jpg, 'copyright', "(C) 2023 by Agnes BATTINI, for test")  # noqa
            self.assert_author(jpg, "Agnes BATTINI")
            self.assert_special(jpg, "No copy allowed unless explicitly approved by Agnes BATTINI")
            self.assert_picture_field(jpg, "width", str(792))
            self.assert_picture_field(jpg, "height", str(356))

        self.assert_file('tests/results/THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/index.htm')  # noqa

        self.assert_no_file(
            'tests/results/ALBUM/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg')  # noqa

        LOGGER.test_msg('')
        LOGGER.test_msg('------- end of Step 1 of pwp_test(30)')
        LOGGER.test_msg('')

        # ------------------------------------------------
        LOGGER.test_msg("")
        LOGGER.test_msg("2d run of pwp_main.")
        LOGGER.test_msg("we keep the ALBUM, and TRIAGE")
        LOGGER.test_msg("and verify that :")
        LOGGER.test_msg("- Previous pictures in ALBUM are still there")
        LOGGER.test_msg("- no images have been processed and moved to ALBUM")
        LOGGER.test_msg("- no thumbnails generated")
        LOGGER.test_msg("")

        cmdline = self.build_test_cmdline({'--language': 'fr',
                                           "--backup-test-stamp": "program-30-2-start-time"})  # purely local
        # --------------------------------
        self.process(cmdline)
        # --------------------------------

        # verify all pictures are still there
        self.check(30, "program-30-start-time", vector)

        # verify old pictures are not copied again in Album
        self.assert_trace("New file 'TRIAGE/Armor-cup/Armor-0.jpg' is already in album")
        self.assert_trace("New file 'TRIAGE/Armor-cup/Armor-1.jpg' is already in album")
        self.assert_trace("New file 'TRIAGE/Armor-cup/Armor-2.jpg' is already in album")
        self.assert_trace("New file 'TRIAGE/Corse/IMG-20200517-WA0000.jpg' is already in album")
        self.assert_trace("New file 'TRIAGE/Corse/IMG-20210818-WA0000.jpg' is already in album")
        self.assert_trace("New file 'TRIAGE/Corse/IMG-20210819-WA0004 - Modified.jpg' is already in album")
        self.assert_trace("New file 'TRIAGE/Corse/IMG-20210819-WA0004.jpg' is already in album as")
        self.assert_trace("New file 'TRIAGE/Forêt-de-la-Corbière/2023-06-11-17h02-40-Forêt-de-la-Corbière.png' is al") # noqa
        self.assert_trace("New file 'TRIAGE/Forêt-de-la-Corbière/Foret01.jpg' is already in album as")   # noqa
        self.assert_trace("New file 'TRIAGE/test/picture-with-gps.jpg' is already in album as")   # noqa

        # verify old Thumbnails are not created again
        self.assert_trace("Thumbnail THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/"
                          "2023-06-17-11h05-44-Armor-cup-sq.jpg is more recent than ")
        self.assert_trace("Thumbnail THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/"
                          "2023-06-17-11h05-44-Armor-cup-th.jpg is more recent than ")
        self.assert_trace("Thumbnail THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/"
                          "2023-06-17-11h05-44-Armor-cup-me.jpg is more recent than ")
        self.assert_trace("Thumbnail THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/"
                          "2023-06-17-11h05-44-Armor-cup-cu_e250.jpg is more recent than ")

        self.assert_trace("Thumbnail THUMBNAILS/2023/2023-02-Février-19-test/"
                          "2023-02-19-11h38-23-test-sq.jpg is more recent than ")
        LOGGER.test_msg('')
        LOGGER.test_msg('------- end of Step 2 of pwp_test(30)')
        LOGGER.test_msg('')

        # ------------------------------------------------
        LOGGER.test_msg("")
        LOGGER.test_msg("3rd run of pwp_main.")
        LOGGER.test_msg("we keep the ALBUM, but change TRIAGE")
        LOGGER.test_msg("")

        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results/Triages")

        cmdline = self.build_test_cmdline({'--language': 'fr',
                                           "--backup-test-stamp": "program-30-start-time"})  # purely local

        vector = PwpVector(cmdline, [
            # we add new files
            {'in-source': "PICTURES/Armor-cup/20230617_111349-new.jpg",
             'in-album': "2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h13-50-Armor-cup.jpg"},  # noqa

            {'in-source': "PICTURES/Armor-cup/20230617_113128-new.jpg",
             'in-album': "2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h31-28-Armor-cup.jpg"},  # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/IMG20230611164005-new.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h40-05-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/IMG20230611163210-new.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h32-10-Forêt-de-la-Corbière.jpg"}, # noqa
            # noqa

            # and keep some old ones, with a different name to verify they are not clobbered in ALBUM
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-album': "2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg"},  # noqa

            {'in-source': "PICTURES/Forêt-de-la-Corbière/20230611_170225.jpg",  # noqa
             'in-album': "2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-17h02-25-Forêt-de-la-Corbière.jpg"}])  # noqa

        # --------------------------------
        self.process(cmdline)
        # --------------------------------

        LOGGER.test_msg("")
        LOGGER.test_msg("Then, verify that :")
        LOGGER.test_msg("- old files in ALBUM have been kept")
        LOGGER.test_msg("- new files have been added to ALBUM")
        LOGGER.test_msg("- when an existing file has been added to TRIAGE with a different name,")
        LOGGER.test_msg("  it is still NOT added again to ALBUM")
        LOGGER.test_msg("")

        vector.check(self, "program-30-start-time")

        # this one is kept from previous run
        self.assert_file('tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                         '2023-06-11-17h02-25-Forêt-de-la-Corbière.jpg')  # noqa

        # if the following file was present, it would mean that 'same file detection'  is broken
        self.assert_no_file('tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                            '2023-06-11-17h02-26-Forêt-de-la-Corbière.jpg')  # noqa

        # if the following file was present, it would mean that 'same file detection' is broken
        self.assert_no_file(
            'tests/results/ALBUM/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg')  # noqa

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_31(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS --enable-rename FALSE')
        LOGGER.test_msg('')

        self.reset_data()
        ACTOR.rmtree("tests/results")

        cmdline = self.build_test_cmdline({'--enable-rename': 'false'})  # purely local

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-local.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-triage': "Armor-cup/20230617_110544.jpg",
             'in-album': "Armor-cup/20230617_110544.jpg",
             'orientation': '1',
             'author': "Agnes BATTINI",
             'special': "No copy allowed unless explicitly approved by Agnes BATTINI",
             'copyright': '(C) 2023 by Agnes BATTINI, for test'}])

        # ----------------------------------------------------
        main = self.process(cmdline)
        # ----------------------------------------------------

        vector.check(self, main.start_time)

        self.assert_no_file('tests/results/ALBUM/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                            '2023-06-17-11h05-44-Armor-cup.jpg')  # noqa

        LOGGER.test_msg('')
        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def program_32(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS')
        LOGGER.test_msg('')
        LOGGER.test_msg('management of txt and mp4 in TRIAGE, including copyright set for mp4')
        LOGGER.test_msg(f"BASE = {os.getcwd()}")
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results/TRIAGE")
        ACTOR.copy("tests/sources/PICTURES/Vendée/2023-07-02-14h00-00-Comments.txt",
                   "tests/results/TRIAGE/Vendée/2023-07-02-14h00-00-Comments.txt")
        # -> 2023-07-02-14h00-00-Comments.txt

        ACTOR.copy("tests/sources/PICTURES/Vendée/IMG20230702144522.jpg",
                   "tests/results/TRIAGE/Vendée/IMG20230702144522.jpg")
        # -> 2023-07-02-14h45-22-Vendée.jpg

        ACTOR.copy("tests/sources/PICTURES/Vendée/IMG20230704125307.jpg",
                   "tests/results/TRIAGE/Vendée/IMG20230704125307.jpg")
        # -> 2023-07-04-12h53-07-Vendée.jpg

        ACTOR.copy("tests/sources/VIDEO/Opéra-Paris.mp4",
                   "tests/results/TRIAGE/Vendée/Opéra-Paris.mp4")
        # -> 2023-01-27-17h59-39-Vendée.mp4

        ACTOR.copy("tests/sources/piwiPre-local.ini", "tests/results/piwiPre.ini")  # noqa

        cmdline = self.build_test_cmdline({})  # purely local
        # --------------------------------
        self.process(cmdline)
        # --------------------------------

        album = "tests/results/ALBUM"  # noqa
        self.assert_file(f"{album}/2023/2023-07-Juillet-04-Vendée/2023-07-04-12h53-07-Vendée.jpg")  # noqa
        self.assert_file(f"{album}/2023/2023-07-Juillet-02-Vendée/2023-07-02-14h00-00-Comments.txt")  # noqa
        self.assert_file(f"{album}/2023/2023-01-Janvier-27-Vendée/2023-01-27-17h59-39-Vendée.mp4")  # noqa

        mp4 = PwpMp4(f"{album}/2023/2023-01-Janvier-27-Vendée/2023-01-27-17h59-39-Vendée.mp4",  # noqa
                     config=self.home_config)  # noqa
        self.assert_mp4_field(mp4, 'copyright', "(C) 2023 by Famille BATTINI, for test")
        self.assert_mp4_field(mp4, 'author', "Famille BATTINI")
        self.assert_mp4_field(mp4, 'special', "No copy allowed unless explicitly approved by Famille BATTINI")
        self.assert_mp4_field(mp4, 'creation', "2023-01-27 17:59:39")

        thumbnails = "tests/results/THUMBNAILS/2023/2023-07-Juillet-04-Vendée"  # noqa
        self.assert_file(f"{thumbnails}/2023-07-04-12h53-07-Vendée-th.jpg")  # noqa
        self.assert_file(f"{thumbnails}/2023-07-04-12h53-07-Vendée-me.jpg")  # noqa
        self.assert_file(f"{thumbnails}/2023-07-04-12h53-07-Vendée-cu_e250.jpg")  # noqa

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_33(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('Verifying dates, from PICTURES/Forêt-de-la-Corbière and PICTURES/Thabor')  # noqa
        LOGGER.test_msg('')

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results/TRIAGE")

        ACTOR.copy("tests/sources/PICTURES/Forêt-de-la-Corbière/20230611_170225.jpg",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/P01.jpg")  # noqa
        # -> 2023-06-11-21h02-25-Forêt-de-la-Corbière.jpg                                   # noqa

        ACTOR.copy("tests/sources/PICTURES/Forêt-de-la-Corbière/IMG20230611162736.jpg",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/P02.jpg")  # noqa
        # -> 2023-06-11-10h27-36-Forêt-de-la-Corbière.jpg                                   # noqa

        ACTOR.copy("tests/sources/PICTURES/Forêt-de-la-Corbière/IMG20230611163210-new.jpg",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/P03.jpg")  # noqa
        # -> 2023-06-11-10h32-10-Forêt-de-la-Corbière.jpg                                         # noqa

        ACTOR.copy("tests/sources/PICTURES/Forêt-de-la-Corbière/IMG20230611164005-new.jpg",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/P04.jpg")  # noqa
        # -> 2023-06-11-10h40-05-Forêt-de-la-Corbière.jpg                                       # noqa

        ACTOR.copy("tests/sources/OTHER/Comments.txt",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/Comments.txt")  # noqa
        # -> Comments.txt

        ACTOR.copy("tests/sources/PICTURES/Thabor/canard.jpg",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/P05.jpg")  # noqa
        # -> 2023-06-11-14h24-38-Forêt-de-la-Corbière.jpg                # noqa

        ACTOR.copy("tests/sources/PICTURES/Thabor/canards2.jpg",  # noqa
                   "tests/results/TRIAGE/Forêt-de-la-Corbière/P06.jpg")  # noqa
        # -> 2023-06-11-14h25-06-Forêt-de-la-Corbière.jpg                # noqa

        ACTOR.copy("tests/sources/piwiPre-dates.ini", "tests/results/piwiPre.ini")

        cmdline = self.build_test_cmdline({'--enable-date-in-filename': 'false'})  # purely local
        # ----------------------------------------------------------------
        self.process(cmdline)
        # ----------------------------------------------------------------

        # Forest, SM-A336B: +4h
        self.assert_file("tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/" +  # noqa
                         "2023-06-11-21h02-25-Forêt-de-la-Corbière.jpg")  # noqa
        # noqa Thabor, C4100Z,C4000Z: absolute date
        self.assert_file("tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/" +  # noqa
                         "2023-06-11-14h24-38-Forêt-de-la-Corbière.jpg")  # noqa
        self.assert_file("tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/" +  # noqa
                         "2023-06-11-14h25-06-Forêt-de-la-Corbière.jpg")  # noqa
        # NO-DATE
        self.assert_file("tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/" +  # noqa
                         "Comments.txt")
        # Forest OPPOReno2 : -6h
        self.assert_file("tests/results/ALBUM/2023/2023-06-Juin-11-Forêt-de-la-Corbière/" +  # noqa
                         "2023-06-11-10h32-10-Forêt-de-la-Corbière.jpg")  # noqa

        # 2nd run: test with enable-date-in-filename, triage context
        # ---------------------------------------------------------

        ACTOR.rmtree("tests/results")

        ACTOR.copy("tests/sources/piwiPre-local.ini",
                   "tests/results/TRIAGE/piwiPre.ini")

        # next file has EXIF data, but filename has a different date, which should be kept
        ACTOR.copy("tests/sources/Names/Allauch/2222-10-11-12h13-14-fake-date.jpg",  # noqa
                   "tests/results/TRIAGE/Allauch/2222-10-11-12h13-14-fake-date.jpg")  # noqa

        # Next file has a Whatsapp name with a name, but no exif data
        ACTOR.copy("tests/sources/Names/Corsica/IMG-20200517-WA0000.jpg",
                   "tests/results/TRIAGE/Corsica/IMG-20200517-WA0000.jpg")

        # file with a date in directory name, not in filename, no exif data
        ACTOR.copy("tests/sources/Names/2020-05-Mai-17-Corsica/IMG-without-info.jpg",
                   "tests/results/TRIAGE/2020-05-Mai-17-Corsica/IMG-without-info.jpg")

        cmdline = self.build_test_cmdline({})  # purely local
        # ----------------------------------------------------------------
        self.process(cmdline)
        # ----------------------------------------------------------------

        # date and time from filename
        self.assert_file("tests/results/ALBUM/2222/2222-10-Octobre-11-Allauch/" +  # noqa
                         "2222-10-11-12h13-14-Allauch.jpg")  # noqa

        # date from filename
        self.assert_file("tests/results/ALBUM/2020/2020-05-Mai-17-Corsica/" +  # noqa
                         "2020-05-17-12h00-00-Corsica.jpg")  # noqa

        # date from directory, time from file last modification time
        # windows and Linux disagree about what is the Last Modification Time of the file.
        #
        file_name = "tests/sources/Names/2020-05-Mai-17-Corsica/IMG-without-info.jpg"
        m_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_name))
        new_name = f"2020-05-17-{m_time.hour:02}h{m_time.minute:02}-{m_time.second:02}-Corsica.jpg"
        self.assert_file("tests/results/ALBUM/2020/2020-05-Mai-17-Corsica/" + new_name)  # noqa
        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def program_34(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('dryrun, sources/PICTURES -> ALBUM, THUMBNAILS, album')
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results/TRIAGE")

        cmdline = self.build_test_cmdline({'--dryrun': 'true'})  # purely local

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-local.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "piwiPre-corse.ini", 'in-results': "TRIAGE/Corse/piwiPre.ini"},  # noqa
            {'in-source': "PICTURES/Armor-cup/20230617_110544.jpg",
             'in-triage': "Armor-cup/20230617_110544.jpg",  # we keep in-triage to perform assert_info
             'in-album': "2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg"}])  # noqa

        self.copy_corsica(vector)

        # ----------------------------------------------------------------
        self.process(cmdline)
        # ----------------------------------------------------------------

        self.assert_no_dir("tests/results/ALBUM")
        self.assert_no_dir("tests/results/THUMBNAILS")
        self.assert_no_dir("tests/results/BACKUP")

        self.assert_trace("Would rename 'TRIAGE/Armor-cup/20230617_110544.jpg' : " +
                         "'ALBUM/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg'")  # noqa

        # CAVEAT: conflict management has NOT occurred, because the files are not created in ALBUM thanks to dryrun
        #         So we do *not* know the exact thumbnail name
        #         hence the message is not accurate
        self.assert_trace("Would create Thumbnail 120x120 crop=True " +
                         "for TRIAGE/Armor-cup/20230617_110544")  # noqa

        self.assert_trace("Would create Thumbnail 120x120 crop=True " +
                         "for TRIAGE/Corse/IMG-20200517-WA0000.jpg")  # noqa
        self.assert_trace("Would create Thumbnail 120x120 crop=True " +
                         "for TRIAGE/Corse/IMG-20210818-WA0000.jpg")  # noqa
        self.assert_trace("Would create Thumbnail 120x120 crop=True " +
                         "for TRIAGE/Corse/IMG-20210819-WA0004 - Modified.jpg")  # noqa
        self.assert_trace("Would create Thumbnail 120x120 crop=True " +
                         "for TRIAGE/Corse/IMG-20210819-WA0004.jpg")  # noqa

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_35(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        if not self.check_done('program_34'):
            self.program_34()

        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS + corse.ini')  # noqa
        LOGGER.test_msg("testing the generation of filenames according to a different naming scheme")

        cmdline = self.build_test_cmdline({})  # purely local
        # ----------------------------------------------------------------
        self.process(cmdline)
        # ----------------------------------------------------------------

        self.reset_done('program_34')

        self.assert_dir("tests/results/ALBUM")
        self.assert_dir("tests/results/THUMBNAILS")

        self.assert_file("tests/results/ALBUM/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg")  # noqa
        self.assert_file(
            "tests/results/THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup-sq.jpg")  # noqa

        self.assert_file("tests/results/ALBUM/tmp/Corsica/2020-05-17-12h00-00-Corsica.jpg")
        self.assert_file("tests/results/ALBUM/tmp/Corsica/2021-08-18-12h00-00-Corsica.jpg")
        self.assert_file("tests/results/ALBUM/tmp/Corsica/2021-08-19-12h04-00-Corsica.jpg")
        self.assert_file("tests/results/ALBUM/tmp/Corsica/2021-08-19-12h04-01-Corsica.jpg")

        self.assert_file("tests/results/THUMBNAILS/tmp/Corsica/2021-08-19-12h04-00-Corsica-sq.jpg")
        self.assert_file("tests/results/THUMBNAILS/tmp/Corsica/2021-08-19-12h04-00-Corsica-me.jpg")

        self.assert_file("tests/results/THUMBNAILS/tmp/Corsica/2021-08-19-12h04-01-Corsica-th.jpg")
        self.assert_file("tests/results/THUMBNAILS/tmp/Corsica/2021-08-19-12h04-01-Corsica-cu_e250.jpg")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def runner_36(self, set_thumbnails='local', set_album='local', set_auto_config='local',
                  enable_database=False):

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({"--backup-test-stamp": "runner-36-start-time"},
                                          set_thumbnails=set_thumbnails,
                                          set_album=set_album,
                                          set_auto_config=set_auto_config,
                                          enable_database=enable_database,
                                          offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-local.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "piwiPre-autoconfig.ini", 'in-results': "TRIAGE/Armor-cup/piwiPre.ini"},
            {'in-source': "piwiPre-autoconfig.ini", 'in-results': "TRIAGE/Corse/piwiPre.ini"}])  # noqa

        self.copy_armor(vector, for_auto_conf=True)
        self.copy_corsica(vector, for_auto_conf=True)

        # ----------------------------------------------------------------
        self.process(cmdline)
        # ----------------------------------------------------------------

        self.check(36, backup_prefix="runner-36-start-time", vector=vector)

        album = cmdline['result-album']  # path relative to cwd, which was changed to 'tests/results'

        self.assert_no_file(album + "/2023/06/17/Armor-cup-003.jpg")  # noqa

        # verify that the.ini files have been modified with the right base:

        auto_config = cmdline['result-auto-config']  # path relative to BASE, which was changed to 'tests/results'

        self.assert_file_contains(auto_config + '/' + offset + "/2023/06/17/piwiPre.ini",
                                  "names: '" + offset + "/{Y}/{m}/{d}/Armor-cup-{count}.{suffix}'")

        self.assert_file_contains(auto_config + '/' + offset + "/2020/05/17/piwiPre.ini",
                                  "names: '" + offset + "/{Y}/{m}/{d}/Corse-{count}.{suffix}'")  # noqa

    def program_36(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS + autoconfig, prepare program_37')  # noqa
        LOGGER.test_msg(' - Manually set .ini files that should be used in autoconfig')
        LOGGER.test_msg(' - Verify they are actually built')
        ACTOR.rmtree("tests/results")

        # ----------------------------------------------------------------
        self.runner_36(set_thumbnails='local', set_album="local")
        # ----------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def runner_37(self, set_thumbnails='local', set_album='local', enable_database=False):
        LOGGER.test_msg('remove a thumbnail, do a verify-album and check')
        LOGGER.test_msg(' - files have not changed')
        LOGGER.test_msg(' - thumbnail is there again')
        LOGGER.test_msg(' - taking into account the generated autoconfig .ini')

        cmdline = self.vectors[36].cmdline

        thumbnails = cmdline['result-thumbnails']  # path relative to cwd, which was changed to 'tests/results'

        ACTOR.delete(thumbnails + "/tmp/2023/06/17/Armor-cup-001-sq.jpg")

        new_cmdline = self.build_test_cmdline({
            "--verify-album": '{album}/' + cmdline['offset'] + '/2023/06/17',
            "--triage": None,
            # "--enable_rename": 'false',
        },
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            enable_database=enable_database,
            offset=cmdline['offset'])

        # ----------------------------------------------------------------
        self.process(new_cmdline)
        # ----------------------------------------------------------------

        self.check(36, backup_prefix="runner-36-start-time", after_verify_album=True)

    def program_37(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        if not self.check_done('program_36', 36):
            self.program_36()

        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS + autoconfig')  # noqa

        # ---------------------------------------------------------
        self.runner_37(set_thumbnails='local', set_album="local")
        # ---------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_38(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function

        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('tests auto-config with a test pattern, REQ 0213, ONLY with local directories')
        self.reset_data()
        ACTOR.rmtree("tests/results")
        ACTOR.copytree("tests/sources/TEST-38/ALBUM", "tests/results/ALBUM")
        ACTOR.copytree("tests/sources/TEST-38/AUTO-CONFIG", "tests/results/AUTO-CONFIG")

        # ---------------------------------------------------------------------------
        self.verify_local_album('ALBUM/2002', enable_rename='false', time_stamp="")
        # ---------------------------------------------------------------------------

        with PwpJpg('tests/results/ALBUM/2002/2002-12-Decembre-22-Allauch/' +  # noqa
                    '2002-12-22-16h25-45-panorama-28.jpg',
                    config=self.home_config) as jpg:  # noqa
            self.assert_jpg_field(jpg, 'copyright', "This (C) is OK for Allauch")  # noqa
            # this one was set by piwiPre.ini in tests/sources/TEST-38/AUTO-CONFIG/2002/2002-12-Decembre-22-Allauch  # noqa

        with PwpJpg('tests/results/ALBUM/2002/2002-12-Decembre-01-Famille/' +  # noqa
                    '2002-12-01-15h03-09-FleurGP.jpg',
                    config=self.home_config) as jpg:  # noqa
            self.assert_jpg_field(jpg, 'copyright', 'This (C) is OK for FleurGP')
        # this one was inherited from piwiPre-local.ini

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_40(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('TRIAGE -> ALBUM, THUMBNAILS, no database')
        LOGGER.test_msg('')
        LOGGER.test_msg('Tests Triage for renaming, copyright, author, special')
        LOGGER.test_msg('with .mp4, .avi')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({
            "--backup-test-stamp": "test-time-stamp-40",
        }, offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"},
        ])

        self.copy_video(vector)

        # ----------------------------------------------------------------
        main = self.process(cmdline)
        # ----------------------------------------------------------------

        self.check(40, main.start_time, vector)

        LOGGER.test_msg('')
        LOGGER.test_msg('------- end of  program_40')
        LOGGER.test_msg('')

        self.done(mn)

    def verify_41(self, album, offset):
        LOGGER.test_msg(f'Verify {album}, {offset}')

        # from sample-mov
        self.assert_no_file(f'{album}/{offset}/2007/2007-04-Avril-03-test/sample-mov.MOV')
        # source is removed, because backup-ed and changed into mp4
        self.assert_file(f'tests/results/BACKUP/test-time-stamp-40/ALBUM/{offset}' +
                         '/2007/2007-04-Avril-03-test/sample-mov.MOV')
        self.assert_file(f'{album}/{offset}/2007/2007-04-Avril-03-test/2007-04-03-18h04-24-test.mp4')  # noqa
        with PwpMp4(f'{album}/{offset}/2007/2007-04-Avril-03-test/2007-04-03-18h04-24-test.mp4',
                    config=self.home_config) as mp4:
            self.assert_mp4_field(mp4, 'copyright', "(C) 2007 by Famille BATTINI, for test")  # noqa
            self.assert_mp4_field(mp4, 'author', "Famille BATTINI")
            self.assert_mp4_field(mp4, 'special', "No copy allowed unless explicitly approved by Famille BATTINI")
            self.assert_mp4_field(mp4, 'creation', '2007-04-03 18:04:24')

    def program_41(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        if not self.check_done('program_40', 40):
            self.program_40()

        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('tests verify-album with mp4, avi')  # noqa
        LOGGER.test_msg('uses a purely local configuration')
        LOGGER.test_msg('')

        offset = self.get_vector_uid(40)

        # add one video directly in ALBUM (not in the right directory)
        ACTOR.copy("tests/sources/VIDEO/sample-mov.MOV",
                   f"tests/results/ALBUM/{offset}/2007/2007-04-Avril-03-test/sample-mov.MOV")
        # change one video to a different directory
        ACTOR.move(f"tests/results/ALBUM/{offset}/2023/2023-01-Janvier-27-test/2023-01-27-17h59-39-test.mp4",  # noqa
                   f"tests/results/ALBUM/{offset}/2007/2007-04-Avril-03-test/sample2-mp4.mp4")

        # -----------------------------------------------------------------------------------------
        self.verify_local_album(f"ALBUM/{offset}/2023/2023-01-Janvier-27-test",
                                time_stamp="test-time-stamp-40",
                                enable_rename='true')
        self.verify_local_album(f"ALBUM/{offset}/2007/2007-04-Avril-03-test",
                                time_stamp="test-time-stamp-40",
                                enable_rename='true')
        # -----------------------------------------------------------------------------------------

        self.check(40, "test-time-stamp-40", after_verify_album=True)
        self.verify_41('tests/results/ALBUM', offset)

        # check again 2023, to verify that mp4 in place do not generate errors

        self.verify_local_album(f"ALBUM/{offset}/2023/2023-01-Janvier-27-test",
                                time_stamp="test-time-stamp-40",
                                enable_rename='true')  # noqa

        # verify nothing as changed from program_40
        self.check(40, "test-time-stamp-40", after_verify_album=True)
        self.verify_41('tests/results/ALBUM', offset)

        LOGGER.test_msg('')
        LOGGER.test_msg('------- end of  program_41')
        LOGGER.test_msg('')
        self.done(mn)

    # =====================================================================================================
    # ================================= 100: Managing the real 'network share' location

    def runner_100(self, set_album: str, set_thumbnails: str, set_auto_config: str,
                   delete=True):
        ACTOR.rmtree("tests/results")

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({"--backup-test-stamp": "runner-100-time-stamp"},
                                          set_thumbnails=set_thumbnails,
                                          set_album=set_album,
                                          set_auto_config=set_auto_config,
                                          offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"}])

        self.copy_armor(vector)

        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        self.check(100, "runner-100-time-stamp", vector)

        album = cmdline['result-album']  # album is a path relative to cwd, which was changed to 'tests/results'

        self.assert_no_file(
            f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg")  # noqa

        if delete:
            self.clean_remote_tmp(100)

    def program_100(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')

        self.runner_100(set_album='local', set_thumbnails='local', set_auto_config='local', delete=False)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_101(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        # the same test as the previous, but we use the real location home_config['album']

        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg("")
        LOGGER.test_msg("tests/sources/ to album, 'thumbnails', as read from HOME/.piwiPre.ini")
        LOGGER.test_msg("")

        if 100 in self.vectors:
            self.clean_remote_tmp(100)

        self.runner_100(set_album='local', set_thumbnails='home', set_auto_config='local', delete=True)

        LOGGER.test_msg("")
        LOGGER.test_msg("tests/sources/ to album, thumbnails, as read from HOME/.piwiPre.ini")
        LOGGER.test_msg("")

        if 100 in self.vectors:
            self.clean_remote_tmp(100)

        self.runner_100(set_album='home', set_thumbnails='home', set_auto_config='home', delete=True)
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def runner_102(self, vector_nb, set_thumbnails='local', set_album='local', set_auto_config='local',
                   enable_database: bool = False):

        LOGGER.test_msg(f"PICTURES -> Album:{set_album}, thumbnails:{set_thumbnails} database:{enable_database}")
        LOGGER.test_msg("")
        LOGGER.test_msg("This SHOULD be your remote server used for test")
        LOGGER.test_msg("and other SQL database information (login, password...) SHOULD be available.")
        LOGGER.test_msg("")
        LOGGER.test_msg("files will be stored in Album/tmp, and cleaned when tests are complete")
        LOGGER.test_msg("")

        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({},
                                          set_thumbnails=set_thumbnails,
                                          set_album=set_album,
                                          set_auto_config=set_auto_config,
                                          enable_database=enable_database,
                                          offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"}])

        self.copy_armor(vector, f"Armor-{vector_nb}")

        # -------------------------------------------------------------------
        main = self.process(cmdline)
        # -------------------------------------------------------------------

        self.check(vector_nb, main.start_time, vector=vector)

    def program_102(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('runner_102')

        # ---------------------------------------------------------------------
        self.runner_102(102, set_album='home', set_thumbnails='home', enable_database=False)
        # ---------------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_103(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('CAVEAT: Here, we test the MD5 of JPEG files, which obviously depend on JPEG algo details ')
        LOGGER.test_msg('so, it is PROBABLE that the MD5 change if the JPEG library changes')
        LOGGER.test_msg('it would be great to remove this dependency but this is NOT done')
        LOGGER.test_msg('so, if the JPEG implementation changes, one HAS TO change the md5 values !')
        LOGGER.test_msg('')
        ACTOR.configure(self.home_config)  # enable db access for the test harness

        if ACTOR.sql_connection is None:
            LOGGER.test_msg("No connection to the SQL database server, aborting ")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------------
        self.runner_102(103, set_album='home', set_thumbnails='home', set_auto_config='home',
                        enable_database=True)
        # ---------------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_104(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('This test program is just a clean of the previous ones, removing temporary data')

        ACTOR.configure(self.home_config)  # enable db access for the test harness
        if ACTOR.sql_connection is None:
            LOGGER.test_msg("No connection to the SQL database server, aborting ")
            self.done(mn, ok=False)
            return

        if 102 in self.vectors:
            self.clean_remote_tmp(102)
        if 103 in self.vectors:
            self.clean_remote_tmp(103)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_2105(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('103 then 104')
        self.program_103()
        self.program_104()
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    # =====================================================================================================
    # ------------ 200 : Starting tests for --verify-album

    def runner_200(self, set_thumbnails='local', set_album='local', set_auto_config='local',
                   enable_database=False):

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({'--backup-test-stamp': "runner-200-start-time"},
                                          set_thumbnails=set_thumbnails,
                                          set_album=set_album,
                                          set_auto_config=set_auto_config,
                                          enable_database=enable_database,
                                          offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "piwiPre-corse.ini", 'in-results': "TRIAGE/Corse/piwiPre.ini"}  # noqa
        ])

        self.copy_armor(vector)
        self.copy_corsica(vector, standard=False)
        self.copy_forest(vector)

        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        album = cmdline['--album']

        self.assert_trace("RENAME: 'TRIAGE/Armor-cup/Armor-0.jpg' : '" +  # noqa
                         f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg'")  # noqa

        self.assert_trace("RENAME: 'TRIAGE/Armor-cup/Armor-1.jpg' : '" +  # noqa
                         f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg'")  # noqa

        self.assert_trace("New file 'TRIAGE/Armor-cup/Armor-2.jpg' is already in album as '" +  # noqa
                         f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg'")  # noqa

        self.check(200, backup_prefix="runner-200-start-time", vector=vector)

    def program_200(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('------------ Starting tests for --verify-album, local config')
        LOGGER.test_msg('')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS')
        LOGGER.test_msg('')

        ACTOR.rmtree('tests/results')

        # ---------------------------------------------------------------------------------------------
        self.runner_200(set_thumbnails='local', set_album='local', set_auto_config='local', enable_database=False)
        # ---------------------------------------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def runner_201(self, set_thumbnails='local', set_album='local', set_auto_config='local',
                   enable_database=False):

        offset = self.vectors[200].cmdline["offset"]
        album_and_offset = self.vectors[200].cmdline["--album"] + '/' + offset

        cmdline = self.build_test_cmdline(
            {'--verify-album': f"{album_and_offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière",  # noqa
             '--triage': None},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)

        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        cmdline = self.build_test_cmdline({'--verify-album': f"{album_and_offset}/2023/2023-06-Juin-17-Armor-cup",
                                           '--backup-test-stamp': 'runner-200-start-time', # noqa
                                           '--triage': None},
                                          set_thumbnails=set_thumbnails,
                                          set_album=set_album,
                                          enable_database=enable_database,
                                          set_auto_config=set_auto_config,
                                          offset=offset)

        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------
        cmdline = self.build_test_cmdline({'--verify-album': f"{album_and_offset}/Corsica",
                                           '--backup-test-stamp': 'runner-200-start-time',
                                           '--triage': None},
                                          set_thumbnails=set_thumbnails,
                                          set_album=set_album,
                                          set_auto_config=set_auto_config,
                                          enable_database=enable_database,
                                          offset=offset)

        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        # nothing should have changed
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière" +  # noqa
                         "/2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière" +  # noqa
                         "/2023-06-11-16h28-04-Forêt-de-la-Corbière.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière" +  # noqa
                         "/2023-06-11-16h28-11-Forêt-de-la-Corbière.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière" +  # noqa
                         "/2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière" +  # noqa
                         "/2023-06-11-17h02-16-Forêt-de-la-Corbière.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière" +  # noqa
                         "/2023-06-11-17h02-25-Forêt-de-la-Corbière.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-17-Armor-cup" +  # noqa
                         "/2023-06-17-11h05-44-Armor-cup.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/2023/2023-06-Juin-17-Armor-cup" +  # noqa
                         "/2023-06-17-11h05-45-Armor-cup.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/Corsica/2020-05-17-12h00-00-Corsica.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/Corsica/2021-08-18-12h00-00-Corsica.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/Corsica/2021-08-19-12h04-00-Corsica.jpg' has not changed")  # noqa
        self.assert_trace("File '" + album_and_offset + "/Corsica/2021-08-19-12h04-01-Corsica.jpg' has not changed")  # noqa

        self.check(200, backup_prefix='runner-200-start-time', after_verify_album=True)

    def program_201(self):
        if not self.check_done('program_200', vector_nb=200):
            self.program_200()
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_200')
        LOGGER.test_msg('--verify-album, without modifications of ALBUM, without database')

        self.runner_201(set_thumbnails='local', set_album='local', enable_database=False)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def runner_202(self, set_thumbnails='local', set_album='local', set_auto_config='local',
                   enable_database=False):

        offset = self.vectors[200].cmdline["offset"]
        album_and_offset = self.vectors[200].cmdline["--album"] + '/' + offset

        for pattern in self.vectors[200].items:
            if pattern.triage_info:
                pattern.triage_info = None
                # means that we have not copied it from triage, so we will not test for RENAME

        cmdline1 = self.build_test_cmdline(
            {
                '--verify-album': f'{album_and_offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière',  # noqa
                '--triage': None,
                '--dryrun': 'true'},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)
        cmdline2 = self.build_test_cmdline(
            {
                '--verify-album': f'{album_and_offset}/2023/2023-06-Juin-17-Armor-cup',  # noqa
                '--triage': None,
                '--dryrun': 'true'},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)
        cmdline3 = self.build_test_cmdline(
            {
                '--verify-album': f'{album_and_offset}/Corsica',
                '--triage': None,
                '--dryrun': 'true'},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)

        album = cmdline1['--album']
        thumbnails = cmdline1['--thumbnails']
        remote_thumbnails = (cmdline1['--remote-thumbnails']
                             if cmdline1['--enable-remote-thumbnails'] == 'true' else None)

        # directories may be absolute (//NAS/...) or relative to tests/results
        abs_album = f'{album}/{offset}' if album[0] == '/' else f'tests/results/{album}/{offset}'
        abs_thumbnails = f'{thumbnails}/{offset}' if thumbnails[0] == '/' else f'tests/results/{thumbnails}/{offset}'

        # next picture has a bad name
        ACTOR.move(abs_album + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg',  # noqa
                   abs_album + '/2023/2023-06-Juin-17-Armor-cup/P1.jpg')  # noqa

        # next picture has a bad copyright information, without '2023'
        ACTOR.delete(abs_album + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                     '2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg')  # noqa
        ACTOR.copy('tests/sources/Modified/2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg',  # noqa
                   abs_album +
                   '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg')  # noqa

        # next picture has a wrong rotation
        ACTOR.delete(abs_album + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                     '2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg')  # noqa
        ACTOR.copy('tests/sources/Modified/2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg',  # noqa
                   abs_album +
                   '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg')  # noqa

        if remote_thumbnails:
            file_to_delete = cmdline1['--remote-thumbnails'] + "/Corsica/2020-05-17-12h00-00-Corsica-sq.jpg"
            ACTOR.remote_delete(file_to_delete)
        else:
            ACTOR.delete(abs_thumbnails + "/Corsica/2020-05-17-12h00-00-Corsica-sq.jpg")  # noqa

        # -----------------------------------------------
        self.process(cmdline1)
        self.process(cmdline2)
        self.process(cmdline3)
        # -----------------------------------------------

        # verify files modified have not been reset to their normal value, because --dryrun

        self.assert_no_file(abs_album + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg')  # noqa
        self.assert_file(abs_album + '/2023/2023-06-Juin-17-Armor-cup/P1.jpg')  # noqa

        if remote_thumbnails:
            self.assert_no_remote_file(remote_thumbnails + '/Corsica/2020-05-17-12h00-00-Corsica-sq.jpg')  # noqa
        else:
            self.assert_no_file(abs_thumbnails + '/Corsica/2020-05-17-12h00-00-Corsica-sq.jpg')  # noqa

        with PwpJpg(abs_album + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                    "2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg",  # noqa
                    config=self.home_config) as jpg:  # noqa
            self.assert_no_copyright(jpg, '2023')

        with PwpJpg(abs_album + "/2023/2023-06-Juin-11-Forêt-de-la-Corbière/" +  # noqa
                    "2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg",  # noqa
                    config=self.home_config) as jpg:  # noqa
            self.assert_jpg_no_field(jpg, 'orientation', "1")

        # now, verify that pictures that would be backup-ed without --dryrun are NOT backup-ed
        back_path = (f'tests/results/BACKUP/runner-200-start-time/ALBUM/{offset}/' +
                     '2023/2023-06-Juin-17-Armor-cup/')
        self.assert_no_file(back_path + 'P1.jpg')

        back_path = (f'tests/results/BACKUP/runner-200-start-time/ALBUM/{offset}/' +
                     '2023/2023-06-Juin-11-Forêt-de-la-Corbière/')                                  # noqa
        self.assert_no_file(back_path + '2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg')             # noqa
        self.assert_no_file(back_path + '2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg')             # noqa

    def program_202(self):
        if not self.check_done('program_200', vector_nb=200):
            self.program_200()
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('--verify-album, --dryrun, with some modifications')
        LOGGER.test_msg('must be executed AFTER program_200, or program_201')
        LOGGER.test_msg('')

        self.reset_done('program_200')
        self.runner_202(set_thumbnails='local', set_album='local', enable_database=False)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def runner_203(self, set_thumbnails='local', set_album='local', set_auto_config='local',
                   enable_database=False):

        vector = self.vectors[200]
        offset = vector.cmdline["offset"]
        album_and_offset = vector.cmdline["--album"] + '/' + offset

        cmdline1 = self.build_test_cmdline(
            {'--verify-album': f'{album_and_offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière',  # noqa
             "--backup-test-stamp": "runner-200-start-time",
             '--triage': None},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)
        cmdline2 = self.build_test_cmdline(
            {'--verify-album': f'{album_and_offset}/2023/2023-06-Juin-17-Armor-cup',
             "--backup-test-stamp": "runner-200-start-time",  # noqa
             '--triage': None},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)
        cmdline3 = self.build_test_cmdline(
            {'--verify-album': f'{album_and_offset}/Corsica',
             "--backup-test-stamp": "runner-200-start-time",
             '--triage': None},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)
        # Here, we verify that auto-config is OK, even in the remote case !
        # -----------------------------------------------
        self.process(cmdline1)
        self.process(cmdline2)
        self.process(cmdline3)
        # -----------------------------------------------

        self.check(200, backup_prefix="runner-200-start-time", after_verify_album=True)

        # now, verify that pictures that should be backup-ed are backup-ed
        back_path = (f'tests/results/BACKUP/runner-200-start-time/ALBUM/{offset}/' +
                     '2023/2023-06-Juin-17-Armor-cup/')
        self.assert_file(back_path + 'P1.jpg')
        back_path = (f'tests/results/BACKUP/runner-200-start-time/ALBUM/{offset}/' +
                     '2023/2023-06-Juin-11-Forêt-de-la-Corbière/')  # noqa
        self.assert_file(back_path + '2023-06-11-16h27-36-Forêt-de-la-Corbière.jpg')  # noqa
        self.assert_file(back_path + '2023-06-11-16h28-17-Forêt-de-la-Corbière.jpg')  # noqa

    def program_203(self):
        if not self.check_done('program_202', 200):
            self.program_202()
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('--verify-album, with some modifications, without dryrun')
        LOGGER.test_msg('MUST be executed AFTER program_202')
        LOGGER.test_msg('')

        self.runner_203(set_thumbnails='local', set_album='local', enable_database=False)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def runner_204(self, set_thumbnails='local', set_album='local',
                   set_auto_config='local',
                   enable_database=False):

        vector = self.vectors[200]
        offset = vector.cmdline["offset"]
        album_and_offset = vector.cmdline["--album"] + '/' + offset

        cmdline = self.build_test_cmdline(
            {'--verify-album': f'{album_and_offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière',  # noqa
             "--backup-test-stamp": "runner-200-start-time",
             '--triage': None,
             '--dryrun': 'true'},
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)

        thumbnails = cmdline['--thumbnails']
        remote_thumbnails = cmdline['--remote-thumbnails'] if '--enable-remote-thumbnails' in cmdline and \
                                                              cmdline['--enable-remote-thumbnails'] == 'true' else None

        # directories may be absolute (//NAS/...) or relative to tests/results
        abs_thumbnails = f'{thumbnails}/{offset}' if thumbnails[0] == '/' else f'tests/results/{thumbnails}/{offset}'

        if remote_thumbnails:
            ACTOR.remote_create(remote_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg')  # noqa
            ACTOR.remote_create(remote_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg')  # noqa
            # TODO: remove remote thumbnails
        else:
            ACTOR.create(abs_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg')  # noqa
            ACTOR.create(abs_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg')  # noqa
            ACTOR.delete(abs_thumbnails +
                         '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                         '2023-06-11-17h02-40-Forêt-de-la-Corbière-th.jpg')  # noqa
            ACTOR.delete(abs_thumbnails +
                         '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/' +  # noqa
                         '2023-06-11-16h27-36-Forêt-de-la-Corbière-sq.jpg')  # noqa
        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        # cannot do a verify_200: thumbnails have been removed
        # self.verify_200(cmdline, with_src=False)

        if remote_thumbnails is not None:
            self.assert_remote_file(remote_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg')  # noqa
            self.assert_remote_file(remote_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg')  # noqa
            # TODO: assert for would remove remote thumbnail
        else:
            self.assert_file(abs_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg')  # noqa
            self.assert_file(abs_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg')  # noqa
            local_file_path = f"{thumbnails}/{offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg"  # noqa
            self.assert_trace(f"Would delete '{local_file_path}' when removing extra thumbnail")
            local_file_path = f"{thumbnails}/{offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg"  # noqa
            self.assert_trace(f"Would delete '{local_file_path}' when removing extra thumbnail")

    def program_204(self):
        if not self.check_done('program_200', 200):
            self.program_200()
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg('must be executed AFTER program_200, CAN be executed after 201/202/203')
        LOGGER.test_msg('--verify-album --enable-thumbnails-delete, with modification, --dryrun')
        LOGGER.test_msg('')
        LOGGER.test_msg('We modify the thumbnails repository by :')
        LOGGER.test_msg(' - adding 2 fake thumbnails ')
        LOGGER.test_msg(' - removing 2 thumbnails ')

        LOGGER.test_msg('and verify --dryrun detects they would be removed ')
        LOGGER.test_msg('')
        LOGGER.test_msg('CAVEAT:')
        LOGGER.test_msg('       --dryrun does NOT correctly detect thumbnails creation')
        LOGGER.test_msg('         so we can not test the generated messages')
        LOGGER.test_msg('')

        self.runner_204(set_thumbnails='local', set_album='local', enable_database=False)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def runner_205(self, set_thumbnails='local', set_album='local',
                   set_auto_config='local',
                   enable_database=False):

        vector = self.vectors[200]
        offset = vector.cmdline["offset"]
        album_and_offset = vector.cmdline["--album"] + '/' + offset

        cmdline = self.build_test_cmdline(
            {'--verify-album': f'{album_and_offset}/2023/2023-06-Juin-11-Forêt-de-la-Corbière',  # noqa
             "--backup-test-stamp": "runner-200-start-time",
             '--triage': None},  # no --dryrun
            set_thumbnails=set_thumbnails,
            set_album=set_album,
            set_auto_config=set_auto_config,
            enable_database=enable_database,
            offset=offset)

        thumbnails = cmdline['--thumbnails']
        if '--enable-remote-thumbnails' in cmdline and cmdline['--enable-remote-thumbnails'] == 'true':
            remote_thumbnails = cmdline['--remote-thumbnails'] + '/' + offset
        else:
            remote_thumbnails = None

        # directories may be absolute (//NAS/...) or relative to tests/results
        abs_thumbnails = f'{thumbnails}/{offset}' if thumbnails[0] == '/' else f'tests/results/{thumbnails}/{offset}'

        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        self.check(200, backup_prefix="runner-200-start-time", after_verify_album=True)

        if remote_thumbnails is not None:
            self.assert_no_remote_file(
                remote_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg')  # noqa
            self.assert_no_remote_file(
                remote_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg')  # noqa
        else:
            self.assert_no_file(abs_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/foo-sq.jpg')  # noqa
            self.assert_no_file(abs_thumbnails + '/2023/2023-06-Juin-11-Forêt-de-la-Corbière/bat-th.jpg')  # noqa

    def program_205(self):
        if not self.check_done('program_204', 200):
            self.program_204()
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg('must be executed AFTER program_204')
        LOGGER.test_msg('--verify-album, with modification, WITHOUT dryrun')
        LOGGER.test_msg('')
        LOGGER.test_msg('checks that ')
        LOGGER.test_msg('- thumbnails that should have been deleted are deleted,')
        LOGGER.test_msg('- thumbnails that should have been created again are created again,')

        self.runner_205(set_thumbnails='local', set_album='local', enable_database=False)

        self.reset_done('program_204')
        self.reset_done('program_203')
        self.reset_done('program_202')
        self.reset_done('program_201')
        self.reset_done('program_200')

        self.clean_remote_tmp(200)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def program_206(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')

        LOGGER.test_msg('')
        LOGGER.test_msg('--building a LOCAL test case with tests/sources/PICTURES/Armor-cup ')
        LOGGER.test_msg('')

        cmdline = self.build_test_cmdline({'--backup-test-stamp': "runner-206-start-time"},
                                          set_thumbnails='local', set_album='local',
                                          set_auto_config='local',
                                          enable_database=False)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-local.ini", 'in-results': "piwiPre.ini"},
        ])

        self.copy_armor(vector)

        # first, we generate the test pattern in ALBUM
        # -----------------------------------------------
        self.process(cmdline)
        # -----------------------------------------------

        self.check(206, backup_prefix="runner-206-start-time", vector=vector)

        self.assert_no_file('tests/results/THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                            '2023-06-17-11h05-46-Armor-cup.jpg')  # noqa

        # local, local: no need to call clean_remote_tmp    # noqa
        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def program_207(self):
        if not self.check_done('program_206', 206):
            self.program_206()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg("--verify-album --enable-rename , with a different 'names'")
        LOGGER.test_msg('')
        LOGGER.test_msg('Checks that:')
        LOGGER.test_msg('- previous album files are removed')
        LOGGER.test_msg('- new album files have been created')

        ACTOR.copy('tests/sources/piwiPre-names.ini', 'tests/results/piwiPre.ini')
        self.reset_done('program_206')

        vector = self.vectors[206]
        pattern = vector.find({'in_triage': 'tests/results/TRIAGE/Armor-cup/Armor-0.jpg'})
        pattern.in_triage = None
        pattern.in_album = 'tests/results/ALBUM/2023/06/17/Armor-cup-001.jpg'
        pattern.in_thumbnails = 'tests/results/THUMBNAILS/2023/06/17/Armor-cup-001.jpg'
        pattern.thumbs = ['tests/results/THUMBNAILS/2023/06/17/index.htm']
        for item in ['sq.jpg', 'th.jpg', 'me.jpg', 'cu_e250.jpg']:
            pattern.thumbs.append('tests/results/THUMBNAILS/2023/06/17/Armor-cup-001-' + item)

        pattern = vector.find({'in_triage': 'tests/results/TRIAGE/Armor-cup/Armor-1.jpg'})
        pattern.in_triage = None
        pattern.in_album = 'tests/results/ALBUM/2023/06/17/Armor-cup-002.jpg'
        pattern.in_thumbnails = 'tests/results/THUMBNAILS/2023/06/17/Armor-cup-002.jpg'
        pattern.thumbs = ['tests/results/THUMBNAILS/2023/06/17/index.htm']
        for item in ['sq.jpg', 'th.jpg', 'me.jpg', 'cu_e250.jpg']:
            pattern.thumbs.append('tests/results/THUMBNAILS/2023/06/17/Armor-cup-002-' + item)

        pattern = vector.find({'in_triage': 'tests/results/TRIAGE/Armor-cup/Armor-2.jpg'})
        pattern.in_triage = None
        pattern.in_album = 'tests/results/ALBUM/2023/06/17/Armor-cup-002.jpg'
        pattern.in_thumbnails = 'tests/results/THUMBNAILS/2023/06/17/Armor-cup-002.jpg'
        pattern.thumbs = ['tests/results/THUMBNAILS/2023/06/17/index.htm']
        for item in ['sq.jpg', 'th.jpg', 'me.jpg', 'cu_e250.jpg']:
            pattern.thumbs.append('tests/results/THUMBNAILS/2023/06/17/Armor-cup-002-' + item)

        cmdline = self.build_test_cmdline({'--verify-album': 'ALBUM/2023/2023-06-Juin-17-Armor-cup',
                                           '--backup-test-stamp': "runner-206-start-time",
                                           '--triage': None})
        # ------------------------------------------------------------------
        self.process(cmdline)
        # ------------------------------------------------------------------

        self.check(206, backup_prefix="runner-206-start-time")

        self.assert_no_file('tests/results/ALBUM/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                            '2023-06-17-11h05-44-Armor-cup.jpg')  # noqa
        self.assert_no_dir('tests/results/THUMBNAILS/2023/2023-06-Juin-17-Armor-cup')  # noqa

        self.assert_file('tests/results/ALBUM/2023/06/17/Armor-cup-001.jpg')  # noqa
        self.assert_file('tests/results/ALBUM/2023/06/17/Armor-cup-002.jpg')  # noqa

        self.assert_file(
            'tests/results/BACKUP/runner-206-start-time/ALBUM/2023/2023-06-Juin-17-Armor-cup/' +
            '2023-06-17-11h05-44-Armor-cup.jpg')  # noqa
        self.assert_file(
            'tests/results/BACKUP/runner-206-start-time/ALBUM/2023/2023-06-Juin-17-Armor-cup/' +
            '2023-06-17-11h05-45-Armor-cup.jpg')  # noqa

        del self.vectors[206]

        LOGGER.test_msg(f'--------------- end of  {mn}')
        self.done(mn)

    def program_210(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('--verify-album --dryrun in real life')

        # this tests has no asserts, its main usage is to verify coverage

        ACTOR.configure(self.home_config)  # enable db access for the test harness

        album = self.home_config['album']
        target = self.get_first_album()
        if target is None:
            LOGGER.test_msg(f"album '{album}' is empty or no sql connection, no test to do")
            self.done(mn, ok=False)
            return
        else:
            LOGGER.test_msg(f"verifying album '{target}' --dryrun")

            ACTOR.rmtree("tests/results")
            ACTOR.mkdirs("tests/results")
            ACTOR.copy("tests/sources/piwiPre-to-tmp.ini", "tests/results/piwiPre.ini")
            # no need to generate a unique ID? because we will not use 'names'

            # -------------------------------------------------------
            pwp_main(['--base', 'tests/results',
                      '--gui', 'false',
                      '--enable-database', 'false',
                      '--verify-album', f'{album}/{target}',
                      '--triage', None,
                      "--enable-rename", 'false',
                      "--dryrun", "true"])
            # ------------------------------------------------------
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_211(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('start with pictures in triage')
        LOGGER.test_msg('rename directories')
        LOGGER.test_msg('--verify-album a1 , then --verify-album a2,')

        def build():
            ACTOR.rmtree("tests/results")
            ACTOR.mkdirs("tests/results")
            ACTOR.copy("tests/sources/piwiPre-local.ini", "tests/results/piwiPre.ini")
            ACTOR.copy("tests/sources/PICTURES/Vendée/IMG20230702144522.jpg",
                       "tests/results/TRIAGE/IMG20230702144522.jpg")
            ACTOR.copy("tests/sources/PICTURES/Vendée/IMG20230704125307.jpg",
                       "tests/results/TRIAGE/IMG20230704125307.jpg")

        build()

        # ------------------------------------------------------
        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--backup-test-stamp', 'program-211-TTS',
                  '--enable-database', 'false'])
        # ------------------------------------------------------
        self.assert_file('tests/results/ALBUM/2023/2023-07-Juillet-02-TRIAGE/2023-07-02-14h45-22-TRIAGE.jpg')
        self.assert_file('tests/results/ALBUM/2023/2023-07-Juillet-04-TRIAGE/2023-07-04-12h53-07-TRIAGE.jpg')
        self.assert_file('tests/results/BACKUP/program-211-TTS/TRIAGE/IMG20230702144522.jpg')
        self.assert_file('tests/results/BACKUP/program-211-TTS/TRIAGE/IMG20230704125307.jpg')

        LOGGER.test_msg('')
        LOGGER.test_msg('Step 0 OK: files generated')
        LOGGER.test_msg('')

        def copy_files():
            ACTOR.rmtree('tests/results/ALBUM/2023/Chemin')
            ACTOR.rmtree('tests/results/ALBUM/2023/BBQ')
            ACTOR.rmtree('tests/results/ALBUM/2023/2023-07-Juillet-02-Chemin')
            ACTOR.rmtree('tests/results/ALBUM/2023/2023-07-Juillet-04-BBQ')
            ACTOR.copytree('tests/results/ALBUM/2023/2023-07-Juillet-02-TRIAGE', 'tests/results/ALBUM/2023/Chemin')
            ACTOR.copytree('tests/results/ALBUM/2023/2023-07-Juillet-04-TRIAGE',
                           'tests/results/ALBUM/2023/2023-07-Juillet-04-BBQ') # noqa

        copy_files()

        # ------------------------------------------------------
        pwp_main(['--base', 'tests/results',
                  '--quiet', 'true',
                  '--gui', 'false',
                  '--backup-test-stamp', 'program-211-TTS2',
                  '--verify-album', 'ALBUM/2023/2023-07-Juillet-04-BBQ',
                  '--enable-database', 'false'])
        pwp_main(['--base', 'tests/results',
                  '--quiet', 'true',
                  '--backup-test-stamp', 'program-211-TTS3',
                  '--gui', 'false',
                  '--verify-album', 'ALBUM/2023/Chemin',  # noqa
                  '--enable-database', 'false'])
        # ------------------------------------------------------

        def verify():
            self.assert_file('tests/results/ALBUM/2023/2023-07-Juillet-04-BBQ/2023-07-04-12h53-07-BBQ.jpg')
            self.assert_file('tests/results/THUMBNAILS/2023/'
                             '2023-07-Juillet-04-BBQ/2023-07-04-12h53-07-BBQ-sq.jpg')
            self.assert_file('tests/results/BACKUP/program-211-TTS2/ALBUM/'
                             '2023/2023-07-Juillet-04-BBQ/2023-07-04-12h53-07-TRIAGE.jpg')

            self.assert_file('tests/results/ALBUM/2023/2023-07-Juillet-02-Chemin/2023-07-02-14h45-22-Chemin.jpg')
            self.assert_file('tests/results/THUMBNAILS/2023/'
                             '2023-07-Juillet-02-Chemin/2023-07-02-14h45-22-Chemin-sq.jpg')

            # when --verify-album is used, the original files in ALBUM are moved (and saved in BACKUP)
            self.assert_no_file('tests/results/ALBUM/2023/Chemin/2023-07-02-14h45-22-TRIAGE.jpg')
            self.assert_no_file('tests/results/ALBUM/2023/BBQ/2023-07-04-12h53-07-TRIAGE.jpg')

        verify()
        self.assert_file('tests/results/BACKUP/program-211-TTS2/'
                         'ALBUM/2023/2023-07-Juillet-04-BBQ/2023-07-04-12h53-07-TRIAGE.jpg')
        self.assert_file('tests/results/BACKUP/program-211-TTS3/'
                         'ALBUM/2023/Chemin/2023-07-02-14h45-22-TRIAGE.jpg')

        LOGGER.test_msg('')
        LOGGER.test_msg('Step 1 OK: files have been renamed and moved in new directory')
        LOGGER.test_msg('')

        # Continue with '{album} and with absolute PATHS

        copy_files()
        ACTOR.rmtree('tests/results/ALBUM/2023/2023-07-Juillet-02-TRIAGE')
        ACTOR.rmtree('tests/results/ALBUM/2023/2023-07-Juillet-04-TRIAGE')  # noqa

        # ------------------------------------------------------
        pwp_main(['--base', 'tests/results',
                  '--quiet', 'true',
                  '--gui', 'false',
                  '--backup-test-stamp', 'program-211-TTS2',
                  '--verify-album', '{album}/2023',
                  '--enable-verify-sub-album', True,
                  '--enable-database', 'false'])
        # ------------------------------------------------------
        verify()

        LOGGER.test_msg('')
        LOGGER.test_msg('Step 2 OK: {album}/2023 and --enable-verify-sub-album True')
        LOGGER.test_msg('')

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    # ====================================================================
    # 300 : --verify-thumbnails
    # ====================================================================

    def program_300(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        if not self.check_done('program_30', 30):
            self.program_30()

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('verify thumbnails in ALBUM')

        ACTOR.delete("tests/results/THUMBNAILS/2023/2023-06-Juin-17-Armor-cup/" +  # noqa
                     "2023-06-17-11h05-44-Armor-cup-cu_e250.jpg")  # noqa
        ACTOR.delete("tests/results/THUMBNAILS/2021/2021-08-Août-19-Corse/2021-08-19-12h04-00-Corse-sq.jpg")  # noqa
        ACTOR.create("tests/results/THUMBNAILS/2021/2021-08-Août-19-Corse/2021-08-19-12h04-00-Corse-foo.jpg")  # noqa
        ACTOR.create("tests/results/THUMBNAILS/2020/2020-05-Mai-17-Corse/2021-08-19-12h04-00-Corse-sq.jpg")  # noqa
        ACTOR.create("tests/results/THUMBNAILS/2020/2020-05-Mai-17-Corse/foo.txt")  # noqa

        cmdline1 = self.build_test_cmdline({'--triage': None,
                                            '--verify-album': "ALBUM/2020",
                                            "--backup-test-stamp": "program-30-start-time", })
        cmdline2 = self.build_test_cmdline({'--triage': None,
                                            '--verify-album': "ALBUM/2021",
                                            "--backup-test-stamp": "program-30-start-time", })
        cmdline3 = self.build_test_cmdline({'--triage': None,
                                            '--verify-album': "ALBUM/2023",
                                            "--backup-test-stamp": "program-30-start-time", })
        # -----------------------------------------------
        self.process(cmdline1, msg="Verify album 2020, without database")
        self.process(cmdline2, msg="Verify album 2021, without database")
        self.process(cmdline3, msg="Verify album 2023, without database")
        # -----------------------------------------------

        self.check(30, after_verify_album=True, backup_prefix="program-30-start-time")

        self.assert_no_file("tests/results/THUMBNAILS/2021/2021-08-Août-19-Corse/" +  # noqa
                            "2021-08-19-12h04-00-Corse-foo.jpg")  # noqa
        self.assert_no_file("tests/results/THUMBNAILS/2020/2020-05-Mai-17-Corse/" +  # noqa
                            "2021-08-19-12h04-00-Corse-sq.jpg")  # noqa
        self.assert_no_file("tests/results/THUMBNAILS/2020/2020-05-Mai-17-Corse/foo.txt")  # noqa

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    # ====================================================================
    # ssh/sftp
    # ====================================================================

    def program_400(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('testing ssh')
        LOGGER.test_msg('')
        LOGGER.test_msg('CAVEAT: ssh password MUST be set using ssh-add and ssh-agent')
        LOGGER.test_msg('        depending on the method used to start this test,')
        LOGGER.test_msg('        maybe piwiPre has NOT inherited from ssh-add, and the test will fail')

        ACTOR.rmtree("tests/results")
        # No need to set a unique id, nor to clean tmp
        ACTOR.copy("tests/sources/piwiPre-to-tmp.ini", "tests/results/piwiPre.ini")
        ACTOR.create("tests/results/dummy.txt")

        # ----------------------------------------------------------------
        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--test-ssh',
                  '--test-sftp',
                  '--enable-remote-thumbnails', 'true',
                  '--enable-database', 'false'])  # noqa
        # ----------------------------------------------------------------

        self.assert_not_info("SSH error")
        self.assert_trace("sftp test OK")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_401(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('remote thumbnails, with TRIAGE')

        ACTOR.rmtree("tests/results")

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ----------------------------------------------------------------------
        self.runner_100(set_thumbnails='remote', set_album='home', set_auto_config='home', delete=False)
        # ----------------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_402(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        if not self.check_done('program_401', 100):
            self.program_401()

        self.reset_data()  # before any action, e.g. rmtree
        self.reset_done("program_401")

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('verify thumbnails on remote thumbnails, after program_400')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        album = self.home_config['album']
        thumbnails = 'THUMBNAILS'  # used as a cache to remote-thumbnails
        remote = "true"
        offset = self.get_vector_uid(100)

        ACTOR.configure(self.home_config)  # enable ssh for the test harness

        LOGGER.test_msg("")
        LOGGER.test_msg("build a fake local thumbnail in thumbnails: 'fake-local-thumbnail.jpg'")
        LOGGER.test_msg("This thumbnail should be removed from THUMBNAILS and must not appear in remote-thumbnails")
        LOGGER.test_msg("")

        #
        abs_thumbnails = f'{thumbnails}/{offset}' if thumbnails[0] == '/' else f'tests/results/{thumbnails}/{offset}'

        ACTOR.move(abs_thumbnails + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup-th.jpg',  # noqa
                   abs_thumbnails + '/2023/2023-06-Juin-17-Armor-cup/fake-local-thumbnail.jpg')  # noqa

        LOGGER.test_msg("")
        LOGGER.test_msg("Remove some local thumbnails in thumbnails")
        LOGGER.test_msg("They should be constructed again to reflect correctly items in remote-thumbnails")
        LOGGER.test_msg("")

        ACTOR.delete(abs_thumbnails + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup-me.jpg')  # noqa
        ACTOR.delete(abs_thumbnails + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup-me.jpg')  # noqa

        LOGGER.test_msg("")
        LOGGER.test_msg("delete some thumbnails on the remote thumbnails server")
        LOGGER.test_msg("we will verify they are correctly built again")
        LOGGER.test_msg("independently on the presence of their local version in thumbnails")
        LOGGER.test_msg("")

        abs_rem = self.home_config['remote-thumbnails'] + '/' + offset

        ACTOR.remote_delete(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup-me.jpg')  # noqa
        ACTOR.remote_delete(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup-me.jpg')  # noqa
        ACTOR.remote_delete(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup-th.jpg')  # noqa
        ACTOR.remote_delete(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/index.htm')  # noqa

        LOGGER.test_msg("")
        LOGGER.test_msg("build a fake remote thumbnail in remote-thumbnails: 'fake-remote-thumbnail.jpg'")
        LOGGER.test_msg("This thumbnail should be removed from remote-thumbnails")
        LOGGER.test_msg("")

        ACTOR.remote_move(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup-th.jpg',  # noqa
                          abs_rem + '/2023/2023-06-Juin-17-Armor-cup/fake-remote-thumbnail.jpg')  # noqa

        cmdline = self.build_test_cmdline({'--triage': None,
                                           '--album': album,  # /tmp is added by names: ...
                                           '--backup-test-stamp': "runner-100-time-stamp",
                                           '--thumbnails': thumbnails,
                                           '--remote-thumbnails': self.home_config['remote-thumbnails'],
                                           '--enable-remote-thumbnails': remote,
                                           '--verify-album': f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup"})
        # ---------------------------------------------------------------------
        self.process(cmdline)  # noqa
        # ---------------------------------------------------------------------

        self.check(100, "runner-100-time-stamp", after_verify_album=True)

        # always an absolute path

        self.assert_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                                '2023-06-17-11h05-45-Armor-cup-me.jpg')
        self.assert_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                                '2023-06-17-11h05-44-Armor-cup-me.jpg')
        self.assert_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                                '2023-06-17-11h05-45-Armor-cup-th.jpg')
        self.assert_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                                '2023-06-17-11h05-44-Armor-cup-th.jpg')
        self.assert_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/' +  # noqa
                                'index.htm')

        self.assert_no_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/fake-remote-thumbnail.jpg')
        self.assert_no_file(abs_thumbnails + '/2023/2023-06-Juin-17-Armor-cup/fake-remote-thumbnail.jpg')

        self.assert_no_remote_file(abs_rem + '/2023/2023-06-Juin-17-Armor-cup/fake-local-thumbnail.jpg')
        self.assert_no_file(abs_thumbnails + '/2023/2023-06-Juin-17-Armor-cup/fake-local-thumbnail.jpg')

        self.clean_remote_tmp(100)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_436(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('sources/PICTURES -> ALBUM=local, THUMBNAILS=remote + autoconfig, prepare program_437')  # noqa
        LOGGER.test_msg(' - Manually set .ini files that should be used in autoconfig')
        LOGGER.test_msg(' - Verify they are actually built')
        ACTOR.rmtree("tests/results")

        if not self.home_config['remote-auto-config']:
            LOGGER.test_msg("Empty test because no 'remote-auto-config' configuration")
            self.done(mn, ok=False)
            return

        # ----------------------------------------------------------------
        self.runner_36(set_thumbnails='remote', set_album="home", set_auto_config='remote')
        # ----------------------------------------------------------------

        offset = self.get_vector_uid(36)
        remote_auto_config = self.home_config['remote-auto-config'] + '/' + offset

        self.assert_remote_file(remote_auto_config + "/2023/06/17/piwiPre.ini")
        LOGGER.test_msg(f'verify remote {remote_auto_config}/2023/06/17/piwiPre.ini')

        self.assert_remote_file(remote_auto_config + "/2020/05/17/piwiPre.ini")
        LOGGER.test_msg(f'verify remote {remote_auto_config}/2023/05/17/piwiPre.ini')

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_437(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        if not self.check_done('program_436', 36):
            self.program_436()

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('Check autoconfig files are used, in a thumbnails:remote, album:home configuration')  # noqa

        # DO NOT REMOVE "tests/results", we need it to verify vector

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ----------------------------------------------------------------
        self.runner_37(set_thumbnails='remote', set_album="home")
        # ----------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_499(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('cleaning after programs 40x')

        if 100 in self.vectors:
            self.clean_remote_tmp(100)

        # used by program_436
        if 36 in self.vectors:
            self.clean_remote_tmp(36)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    # ----------------------------------------------
    # the same tests as program_200, but with sftp
    def program_500(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('------------ Starting tests for --verify-album, thumbnails:remote album:home')
        LOGGER.test_msg('')
        LOGGER.test_msg('sources/PICTURES -> ALBUM, THUMBNAILS, remote')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        ACTOR.configure(self.home_config)  # enable ssh for the test harness

        # ---------------------------------------------------------------
        self.runner_200(set_thumbnails='remote', set_album='home', set_auto_config='home')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_501(self):
        if not self.check_done('program_500', 200):
            self.program_500()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_500, thumbnails:remote album:home')
        LOGGER.test_msg('--verify-album, without modifications of ALBUM')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_201(set_thumbnails='remote', set_album='home')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_502(self):
        if not self.check_done('program_500', 200):
            self.program_500()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_500, or program_501')
        LOGGER.test_msg('--verify-album, --dryrun, with some modifications')
        LOGGER.test_msg('')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_202(set_thumbnails='remote', set_album='home')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_503(self):
        if not self.check_done('program_502', 200):
            self.program_502()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_502')
        LOGGER.test_msg('--verify-album, with some modifications')
        LOGGER.test_msg('')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_203(set_thumbnails='remote', set_album='home')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_504(self):
        if not self.check_done('program_500', 200):
            self.program_500()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_500, CAN be executed after 501/502/503')
        LOGGER.test_msg('--verify-album --enable-thumbnails-delete, with modification, --dryrun')
        LOGGER.test_msg('')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_204(set_thumbnails='remote', set_album='home')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_505(self):
        if not self.check_done('program_504', 200):
            self.program_504()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_504,')
        LOGGER.test_msg('--verify-album --enable-thumbnails-delete, with modification')
        LOGGER.test_msg('')

        remote_thumbnails = self.home_config['remote-thumbnails']
        if not remote_thumbnails:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_205(set_thumbnails='remote', set_album='home')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.reset_done('program_504')
        self.reset_done('program_503')
        self.reset_done('program_502')
        self.reset_done('program_501')
        self.reset_done('program_500')

        self.clean_remote_tmp(200)

        self.done(mn)

    # ----------------------------------------------------------------------------------------
    # the same tests as program_200, but with remote album over sftp
    # ----------------------------------------------------------------------------------------

    def program_550(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('------------ Starting tests for --verify-album, album: remote')
        LOGGER.test_msg('')
        LOGGER.test_msg('sources/PICTURES -> ALBUM=remote, THUMBNAILS=home')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        if not self.home_config['remote-album']:
            LOGGER.test_msg("Empty test because no 'remote-album' configuration")
            self.done(mn, ok=False)
            return

        ACTOR.configure(self.home_config)  # enable ssh for the test harness

        # ---------------------------------------------------------------
        self.runner_200(set_thumbnails='home', set_album='remote',  set_auto_config='remote')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_551(self):
        if not self.check_done('program_550', 200):
            self.program_550()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_550, thumbnails:home album:remote')
        LOGGER.test_msg('--verify-album, without modifications of ALBUM')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_201(set_thumbnails='home', set_album='remote')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_552(self):
        if not self.check_done('program_550', 200):
            self.program_550()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('--verify-album, --dryrun, with some modifications')
        LOGGER.test_msg('must be executed AFTER program_550, or program_551, thumbnails:home album:remote')
        LOGGER.test_msg('')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_202(set_thumbnails='home', set_album='remote')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_553(self):
        if not self.check_done('program_552', 200):
            self.program_552()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_552, thumbnails:home album:remote')
        LOGGER.test_msg('--verify-album, with some modifications')
        LOGGER.test_msg('')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_203(set_thumbnails='home', set_album='remote')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_554(self):
        if not self.check_done('program_550', 200):
            self.program_550()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_550, CAN be executed after 551/552/553,')
        LOGGER.test_msg(' thumbnails:home album:remote')
        LOGGER.test_msg('--verify-album --enable-thumbnails-delete, with modification, --dryrun')
        LOGGER.test_msg('')

        if not self.home_config['remote-thumbnails']:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_204(set_thumbnails='home', set_album='remote')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_555(self):
        if not self.check_done('program_554', 200):
            self.program_554()

        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('must be executed AFTER program_554, thumbnails:home album:remote')
        LOGGER.test_msg('--verify-album --enable-thumbnails-delete, with modification')
        LOGGER.test_msg('')

        remote_thumbnails = self.home_config['remote-thumbnails']
        if not remote_thumbnails:
            LOGGER.test_msg("Empty test because no 'remote-thumbnails' configuration")
            self.done(mn, ok=False)
            return

        # ---------------------------------------------------------------
        self.runner_205(set_thumbnails='home', set_album='remote')
        # ---------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.reset_done('program_554')
        self.reset_done('program_553')
        self.reset_done('program_552')
        self.reset_done('program_551')
        self.reset_done('program_550')

        self.clean_remote_tmp(200)

        self.done(mn)

    def program_560(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('------------ Starting tests for --verify-album, album: remote')
        LOGGER.test_msg('')
        LOGGER.test_msg('sources/PICTURES -> ALBUM=remote, THUMBNAILS=home')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        if not self.home_config['remote-album']:
            LOGGER.test_msg("Empty test because no 'remote-album' configuration")
            self.done(mn, ok=False)
            return

        ACTOR.configure(self.home_config)  # enable ssh for the test harness

        # ---------------------------------------------------------------
        self.runner_200(set_thumbnails='home', set_album='remote', set_auto_config='local')
        # ---------------------------------------------------------------

        offset = self.get_vector_uid(200)
        vector = self.vectors[200]
        rem_album = vector.cmdline['--remote-album']

        LOGGER.test_msg("")
        LOGGER.test_msg("Delete local 2023-06-17-11h05-44-Armor-cup.jpg, it should be built again")
        LOGGER.test_msg("")
        ACTOR.delete(f"tests/results/ALBUM/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg")
        # this is tested through vector

        LOGGER.test_msg("")
        LOGGER.test_msg("move local 2023-06-17-11h05-45-Armor-cup.jpg, to local-copy-of-45.jpg")
        LOGGER.test_msg("it should be erased from local and not copied to remote")
        LOGGER.test_msg("")

        ACTOR.move(f"tests/results/ALBUM/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg",
                   f"tests/results/ALBUM/{offset}/2023/2023-06-Juin-17-Armor-cup/local-copy-of-45.jpg")

        LOGGER.test_msg("")
        LOGGER.test_msg("move *remote* 2023-06-17-11h05-45-Armor-cup.jpg, to copy-of-45.jpg")
        LOGGER.test_msg("its thumbnails should be generated, and it should be copied to local")
        LOGGER.test_msg("")
        # this is tested through vector

        ACTOR.remote_move(f"{rem_album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg",
                          f"{rem_album}/{offset}/2023/2023-06-Juin-17-Armor-cup/copy-of-45.jpg")

        pattern = vector.find(
            {'in_triage': 'tests/results/TRIAGE/Armor-cup/Armor-1.jpg',
             'in_album': f"tests/results/ALBUM/{offset}" +
                         "/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg"})
        pattern.in_album = f"tests/results/ALBUM/{offset}/2023/2023-06-Juin-17-Armor-cup/copy-of-45.jpg"
        pattern.in_remote_album = f"{rem_album}/{offset}/2023/2023-06-Juin-17-Armor-cup/copy-of-45.jpg"
        new_thumbs = []
        for item in pattern.thumbs:
            new_thumbs.append(item.replace("2023-06-17-11h05-45-Armor-cup", "copy-of-45"))
        pattern.thumbs = new_thumbs

        pattern = vector.find(
            {'in_triage': 'tests/results/TRIAGE/Armor-cup/Armor-2.jpg',
             'in_album': f"tests/results/ALBUM/{offset}" +
                         "/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg"})
        pattern.in_album = None
        pattern.in_remote_album = None
        pattern.thumbs = {}

        # clean completely ALBUM
        ACTOR.delete(f"tests/results/ALBUM/{offset}/Corsica/2020-05-17-12h00-00-Corsica.jpg")
        ACTOR.delete(f"tests/results/ALBUM/{offset}/Corsica/2021-08-18-12h00-00-Corsica.jpg")
        ACTOR.delete(f"tests/results/ALBUM/{offset}/Corsica/2021-08-19-12h04-00-Corsica.jpg")
        ACTOR.delete(f"tests/results/ALBUM/{offset}/Corsica/2021-08-19-12h04-01-Corsica.jpg")

        ACTOR.remote_move(f"{rem_album}/{offset}/Corsica/2020-05-17-12h00-00-Corsica.jpg",
                          f"{rem_album}/{offset}/Corsica/copy-of-17.jpg")
        pattern = vector.find(
            {'in_album': f"tests/results/ALBUM/{offset}/Corsica/2020-05-17-12h00-00-Corsica.jpg"})
        pattern.in_album = None
        pattern.in_remote_album = None
        pattern.thumbs = []

        vector.add([{
            'in-album': "Corsica/copy-of-17.jpg",  # noqa
            'in-remote-album': "Corsica/copy-of-17.jpg",
        }])

        # the remote file should stay in remote-album,
        # but should be compared through MD5 with the other files in the directory

        cmdline = self.build_test_cmdline({'--triage': None,
                                           '--album': 'ALBUM',
                                           '--backup-test-stamp': "runner-200-start-time",
                                           '--thumbnails': vector.cmdline['--thumbnails'],
                                           '--remote-thumbnails': vector.cmdline['--remote-thumbnails'],
                                           '--enable-remote-thumbnails': vector.cmdline['--enable-remote-thumbnails'],
                                           '--enable-remote-album': True,
                                           '--remote-album': vector.cmdline['--remote-album'],
                                           '--enable-rename': False,
                                           '--verify-album': f"ALBUM/{offset}"})
        # ---------------------------------------------------------------------
        self.process(cmdline)  # noqa
        # ---------------------------------------------------------------------

        self.check(200, backup_prefix="runner-200-start-time", after_verify_album=True)

        abs_rem = self.home_config['remote-thumbnails'] + '/' + offset

        self.assert_no_file(f"tests/results/ALBUM/{offset}/2023/2023-06-Juin-17-Armor-cup/local-copy-of-45.jpg")
        self.assert_no_remote_file(f"{abs_rem}/2023/2023-06-Juin-17-Armor-cup/local-copy-of-45.jpg")

        self.clean_remote_tmp(200)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_561(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('------------ Starting tests for --verify-album, album: remote')
        LOGGER.test_msg('')
        LOGGER.test_msg('sources/VIDEO -> ALBUM=remote, THUMBNAILS=home')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        if not self.home_config['remote-album']:
            LOGGER.test_msg("Empty test because no 'remote-album' configuration")
            self.done(mn, ok=False)
            return

        ACTOR.configure(self.home_config)  # enable ssh for the test harness

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({},
                                          set_thumbnails='home',
                                          set_album='remote',
                                          set_auto_config="local",
                                          enable_database=False,
                                          offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"},
        ])

        self.copy_video(vector)

        # ----------------------------------------------------------------
        main = self.process(cmdline)
        # ----------------------------------------------------------------

        self.check(561, main.start_time, vector)

        LOGGER.test_msg('')
        LOGGER.test_msg(f'------- end of {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_599(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('Cleaning program 5XX with --remote-album')
        LOGGER.test_msg('So, this test requires a real database ')

        ACTOR.configure(self.home_config)  # enable db access for the test harness
        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({},
                                          set_thumbnails='home',
                                          set_album='remote',
                                          set_auto_config='local',
                                          enable_database=False,
                                          offset=offset)

        self.vectors[599] = PwpVector(cmdline, [])

        self.clean_remote_tmp(599)

        LOGGER.test_msg('')
        LOGGER.test_msg(f'------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    # ---------------------------------------------------------------------
    # Programs that test the database management
    # ---------------------------------------------------------------------

    def program_600(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('test SQL')

        ACTOR.configure(self.home_config)  # enable db access for the test harness

        if not ACTOR.sql_connection:
            LOGGER.test_msg('NO database configuration, aborting')
            self.done(mn, ok=False)
            return

        ACTOR.rmtree("tests/results")
        # no need to set a unique id, nor to clean tmp
        ACTOR.copy("tests/sources/piwiPre-to-tmp.ini", "tests/results/piwiPre.ini")

        pwp_main(['--base', 'tests/results',
                  '--gui', 'false',
                  '--test-sql',
                  '--enable-database', 'true'])

        self.assert_not_info("SQL ERROR")
        self.assert_trace("test-sql OK")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_601(self, clean_at_end=True):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn} Clean_at_end = {clean_at_end}')
        LOGGER.test_msg('testing --enable-database, including md5 computation and insertion')
        LOGGER.test_msg('So, this test requires a real database, to be configured in HOME ')

        album = self.home_config['album']
        thumbnails = self.home_config['thumbnails']

        ACTOR.configure(self.home_config)  # enable db access for the test harness

        if not ACTOR.sql_connection:
            LOGGER.test_msg('NO database configuration, aborting')
            self.done(mn, ok=False)
            return

        if not (album and thumbnails):
            LOGGER.test_msg('NO album or thumbnails configuration, aborting')
            self.done(mn, ok=False)
            return

        ACTOR.rmtree("tests/results")
        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({}, set_thumbnails='home', set_album='home', set_auto_config='home',
                                          enable_database=True, offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"},
            {'in-source': "GPS/2023-02-19-11h38-23-Plouhinec.jpg",  # noqa
             'in-triage': "test/picture-with-gps.jpg",
             'in-album': "2023/2023-02-Février-19-test/2023-02-19-11h38-23-test.jpg",  # noqa
             'md5sum': '5021904b830ccca656c32410edc3acc0',
             "latitude": "47.988561",
             "longitude": "-4.478702",
             'orientation': '1'}
        ])

        self.copy_armor(vector)
        # 20230617_110544-bis.jpg   -> Armor-0  -> 2023-06-17-11h05-44-Armor-cup
        # 20230617_110544           -> Armor-1  -> 2023-06-17-11h05-45-Armor-cup
        # 20230617_110544           -> Armor-2  -> 2023-06-17-11h05-45-Armor-cup
        # ----------------------------------------------------------------
        main = self.process(cmdline)
        # ----------------------------------------------------------------

        self.check(601, main.start_time, vector)

        self.assert_file(f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg")  # noqa

        LOGGER.test_msg('')
        LOGGER.test_msg('Step 1 OK: files generated')
        LOGGER.test_msg('')

        # now, we modify the picture in album:
        ACTOR.copy("tests/sources/ROTATED/20230617_110544.jpg",
                   f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg")  # noqa

        # Rot                       ->          -> 2023-06-17-11h05-44-Armor-cup

        # ----------------------------------------------------------------
        self.database_synchronize(f'{album}/{offset}/2023')
        # ----------------------------------------------------------------

        # DB information about the modified file has been updated
        md5_44_rot = 'cf599fb7279f4886506d386d50493552'  # previous 'd2464dff83b4847229c81938c0e21718'
        sql_name = f"/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "width", "1800")
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_44_rot)

        # DB information about the unmodified file has been kept,
        md5_23 = '5021904b830ccca656c32410edc3acc0'
        sql_name = f"/{offset}/2023/2023-02-Février-19-test/2023-02-19-11h38-23-test.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "latitude", "47.988561")
        self.assert_db_file_field(sql_name, bd_info, "longitude", "-4.478702")
        self.assert_db_file_field(sql_name, bd_info, "author", "Agnes BATTINI")
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_23)

        if clean_at_end:
            self.clean_remote_tmp(601)
            # here: self.done(mn) is NOT executed, so that program_602 knows that 601 must be done again
        else:
            LOGGER.test_msg(' Not cleaning due to next tests')
            self.done(mn)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

    def program_602(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree
        ACTOR.configure(self.home_config)  # enable db access for the test harness

        if not ACTOR.sql_connection:
            LOGGER.test_msg('NO database configuration, aborting')
            self.done(mn, ok=False)
            return

        if not self.check_done('program_601', 601):
            self.program_601(clean_at_end=False)

        offset = self.get_vector_uid(601)

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('testing --enable-database : delete/add files/directories')
        LOGGER.test_msg('This test is always executed after program_601, without cleaning')
        LOGGER.test_msg('')
        LOGGER.test_msg('CAVEAT: Here, we test the MD5 of JPEG files, which obviously depend on JPEG algo details ')
        LOGGER.test_msg('so, it is PROBABLE that the MD5 change if the JPEG library changes')
        LOGGER.test_msg('it would be great to remove this dependency but this is NOT done')
        LOGGER.test_msg('so, if the JPEG implementation changes, one HAS TO change the md5 values !')
        LOGGER.test_msg('')
        # TODO: MD5 sums are computed (vs cst), so that we can change the JPEG algo without manually changing the md5

        self.reset_done('program_601')
        album = self.home_config['album']

        # delete/add files/dirs to /tmp/2023 WITHOUT synchronization

        ACTOR.copy("tests/sources/PICTURES/Armor-cup/20230617_110544-bis.jpg",
                   "tests/results/TRIAGE/Armor-cup/Armor-1.jpg")
        ACTOR.copy("tests/sources/PICTURES/Armor-cup/20230617_110544.jpg",
                   "tests/results/TRIAGE/Armor-cup/Armor-2.jpg")

        ACTOR.delete("tests/results/TRIAGE/Armor-cup/Armor-0.jpg")

        # what we had:
        # Rot                       ->          -> 2023-06-17-11h05-44-Armor-cup
        # 20230617_110544           ->          -> 2023-06-17-11h05-45-Armor-cup
        # what we add:
        # 20230617_110544-bis       ->  Armor-1 -> 2023-06-17-11h05-46-Armor-cup
        # 20230617_110544           ->  Armor-2 -> 2023-06-17-11h05-44-Armor-cup

        cmdline = self.build_test_cmdline({'--album': album,
                                           '--enable-database': self.home_config['enable-database'], })
        # ----------------------------------------------------------------
        self.process(cmdline)
        # ----------------------------------------------------------------

        # verify the new files in TRIAGE were detected and inserted completely in db

        self.assert_file(f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg")  # noqa
        self.assert_file(f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg")  # noqa
        self.assert_file(f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg")  # noqa
        # following file should NOT be created, because it would mean 2 identical files not detected
        self.assert_no_file(
            f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-47-Armor-cup.jpg")  # noqa

        # this one has not changed
        md5_44_rot = 'cf599fb7279f4886506d386d50493552'  # previous 'd2464dff83b4847229c81938c0e21718'
        sql_name = f"/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-44-Armor-cup.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_44_rot)
        # New file

        md5_45 = '89aade70e5a7b883b3a6b0dfb64eaa8e'  # Previous: 'd181b3d94bb20487d4e9d6faa72b64a8',
        sql_name = f"/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)

        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_45)

        # 20230617_110544-bis
        md5_46 = 'c5b83eee39ef237ab42a473b1139c540'  # previous: 'aa8fe00349ca160e8bf0f88f45f5cea7'
        sql_name = f"/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_46)

        # this one has not changed
        md5_23 = '5021904b830ccca656c32410edc3acc0'
        sql_name = f"/{offset}/2023/2023-02-Février-19-test/2023-02-19-11h38-23-test.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_23)

        #
        # a new modification on the album
        #
        ACTOR.mkdirs(f"{album}/{offset}2023/foo")
        ACTOR.move(f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg",  # noqa
                   f"{album}/{offset}/2023/foo/2023-06-17-11h05-45-test.jpg")

        # ----------------------------------------------------------------
        self.database_synchronize(f"{album}/{offset}/2023")
        # ----------------------------------------------------------------

        # next file has been removed from db because moved to a different directory
        self.assert_db_no_file(f"/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-45-Armor-cup.jpg")  # noqa

        # next file has been created in db, with same data than previous location

        sql_name = f"/{offset}/2023/foo/2023-06-17-11h05-45-test.jpg"
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_45)

        # we should have in tmp:
        # 2023-02-Février-19-Armor-cup        # noqa
        # 2023-06-Juin-17-test                # noqa
        # test
        self.assert_db_dir_field(f"/{offset}/2023/foo", "rank", "3")

        ACTOR.mkdirs(f"{album}/{offset}/2023/bah")

        ACTOR.move(f"{album}/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg",  # noqa
                   f"{album}/{offset}/2023/bah/2023-06-17-11h05-46-test.jpg")

        # ----------------------------------------------------------------
        self.database_synchronize(f"{album}/{offset}/2023")
        # ----------------------------------------------------------------

        # next file has been removed from db
        self.assert_db_no_file(f"/{offset}/2023/2023-06-Juin-17-Armor-cup/2023-06-17-11h05-46-Armor-cup.jpg")  # noqa
        # foo rank has been changed due to bah arrival
        self.assert_db_dir_field(f"/{offset}/2023/foo", "rank", "4")
        # bah has been created in db    # noqa
        self.assert_db_dir_field(f"/{offset}/2023/bah", "rank", "3")

        sql_name = f"/{offset}/2023/bah/2023-06-17-11h05-46-test.jpg"
        bd_info = ACTOR.sql_get_file_info(sql_name)
        self.assert_db_file_field(sql_name, bd_info, "md5sum", md5_46)

        ACTOR.rmtree(f"{album}/{offset}/2023/bah")

        # ----------------------------------------------------------------
        self.database_synchronize(f"{album}/{offset}/2023")
        # ----------------------------------------------------------------

        self.assert_db_dir_field(f"/{offset}/2023/foo", "rank", "3")
        # next file has been removed from db
        self.assert_db_no_file(f"/{offset}/2023/bah/2023-06-17-11h05-46-test.jpg")
        # bah has been removed from db       # noqa
        self.assert_db_no_dir(f"/{offset}/2023/bah")

        self.clean_remote_tmp(601)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_610(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('testing --enable-database, with video files')
        LOGGER.test_msg('So, this test requires a real database ')
        LOGGER.test_msg('')
        LOGGER.test_msg('Verifies renaming, copyright, author, special')
        LOGGER.test_msg('with .mp4, .avi')
        LOGGER.test_msg('')
        ACTOR.rmtree("tests/results")

        album = self.home_config['album']
        thumbnails = self.home_config['thumbnails']
        remote_thumbnails = None  # self.home_config['remote-thumbnails']
        ACTOR.configure(self.home_config)  # enable db access for the test harness

        if not ACTOR.sql_connection:
            LOGGER.test_msg('NO database configuration, aborting')
            self.done(mn, ok=False)
            return

        LOGGER.test_msg(f"album         = {album}")
        LOGGER.test_msg(f"thumbnails           = {thumbnails}")

        ACTOR.mkdirs("tests/results/TRIAGE/test")
        ACTOR.rmtree("tests/results")

        offset = self.get_unique_id()
        cmdline = self.build_test_cmdline({},
                                          set_thumbnails='home',
                                          set_album='home',
                                          set_auto_config='home',
                                          enable_database=True, offset=offset)

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-to-tmp.ini", 'in-results': "piwiPre.ini"},
        ])

        self.copy_video(vector)

        # ----------------------------------------------------------------
        main = self.process(cmdline)
        # ----------------------------------------------------------------

        self.check(610, main.start_time, vector)

        sql_name = f"/{offset}/2007/2007-04-Avril-03-test/2007-04-03-18h04-24-test.mp4"
        bd_info = ACTOR.sql_get_file_info(sql_name)
        # self.assert_db_file_field(sql_name, bd_info, "md5sum", "d73bdd14b06a9394e2df693a22ca3e80")
        # we cannot test the md5sum of mp4 files, because it depends heavily on the encoder!
        self.assert_db_file_field(sql_name, bd_info, "width", "320")
        self.assert_db_file_field(sql_name, bd_info, "height", "240")
        self.assert_db_file_field(sql_name, bd_info, "author", "Famille BATTINI")
        self.assert_db_file_field(sql_name, bd_info, "representative_ext", "jpg")

        sql_name = f"/{offset}/2023/2023-01-Janvier-27-test/2023-01-27-17h59-39-test.mp4"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        # self.assert_db_file_field(sql_name, bd_info, "md5sum", "2b360bae6fa663ce5041edd21b36b4a1")
        # we cannot test the md5sum of mp4 files, because it depends heavily on the encoder!
        self.assert_db_file_field(sql_name, bd_info, "width", "1080")
        self.assert_db_file_field(sql_name, bd_info, "height", "1920")
        self.assert_db_file_field(sql_name, bd_info, "author", "Famille BATTINI")
        self.assert_db_file_field(sql_name, bd_info, "representative_ext", "jpg")

        sql_name = f"/{offset}/2007/2007-04-Avril-03-test/pwg_representative/2007-04-03-18h04-24-test.jpg"
        bd_info = ACTOR.sql_get_file_info(sql_name)
        # self.assert_db_file_field(sql_name, bd_info, "md5sum", "38a514c4e10f90c60ea0c85d12f2f7cb")
        # we cannot test the md5sum of mp4 files, because it depends heavily on the encoder!
        self.assert_db_file_field(sql_name, bd_info, "width", "320")
        self.assert_db_file_field(sql_name, bd_info, "height", "240")
        self.assert_db_file_field(sql_name, bd_info, "author", "Famille BATTINI")
        self.assert_db_file_field(sql_name, bd_info, "representative_ext", "NULL")

        sql_name = f"/{offset}/2023/2023-01-Janvier-27-test/pwg_representative/2023-01-27-17h59-39-test.jpg"  # noqa
        bd_info = ACTOR.sql_get_file_info(sql_name)
        # self.assert_db_file_field(sql_name, bd_info, "md5sum", "a9a52e50722075b853a2a520614a18c1")
        # we cannot test the md5sum of mp4 files, because it depends heavily on the encoder!
        self.assert_db_file_field(sql_name, bd_info, "width", "1080")
        self.assert_db_file_field(sql_name, bd_info, "height", "1920")
        self.assert_db_file_field(sql_name, bd_info, "author", "Famille BATTINI")
        self.assert_db_file_field(sql_name, bd_info, "representative_ext", "NULL")

        if thumbnails[0] != '/':
            # album is a path relative to cwd, which was changed to 'tests/results'
            thumbnails = 'tests/results/' + thumbnails

        self.assert_thumbnail(thumbnails, remote_thumbnails,
                              f"/{offset}/2023/2023-01-Janvier-27-test/pwg_representative/" +  # noqa
                              "2023-01-27-17h59-39-test-me.jpg")
        self.assert_thumbnail(thumbnails, remote_thumbnails,
                              f"/{offset}/2023/2023-01-Janvier-27-test/pwg_representative/" +  # noqa
                              "2023-01-27-17h59-39-test-th.jpg")
        self.assert_thumbnail(thumbnails, remote_thumbnails,
                              f"/{offset}/2023/2023-01-Janvier-27-test/pwg_representative/" +  # noqa
                              "2023-01-27-17h59-39-test-sq.jpg")
        self.assert_thumbnail(thumbnails, remote_thumbnails,
                              f"/{offset}/2023/2023-01-Janvier-27-test/pwg_representative/" +  # noqa
                              "2023-01-27-17h59-39-test-cu_e250.jpg")
        LOGGER.test_msg('')
        LOGGER.test_msg(f'------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_699(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('Cleaning program 6XX with --enable-database, including md5 computation and insertion')
        LOGGER.test_msg('So, this test requires a real database ')

        if not self.check_done('program_610', 610):
            self.program_610()

        # at least, we do 610, and we are sure to clean whatever remains in tmp

        if not ACTOR.sql_connection:
            LOGGER.test_msg('NO database configuration, aborting')
            self.done(mn, ok=False)
            return

        ACTOR.configure(self.home_config)  # enable db access for the test harness

        if 610 in self.vectors:
            self.clean_remote_tmp(610)

        LOGGER.test_msg('')
        LOGGER.test_msg(f'------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_700(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        if not ACTOR.sql_connection:
            LOGGER.test_msg('NO database configuration, aborting')
            self.done(mn, ok=False)
            return

        LOGGER.test_msg(f'--------------- starting {mn}')
        #  LOGGER.test_msg('Here, we assume filename format = {Y}-{m}-{month_name}-{d}-{base}-{count}.{suffix}')

        ACTOR.configure(self.home_config)  # enable db access for the test harness

        dir_to_test = "1973"  # [1973-2023] #
        restart_dir = "2023/2023-06-Juin-17-Armor-Cup"  # noqa

        # "2019/2019-02-Fevrier-13-Thèse-Muriel" # noqa
        # "2009/2009-12-Decembre-11-AlineJulienAurelie" # noqa

        # change this to whatever directory you want to test in real-life

        LOGGER.test_msg(f"This is a real-life test, dir='{dir_to_test}' restart='{restart_dir}'")
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")

        target = self.get_first_album(default=dir_to_test)
        if target != dir_to_test:
            LOGGER.test_msg(f"verifying first album '{target}' because '{dir_to_test}' does not exist")
        if target is None:
            LOGGER.test_msg(f"album '{dir_to_test}' is empty, no test to do")
            self.done(mn, ok=False)
            return

        album = self.home_config['album']
        LOGGER.test_msg(f"verifying  '{album}/{target}' ")
        pwp_main(['--triage', 'None',  # '--debug',
                  '--gui', 'false',
                  '--base', 'tests/results',
                  '--verify-album', f"{album}/{target}",
                  '--enable-verify-sub-album', 'true',
                  '--restart-from-dir', restart_dir,
                  '--enable-thumbnails', 'true',
                  '--enable-thumbnails-delete', 'true',
                  '--enable-metadata', 'true',
                  '--enable-rotation', 'true',
                  '--enable-database', 'true',

                  # '--stop-on-warning', 'true', # being paranoid
                  '--enable-date-in-filename', 'true',
                  '--enable-rename', 'false',
                  '--enable-metadata-reset', 'false',  # CAVEAT: set to true forces modifying metadata
                  # '--enable-remote-thumbnails', 'false'  # no reason the change this. it MUST be set in HOME!
                  ])

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')

        self.done(mn)

    def program_905(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('auto-test of pwpInstaller without gui ')

        if platform.system() != "Windows":
            LOGGER.test_msg("Runs only on Windows systems, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        # ------------------------------------------------------------
        initial_cwd = os.getcwd()

        run_installer(["--mode", "test",
                       "--piwipre", "--ffmpeg", "--mariadb",
                       "--elevation", 'false',
                       "--gui", "false",
                       "--home", os.getcwd() + "/tests/results/HOME",
                       "--appdata", os.getcwd() + "/tests/results/APPDATA",
                       "--program-files", os.getcwd() + "/tests/results/PROGRAMFILES",  # noqa
                       "--chdir", os.getcwd() + "/tests/results"])

        os.chdir(initial_cwd)
        # ------------------------------------------------------------

        self.assert_file("tests/results/ffmpeg/bin/ffmpeg.exe")
        self.assert_file("tests/results/ffmpeg/bin/ffprobe.exe")

        self.assert_file("tests/results/piwiPre/piwiPre.exe")
        self.assert_file("tests/results/piwiPre/piwiPreGui.lnk")
        self.assert_file("tests/results/piwiPre/pwpInstaller.exe")
        self.assert_file("tests/results/piwiPre/pwpInstallerGui.lnk")

        self.assert_file("tests/results/mariadb.msi")

        self.assert_file("tests/results/Microsoft/Windows/Start Menu/Programs/piwiPre/piwiPre.lnk")
        self.assert_file("tests/results/Microsoft/Windows/Start Menu/Programs/piwiPre/pwpInstaller.lnk")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_906(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('auto-test of pwpInstaller WITH gui')

        if not PwpGui.tk_available():
            LOGGER.test_msg("Requires Tk, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        # ------------------------------------------------------------
        initial_cwd = os.getcwd()

        run_installer(["--mode", "test",
                       "--piwipre", "--ffmpeg", "--mariadb",
                       "--elevation", 'false',
                       "--gui", "true",
                       "--chdir", os.getcwd() + "/tests/results"])

        os.chdir(initial_cwd)
        # ------------------------------------------------------------
        # self.assert_file("tests/results/ffmpeg/bin/ffmpeg.exe")
        # self.assert_file("tests/results/ffmpeg/bin/ffprobe.exe")

        self.assert_file("tests/results/piwiPre/piwiPre.exe")
        self.assert_file("tests/results/piwiPre/piwiPreGui.lnk")
        self.assert_file("tests/results/piwiPre/pwpInstaller.exe")
        self.assert_file("tests/results/piwiPre/pwpInstallerGui.lnk")

        # self.assert_file("tests/results/mariadb.msi")

        self.assert_file("tests/results/Microsoft/Windows/Start Menu/Programs/piwiPre/piwiPre.lnk")
        self.assert_file("tests/results/Microsoft/Windows/Start Menu/Programs/piwiPre/pwpInstaller.lnk")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_907(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('auto-test of Configurator +/- gui')

        initial_cwd = os.getcwd()

        # ------------------------------------------------------------
        LOGGER.test_msg('')
        LOGGER.test_msg('test 0 : --gui false, modify "tests/results/HOME/piwiPre.ini" ')
        LOGGER.test_msg('')

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")

        ACTOR.copy("tests/sources/piwiPre-local.ini", "tests/results/HOME/.piwiPre.ini")

        # Let's modify config file in "HOME"
        pwp_main(arguments=[
            '--gui', False,
            '--quiet', 'true',
            '--base', os.getcwd() + "/tests/results/BASE",
            '--enable-create-base', 'true',
            "--home", os.getcwd() + "/tests/results/HOME",],
            test_scenario=[("choose dir", "../HOME"),     # paths are relative to BASE
                           ("album-setup", 'local'),
                           ("thumbnails-setup", 'local'),
                           ("set ssh-host", "a different ssh host"),
                           ("shortcuts",),
                           ("save",),
                           ("exit",),
                           ])

        os.chdir(initial_cwd)
        self.assert_file("tests/results/HOME/.piwiPre.ini")
        # HOME config contains the original data
        self.assert_file_contains("tests/results/HOME/.piwiPre.ini", "album : ALBUM")
        # HOME config contains the modified data
        self.assert_file_contains("tests/results/HOME/.piwiPre.ini", "ssh-host : 'a different ssh host'")

        self.assert_no_file("tests/results/HOME/piwiPreCmd.bat")
        self.assert_no_file("tests/results/HOME/piwiPreGui.lnk")
        self.assert_no_file("tests/results/HOME/piwiPreCmd.sh")
        self.assert_no_file("tests/results/HOME/piwiPreGui.sh")

        # ------------------------------------------------------------
        LOGGER.test_msg('')
        LOGGER.test_msg('test 1 : --gui false, generate "tests/results/BASE/piwiPre.ini" ')
        LOGGER.test_msg('')

        # Let's modify config file in "/BASE"
        pwp_main(arguments=[
            '--gui', False,
            '--quiet', 'true',
            '--base', os.getcwd() + "/tests/results/BASE",
            '--enable-create-base', 'true',
            "--home", os.getcwd() + "/tests/results/HOME", ],
            test_scenario=[("choose dir", "."),
                           ("album-setup", 'local'),
                           ("thumbnails-setup", 'local'),
                           ("set album", "//NAS/Photos"),
                           ("set thumbnails", "ALT-THUMBNAILS"),
                           ("set ssh-user", "my-ssh-user-name"),
                           ("shortcuts",),
                           ("save",),
                           ("exit",),
                           ])
        # Test scenario changes :
        # album: ALBUM --> "//NAS/Photos"
        # thumbnails: THUMBNAILS --> "ALT-THUMBNAILS"

        os.chdir(initial_cwd)
        # ------------------------------------------------------------

        self.assert_file("tests/results/BASE/piwiPre.ini")
        self.assert_file_contains("tests/results/BASE/piwiPre.ini", "album : '//NAS/Photos'")
        self.assert_file_not_contains("tests/results/BASE/piwiPre.ini", "thumbnails : 'THUMBNAILS'")
        self.assert_file_contains("tests/results/BASE/piwiPre.ini", "ssh-user : 'my-ssh-user-name'")
        # we do not want to see in the ini file settings inherited from HOME/.piwiPre.ini
        self.assert_file_not_contains("tests/results/BASE/piwiPre.ini", "enable-database: false")

        if platform.system() == "Windows":
            self.assert_file("tests/results/BASE/piwiPreCmd.bat")
            self.assert_file("tests/results/BASE/piwiPreGui.lnk")
        else:
            self.assert_file("tests/results/BASE/piwiPreCmd.sh")
            self.assert_file("tests/results/BASE/piwiPreGui.sh")

        dest = ACTOR.linux_path(os.path.abspath('tests/results/HOME'))
        self.assert_trace(f"Saved last run location in {dest}/.piwiPre.last")
        LOGGER.test_msg('test 1 : OK ')

        # ------------------------------------------------------------
        LOGGER.test_msg('')
        LOGGER.test_msg('test 2 : ')
        LOGGER.test_msg('       verify "tests/results/BASE/piwiPre.ini" can be read')
        LOGGER.test_msg('       by doing dump-config in tests/results/BASE/TRIAGE/subdir')
        LOGGER.test_msg('')

        initial_cwd = os.getcwd()

        ACTOR.mkdirs("tests/results/BASE/TRIAGE/subdir")
        pwp_main(arguments=[
            '--gui', False,
            '--quiet', 'true',
            '--base', os.getcwd() + "/tests/results/BASE",
            '--enable-create-base', 'true',
            "--home", os.getcwd() + "/tests/results/HOME",],
            test_scenario=[("choose dir", "."),  # aka BASE
                           ("album-setup", 'local'),
                           ("thumbnails-setup", 'local'),
                           ("set album", "ALT-ALBUM"),
                           ("shortcuts",),
                           ("save",),
                           ("choose dir", "TRIAGE/subdir"),  # aka BASE
                           ("set piwigo-user", "my-piwigo-user-name"),
                           ("save",),
                           ("exit",),
                           ])

        os.chdir(initial_cwd)
        # ------------------------------------------------------------

        # verify that settings from TRIAGE/subdir are NOT wrongly dumped in BASE
        self.assert_file_not_contains("tests/results/BASE/piwiPre.ini",
                                      "piwigo-user : 'my-piwigo-user-name'")

        # now, let's see how the configuration is computed in TRIAGE/subdir
        # ------------------------------------------------------------
        main = pwp_main(arguments=[
            '--quiet', 'true',
            '--base', os.getcwd() + "/tests/results/BASE",
            "--home", os.getcwd() + "/tests/results/HOME",
            '--dump-config', "TRIAGE/subdir",
            "--gui", "false"])

        os.chdir(initial_cwd)
        # ------------------------------------------------------------

        self.assert_config(main.dumped_config, "copyright", "(C) {Y} by {author}, for test")  # set in HOME
        self.assert_config(main.dumped_config, "thumbnails", "ALT-THUMBNAILS")  # set in BASE
        self.assert_config(main.dumped_config, "album", "ALT-ALBUM")   # Set BASE
        self.assert_config(main.dumped_config, "piwigo-user", "my-piwigo-user-name")   # Set here

        LOGGER.test_msg('test 2 : OK ')

        # ------------------------------------------------------------
        LOGGER.test_msg('test 3 : --gui true --not-a-flag true ')
        LOGGER.test_msg('       + small test of the GUI ')
        initial_cwd = os.getcwd()

        if not PwpGui.tk_available():
            LOGGER.test_msg("test 3 Requires Tk, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        pwp_main(arguments=[
            '--quiet', 'true',
            '--base', os.getcwd() + "/tests/results/BASE",
            "--home", os.getcwd() + "/tests/results/HOME",
            "--gui", "true",
            "--test-gui-dismiss-errors", "true",
            '--not-a-flag', 'true',
        ],
            test_scenario=[
                ("start GUI test",),
                ("gui error dismiss", ),
                ("gui change parameters",),

                ("gui config", "base"),
                ("gui modify multilevel string", 'ssh-user'),
                ("gui choose multilevel", 'ssh-user'),

                ("gui modify_settings invoke",),
                ("gui settings_ui undo",),
                ("gui settings_ui set", "LOCAL", "LOCAL"),

                ("gui show-hide info", "album"),

                ("gui modify multilevel string", 'album'),
                ("gui dir-chooser enter", "[..]"),
                ("gui dir-chooser select", "ALBUM"),

                ("gui modify multilevel string", 'thumbnails'),
                ("gui dir-chooser enter", "[..]"),
                ("gui dir-chooser select", "THUMBNAILS"),

                ("gui run",),
                ("gui exit",),
            ])

        os.chdir(initial_cwd)
        LOGGER.test_msg('test 3 : OK . The .ini in BASE and HOME are safely read')
        # ------------------------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_908(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('auto-test of piwiPre GUI, with automated test ')
        cmdline = self.build_test_cmdline({'--language': 'fr'})  # purely local
        # CAVEAT: this cmdline is used ONLY to build the vector, not used to run pwp_main

        if not PwpGui.tk_available():
            LOGGER.test_msg("Requires Tk, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-alt.ini", 'in-results': "piwiPre.ini"},
        ])
        # differences between piwiPre-local.ini and piwiPre-alt.ini
        #                     album: ALBUM            -> LOCAL-ALBUM
        #                     thumbnails: THUMBNAILS  -> LOCAL-THUMBNAILS

        ACTOR.mkdirs("tests/results/ALBUM")  # Build it to ease selection in UI
        ACTOR.mkdirs("tests/results/THUMBNAILS")  # Build it to ease selection in UI
        self.copy_armor(vector)
        for vect in vector.items:
            if "copyright" in vect.data:
                del vect.data["copyright"]
            if "special" in vect.data:
                del vect.data["special"]
            if "size" in vect.data:
                del vect.data["size"]

        initial_cwd = os.getcwd()

        # --------------------------------
        # CAVEAT: we do NOT reuse cmdline, so that ALBUM is not set by build_test_cmdline
        main = pwp_main([
            '--language', 'fr',
            '--gui', 'true',
            # '--debug', 'true',
            '--enable-remote-thumbnails', 'false',
            '--enable-remote-album', 'false',
            '--remote-thumbnails', None,
            '--remote-auto-config', None,
            '--remote-album', None,
            "--test-gui-dismiss-errors", "true",
            '--not-a-flag', 'true',
            '--base', 'tests/results'],
            test_scenario=[
                ("start GUI test",),
                ("gui change parameters",),

                ("gui config", "base"),
                ("gui modify multilevel string", 'ssh-user'),
                ("gui choose multilevel", 'ssh-user'),

                ("gui modify_settings invoke",),
                ("gui settings_ui undo",),
                ("gui settings_ui set", "LOCAL", "LOCAL"),

                ("gui show-hide info", "album"),

                ("gui modify multilevel string", 'album'),
                ("gui dir-chooser enter", "[..]"),
                ("gui dir-chooser select", "ALBUM"),

                ("gui modify multilevel string", 'thumbnails'),
                ("gui dir-chooser enter", "[..]"),
                ("gui dir-chooser select", "THUMBNAILS"),

                ("gui run",),
                ("gui exit",),
            ])
        # --------------------------------

        os.chdir(initial_cwd)
        # check will verify that pwiPre has been executed with album=ALBUM and thumbnails=THUMBNAILS,
        # which have been set on the GUI (by scenario), but not saved.
        self.check(908, main.start_time, vector)
        self.assert_file_contains("tests/results/piwiPre.ini",
                                  "album: LOCAL-ALBUM")
        self.assert_file_contains("tests/results/piwiPre.ini",
                                  "thumbnails: LOCAL-THUMBNAILS")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_2106(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('program_906 then program_908')
        self.program_906()
        self.program_908()
        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_909(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        initial_cwd = os.getcwd()
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('test RUN from the UI with config items modified and not saved ')

        cmdline = self.build_test_cmdline({})  # purely local

        # The same test as program_30
        # instead of using piwiPre-local.ini, we use piwiPre-dates.ini,
        # and we change the values on the command-line :
        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-local.ini", 'in-results': "piwiPre.ini"},
            ])
        ACTOR.move("tests/results/piwiPre.ini", "tests/results/piwiPre.ini.bak")
        with open("tests/results/piwiPre.ini.bak", 'r') as in_file:
            with open("tests/results/piwiPre.ini", 'w') as outs:
                content = in_file.readlines()
                for line in content:
                    if line.startswith('copyright : '):
                        line = "copyright : '(C) for test {Y} Modified to generate errors'\n"
                    outs.writelines(line)

        self.copy_armor(vector)

        # --------------------------------
        main = pwp_main(arguments=[
            '--quiet', 'true',
            '--gui', "false",
            '--base', os.getcwd() + "/tests/results",],
            test_scenario=[("choose dir", "."),  # aka BASE
                           ("set copyright", "(C) {Y} by {author}, for test"),
                           ("run-with-gui-config",),
                           ("exit",),
                           ])

        # --------------------------------
        # check will verify the copyright is "(C) 2023 by Agnes BATTINI, for test"
        self.check(909, main.start_time, vector)

        os.chdir(initial_cwd)
        # verify the ini file HAS not been modified
        self.assert_file_not_contains("tests/results/piwiPre.ini",
                                      "copyright : '(C) {Y} by {author}, for test'")
        self.assert_file_contains("tests/results/piwiPre.ini",
                                  "copyright : '(C) for test {Y} Modified to generate errors'")

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_910(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        initial_cwd = os.getcwd()
        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results/HOME")
        ACTOR.mkdirs("tests/results/BASE")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('test RUN from the UI with empty BASE, empty HOME, no thumbnails ')

        cmdline = self.build_test_cmdline({
            '--quiet': 'true',
            '--language': 'fr',
            '--base': initial_cwd + "/tests/results/BASE",
            '--home': initial_cwd + "/tests/results/HOME",
        })  # used ONLY to set up vector

        # The same test as program_30
        # without any .ini
        # and we change the values on the command-line :
        vector = PwpVector(cmdline, [])
        self.copy_armor(vector)

        # TODO: (low interest) copy_armor etc take into account the value of TRIAGE, so that next lines are useless
        # patching vector to get TRIAGE in BASE, see also program_7
        ACTOR.move(initial_cwd + "/tests/results/TRIAGE",
                   initial_cwd + "/tests/results/BASE/TRIAGE")
        for vect in vector.items:
            vect.in_triage = vect.in_triage.replace("TRIAGE", "BASE/TRIAGE")
            vect.in_album = vect.in_album.replace("ALBUM", "BASE/ALBUM")
            if "author" in vect.data:
                del vect.data["author"]
            if "copyright" in vect.data:
                del vect.data["copyright"]
            if "special" in vect.data:
                del vect.data["special"]
            if "size" in vect.data:
                del vect.data["size"]
            vect.thumbs = []

        # --------------------------------
        main = pwp_main(arguments=[
            '--quiet', 'true',
            '--gui', 'false',
            '--language', 'fr',
            '--base', initial_cwd + "/tests/results/BASE",
            '--home', initial_cwd + "/tests/results/HOME",],
            test_scenario=[("choose dir", "."),  # aka BASE
                           ("set copyright", "(C) {Y} by {author}, for test"),
                           ("thumbnails-setup", "unused"),
                           ("run-with-gui-config",),
                           ("exit",),
                           ])
        # ----------------------------------------------------

        os.chdir(initial_cwd)
        # --------------------------------
        # check will verify the pictures are computed, but we do not do fully the test
        self.check(910, main.start_time, vector)
        self.assert_dir("tests/results/BASE/BACKUP")
        self.assert_no_dir("tests/results/BASE/THUMBNAILS")     # we said thumbnails = unused

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_911(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('Automated test of piwiPre GUI, scenario similar to 211, with different directories ')
        LOGGER.test_msg('piwiPre started by pwpInstaller on an empty BASE and empty HOME')
        LOGGER.test_msg('Verify we can create BASE, create its .ini ')
        LOGGER.test_msg('Populate TRIAGE without sub-folders')
        LOGGER.test_msg('Run piwiPre, which creates day-based directories in ALBUM')
        LOGGER.test_msg('Rename the directories')
        LOGGER.test_msg('Run piwiPre again with --verify-album')
        LOGGER.test_msg('and assert files were correctly managed')
        LOGGER.test_msg('')

        if not PwpGui.tk_available():
            LOGGER.test_msg("Requires Tk, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        ACTOR.rmtree('tests/results')
        ACTOR.mkdirs("tests/results/HOME")

        # ACTOR.copy("tests/sources/piwiPre-local.ini", "tests/results/HOME/.piwiPre.ini")

        def build_pattern():
            # CWD should be /tests/results/BASE when we run this
            ACTOR.copy("../../sources/PICTURES/Vendée/IMG20230702144522.jpg",
                       "../../results/BASE/TRIAGE/IMG20230702144522.jpg")
            ACTOR.copy("../../sources/PICTURES/Vendée/IMG20230704125307.jpg",
                       "../../results/BASE/TRIAGE/IMG20230704125307.jpg")

        def move_files():
            # CWD should be /tests/results/BASE when we run this
            ACTOR.rmtree('../../results/BASE/ALBUM/2023/Chemin')
            ACTOR.rmtree('../../results/BASE/ALBUM/2023/BBQ')
            ACTOR.rmtree('../../results/BASE/ALBUM/2023/2023-07-Juillet-02-Chemin')
            ACTOR.rmtree('../../results/BASE/ALBUM/2023/2023-07-Juillet-04-BBQ')
            ACTOR.copytree('../../results/BASE/ALBUM/2023/2023-07-Juillet-02-TRIAGE',
                           '../../results/BASE/ALBUM/2023/Chemin')
            ACTOR.copytree('../../results/BASE/ALBUM/2023/2023-07-Juillet-04-TRIAGE',
                           '../../results/BASE/ALBUM/2023/2023-07-Juillet-04-BBQ')
            ACTOR.rmtree('../../results/BASE/ALBUM/2023/2023-07-Juillet-02-TRIAGE')
            ACTOR.rmtree('../../results/BASE/ALBUM/2023/2023-07-Juillet-04-TRIAGE')

        pwp_main(['--language', 'fr',
                  '--gui', 'true',
                  '--home', os.getcwd() + '/tests/results/HOME',
                  '--base', os.getcwd() + '/tests/results/BASE',
                  '--enable-create-base', "true"],
                 test_scenario=[
                     ("start GUI test",),
                     # configure BASE with thumbnails useless
                     ("gui change parameters",),
                     ("gui config", "."),

                     ("gui modify_settings invoke",),
                     ("gui settings_ui undo",),
                     ("gui settings_ui set", "LOCAL", "UNUSED"),
                     ("gui save", "."),

                     # copy tests/sources/PICTURES/Vendée/* in TRIAGE (i.e. WITHOUT the Vendée dir !)
                     ("gui execute", build_pattern),

                     # run piwiPre
                     ("gui run",),
                     ("gui pause",),    # wait 1 second for RUN to complete, just in case
                     # move 'tests/results/BASE/ALBUM/2023/2023-07-Juillet-02-TRIAGE'
                     #   -> 'tests/results/BASE/ALBUM/2023/Chemin'
                     # move 'tests/results/BASE/ALBUM/2023/2023-07-Juillet-04-TRIAGE'
                     #   -> 'tests/results/BASE/ALBUM/2023/BBQ'
                     ("gui execute", move_files),
                     ("gui pause", ),

                     # change config dir to CMD LINE
                     ("gui config", "[CMD LINE]"),
                     ("gui pause", ),

                     # change verify-album to ALBUM/2023, starting point = BASE
                     ("gui modify multilevel string", 'verify-album'),
                     # ("gui dir-chooser enter", ".."),
                     ("gui dir-chooser enter", "ALBUM"),
                     ("gui dir-chooser select", "2023"),

                     ("gui modify multilevel bool", "enable-verify-sub-album"),
                     ("gui set multilevel bool", "enable-verify-sub-album", "true"),
                     # run piwiPre
                     ("gui run",),

                     # exit
                     ("gui exit",),
                 ])
        # ------------------------------------------

        self.assert_file('tests/results/BASE/ALBUM/2023/2023-07-Juillet-04-BBQ/2023-07-04-12h53-07-BBQ.jpg')
        self.assert_file('tests/results/BASE/ALBUM/2023/2023-07-Juillet-02-Chemin/2023-07-02-14h45-22-Chemin.jpg')

        # other files are verified in program_211
        # ------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_912(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('Automated test of ')
        LOGGER.test_msg('Started an empty BASE and empty HOME')
        LOGGER.test_msg('Create a new BASE : BASE2')
        LOGGER.test_msg('build its .ini')
        LOGGER.test_msg('verify the .ini is valid and BASE2 set in .last file')
        LOGGER.test_msg('')

        if not PwpGui.tk_available():
            LOGGER.test_msg("Requires Tk, test aborted")
            LOGGER.test_msg(f'--------------- end of {mn}')
            self.done(mn, ok=False)
            return

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results/HOME")

        pwp_main(['--language', 'fr',
                  '--gui', 'true',
                  '--home', os.getcwd() + '/tests/results/HOME',
                  '--base', os.getcwd() + '/tests/results/BASE',
                  '--enable-create-base', "true"],
                 test_scenario=[
                     ("start GUI test",),

                     ("gui change parameters",),    # Button: Change Params

                     ('gui choose base', ),         # Button: Choose Base
                     # choose to create a new base
                     ('gui select base', True),     # Button Create a new Base [Choose]
                     # create BASE 2
                     ("gui dir-chooser create", "BASE2"),
                     ("gui dir-chooser select", "BASE2"),

                     ("gui config", "."),

                     ("gui modify multilevel string", 'triage'),
                     ("gui dir-chooser enter", ".."),
                     ("gui dir-chooser create", "TRIAGE2"),
                     ("gui dir-chooser select", "TRIAGE2"),
                     ("gui save", "."),

                     # exit
                     ("gui exit",),
                 ])
        # ------------------------------------------

        self.assert_file('tests/results/BASE2/piwiPre.ini')
        self.assert_file_contains('tests/results/BASE2/piwiPre.ini', "triage : TRIAGE2")

        current_host = socket.gethostname()
        current_host = re.sub(r'\W+', "-", current_host)
        filename = f"tests/results/HOME/.piwiPre.last.{current_host}"
        self.assert_file(filename)
        self.assert_file_contains(filename, 'BASE2')

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    # ==================================================================================
    # Programs above 1000 are NOT automatically passed
    # ==================================================================================

    def program_1006(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('MANUAL test of piwiPre GUI, without automated test ')
        LOGGER.test_msg('An error GUI should be generated and manually acknowledged')
        LOGGER.test_msg('')
        ACTOR.mkdirs("tests/results/HOME")

        ACTOR.copy("tests/sources/piwiPre-local.ini", "tests/results/HOME/.piwiPre.ini")

        pwp_main(['--language', 'fr',
                  '--gui', 'true',
                  '--home', os.getcwd() + '/tests/results/HOME',
                  '--base', os.getcwd() + '/tests/results/BASE',
                  '--not-a-flag', 'true',                     # should generate an error, which is seen until ack
                  '--enable-create-base', "true"],
                 )

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_1007(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('MANUAL test of piwiPre GUI, without automated test ')
        LOGGER.test_msg('Scenario of piwiPre started by pwpInstaller on an empty BASE and empty HOME')
        LOGGER.test_msg('')
        ACTOR.mkdirs("tests/results/HOME")

        # ------------------------------------------
        pwp_main(['--language', 'fr',
                  '--gui', 'true',
                  '--home', os.getcwd() + '/tests/results/HOME',
                  '--base', os.getcwd() + '/tests/results/BASE',
                  '--enable-create-base', "true"])
        # ------------------------------------------

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    def program_1008(self):
        mn = inspect.getframeinfo(inspect.currentframe()).function
        self.reset_data()  # before any action, e.g. rmtree

        ACTOR.rmtree("tests/results")
        ACTOR.mkdirs("tests/results")
        LOGGER.test_msg(f'--------------- starting {mn}')
        LOGGER.test_msg('')
        LOGGER.test_msg('auto-test of piwiPre GUI, without automated test ')
        LOGGER.test_msg('')
        LOGGER.test_msg('**** This test program assumes that the following actions are done manually')
        LOGGER.test_msg('**** 1) Change album -> ALBUM')
        LOGGER.test_msg('**** 2) Change thumbnails   -> THUMBNAILS')
        LOGGER.test_msg('**** 3) Run piwiPre from BASE')
        LOGGER.test_msg('**** 4) Quit')
        LOGGER.test_msg('')

        cmdline = self.build_test_cmdline({'--language': 'fr'})  # purely local
        # CAVEAT: this cmdline is used ONLY to build the vector, not used to run pwp_main

        vector = PwpVector(cmdline, [
            {'in-source': "piwiPre-alt.ini", 'in-results': "piwiPre.ini"},
        ])
        # differences between piwiPre-local.ini and piwiPre-alt.ini
        #                     album: ALBUM      -> LOCAL-ALBUM
        #                     thumbnails: THUMBNAILS          -> LOCAL-THUMBNAILS

        ACTOR.mkdirs("tests/results/ALBUM")  # Build it to ease selection in UI
        ACTOR.mkdirs("tests/results/THUMBNAILS")  # Build it to ease selection in UI
        self.copy_armor(vector)
        for vect in vector.items:
            if "copyright" in vect.data:
                del vect.data["copyright"]
            if "special" in vect.data:
                del vect.data["special"]
            if "size" in vect.data:
                del vect.data["size"]

        initial_cwd = os.getcwd()

        # -------------------------------------------------------------------------------
        # CAVEAT: we do NOT reuse cmdline, so that ALBUM is not set by build_test_cmdline
        main = pwp_main(['--language', 'fr',
                         '--gui', 'true',
                         '--enable-remote-thumbnails', 'false',
                         '--enable-remote-album', 'false',
                         '--remote-thumbnails', None,
                         '--remote-album', None,
                         '--remote-auto-config', None,
                         '--base', 'tests/results'])
        # --------------------------------------------------------------------------------

        self.check(1008, main.start_time, vector)

        os.chdir(initial_cwd)

        LOGGER.test_msg(f'--------------- end of  {mn}')
        LOGGER.test_msg('')
        self.done(mn)

    # ====================================================================

    def run_number(self, number, running_all):
        initial_cwd = os.getcwd()
        name = f"program_{number}"

        try:
            if name in self.programs:
                self.programs[name]()
            else:
                if not running_all:
                    LOGGER.test_msg('')
                    LOGGER.test_msg(f'---- No program {name}')
                    LOGGER.test_msg('')
        # except PwpError:  # traps all errors and subclasses
        #    LOGGER.test_msg("continuing tests after PwpError")
        except SystemExit:
            LOGGER.test_msg("continuing tests after SystemExit")
        os.chdir(initial_cwd)

    def program_0(self):
        LOGGER.test_msg('----------------------------- starting program_0')
        LOGGER.test_msg(f"USER         = '{getpass.getuser()}'")
        LOGGER.test_msg(f"BASE         = '{os.getcwd()}' ")
        LOGGER.test_msg(f"HOME         = '{os.path.expanduser('~')}' ")

        for i in self.program_numbers:   # [ 906, 907, 908, 909]:   self.program_numbers:
            if i < 1000:
                self.run_number(i, running_all=True)

        LOGGER.test_msg('----------------------------- end program_0')
        LOGGER.test_msg('')
        LOGGER.test_msg('End of ALL TESTS')
        LOGGER.test_msg('')
        end = datetime.datetime.now()

        LOGGER.test_msg(f"--- scenario     = {self.scenario}/{self.scenario_OK}")
        LOGGER.test_msg(f"--- asserts      = {self.asserts}")
        LOGGER.test_msg(f"--- end          = {end} ---")
        LOGGER.test_msg(f"--- duration     = {end - self.start_time}")
        files = 0
        for k in self.files_processed:
            LOGGER.test_msg(f"--- {k:20} = {self.files_processed[k]} ")
            files += self.files_processed[k]
        if files:
            LOGGER.test_msg(f"--- duration/file = {(end - self.start_time) / files}")
        LOGGER.test_msg("------------------------------------")


def test_all_programs():  # because it is called test_XXX, tox runs it
    all_tests = PwpTester()
    all_tests.program_0()


def run_pwp(arguments):
    LOGGER.start()
    LOGGER.test_msg('--------------- starting run_pwp()')
    parser = argparse.ArgumentParser(description='testing piwiPre ')
    parser.add_argument('--number', '-n', help='test number', action='store')
    args = parser.parse_args() if arguments is None else parser.parse_args(arguments)

    number = int(args.number) if args.number else 0

    all_tests = PwpTester()
    all_tests.run_number(number, running_all=False)


if __name__ == '__main__':
    run_pwp(sys.argv[1:])
