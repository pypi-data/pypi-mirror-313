# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

import datetime
import logging
import re
import os
import pathlib
import subprocess

# pip install Pillow
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import ImageOps

# pip install iptcinfo3
from iptcinfo3 import IPTCInfo

from piwiPre.pwpActor import ACTOR, PwpSummary
from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpErrors import LOGGER
from piwiPre.pwpDir import PwpDirEntry, PwpFileEntry


class PwpData:
    """Root class for PwpJpg and PwpMp4"""
    # opened_objects = {}
    jpg = ("jpg", "jpeg")
    image = ("png", "gif", "bmp", "eps", "ico", "pbm", "pgm", "pnm", "tga", "tiff", "webp", "xbm", "wmf", "xpm")
    # see https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    mp4 = ("mp4",)
    video = ("webm", "ogv", "m4v", "mov",
             "mkv", "flv", "vob", "ogg", "avi", 'mts', 'm2ts', 'ts', "wmv", 'rm', 'rmvb', 'asf',
             "mpg", "mp2", "mpeg", "mpe", "mpv", "m2v", "m4v")
    kept = ('txt', )

    avoided = ('ini', 'db')

    # .ini file are not copied from triage to album, and kept in verify-album

    JPG = "jpg"
    IMAGE = "image"
    MP4 = "mp4"
    VIDEO = "video"
    KEPT = "kept"
    AVOIDED = "avoided"

    def __init__(self, filename, working, backup):
        """
        :param filename: the current name
        :param working: file we can modify, can be filename or a tmp file
        :param backup: where we will copy, if modifications are allowed in place
        """
        self.filename = filename
        self.working = working
        self.backup = backup
        self.width = None
        self.height = None

        self.suffix = pathlib.Path(filename).suffix[1:]
        self.representative = None          # picture that represents the file if this is a video
        self.to_abort = False

        self.can_be_inserted_in_db = False  # will be set to True for images and video

        if filename and ACTOR.isfile(filename):
            self.size = os.stat(filename).st_size
            self.modified_time = os.path.getmtime(filename)
        else:
            self.size = None
            self.modified_time = datetime.datetime.now().timestamp()

        # metadata from file JPG, MP4, etc metadata inside the file
        self.copyright = None
        self.special = None
        self.author = None
        self.creation = None
        self.model = None
        self.latitude = None
        self.longitude = None

        # these metadata exists only for JPG
        self.iptc_info = None
        self.exif_data = None

        self.is_modified = False

    def __enter__(self):
        return self  # everything done in __init__

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.close()

    def incr_logger_count(self, item=None):
        LOGGER.internal_error("incr_logger_count()")

    @staticmethod
    def get_type(filename):
        suffix = pathlib.Path(filename).suffix[1:].lower()

        if suffix in PwpData.jpg:
            return PwpData.JPG

        if suffix in PwpData.image:
            return PwpData.IMAGE

        if suffix in PwpData.mp4:
            return PwpData.MP4

        if suffix in PwpData.video:
            return PwpData.VIDEO

        if suffix in PwpData.kept:
            return PwpData.KEPT

        return PwpData.AVOIDED

    @staticmethod
    def create(filename, config: PwpConfig,
               tmp: str or None = None,
               backup: str or None = None):
        """
        Decides the flavor of PwpFile to build, depending on filename suffix.

        :param filename: the current name of the file
        :param tmp: where we will copy, if modifications are not allowed in place
        :param backup: where we will copy, if modifications are allowed in place
        :param config: current configuration
        :returns: a PwpFile, opened.
        """

        file_type = PwpData.get_type(filename)

        if file_type == PwpData.JPG:
            # backup = None if stage == "triage" else back-up  # now, we always back-up files even in triage # noqa
            working = tmp
            return PwpJpg(filename, config=config, working=working, backup=backup)

        if file_type == PwpData.IMAGE:
            # so, images that are not JPG, e.g. PNG
            # if we have to modify, then we need to back up
            if tmp:
                # this happens when we manage a png with enable-rename false
                le = len(pathlib.Path(tmp).suffix[1:])
                tmp = tmp[:-le] + 'jpg'
                # here, we FORCE working to be a JPG file
            return PwpImage(filename, config=config, working=tmp, backup=backup)

        if file_type == PwpData.MP4:
            # backup = None if stage == "triage" else backup  # always backup in triage
            working = tmp
            return PwpMp4(filename, config=config, working=working, backup=backup)

        if file_type == PwpData.VIDEO:
            # if we have to modify, then we need to back up
            if tmp:
                le = len(pathlib.Path(tmp).suffix[1:])
                tmp = tmp[:-le] + 'mp4'
            return PwpVideo(filename, config=config, working=tmp, backup=backup)

        if file_type == PwpData.KEPT:
            return PwpKept(filename, backup)

        return PwpAvoided(filename, backup)

    def close(self):
        # self.release(force_close=False)
        pass  # nothing to do on txt files

    def do_backup(self):
        if self.backup:
            LOGGER.trace(f"backup {self.filename} to {self.backup}")
            ACTOR.copy(self.filename, self.backup)
            self.backup = None  # so that it is not backup-ed once more
            self.incr_logger_count("Backup")

    def close_if_backup(self):
        """
        closes the file BEFORE it is modified.
        if backup is set, copies the file to back up
        :return: None
        """
        self.do_backup()
        self.close()

    def patch_after_rename(self, new_filepath):
        """
        For some objects, it is necessary to patch the name that rename generates
        :param new_filepath:
        :return: patched version
        """
        LOGGER.internal_error(f"patch_after_rename({self.filename})")
        # return new_filepath

    def save_with_info(self, _config, new_iptc=None):
        LOGGER.internal_error(f"save_with_info({self.filename})")
        # pass  # nothing to do on txt files

    def handles_metadata(self):
        LOGGER.internal_error(f"handles_metadata({self.filename})")
        #  return False

    def write_metadata(self, _new_author, _new_copyright, _new_special, _new_date, _config):
        LOGGER.internal_error(f"write_metadata({self.filename})")
        return self

    def rotate(self, _stage: str, _any):
        LOGGER.internal_error(f"rotate({self.filename})")
        return self  # nothing to do with text or mp4

    @staticmethod
    def str_ptime(str_rep, str_format):    # noqa
        try:
            return datetime.datetime.strptime(str_rep, str_format)
        except ValueError:
            return None

    @staticmethod
    def datetime(filename, year, month, day, hour, minute, second):
        try:
            from_filename = datetime.datetime(year=year,
                                              month=month,
                                              day=day,
                                              hour=hour,
                                              minute=minute,
                                              second=second)
            return from_filename
        except ValueError as e:
            LOGGER.trace(f"Error {e} in date from filename {filename} ")
            LOGGER.trace(f"year={year}  month={month} day={day}")
            LOGGER.trace(f"hour={hour}  minute={minute} second={second}")
            return None

    @staticmethod
    def get_date(str_rep):
        if str_rep is None:
            LOGGER.internal_error("get_date(None)")

        r = re.match(r"\d\d\d\d:\d\d:\d\d \d\d:\d\d:\d\d", str_rep)
        if r and str_rep != '0000:00:00 00:00:00':
            return PwpData.str_ptime(str_rep, '%Y:%m:%d %H:%M:%S')

        r = re.match(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d", str_rep)
        if r:
            return PwpData.str_ptime(str_rep, '%Y-%m-%d %H:%M:%S')

        # '2023-01-27T17:59:39.000000Z' strptimes has difficulties, there  # noqa
        r = re.match(r"(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)", str_rep)
        if r:
            return datetime.datetime(year=int(r.group(1)),
                                     month=int(r.group(2)),
                                     day=int(r.group(3)),
                                     hour=int(r.group(4)),
                                     minute=int(r.group(5)),
                                     second=int(r.group(6)))

        # r = re.match(r"\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d", str_rep)
        # if r:
        #     return PwpFile.str_ptime(str_rep, '%Y/%m/%d %H:%M:%S')
        LOGGER.internal_error(f"get_date({str_rep})")

    @staticmethod
    def date_from_dico(filename, file_info) -> datetime or None:
        """
        date_from_dico(file_info)
        :param filename: name of the file
        :param file_info: dictionary, an output from ACTOR.get_info_from_format
        :return: datetime.datetime
        """
        if file_info is None or\
                'Y' not in file_info or file_info['Y'] is None or \
                'm' not in file_info or file_info['m'] is None or \
                'd' not in file_info or file_info['d'] is None:
            return None

        if file_info['H']:
            hour = int(file_info['H'])
        elif 'count' in file_info and file_info['count']:
            hour = int(int(file_info['count']) / 3600)
        else:
            hour = 0

        if file_info['M']:
            minute = int(file_info['M'])
        elif 'count' in file_info and file_info['count']:
            minute = int(int(file_info['count']) / 60)
        else:
            minute = 0

        if file_info['S']:
            second = int(file_info['S'])
        elif 'count' in file_info and file_info['count']:
            second = int(file_info['count']) % 60
        else:
            second = 0

        return PwpData.datetime(filename,
                                year=int(file_info['Y']),
                                month=int(file_info['m']),
                                day=int(file_info['d']),
                                hour=hour,
                                minute=minute,
                                second=second)

    def guess_file_date(self, image_path: str, config: PwpConfig, default_to_filedate=True)\
            -> datetime or None:
        """
        :param image_path: the full path to image
        :param config: the current configuration
        :param default_to_filedate: if True and no date found, returns the file date
        :return: date
        """  # noqa

        filename = os.path.basename(image_path)
        template = os.path.basename(config['names'])
        # check if the date can be extracted from the filename, according to current template
        file_info = ACTOR.get_info_from_format(template, filename)
        from_filename = self.date_from_dico(filename, file_info)

        if from_filename:
            return from_filename

        # TODO: Manage timezone and AM/PM

        m = re.match(r"VID(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)\.mp4", filename) or \
            re.match(r"VID_(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\.mp4", filename) or \
            re.match(r".*-(\d\d\d\d)-(\d\d)-(\d\d)-(\d\d)h(\d\d)-(\d\d).*\.jpg", filename)
        if m:  # pragma: no cover
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            hours = int(m.group(4))
            minutes = int(m.group(5))
            seconds = int(m.group(6))
            from_filename = PwpJpg.datetime(filename, year=year, month=month, day=day,
                                            hour=hours, minute=minutes, second=seconds)
            if from_filename:
                return from_filename
            # in real life, this can happen, but we have (yet) no test case for this

        m = re.match(r"IMG-(\d\d\d\d)-(\d\d)(\d\d)-W.(\d\d)(\d\d).*\.jpg", filename) or \
            re.match(r"IMG-(\d\d\d\d)(\d\d)(\d\d)-W.(\d\d)(\d\d).*\.jpg", filename)
        # for WhatsApp images, which does not have IPTC date information, but get a date in the picture name
        if m:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            hours = int(m.group(4)) + 12
            minutes = int(m.group(5))
            seconds = 0
            from_filename = PwpData.datetime(filename, year=year, month=month, day=day,
                                             hour=hours, minute=minutes, second=seconds)
            if from_filename:
                return from_filename

        # maybe the date can be extracted from the directory, and time from the file
        if default_to_filedate and ACTOR.isfile(image_path):
            template = os.path.basename(os.path.dirname(config['names']))  # the 1st item in dir hierarchy
            dir_name = os.path.basename(os.path.dirname(image_path))
            dir_info = ACTOR.get_info_from_format(template, dir_name)
            if dir_info is not None:
                file_date = datetime.datetime.fromtimestamp(os.path.getmtime(image_path))

                dir_info['H'] = file_date.hour
                dir_info['M'] = file_date.minute
                dir_info['S'] = file_date.second
                from_filename = self.date_from_dico(filename, dir_info)

                if from_filename:
                    return from_filename

        if default_to_filedate and ACTOR.isfile(image_path):
            LOGGER.debug(f"Cannot guess date for {image_path}")
            return datetime.datetime.fromtimestamp(os.path.getmtime(image_path))
        return None

    @staticmethod
    def date_to_str(c_date):
        return f"{c_date.year:04}/{c_date.month:02}/{c_date.day:02} " + \
            f"{c_date.hour:02}:{c_date.minute:02}:{int(c_date.second):02}"

    def compute_new_date_author(self, config: PwpConfig):
        """
        :param config: current configuration
        :return: date, author
        """

        from_filename = self.guess_file_date(self.filename, config, default_to_filedate=False)
        if from_filename and config['enable-date-in-filename']:
            author = config.author(self.model, from_filename)
            return from_filename, author

        from_exif = self.creation
        if from_exif:
            LOGGER.debug(f"Date = {self.date_to_str(from_exif)}  before correction")
        else:
            LOGGER.debug("Date = None before correction")

        corr_fr_exif = config.fix_date(self.filename, from_exif, self.model)

        if corr_fr_exif:
            LOGGER.debug(f"Date = {self.date_to_str(corr_fr_exif)} after correction")

            author = config.author(self.model, corr_fr_exif)
            return corr_fr_exif, author
        else:
            LOGGER.debug("Date = None after correction")                              # pragma: no cover: defensive code

        if from_filename:
            author = config.author(self.model, from_filename)
            return from_filename, author

        LOGGER.debug(f"No exif nor file dates in '{self.filename}'")                  # pragma: no cover: defensive code

        file_date = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))  # pragma: no cover: defensive code
        author = config.author(self.model, file_date)                                 # pragma: no cover: defensive code
        return file_date, author                                                      # pragma: no cover: defensive code

    def verify_metadata(self, _stage,
                        config: PwpConfig,
                        summary: PwpSummary,
                        new_date: datetime,
                        new_author="Photographer",
                        enable_reset=True):
        """
        :param _stage: triage or album
        :param config: local configuration
        :param new_date: date to set
        :param new_author: author to set in exif
        :param summary: remembers the actions taken, for debug
        :param enable_reset: is True, always write metadata, if False, write only if not set

                self is supposed to be open

        if necessary:
        - saves the file to back up
        - rotates the file
        - stores the rotated picture in a copy
        - set is_modified to True
        - manages LOGGER.info()

        lives the file open for further processing

        :return self or a copy, modified"""

        if config['enable-metadata'] is False or self.handles_metadata() is False:
            return self, False

        is_modified = False
        if (enable_reset and self.creation != new_date) or self.creation is None or self.creation == '':
            summary.meta_date = True
            is_modified = True

        dico = config.format_dict(new_date, new_author)

        info_format = config.format('instructions')

        new_special = info_format.format(**dico)
        if (enable_reset and self.special != new_special) or self.special is None or self.special == '':
            summary.meta_instructions = True
            is_modified = True

        if (enable_reset and self.author != new_author) or self.author is None or self.author == '':
            summary.meta_author = True
            is_modified = True

        copyright_format = config.format('copyright')
        new_copyright = copyright_format.format(**dico)
        if (enable_reset and self.copyright != new_copyright) or self.copyright is None or self.copyright == '':
            summary.meta_copyright = True
            is_modified = True

        if not is_modified:
            return self, is_modified

        modifications = summary.get_meta()

        # LOGGER.msg(f"write IPTC info '{self.filename}'")
        if config['dryrun']:
            LOGGER.trace(f"Would insert meta[{modifications}] metadata in '{self.working}'")
            return self, is_modified

        if self.is_modified:
            # this happens if the file was rotated
            # saving it is useless, and we already have a copy
            pass
        else:
            # here, the file WILL be modified
            self.close_if_backup()

        new_image = self.write_metadata(new_author, new_copyright, new_special, new_date, config)
        new_image.incr_logger_count("Metadata")

        LOGGER.trace(f"metadata meta[{modifications}] inserted in '{new_image.filename}'")

        return new_image, is_modified

    @staticmethod
    def get_remote_thumbnails_filename(config, filename):
        """
        :param config: local configuration
        :param filename: local name
        :return: the remote path to be used for sftp
        """
        if config['enable-remote-thumbnails'] and ACTOR.ssh_connection:
            remote_file = filename.replace(config['thumbnails'], config['remote-thumbnails'])
            return remote_file
        return None

    def thumbnail(self, filename, width, height, crop, config: PwpConfig, force_rebuild: bool,
                  thumbs_dir: PwpDirEntry, summary: PwpSummary):
        # no thumbnail generated
        return

    def verify_orientation(self, _stage: str, _config: PwpConfig, _summary: PwpSummary):
        return self, None

# ------------------------------------------------------------------------------------------------
# PwpImage
# ------------------------------------------------------------------------------------------------


class PwpImage(PwpData):
    """Class for images that will be moved to Jpg"""

    def __init__(self, filename, config: PwpConfig,
                 working: str or None = None,
                 backup: str or None = None,
                 image=None, iptc_info=None):
        super().__init__(filename, working=working, backup=backup)
        self.creation = self.guess_file_date(filename, config, default_to_filedate=True)

        self.can_be_inserted_in_db = True

        self.iptc_info = iptc_info
        self.image = image
        if image is not None:
            self.image = image
        elif self.filename is not None:
            self.image = Image.open(self.filename)
            if self.image is None:
                LOGGER.error(f"error opening image {self.filename}")

        self.width, self.height = self.image.size

    def incr_logger_count(self, item=None):
        LOGGER.incr_picture("Image" + (f": {item}" if item else ""))

    def close(self):
        """close the image WITHOUT saving"""
        if self.image:
            self.image.close()
            super().close()
            # is self.image is None, the close has already been done
        self.image = None
        if self.filename and ACTOR.isfile(self.filename + '~'):
            ACTOR.delete(self.filename + '~')

    def reopen(self):
        if self.image is None:  # pragma: no cover: defensive code
            if not ACTOR.isfile(self.filename):
                LOGGER.internal_error(f"reopen('{self.filename}'")
            self.image = Image.open(self.filename)

    # We never need patch_after_rename for images,
    # because ALL images are silently converted to JPG in verify_orientation or verify_metadata
    # because we do not read metadata of non JPG files, we do not find metadata,
    # and verify_metadata always generate a JPG file

    def save_with_info(self, config: PwpConfig, new_iptc=None):
        if config['dryrun']:
            LOGGER.debug(f"would save image '{self.filename}'")  # pragma: no cover: defensive code
        else:
            # need to create the file BEFORE setting the iptc info
            if self.image is None:
                LOGGER.internal_error("Image is None")
            ACTOR.mkdirs(os.path.dirname(self.filename))
            self.image.save(self.filename, exif=self.exif_data)
            self.image.close()
            if new_iptc:
                info_resized = IPTCInfo(self.filename, force=True)
                info_resized['copyright notice'] = new_iptc['copyright notice']
                info_resized['special instructions'] = new_iptc['special instructions']
                info_resized['by-line'] = new_iptc['by-line']
                self.iptc_info = info_resized

            if self.iptc_info:
                self.iptc_info.save()

        self.is_modified = False
        self.close()

    def verify_orientation(self, stage: str, config: PwpConfig, summary: PwpSummary):
        ACTOR.copy(self.filename, self.working, forced=True)
        # here, we copy self to working, which DOES have a .jpg extension
        # so, we MAY end-up with a PNG data within a JPG filename
        # this is NOT an issue, because working WILL be modified and saved,
        # and then it WILL have the right JPG format !
        # not very clean, but works.
        # but DOES NOT TAKE enable-conversion into account.

        if stage == "album":
            if config['dryrun']:  # pragma: no cover: defensive code
                ACTOR.copy(self.filename, self.backup, forced=True)
            else:
                ACTOR.move(self.filename, self.backup, forced=True)
            LOGGER.trace(f"backup {self.filename} to {self.backup}")
        if self.working[-4:] == ".jpg":
            new_image = PwpJpg(filename=self.working,
                               working=self.working,
                               backup=None,
                               config=config)  # because the original file has already been back upped
            return new_image.verify_orientation(stage, config, summary)
        else:
            # if this is not a JPG, we DO NOT verify the orientation

            # CAVEAT: This part of the code (i.e. when enable-conversion = false) is NOT Tested
            #
            new_image = PwpData.create(filename=self.working,
                                       config=config,
                                       tmp=self.working,
                                       backup=None)  # because the original file has already been back upped
            return new_image

    def thumbnail(self, filename, width, height, crop, config: PwpConfig, force_rebuild: bool,
                  thumbs_dir: PwpDirEntry, summary: PwpSummary):
        """
        Build a thumbnail and copy it to remote if necessary.
        The thumbnails files are created from local pictures.

        - If a local thumbnail exist and is more recent than the picture,
          then it is considered as valid, and put to the remote location
        - in all other cases, the thumbnail is created again, and put to the remote location afterward

        :param filename: filename name of the thumbnail
        :param width: expected max width
        :param height: expected max height
        :param crop: boolean
        :param config: current configuration
        :param force_rebuild: True, False. If True, MUST rebuild the thumbnail.
        :param thumbs_dir: DirEntry of the directory
        :param summary:
        :return: None
        """

        def after_creation(created: bool):
            """
            Executes actions after the creation of the thumbnail:
            - clean filename~
            - put to remote if necessary
            - setup summary
            :return: None
            """
            pwp_file = PwpFileEntry.lookup(filename, context='thumbnails', config=config)

            if ACTOR.isfile(self.filename + '~'):
                ACTOR.delete(self.filename + '~')  # pragma: no cover: defensive code

            suf = filename[-6:-4]
            if created:
                if suf == "50":
                    summary.thumb_cu = True
                elif suf == "th":
                    summary.thumb_th = True
                elif suf == "me":
                    summary.thumb_me = True
                elif suf == "sq":
                    summary.thumb_sq = True
                else:
                    LOGGER.internal_error(f"Illegal thumbnail {filename}")

            if pwp_file.put():
                remote_path = os.path.dirname(pwp_file.remote)
                LOGGER.trace(f"Thumbnail {filename} sftp to {remote_path}")
                if suf == "50":
                    summary.rem_thumb_cu = True
                elif suf == "th":
                    summary.rem_thumb_th = True
                elif suf == "me":
                    summary.rem_thumb_me = True
                elif suf == "sq":
                    summary.rem_thumb_sq = True
                else:
                    LOGGER.internal_error(f"Illegal thumbnail {filename}")

            self.incr_logger_count("Thumbnail")
            # --------------------------------------- end of subroutine

        if filename in thumbs_dir.files and force_rebuild:
            del thumbs_dir.files[filename]

        if thumbs_dir.exists_and_younger_than(filename, datetime.datetime.fromtimestamp(self.modified_time)):
            LOGGER.trace(f"Thumbnail {filename} is more recent than {self.filename}")
            after_creation(created=False)
            return

        if config['dryrun']:  # pragma: no cover: defensive code
            LOGGER.trace(f"Would create Thumbnail {width}x{height} crop={crop} name={filename}")
            return

        LOGGER.trace(f"Thumbnail {width}x{height} crop={crop} {filename}")

        self.reopen()
        if not crop:
            im_resized = PwpJpg(filename, working=None, backup=None,
                                image=self.image.copy(), iptc_info=self.iptc_info,
                                config=config)
            im_resized.image.thumbnail((width, height), resample=Image.Resampling.LANCZOS)
        else:
            im_resized = PwpJpg(filename, working=None, backup=None,
                                image=ImageOps.fit(self.image, (width, height)),
                                iptc_info=self.iptc_info,
                                config=config)

        dir_name = os.path.dirname(filename)

        ACTOR.mkdirs(dir_name)
        im_resized.set_exif_data('ImageWidth', im_resized.image.width)
        im_resized.set_exif_data('ImageLength', im_resized.image.height)

        if not self.iptc_info:
            # if the source image is not JPG and enable-rename false,
            # then self is not a JPG and self.iptc_info is empty
            LOGGER.config_error(f"--enable-rename false, so '{filename}' cannot be safely managed")

        new_iptc = {'copyright notice': self.iptc_info['copyright notice'] or [],
                    'special instructions': self.iptc_info['special instructions'] or [],
                    'by-line': self.iptc_info['by-line'] or []
                    }

        im_resized.is_modified = True
        im_resized.save_with_info(config, new_iptc=new_iptc)

        after_creation(created=True)

    def handles_metadata(self):
        return True


# ------------------------------------------------------------------------------------------------
# PwpJpg
# ------------------------------------------------------------------------------------------------


class PwpJpg(PwpImage):
    logger = logging.getLogger('iptcinfo')
    logger.setLevel(logging.ERROR)
    tags_reverse = dict(((v, k) for k, v in TAGS.items()))
    orientations = ((None, False),  # 0: is an error
                    (None, False),  # 1: nothing to do
                    (Image.Transpose.FLIP_LEFT_RIGHT, False),  # 2
                    (Image.Transpose.ROTATE_180, False),  # 3
                    (Image.Transpose.FLIP_TOP_BOTTOM, False),  # 4
                    (Image.Transpose.ROTATE_270, True),  # 5
                    (Image.Transpose.ROTATE_270, False),  # 6
                    (Image.Transpose.ROTATE_90, True),  # 7
                    (Image.Transpose.ROTATE_90, False))  # 8
    orient_names = (('None', 'No flip'),  # 0: is an error
                    ('None', 'No flip'),  # 1: nothing to do
                    ('FLIP_LEFT_RIGHT', 'No flip'),  # 2
                    ('ROTATE_180', 'No flip'),  # 3
                    ('FLIP_TOP_BOTTOM', 'No flip'),  # 4
                    ('ROTATE_270', 'Flip'),  # 5
                    ('ROTATE_270', 'No flip'),  # 6
                    ('ROTATE_90', 'Flip'),  # 7
                    ('ROTATE_90', 'No flip'))  # 8
    orient_summa = ('--',  # 0: is an error
                    '--',  # 1: nothing to do
                    '|-',  # 2
                    '^-',  # 3
                    'V-',  # 4
                    '<|',  # 5
                    '<-',  # 6
                    '>|',  # 7
                    '>-')  # 8

    def __init__(self, filename, config: PwpConfig, working=None, backup=None, image=None, iptc_info=None):
        super().__init__(filename, config, working, backup,  image=image, iptc_info=iptc_info)
        self.exif_data = None

        self.sub_sec_time = None
        self.orientation = 1

        self.latitude = None
        self.longitude = None

        # NB: width, height = self.image.size

        # the values initialized here are the INITIAL values BEFORE piwiPre actions
        self.exif_data = self.image.getexif()
        if self.exif_data:
            exif_table = {}
            gps_data = {}
            for tag, value in self.exif_data.items():
                decoded = TAGS.get(tag, tag)
                exif_table[decoded] = value
                if decoded == 'GPSInfo':
                    gps_info = self.exif_data.get_ifd(tag)
                    for key, val in gps_info.items():
                        sub_decoded = GPSTAGS.get(key, key)
                        gps_data[sub_decoded] = val

            date_time = exif_table['DateTime'] if 'DateTime' in exif_table else \
                exif_table['DateTimeOriginal'] if 'DateTimeOriginal' in exif_table else None

            self.creation = self.get_date(date_time)

            self.make = exif_table['Make'] if 'Make' in exif_table else None
            self.model = exif_table['Model'] if 'Model' in exif_table else None
            self.sub_sec_time = exif_table['SubsecTime'] if 'SubsecTime' in exif_table else None   # noqa
            self.orientation = int(exif_table['Orientation']) if 'Orientation' in exif_table else 1

            self.latitude = self.get_gps(gps_data, 'GPSLatitudeRef', 'GPSLatitude')
            self.longitude = self.get_gps(gps_data, 'GPSLongitudeRef', 'GPSLongitude')

            # sst2 = self.get_data(exif_data, 'SubsecTimeOriginal')     # noqa
            # sst3 = self.get_data(exif_data, 'SubsecTimeDigitized')    # noqa
        else:
            LOGGER.debug(f"No exif data in '{self.filename}'")

        if iptc_info:
            self.iptc_info = iptc_info
        elif self.filename and ACTOR.isfile(self.filename):
            self.iptc_info = IPTCInfo(self.filename, force=True)

        if isinstance(self.iptc_info, IPTCInfo):
            b1 = self.iptc_info['special instructions']
            self.special = self.decode(b1, self.filename, "special")
            b2 = self.iptc_info['copyright notice']
            self.copyright = self.decode(b2, self.filename, "copyright")
            b3 = self.iptc_info['by-line']
            self.author = self.decode(b3, self.filename, "author")

        #  self.close() # NO: we keep the file open because we may want to rotate it.

    @staticmethod
    def decode(buffer, filename, info):
        if not buffer:
            return None
        try:
            return buffer.decode('utf8')
        except UnicodeDecodeError as e:
            LOGGER.trace(f"Error {e} while decoding IPTC {info} for {filename}")  # pragma: no cover: defensive code
        return None

    def incr_logger_count(self, item=None):
        LOGGER.incr_picture("Jpg" + (f": {item}" if item else ""))

    def patch_after_rename(self, new_filepath):
        """
        For some objects, it is necessary to patch the name that rename generates
        :param new_filepath:
        :return: patched version
        """
        return new_filepath

    def handles_metadata(self):
        return True

    # management of GPS data in EXIF:
    # exif standard can be found on http://web.archive.org/web/20131018091152/http://exif.org/Exif2-2.PDF
    # Name              TagID (hex)     Type        Count
    # GPSLatitudeRef    1               ascii       2       'N' for north, 'S' for south
    # GPSLatitude       2               RATIONAL    3
    # GPSLongitudeRef   3               ascii       2       'E'/'W'
    # Longitude         4               RATIONAL    3
    #
    # Rational:
    #   method 1:   degrees, minutes and second : dd/1,mm/1,ss/1
    #   method 2:   degrees and minutes :  dd/1,mmmm/100,0/1.

    @staticmethod
    def get_gps(data: dict, ref, rational):
        """
        decodes from DMS or DM to float
        :param data: dict of gps data
        :param ref: string for N/S or E/W reference
        :param rational: string for 3 valued data
        :return: lat (or long)
        """
        if rational not in data.keys() or ref not in data.keys():
            return None

        sign = -1 if data[ref] in ['S', 'W'] else 1
        deg, minutes, sec = data[rational]
        return sign * round(float(deg + minutes/60 + sec / 3600), 6)  # 6 is te precision of floats in the database

    def set_exif_data(self, tag_id, value):
        # https://www.thepythoncode.com/code/extracting-image-metadata-in-python
        # get the tag name, instead of human unreadable tag id
        tag = self.tags_reverse.get(tag_id)
        self.exif_data[tag] = value

    def write_metadata(self, new_author: str, new_copyright: str, new_special: str,
                       new_date: datetime.datetime,
                       config: PwpConfig):
        if not self.iptc_info:
            LOGGER.error(f"ERROR writing IPTC from '{self.filename}'")

        if self.working != self.filename:
            ACTOR.copy(self.filename, self.working)

            new_image = PwpJpg(filename=self.working,
                               working=self.working,
                               backup=None,
                               config=config)            # because the original file has already been back upped
        else:
            new_image = self
            self.reopen()

        new_author = new_author or ''
        new_special = new_special or ''
        new_copyright = new_copyright or ''

        new_image.special = new_special
        new_image.copyright = new_copyright
        new_image.author = new_author
        new_image.creation = new_date

        new_iptc = {'copyright notice': new_copyright.encode("utf8"),
                    'special instructions': new_special.encode("utf8"),
                    'by-line': new_author.encode("utf8")
                    }
        date_str = new_date.strftime("%Y-%m-%d %H:%M:%S")
        new_image.set_exif_data('DateTime', date_str)
        new_image.set_exif_data('DateTimeOriginal', date_str)

        new_image.is_modified = True   # to ensure file IS written
        new_image.save_with_info(config, new_iptc)
        return new_image

    def verify_orientation(self, _stage: str, config: PwpConfig, summary: PwpSummary):
        """
        self is supposed to be open

        if necessary:
        - saves the file to back up
        - rotates the file
        - stores the rotated picture in a copy
        - set is_modified to True
        - manages LOGGER.info()

        lives the file open for further processing
        return: self or a copy, modified"""

        if config['enable-rotation'] is False:
            return self, "", False

        (angle, flip) = self.orientations[self.orientation]
        (a, r) = self.orient_names[self.orientation]
        summary.rotation = self.orient_summa[self.orientation]

        modified = False
        new_image = self
        # here, new_image is always the image we want to handle

        if angle is not None:
            if config['dryrun']:
                LOGGER.trace(f"Would clean ROTATION {self.orientation} {a} {r} '{self.filename}'")
            else:
                transposed = self.image.transpose(method=angle)
                width = self.image.width
                height = self.image.height
                self.close_if_backup()

                new_image = PwpJpg(filename=self.working,
                                   working=self.working,
                                   backup=None,  # because the original file has already been back upped
                                   image=transposed, iptc_info=self.iptc_info,
                                   config=config)
                new_image.set_exif_data('ImageWidth', width)
                new_image.set_exif_data('ImageLength', height)
                new_image.set_exif_data('Orientation', 1)
                new_image.is_modified = True

                LOGGER.trace(f"ROTATION {self.orientation} {a} {r} '{self.filename}'")
                modified = True

        if flip:
            if config['dryrun']:
                LOGGER.trace(f"Would clean FLIP {self.orientation} {a} {r}'{self.filename}'")
            else:
                transposed = new_image.image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
                new_image.close_if_backup()

                new_image = PwpJpg(filename=self.working,
                                   working=self.working,
                                   backup=None,  # because the original file has already been back upped
                                   image=transposed,
                                   iptc_info=self.iptc_info,
                                   config=config)
                new_image.set_exif_data('Orientation', 1)
                new_image.is_modified = True
                LOGGER.trace(f"FLIP {self.orientation} {a} {r}'{self.filename}'")

                modified = True

        return new_image, modified


# ------------------------------------------------------------------------------------------------
# PwpVideo
# ------------------------------------------------------------------------------------------------


class PwpVideo(PwpData):
    """
    PwpVideo: the base class for all video files, supported or not
    uses ffmpeg and ffproble to set/get metadata
    """  # noqa

    def __init__(self, filename, working, backup, config: PwpConfig):
        super().__init__(filename, working, backup)
        self.get_metadata(config)
        self.can_be_inserted_in_db = True
        self.representative = os.path.dirname(filename) + '/pwg_representative/' + pathlib.Path(filename).stem + '.jpg'

    def incr_logger_count(self, item=None):
        LOGGER.incr_picture("Video" + (f": {item}" if item else ""))

    def handles_metadata(self):
        return True

    def get_metadata(self, config: PwpConfig):
        ffprobe = config['ffmpeg-path'] + '/ffprobe'
        cmd = [ffprobe, "-hide_banner", "-i", self.filename]
        res = None
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, text=True)
        except subprocess.CalledProcessError as e:
            LOGGER.internal_error(f"ERROR {e} while getting metadata for '{self.filename}'")

        if res is None:
            LOGGER.internal_error(f"Unknown ERROR while getting metadata for '{self.filename}'")

        buffer = res.stdout.splitlines()  # (res.stdout.decode('utf8') + res.stderr.decode('utf8'))
        for line in buffer:
            r = re.match(r"\s\s\s\sartist\s*: (.*)$", line)
            if r:
                self.author = r.group(1)
                continue

            r = re.match(r"\s\s\s\scomment\s*: (.*)$", line)
            if r:
                self.special = r.group(1)
                continue

            r = re.match(r"\s\s\s\scopyright\s*: (.*)$", line)
            if r:
                self.copyright = r.group(1)
                continue

            r = re.match(r"\s\s\s\screation_time\s*: (.*)$", line)
            if r:
                str_rep = r.group(1)
                self.creation = self.get_date(str_rep)
                continue

            r = re.match(r"\s+Stream .* Video: .*, (\d+)x(\d+).*, \d+ kb/s, .*$", line)
            #  Stream #0:0[0x1](und): Video: h264 (High 4:2:2) (avc1 / 0x31637661), ..., 320x240, 546 kb/s, ...
            #  Stream #0:0[0x1](eng): Video: h264 (High)..., 1080x1920 [SAR 1:1 DAR 9:16], 5819 kb/s, ...
            if r:
                self.width = int(r.group(1))
                self.height = int(r.group(2))
                continue
        LOGGER.debug(f"Video '{self.filename}' width {self.width} height {self.height}")

    def write_metadata(self, new_author: str, new_copyright: str, new_special: str,
                       new_date: datetime.datetime, config: PwpConfig):
        self.close_if_backup()
        ACTOR.mkdirs(os.path.dirname(self.working), forced=True)

        modified = False
        path = config['ffmpeg-path'] or ""
        if path and path[-1] != "/":
            path += '/'
        ffmpeg = path + 'ffmpeg'
        cmd = [ffmpeg, "-i", self.filename,
               "-loglevel", "error",
               "-err_detect", "ignore_err",
               "-movflags", "+faststart",   # see https://ffmpeg.org/ffmpeg-formats.html fragmentation  # noqa
               "-c:v", "libx264",
               "-profile:v", "high",
               "-c:a", "aac",
               #  "-b:a", "128k", #  set audio bitrate to mp4 default                                   # noqa
               #  "-ar", "48k",   # set the audio sampling frequency
               "-pix_fmt", "yuvj420p",  # videoJS does not support 4:2:2 with firefox, but does with chrome... # noqa
               # this raises a warning,
               # color range should be specified with a separate flag, but doc still unclear
               ]
        if new_author:
            cmd.extend(['-metadata', f'artist={new_author}'])           # NB: wrong warning extend
            modified = True
        if new_special:
            cmd.extend(['-metadata', f'comment={new_special}'])         # NB: wrong warning extend
            modified = True
        if new_copyright:
            cmd.extend(['-metadata', f'copyright={new_copyright}'])     # NB: wrong warning extend
            modified = True
        if new_date:
            str_date = new_date.strftime("%Y-%m-%d %H:%M:%S.000000Z")  # To check: "%f" instead of 0000
            cmd.extend(['-metadata', f'creation_time={str_date}'])
            modified = True

        # example cmd:
        # "C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe" -i "2016-06-18_Gym_144055.mp4" -loglevel error           # noqa
        #  -movflags +faststart -c:v libx264  -profile:v main -c:a aac -ar 48k -b:a 128k -pix_fmt yuvj420p # noqa
        #  -metadata author="Author"  "\\NAS\photo\Gym\2016-06-18-Gym\2016-06-18_Gym_144055.mp4"                  # noqa

        cmd.append(self.working)

        if not modified:
            return self

        # if the original file is mp4 and has not been already processed by piwiPre
        # then there is almost no chance that it already has all metadata
        # so we end-up converting it again, which adds the faststart mp4 option
        try:
            subprocess.run(cmd, capture_output=True, check=True)  # capture = True avoid seeing output of cmd
        except subprocess.CalledProcessError as e:
            LOGGER.internal_error(f"ERROR {e} while transcoding '{self.filename}' -> '{self.working}'")

        return PwpData.create(self.working,
                              config=config,
                              tmp=self.working,
                              backup=None)

    def verify_orientation(self, _stage: str, _config: PwpConfig, _summary: PwpSummary):
        return self, False

    def patch_after_rename(self, new_filepath):
        """
        For KEPT objects, it is necessary to patch the name that rename generates:
        :param new_filepath: after rename
        :return: patched version
        """
        old_filename = os.path.basename(self.filename)
        suffix = pathlib.Path(old_filename).suffix[1:]
        le = len(suffix)
        new_filepath = new_filepath[:-le] + 'mp4'
        return new_filepath

    @staticmethod
    def build_representative(source, destination, config: PwpConfig,
                             new_author: str, new_copyright: str, new_special: str,
                             new_date: datetime.datetime):
        #
        # ffmpeg  -i input -loglevel error- vf select='eq(pict_type\,I)'  -frames:v 1 -q:v 2 output.jpg
        #
        path = config['ffmpeg-path'] or ""
        if path and path[-1] != "/":
            path += '/'
        ffmpeg = path + 'ffmpeg'
        cmd = [ffmpeg,
               "-i", source,
               "-loglevel", "error",
               "-vf", "select='eq(pict_type\\,I)'",
               "-frames:v", "1",
               "-q:v", "2",
               destination,
               ]
        if new_author:
            cmd.extend(['-metadata', f'artist={new_author}'])
        if new_special:
            cmd.extend(['-metadata', f'comment={new_special}'])
        if new_copyright:
            cmd.extend(['-metadata', f'copyright={new_copyright}'])
        if new_date:
            str_date = new_date.strftime("%Y-%m-%d %H:%M:%S.000000Z")  # To check: "%f" instead of 0000
            cmd.extend(['-metadata', f'creation_time={str_date}'])

        try:
            subprocess.run(cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            LOGGER.internal_error(f"ERROR {e} while building representative for '{source}'")

        jpg = PwpData.create(destination, config=config, tmp=destination)
        # working = destination insures that the metadata is writen correctly

        # stage = album because representative is always inside album
        jpg.write_metadata(new_author=new_author, new_copyright=new_copyright, new_special=new_special,
                           new_date=new_date, config=config)
        jpg.close()
        LOGGER.trace(f"Built representative '{destination}' for '{source}'")


class PwpMp4(PwpVideo):
    def __init__(self, filename,  config: PwpConfig, working=None, backup=None):
        super().__init__(filename, config=config, working=working, backup=backup)

    def incr_logger_count(self, item=None):
        LOGGER.incr_picture("Mp4" + (f": {item}" if item else ""))

    def handles_metadata(self):
        return True


class PwpAvoided(PwpData):
    def __init__(self, filename, backup):
        super().__init__(filename, None, backup=backup)
        self.to_abort = True

    def incr_logger_count(self, item=None):
        LOGGER.incr_picture("Not managed" + (f": {item}" if item else ""))


class PwpKept(PwpData):
    def __init__(self, filename, backup):
        super().__init__(filename, None, backup=backup)

    def incr_logger_count(self, item=None):
        LOGGER.incr_picture("Kept" + (f": {item}" if item else ""))

    def handles_metadata(self):
        return False

    def patch_after_rename(self, new_filepath):
        """
        For KEPT objects, it is necessary to patch the name that rename generates:
        :param new_filepath: after rename
        :return: patched version
        """
        old_filename = os.path.basename(self.filename)
        new_filepath = os.path.dirname(new_filepath) + '/' + old_filename  # to keep filename
        return new_filepath
