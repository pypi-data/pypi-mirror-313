# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import sys
import re
import os
import shutil

# pip install GitPython
# The git executable must be specified in one of the following ways:
#     - be included in your $PATH
#     - be set via $GIT_PYTHON_GIT_EXECUTABLE
#     - explicitly set via git.refresh()


import git
import argparse
import datetime
import getpass

# this file is run by tox.
# All installation commands are executed using {toxinidir} (the directory where tox.ini resides) as CWD # noqa
# to test without tox, run: 'cd .. ; python piwiPre/pwpPatcher.py  '                                    # noqa
# the following line is mandatory to execute from shell
# tox does it automatically, so not necessary if running only from tox.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from piwiPre.pwpParser import build_official_rst
from piwiPre.pwpImageEmbedder import PwpEmbedder
from piwiPre.pwpVersion import PwpVersion


class PwpPatcher:
    def __init__(self, arguments=None, standalone=True):
        if not standalone:
            return  # pragma: no cover

        self.parser = argparse.ArgumentParser(description='manages tags and modifies accordingly files that want it ')
        self.parser.add_argument('--Major', '-M', help="Promotes as Major release i.e. X++.",
                                 action='store_true')
        self.parser.add_argument('--minor', '-m', help="Promotes as minor version ie x.Y++",
                                 action='store_true')
        self.parser.add_argument('--patch', '-p', help="Increments patch version ie x.y.Z++",
                                 action='store_true')
        self.parser.add_argument('--commit', '-c', help="Commits, implicit if -M, -m, -p",
                                 action='store_true')
        self.parser.add_argument('--set-tag', help="Sets the tag. ***NOT*** implicit with -M, -m, -p",
                                 action='store_true')

        self.parser.add_argument('--full-help', help="more explanations",
                                 action='store_true')
        self.parser.add_argument('--print', help="prints the last tag spec and exits",
                                 action='store_true')

        self.parser.add_argument('--download', '-d', help="patches download.rst",
                                 action='store_true')
        self.parser.add_argument('--autotest', help="autotest, no real action",
                                 action='store_true')
        self.parser.add_argument('--push', help="push to remote git server",
                                 action='store_true')
        self.parser.add_argument('--sphinx', help="runs sphinx to update the doc",
                                 action='store_true')

        self.parser.add_argument('--exe', help="builds the exe with PyInstaller",
                                 action='store_true')
        self.parser.add_argument('--pypi', help="uploads package to Pypi",
                                 action='store_true')
        self.parser.add_argument('--gitlab', help="uploads exe to gitlab",
                                 action='store_true')

        self.repo = git.Repo('.')

        self.origin = self.repo.remote("origin")

        tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_datetime)
        if len(tags) > 0:
            latest_tag = tags[-1]
            tag_version = str(latest_tag)
        else:  # pragma: no cover
            # latest_tag = None
            tag_version = "0.0.0"

        full_tag = re.sub(r"[^\d.]*", '', tag_version)
        m = re.match(r"(\d+)\.*(\d*)\.*(\d*)", full_tag)
        self.release = int(m.group(1)) if m.group(1) else 0
        self.version = int(m.group(2)) if m.group(2) else 0
        self.patch = int(m.group(3)) if m.group(3) else 0
        self.spec = full_tag
        # if latest_tag:
        #     self.date = latest_tag.commit.committed_datetime.strftime("%m/%d/%Y %H:%M:%S")  # noqa
        # else:  # pragma: no cover
        #     self.date = datetime.datetime.now()
        self.date = datetime.datetime.now()
        self.update_spec()
        self.args = self.parser.parse_args() if arguments is None else self.parser.parse_args(arguments)

    def __del__(self):
        if self.parser:
            print("del parser")
            del self.parser
        if self.repo:
            print("del repo")
            del self.repo
        if self.origin:
            print("del origin")
            del self.origin
        if self.args:
            print("del args")
            del self.args
        if self.date:
            print("del date")
            del self.date
        if self.spec:
            del self.spec
            print("del spec")

    def update_spec(self):
        self.spec = str(self.release)
        if self.version != 0 or self.patch != 0:
            self.spec += '.' + str(self.version)
            if self.patch != 0:
                self.spec += '.' + str(self.patch)

    def manage_tags(self):
        if self.args.set_tag:
            # instead or getting the latest tag from git,
            # we read it from version.py
            self.patch = PwpVersion.patch
            self.version = PwpVersion.version
            self.release = PwpVersion.release

            n = datetime.datetime.now()
            self.date = n.strftime("%m/%d/%Y %H:%M:%S")
            self.update_spec()
            print(f"msg     reusing tag '{self.spec}' not set")

        if self.args.patch:
            self.patch += 1

        if self.args.minor:
            self.version += 1
            self.patch = 0

        if self.args.Major:
            self.release += 1
            self.version = 0
            self.patch = 0

        if self.args.Major or self.args.minor or self.args.patch or self.args.set_tag:
            n = datetime.datetime.now()
            self.date = n.strftime("%m/%d/%Y %H:%M:%S")
            self.update_spec()

            print(f"msg     new tag '{self.spec}'")
            return True
        return False

    @staticmethod
    def open(file_name, mode):
        try:
            ins = open(file_name, mode, encoding="utf-8")
        except OSError as error:
            print(f"FATAL ERROR: Cannot open('{file_name}',{mode}) : {str(error)}, aborting")
            exit(-1)
        return ins

    @staticmethod
    def rename(old, new):
        if os.path.isfile(new):
            os.remove(new)
        try:
            os.rename(old, new)
        except OSError as error:
            print(f"FATAL ERROR: Cannot rename('{old}','{new}') : {str(error)}, aborting")
            exit(-1)
        return

    def update_file(self, src: str, dst: str, dico: dict, duplicate=False):

        new_file = dst + '.new'
        old_file = dst + '.bak'

        ins = self.open(src, "r")
        content = ins.readlines()
        ins.close()

        outs = self.open(new_file, "w")
        useful = False
        previous = []
        for line in content:
            modified = line
            for before, after in dico.items():
                modified = re.sub(before, after, modified)
            if modified not in previous:
                previous.append(modified)
            else:
                # we have already done that modification once, we do not do it twice
                modified = line
            outs.writelines(modified)

            if modified != line:
                useful = True
                if duplicate:
                    outs.writelines(line)

        outs.close()

        if not useful and src == dst:  # pragma: no cover
            os.remove(new_file)
            print(f"msg     file '{dst}' does not need patch")
            return
        else:   # pragma: no cover
            if os.path.isfile(old_file):
                os.remove(old_file)

            if src == dst:
                self.rename(src, old_file)
                self.rename(new_file, dst)
            else:
                shutil.copy2(src, old_file)
                self.rename(new_file, dst)

            print(f"msg     file '{dst}' patched")

    @staticmethod
    def update_logo(source, dst):
        if os.path.isfile(dst) and os.path.getmtime(dst) > os.path.getmtime(source):
            print(f"msg     file '{dst}' is older than source '{source}': update useless")  # pragma: no cover
            return

        embedder = PwpEmbedder()
        embedder.resize_and_convert(source, dst, 50, 29)

    def update_from_source(self, source, dst):
        if os.path.getmtime(dst) > os.path.getmtime(source) and not self.args.autotest:
            print(f"msg     file '{dst}' is older than source '{source}': patch useless")  # pragma: no cover
            return                                                                              # pragma: no cover

        with self.open(source, "r") as ins:
            content = ins.readlines()

        new_file = dst + '.new'                                                         # pragma: no cover
        old_file = dst + '.bak'

        outs = self.open(new_file, "w")
        do_add = True
        with self.open(dst, "r") as ins:
            for line in ins:
                if do_add:
                    outs.write(line)

                    if re.match(r' *def print\(.*\):\n', line):
                        for cl in content:
                            patched = re.sub('"', '\\"', cl[:-1])
                            outs.write(f'        print("{patched}")\n') # add \t\t\t # noqa ???
                        outs.write('    # End of patched text\n')
                        do_add = False
                else:
                    if re.match(r' +# End of patched text\n', line):
                        do_add = True
        outs.close()

        if os.path.isfile(old_file):
            os.remove(old_file)
        shutil.move(dst, old_file)
        self.rename(new_file, dst)
        print(f"msg     file '{dst}' patched")

    def run(self):
        if self.args.autotest:
            self.args.full_help = True

        if self.args.print:
            print(self.spec)
            return

        print(f"msg     initial tag '{self.spec}' at '{self.date}'")

        if self.args.full_help:
            print("if -M, -m or -p, updates the current tag")
            print("     verifies that the current tag is writen in piwiPre/pwpVersion.py")
            print("     verifies that piwiPre/pwpLicence.py is up to date vs source")
            print("if ")
            print("   - the new tag is a Major or a minor (but *not* a patch), then the corresponding exe and module")
            print("     will be published, assuming here that they have been tested OK)")
            print("     therefore download.rst and téléchargement.rst are also modified")
            print("   - or -d")
            print("then download.rst and téléchargement.rst are updated")

            print("if --commit, commits ALL modified files")
            print("     commit, is implicit if set-tag, -M, -m or -p")

            print("if --set-tag, sets the tag locally (and remotely if --push)")
            print("     else, do not set the tag, which allows to patch source files before setting the tag")
            print("     if a new tag puts the tag LOCALLY on git, but *not* remotely on GitLab")

        if self.args.push:
            self.args.set_tag = True

        if self.args.Major or self.args.minor or self.args.patch or self.args.set_tag:
            self.args.commit = True

        new_tag = self.manage_tags()

        if self.args.autotest:
            self.args.Major = True
            self.manage_tags()
            self.args.Major = False
            self.args.minor = True
            self.manage_tags()
            self.args.minor = False
            self.args.patch = True
            new_tag = self.manage_tags()

        if self.args.autotest:
            shutil.copy2('piwiPre/pwpLicence.py', 'tests/results/pwpLicence.py')

        self.update_logo("pwpLogo.png",
                         "piwiPre/pwpLogoSmall.py" if not self.args.autotest else "tests/results/pwpLogoSmall.py",
                         )
        self.update_from_source('LICENCE',
                                'piwiPre/pwpLicence.py' if not self.args.autotest else 'tests/results/pwpLicence.py')

        url_base = 'https://gitlab.com/api/v4/projects/48915444/packages/generic/piwiPre'

        self.update_file('piwiPre/pwpVersion.py',
                         'piwiPre/pwpVersion.py' if not self.args.autotest else 'tests/results/pwpVersion.py',
                         {r"help = '([^']*)'": f"help = '{self.spec} at {self.date}'",
                          r"spec = '([^']*)'": f"spec = '{self.spec}'",
                          r"release = (\d*)": f"release = {self.release}",
                          r"version = (\d*)": f"version = {self.version}",
                          r"patch = (\d*)": f"patch = {self.patch}",
                          r"date = '([^']*)'": f"date = '{self.date}'",
                          r"url = '([^']*)'": f"url = '{url_base}/{self.spec}/piwiPre-{self.spec}.exe'",
                          r"installer = '([^']*)'":
                              f"installer = '{url_base}/{self.spec}/pwpInstaller-{self.spec}.exe'",
                          r"configurator = '([^']*)'":
                              f"configurator = '{url_base}/{self.spec}/pwpConfigurator-{self.spec}.exe'"
                          })

        # - Windows one-file exe on gitlab artifacts:
        # `piwiPre-1.8.3.exe
        # <https://gitlab.com/api/v4/projects/22464405/packages/generic/piwiPre/1.8.3/piwiPre-1.8.3.exe>`_

        prologue_en = '- Windows one-file exe on gitlab artifacts:'
        prologue2_en = '- Windows installer on gitlab artifacts:'
        prologue_fr = "- l'exécutable Windows sur le serveur d'artefacts gitlab:"
        prologue2_fr = "- L'installateur Windows:"

        if self.args.download or (new_tag and self.patch == 0) or self.args.autotest or self.args.set_tag:
            self.update_file('source/download.rst',
                             'source/download.rst' if not self.args.autotest else 'tests/results/download.rst',
                             {
                                 r".*Windows one-file exe.*": f"{prologue_en} `piwiPre-{self.spec}.exe " +
                                                              f"<{url_base}/{self.spec}/piwiPre-{self.spec}.exe>`_",
                                 r".*Windows instal.*": f"{prologue2_en} `pwpInstaller-{self.spec}.exe " +  # noqa
                                                        f"<{url_base}/{self.spec}/pwpInstaller-{self.spec}.exe>`_",
                             },
                             duplicate=True)
            self.update_file('source/fr/téléchargement.rst',
                             'source/fr/téléchargement.rst' if not self.args.autotest else
                             'tests/results/téléchargement.rst',
                             {
                                 r".*exécutable Windows.*": f"{prologue_fr} `piwiPre-{self.spec}.exe " +
                                                            f"<{url_base}/{self.spec}/piwiPre-{self.spec}.exe>`_",
                                 r".*lateur Wind.*": f"{prologue2_fr} `pwpInstaller-{self.spec}.exe " +  # noqa
                                                     f"<{url_base}/{self.spec}/pwpInstaller-{self.spec}.exe>`_",
                             },
                             duplicate=True)

        self.update_file('version.txt',
                         'version.txt' if not self.args.autotest else 'tests/results/version.txt',
                         {r"(.+)":  self.spec})
        build_official_rst(self.args.autotest)

        if self.args.autotest:
            print(f"msg     final tag '{self.spec}' at '{self.date}'")
            return

        if self.args.sphinx:      # pragma: no cover
            res = os.system("python -m sphinx source public/html -W -b html")
            print(f"msg     DONE: sphinx -> {res}")

        if self.args.commit:      # pragma: no cover
            commit = self.repo.git.commit('-a', '-m', f'set tag {self.spec}', '--date', self.date)
            print(f"msg     DONE: git commit '{str(commit)}' ")

        if self.args.set_tag:      # pragma: no cover
            self.repo.git.tag(self.spec)
            print(f"msg     DONE: git tag '{self.spec}'")

        if self.args.push and self.origin:      # pragma: no cover
            res = self.repo.git.push('origin', self.spec)
            print(f"msg     DONE: git push {res}")

        if self.args.exe:      # pragma: no cover
            res = os.system("python -m PyInstaller -y piwiPre/__main__.py --onefile --name piwiPre")  # noqa
            print(f"msg     DONE: build exe piwiPre -> {res}")
            res = os.system("python -m PyInstaller -y piwiPre/pwpInstaller.py --onefile --name pwpInstaller")  # noqa
            print(f"msg     DONE: build exe pwpInstaller -> {res}")

        if self.args.pypi or self.args.gitlab:    # pragma: no cover
            pypi = "--Pypi" if self.args.pypi else ""
            gitlab = "--GitLab" if self.args.gitlab else ""

            res = os.system(f"python upload.py {pypi} {gitlab}")
            print(f"msg     DONE: upload .py {pypi} {gitlab} -> {res}")
        else:
            return


def patcher_main(arguments):
    arguments = arguments or []
    print('msg     --------------- starting patcher_main')
    print("msg")
    print(f"msg     current user = '{getpass.getuser()}'")
    print(f"msg     current dir  = '{os.getcwd()}'")
    print(f"msg     HOME         = '{os.path.expanduser('~')}' ")
    print("msg")

    my_patcher = PwpPatcher(arguments=arguments)
    my_patcher.run()
    del my_patcher
    print('msg     --------------- ending patcher_main')


if __name__ == "__main__":
    retval = patcher_main(sys.argv[1:])
    print(f"retval = {retval}")
    sys.exit(retval)
