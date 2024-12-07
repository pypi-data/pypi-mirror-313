import os
import datetime

from piwiPre.pwpActor import ACTOR
from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpErrors import LOGGER

# DONE:
#  Optimize md5sum by caching pwpDirEntry in a class variable
#  cache is reset at the end of run_stage_dir
#  files created/removed must be reflected in cache
#  A method to achieve this is to perform ALL actions through PwpFileEntry


class ItemEntry:
    def __init__(self, local: str or None, is_file: bool):
        self.basename = os.path.basename(local) if local else None
        self.is_file = is_file      # file = True, else  dir

        self.local = local          # local is the theoretical local name
        self.is_local = False       # is_local means that the file/dir DOES exist

        self.remote = None          # remote is the theoretical remote name
        self.is_remote = False      # is_remote means that the file/dir DOES exist

    def remove(self, father: 'ItemEntry' or None, msg: str = ''):
        LOGGER.internal_error(f"ItemEntry.remove({self})")

    def set_remote(self, remote):
        self.remote = remote
        self.basename = os.path.basename(remote)
        self.is_remote = True

    def set_local(self, local):
        self.local = local
        self.basename = os.path.basename(local)
        self.is_local = True


class PwpDirEntry(ItemEntry):
    cache = {}

    def __init__(self, local: str, config: PwpConfig, context: str):
        """
        PwpDirEntry(self, local: str, config: PwpConfig, context: str)
        :param local: dir path in the local filesystem
        :param config: config
        :param context: either local, thumbnails or album.
        """
        super().__init__(local=local, is_file=False)
        self.sons: dict[str, PwpDirEntry] = {}
        self.files: dict[str, PwpFileEntry] = {}
        self.config = config
        self.context = context
        self.local = local
        self.is_local = os.path.isdir(local)
        self.is_opened = False

        if context == 'album' and ACTOR.ssh_connection and config['remote-album'] and config['enable-remote-album']:
            if not ACTOR.is_a_subdir(local, config['album']):
                LOGGER.internal_error(f"Illegal dir path '{local}' does not start with album '{config['album']}'")
            self.remote = local.replace(config['album'], config['remote-album'], 1)

        elif (context == 'thumbnails' and ACTOR.ssh_connection and
              config['remote-thumbnails'] and config['enable-remote-thumbnails']):
            if not ACTOR.is_a_subdir(local, config['thumbnails']):
                LOGGER.internal_error(f"Illegal dir path {local} " +
                                      f"does not start with thumbnails '{config['thumbnails']}'")
            self.remote = local.replace(config['thumbnails'], config['remote-thumbnails'], 1)
        elif (context == 'auto-config' and ACTOR.ssh_connection and
              config['remote-auto-config'] and config['enable-remote-auto-config']):
            if not ACTOR.is_a_subdir(local, config['auto-config']):
                LOGGER.internal_error(f"Illegal dir path {local} " +
                                      f"does not start with auto-config '{config['auto-config']}'")
            self.remote = local.replace(config['auto-config'], config['remote-auto-config'], 1)

        if self.basename is None:  # pragma: no cover: defensive code
            if self.remote is None:
                LOGGER.internal_error("PwpDirEntry(None, None")
            self.basename = os.path.basename(self.remote)

        if self.local in PwpDirEntry.cache:
            LOGGER.internal_error(f"Duplicate DirEntry {self.local}")
        PwpDirEntry.cache[self.local] = self

    def __str__(self):
        return f"Dir({self.local})"

    @staticmethod
    def clean_cache():
        PwpDirEntry.cache = {}
        # LOGGER.msg("clean_cache")

    def file_entries(self):
        return list(self.files.values())

    def all_entries(self):
        return list(self.sons.values()) + list(self.files.values())

    def is_empty(self):
        return len(self.files) + len(self.sons) == 0

    def remove(self, father: 'ItemEntry' or None, msg: str = ''):
        if self.local:
            ACTOR.rmtree(self.local, msg=msg)
            if msg:
                LOGGER.msg(f"{msg} : local dir {self.local}")
        if self.remote:
            ACTOR.remote_rmtree(self.remote, msg=msg)
            if msg:
                LOGGER.msg(f"{msg} : remote dir {self.remote}")
        if father:
            father.sons.pop(self.basename)

    # @staticmethod
    # def create(local: str, config: PwpConfig, context: str):
    #     if local in PwpDirEntry.cache:
    #         return PwpDirEntry.cache[local]
    #     return PwpDirEntry(local, config, context)

    @staticmethod
    def open(local: str, config: PwpConfig, context: str):
        if local in PwpDirEntry.cache:
            res = PwpDirEntry.cache[local]
        else:
            res = PwpDirEntry(local, config, context)
        res.read()
        return res

    def read(self):
        if not self.is_opened:
            self.sons: dict[str, PwpFileEntry] = {}
            self.files: dict[str, PwpFileEntry] = {}
            if os.path.isdir(self.local):
                all_files = os.listdir(self.local)
                basename: str
                for basename in all_files:
                    local_path = self.local + '/' + basename
                    # There is no reason why item would be already created
                    if ACTOR.isfile(local_path):
                        existing = self.files[basename] if basename in self.files else None
                        this_file = existing or PwpFileEntry(local_path,
                                                             config=self.config, context=self.context,
                                                             father=self)
                        this_file.set_local(local_path)
                        self.files[basename] = this_file
                        # FileEntry always check for local presence of the file
                    else:
                        existing = self.sons[basename] if basename in self.sons else None
                        this_dir = existing or PwpDirEntry(local_path, self.config, self.context)
                        this_dir.set_local(local_path)
                        self.sons[basename] = this_dir
                        # DirDescr always check for local presence of the file
            self.is_opened = True

            if self.remote:
                all_r_files = ACTOR.remote_ls(self.remote, forced=True, warn_if_absent=False)

                for basename, dico in all_r_files.items():
                    local_path = self.local + '/' + basename if self.local else None
                    remote_path = self.remote + '/' + basename

                    if dico['type'] == 'file':
                        existing = self.files[basename] if basename in self.files else None
                        this_file = existing or PwpFileEntry(local_path,
                                                             config=self.config, context=self.context,
                                                             father=self)
                        this_file.set_remote(remote_path)
                        this_file.remote_size = dico['size']
                        this_file.remote_mdt = dico['date']
                        self.files[basename] = this_file
                    else:  # must be a directory
                        existing = self.sons[basename] if basename in self.sons else None
                        if existing:
                            this_dir = existing
                        else:
                            ACTOR.mkdirs(local_path)
                            this_dir = PwpDirEntry(local_path, self.config, self.context)
                        this_dir.set_local(local_path)
                        this_dir.set_remote(remote_path)
                        self.sons[basename] = this_dir
            LOGGER.trace(f"read({self.local, self.remote})")

        def get_base(item):
            return item.basename if item is not None else None

        all_files = sorted(self.files.values(), key=get_base)
        all_sons = sorted(self.sons.values(), key=get_base)
        return all_files, all_sons

    def exists_and_younger_than(self, path, mdt: datetime.datetime):
        filename = os.path.basename(path)
        if filename not in self.files:
            return False
        return self.files[filename].is_younger_than(mdt)


class PwpFileEntry(ItemEntry):
    def __init__(self, local: str, context: str, config: PwpConfig, father: PwpDirEntry or None = None):
        """

        :param local: local path, or None
        """

        super().__init__(local=local, is_file=True)
        self.size = None
        self.mdt = None
        self.md5sum = None
        if father is None:
            father = PwpDirEntry.open(os.path.dirname(local), config=config, context=context)
        self.father = father
        self.config = config

        basename = os.path.basename(self.local)
        if basename in father.files:
            LOGGER.internal_error(f'duplicate file {self.father}')

        father.files[basename] = self

        if ACTOR.isfile(local):
            self.is_local = True
            self.size = os.stat(local).st_size
            self.mdt = datetime.datetime.fromtimestamp(os.path.getmtime(local))
        else:
            self.is_local = False
            self.size = None
            self.mdt = None

        self.remote = None
        if (ACTOR.ssh_connection and self.config['enable-remote-thumbnails'] and
                ACTOR.is_a_subdir(self.local, self.config['thumbnails'])):
            self.remote = self.local.replace(self.config['thumbnails'], self.config['remote-thumbnails'])
        elif (ACTOR.ssh_connection and
              self.config['enable-remote-album'] and
              ACTOR.is_a_subdir(self.local, self.config['album'])):
            self.remote = self.local.replace(self.config['album'], self.config['remote-album'])
        elif (ACTOR.ssh_connection and
              self.config['enable-remote-auto-config'] and
              ACTOR.is_a_subdir(self.local, self.config['auto-config'])):
            self.remote = self.local.replace(self.config['auto-config'], self.config['remote-auto-config'])

        self.remote_size = None
        self.remote_mdt = None
        self.remote_md5sum = None

        if self.basename is None:
            if self.remote is None:
                LOGGER.internal_error("PwpFileEntry(None, None")
            self.basename = os.path.basename(self.remote)

    def exists(self):
        if self.is_local and not self.remote:
            # we are in a purely local configuration, otherwise remote would be set
            return True

        if self.remote and self.is_remote:
            # we are in a remote configuration, only is_remote is important, we do not care about is_local
            return True

        return False

    @staticmethod
    def lookup(local: str, context: str, config: PwpConfig):
        father = PwpDirEntry.open(os.path.dirname(local), config=config, context=context)
        if os.path.basename(local) in father.files:
            return father.files[os.path.basename(local)]
        return PwpFileEntry(local, context=context, config=config)

    def is_younger_than(self, mdt: datetime.datetime):
        if self.is_local:
            return self.mdt >= mdt
        # if there is only a remote file, we are paranoiac and create again the thumbnail
        return False

    def remove(self, father: 'ItemEntry' or None, msg: str = ''):
        if self.is_local:
            ACTOR.delete(self.local, msg=msg)
            if msg:
                LOGGER.msg(f"delete file {self.local} {msg} ")
        if self.is_remote:
            ACTOR.remote_delete(self.remote, msg=msg)
            if msg:
                LOGGER.msg(f"remote delete file{self.remote} {msg} ")
        if father:
            father.files.pop(self.basename)

    def get_remote_md5(self):
        if not self.is_remote:
            return None
        if not self.remote_md5sum:
            sql_file_info = ACTOR.sql_get_file_info(self.remote)
            if sql_file_info and sql_file_info.md5sum:
                self.remote_md5sum = sql_file_info.md5sum
                LOGGER.test_msg(f"file '{self.local}' in database without md5sum")
                # piwiPre always insert md5sum in the database, and this is enforced when doing verify-album
            else:
                self.remote_md5sum = ACTOR.remote_compute_md5(self.remote)
        return self.remote_md5sum

    def get_md5(self):
        if self.is_local and self.md5sum is None:
            self.md5sum = ACTOR.compute_md5(self.local)
        if self.is_remote:
            self.get_remote_md5()

    def remote_equals_local(self):
        self.get_md5()
        return self.md5sum == self.remote_md5sum

    #       When the same file exists in album and remote-album,
    #       piwiPre verifies that it is actually the same file by comparing the md5 sums
    #       if different, the local file is clobbered by a copy of the remote file

    def get(self):
        """
        get the file from remote location if needed.
        :return: True if the file is really here, maybe after remote-get
                 False if the file is NOT here,
                 The only case when this should happen is --dryrun
        """
        if not self.is_remote:
            return True
        if self.is_local and self.remote_equals_local():
            return True
        if ACTOR.dryrun:
            LOGGER.msg(f"Would have get {self.local} from remote location")
            return False

        if self.is_local:
            LOGGER.info(f"Incoherent local file '{self.local}' refresh it from remote location")
        ACTOR.remote_get(self.remote, self.local)

        self.is_local = True
        self.md5sum = self.remote_md5sum
        return True

    def put(self):
        if self.remote:
            ACTOR.remote_put(self.local, os.path.dirname(self.remote))
            self.is_remote = True
            self.remote_md5sum = self.md5sum
            return True
        return False

    def synchronize(self):
        if self.is_local and self.is_remote:
            return
        if self.is_local:
            self.put()
            return
        if self.is_remote:
            self.get()

    def local_coherent_with_remote(self):
        """
        local_coherent_with_remote() : detects incoherent local file and deletes it.
        - if there is only one remote file, there is no conflict.
        - if there is a local file without a remote file, this is a violation of assert 2), a warning is raised and
          the local file is ignored.
        - if md5(local) == md5(remote), then it is the same file, and there is no conflict between them
        - if there are 2 files with a different md5, then piwipre considers that the remote version is valid,
          then a warning is raised and the local version is ignored
        :return: True if local file is normal, False if it is incoherent and removed.
        """

        if self.is_local:
            if self.is_remote:
                if self.remote_equals_local():
                    return True
                self.is_local = False
                LOGGER.info(f"Incoherent local and remote {self.local}: ignore local version")
                return False

            if self.remote:
                # so enable-remote is True, we SHOULD have a remote file, but self.is_remote is false
                self.is_local = False
                LOGGER.info(f"Local file '{self.local}' without remote : ignore local version")
                return False

        return True
