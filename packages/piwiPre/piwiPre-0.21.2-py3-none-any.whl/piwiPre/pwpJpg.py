# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

import datetime
import logging
import re
import os

# pip install Pillow
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import ImageOps

# pip install iptcinfo3
from iptcinfo3 import IPTCInfo

from piwiPre.pwpActor import ACTOR
from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpErrors import LOGGER, PwpConfigError


class PwpObject:
    """Root class for PwpJpg and PwpMP4"""

    def __init__(self, filename):
        self.filename = filename
        self.copyright = None
        self.special = None
        self.author = None

    def close(self):
        pass  # nothing to do on txt files

    def write_metadata(self, _new_author, _new_copyright, _new_special):
        pass  # nothing to do on txt files

    def rotate(self, _stage: str, _any):
        return False  # nothing to do with text or mp4

    @staticmethod
    def guess_file_date(image_path: str, config: PwpConfig):
        """
        :param image_path: the full path to image
        :param config: the current configuration
        :return: date
        """

        dates = config['dates']
        if not isinstance(dates, dict):
            dates = {}
        if dates is not None and 'NO-DATE' in dates:
            spec = dates['NO-DATE']
            if 'forced' not in spec:
                raise PwpConfigError("date:NO-DATE config without a 'forced' statement")
            new_date = spec['forced']
            return datetime.datetime(**new_date)

        filename = os.path.basename(image_path)
        template = os.path.basename(config['names'])
        file_info = ACTOR.get_info_from_format(template, filename)
        if file_info is not None and 'Y' in file_info and file_info['Y'] is not None and \
                'm' in file_info and file_info['m'] is not None and \
                'd' in file_info and file_info['d'] is not None and \
                'H' in file_info and file_info['H'] is not None and \
                'S' in file_info and file_info['S'] is not None:
            return datetime.datetime(year=int(file_info['Y']),
                                     month=int(file_info['m']),
                                     day=int(file_info['d']),
                                     hour=int(file_info['H']),
                                     minute=int(file_info['M']),
                                     second=int(file_info['S']))  # TODO: Manage timezone and AM/PM

        m = re.match(r"VID(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)\.mp4", filename) or \
            re.match(r"VID_(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\.mp4", filename) or \
            re.match(r".*-(\d\d\d\d)-(\d\d)-(\d\d)-(\d\d)h(\d\d)-(\d\d).*\.jpg", filename)
        if m:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            hours = int(m.group(4))
            minutes = int(m.group(5))
            seconds = int(m.group(6))
            return datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)

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
            return datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)

        LOGGER.debug(f"Cannot guess date for {image_path}")
        return datetime.datetime.fromtimestamp(os.path.getmtime(image_path))

    def set_metadata(self, _stage, config: PwpConfig,
                     date=datetime.datetime.today(),
                     new_author="Photographer",
                     confirm=True):
        """
        :param _stage: triage or album
        :param config: local configuration
        :param date: date to set
        :param new_author: author to set in exif
        :param confirm: is True, always write metadata, if False, write only if not set
        :return: True if the file was modified
        """
        self.close()  # we know that image will be no more modified

        if config['enable-metadata'] is False:
            return False

        info_format = config.format('instructions')
        info_dico = config.format_dict(date, new_author)
        new_special = info_format.format(**info_dico)
        if confirm:
            modified = self.special is None or self.special == ''
        else:
            modified = self.special != new_special

        if confirm:
            modified = modified or (self.author is None or self.author == '')
        else:
            modified = modified or self.author != new_author

        info_format = config.format('copyright')
        info_dico = config.format_dict(date, new_author)
        new_copyright = info_format.format(**info_dico)
        if confirm:
            modified = modified or (self.copyright is None or self.copyright == '')
        else:
            modified = modified or self.copyright != new_copyright

        if not modified:
            return False

        # LOGGER.msg(f"write IPTC info '{self.filename}'")
        if config['dryrun']:
            return modified

        return self.write_metadata(new_author, new_copyright, new_special)


class PwpJpg(PwpObject):
    logger = logging.getLogger('iptcinfo')
    logger.setLevel(logging.ERROR)
    tags_reverse = dict(((v, k) for k, v in TAGS.items()))
    orientations = ((None, False),  # 0: is an error
                    (None, False),  # 1: nothing to do
                    (Image.FLIP_LEFT_RIGHT, False),  # 2
                    (Image.ROTATE_180, False),  # 3
                    (Image.FLIP_TOP_BOTTOM, False),  # 4
                    (Image.ROTATE_270, True),  # 5
                    (Image.ROTATE_270, False),  # 6
                    (Image.ROTATE_90, True),  # 7
                    (Image.ROTATE_90, False))  # 8
    orient_names = (('None', 'No flip'),  # 0: is an error
                    ('None', 'No flip'),  # 1: nothing to do
                    ('FLIP_LEFT_RIGHT', 'No flip'),  # 2
                    ('ROTATE_180', 'No flip'),  # 3
                    ('FLIP_TOP_BOTTOM', 'No flip'),  # 4
                    ('ROTATE_270', 'Flip'),  # 5
                    ('ROTATE_270', 'No flip'),  # 6
                    ('ROTATE_90', 'Flip'),  # 7
                    ('ROTATE_90', 'No flip'))  # 8

    def __init__(self, filename=None, image=None, iptc_info=None):
        super().__init__(filename)
        self.image = image
        self.exif_data = None
        self.DateTimeOriginal = None
        self.DateTime = None
        self.Make = None
        self.Model = None
        self.SubSecTime = None
        self.orientation = 1
        self.iptc_info = None

        if filename is not None:
            self.image = Image.open(filename)

        if self.image is None:
            LOGGER.warning(f"error opening jpg image {filename}")

        # the values initialized here are the INITIAL values BEFORE piwiPre actions
        self.exif_data = self.image.getexif()
        if self.exif_data:
            self.DateTimeOriginal = self.get_exif_value('DateTimeOriginal')
            self.DateTime = self.get_exif_value('DateTime')
            self.Make = self.get_exif_value('Make')
            self.Model = self.get_exif_value('Model')
            self.SubSecTime = self.get_exif_value('SubsecTime')  # noqa
            orient = self.get_exif_value('Orientation')
            self.orientation = int(orient) if orient is not None else 1

            # sst2 = self.get_data(exif_data, 'SubsecTimeOriginal')     # noqa
            # sst3 = self.get_data(exif_data, 'SubsecTimeDigitized')    # noqa
        else:
            LOGGER.debug(f"No exif data in '{self.filename}'")

        if filename:
            self.iptc_info = IPTCInfo(self.filename, force=True)
        else:
            self.iptc_info = iptc_info

        if isinstance(self.iptc_info, IPTCInfo):
            b1 = self.iptc_info['special instructions']
            self.special = b1.decode('utf8') if b1 is not None else None
            b2 = self.iptc_info['copyright notice']
            self.copyright = b2.decode('utf8') if b2 is not None else None
            b3 = self.iptc_info['by-line']
            self.author = b3.decode('utf8') if b3 is not None else None

        # self.close() # NO: we keep the file open because we may want to rotate it.

    def reopen(self):
        if self.image is None:
            self.image = Image.open(self.filename)

    def close(self):
        """close the image WITHOUT saving"""
        if self.image:
            self.image.close()
        self.image = None

    def save(self, filename, config: PwpConfig):
        self.filename = filename
        if not config['dryrun']:
            self.image.save(filename, exif=self.exif_data)
        self.image.close()
        if os.path.isfile(filename + '~'):
            os.remove(filename + '~')

    def get_exif_value(self, tag_id):
        # https://www.thepythoncode.com/code/extracting-image-metadata-in-python
        # get the tag name, instead of human unreadable tag id
        tag = self.tags_reverse.get(tag_id)
        data = self.exif_data.get(tag)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        return data

    def set_exif_data(self, tag_id, value):
        # https://www.thepythoncode.com/code/extracting-image-metadata-in-python
        # get the tag name, instead of human unreadable tag id
        tag = self.tags_reverse.get(tag_id)
        self.exif_data[tag] = value

    def get_jpg_new_date(self, config: PwpConfig):
        """
        :param config: current configuration
        :return: date, author
        """

        author = config.default_author()

        if self.exif_data is None:
            return self.guess_file_date(self.filename, config), author

        stamp = self.DateTimeOriginal or self.DateTime
        if not stamp:
            LOGGER.debug(f"No exif dates in '{self.filename}'")
            return self.guess_file_date(self.filename, config), author

        m = re.match(r"(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)", stamp)
        if not m:
            LOGGER.debug(f"ERROR reading date from filename '{self.filename}'")
            return self.guess_file_date(self.filename, config), author

        (year, month, day, h, m, s) = m.groups()  # noqa
        year = int(year)
        month = int(month)
        day = int(day)
        h = int(h)
        m = int(m)
        s = int(s)

        apn = self.get_exif_value('Model')
        if apn is not None:
            apn = re.sub(r"\t", "", apn)
            apn = re.sub(r"\s", "", apn)
            apn = re.sub(r"\x00", "", apn)

        LOGGER.debug(f"Date = {year:04}/{month:02}/{day:02} {h:02}:{m:02}:{s:02} before correction")
        photo_date = datetime.datetime(year=year, month=month, day=day, hour=h, minute=m, second=s)

        author = config.author(apn, photo_date)
        new_date = config.fix_date(self.filename, photo_date, apn)

        LOGGER.debug(f"Date = {new_date.year:04}/{new_date.month:02}/{new_date.day:02} " +
                     f"{new_date.hour:02}:{new_date.minute:02}:{new_date.second:02} after correction")

        return new_date, author

    def write_metadata(self, new_author, new_copyright, new_special):
        if not self.iptc_info:
            LOGGER.debug(f"ERROR writing IPTC from '{self.filename}'")
            return False

        self.iptc_info['by-line'] = new_author
        self.iptc_info['special instructions'] = new_special
        self.iptc_info['copyright notice'] = new_copyright

        self.iptc_info.save()
        ACTOR.delete(self.filename + '~')
        return True

    @staticmethod
    def get_remote_web_filename(config, filename):
        """
        :param config: local configuration
        :param filename: local name
        :return: the remote path to be used for sftp
        """
        remote = (config['enable-remote-copy'] and config['remote-web'] and
                  config['remote-host'] and config['remote-port'])
        remote_file = None
        if remote:
            win_rel_path = os.path.relpath(filename, config['web'])
            rel_path = win_rel_path.replace('\\', '/')
            remote_file = config['remote-web'] + '/' + rel_path
        return remote_file

    def thumbnail(self, filename, width, height, crop, config: PwpConfig, allow_clobber: bool):
        """
        Build a thumbnail
        :param filename: filename name of the thumbnail
        :param width: expected max width
        :param height: expected max height
        :param crop: boolean
        :param config: current configuration
        :param allow_clobber: True, False
        :return: True if the thumbnail has been generated
        """

        if os.path.isfile(filename):
            if allow_clobber:
                ACTOR.delete(filename)
            else:
                return False

        remote_file = self.get_remote_web_filename(config, filename)
        if remote_file and ACTOR.remote_isfile(remote_file) and not allow_clobber:
            LOGGER.info(f"Thumbnail {filename} already exists remotely as {remote_file}")
            return False

        if config['dryrun']:
            LOGGER.info(f"Would create Thumbnail {width}x{height} crop={crop} name={filename}")
            return False
        LOGGER.info(f"Thumbnail {width}x{height} crop={crop} {filename}")

        if not crop:
            im_resized = PwpJpg(image=self.image.copy(), iptc_info=self.iptc_info)
            im_resized.image.thumbnail((width, height), resample=Image.LANCZOS)
        else:
            im_resized = PwpJpg(image=ImageOps.fit(self.image, (width, height)), iptc_info=self.iptc_info)

        dir_name = os.path.dirname(filename)

        ACTOR.mkdirs(dir_name)
        im_resized.set_exif_data('ImageWidth', im_resized.image.width)
        im_resized.set_exif_data('ImageLength', im_resized.image.height)
        im_resized.save(filename, config)

        info_resized = IPTCInfo(filename, force=True)
        info_resized['copyright notice'] = self.iptc_info['copyright notice']
        info_resized['special instructions'] = self.iptc_info['special instructions']
        info_resized.save()
        ACTOR.delete(filename + '~')
        ACTOR.delete(self.filename + '~')

        if remote_file:
            remote_path = os.path.dirname(remote_file)
            LOGGER.info(f"Thumbnail {filename} sftp to {remote_path}")
            ACTOR.remote_put(filename, remote_path)
        return True

    def rotate(self, stage: str, config: PwpConfig):
        """ return True if picture was modified"""
        if config['enable-rotation'] is False:
            return False

        modified = False
        (angle, flip) = self.orientations[self.orientation]
        (a, r) = self.orient_names[self.orientation]

        new_image = self
        if angle is not None:
            if config['dryrun']:
                LOGGER.debug(f"Would clean ROTATION {self.orientation} {a} {r} '{self.filename}'")
            else:
                self.reopen()
                transposed = self.image.transpose(method=angle)
                new_image = PwpJpg(image=transposed, iptc_info=self.iptc_info)
                new_image.set_exif_data('ImageWidth', self.image.width)
                new_image.set_exif_data('ImageLength', self.image.height)
                new_image.set_exif_data('Orientation', 1)
                modified = True
                LOGGER.debug(f"ROTATION {self.orientation} {a} {r} '{self.filename}'")

        if flip:
            if config['dryrun']:
                LOGGER.debug(f"Would clean FLIP {self.orientation} {a} {r}'{self.filename}'")
            else:
                new_image.reopen()
                new_image = PwpJpg(image=new_image.image.transpose(method=Image.FLIP_LEFT_RIGHT),
                                   iptc_info=self.iptc_info)
                new_image.set_exif_data('Orientation', 1)
                modified = True
                LOGGER.debug(f"FLIP {self.orientation} {a} {r}'{self.filename}'")

        if modified and not config['dryrun']:
            new_image.save(self.filename, config)
        return modified
