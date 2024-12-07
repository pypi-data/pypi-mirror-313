# see https://www.kaggle.com/code/humananalog/examine-mp4-files-with-python-only

# More information about the MP4 file format at the following links:
#
#     http://xhelmboyx.tripod.com/formats/mp4-layout.txt
#     https://github.com/OpenAnsible/rust-mp4/raw/master/docs/ISO_IEC_14496-14_2003-11-15.pdf
#     https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFPreface/qtffPreface.html

# import os, sys
import struct
import datetime
import sys
import argparse

from piwiPre.pwpActor import ACTOR
from piwiPre.pwpErrors import PwpError, LOGGER
from piwiPre.pwpJpg import PwpObject


class PwpMp4Box:
    having_sons = ["moov", "udta", "trak"]  # noqa

    def __init__(self, f, father, context, offset: int, get_boxes=True):
        self.option_1 = False
        self.length = None
        self.name = None
        self.data = None
        self.father = father
        self.context = context
        self.offset = offset
        self.file = f
        self.header_length = 8
        self.boxes = {}
        self.boxes_list = []

        self.length = self.get_unsigned(f, 4)
        if self.length is None:
            return

        self.name = self.get_str(f, 4)
        # Note: if any box grows in excess of 2^32 bytes (> 4.2 GB), the box size can be extended
        # in increments of 64 bits (18.4 EB).
        # By setting the box size to 1 and appending a new 64 bit box size.
        if self.length == 1:
            self.option_1 = True
            data = f.read(8)
            self.length, = struct.unpack("> Q", data)
            self.header_length += 8
        if get_boxes and self.name in self.having_sons:
            self.boxes, self.boxes_list = PwpMp4.find_boxes(f, self)
            f.seek(self.offset + self.length, 0)  # because some boxes may have been read not completely
        else:
            self.data = f.read(self.length - self.header_length)

    def pack_header(self):
        s = struct.Struct("> I 4s")
        s1 = struct.Struct("> I 4s Q")
        if self.option_1:
            data = s1.pack(1, self.name.encode(), self.length)
        else:
            data = s.pack(self.length, self.name.encode())
        return data

    def print(self, suffix=""):
        fl = " Header type 1" if self.option_1 else ""
        fn = self.father.name if self.father else "root"
        LOGGER.msg(f"{suffix}box({fn}):'{self.name}' offset {self.offset:8} length {self.length:8} {fl} {self.context}")
        for box in self.boxes_list:
            box.print(suffix=suffix + "  ")
        if len(self.boxes_list) > 0:
            LOGGER.msg(f"{suffix}--- end of {self.name}")

    @staticmethod
    def get_str(f, length):
        data = f.read(length)
        if data == b"":
            return None
        val = data.decode('utf8')
        return val

    @staticmethod
    def get_unsigned(f, length):
        data = f.read(length)
        if data == b"":
            return None
        val = int.from_bytes(data, "big")
        return val

    def equals(self, box):
        return self.name == box.name and self.offset == box.offset and \
            self.option_1 == box.option_1 and self.length == box.length


class PwpMp4(PwpObject):
    def __init__(self, filename):
        super().__init__(filename)

        self.root_boxes = {}
        self.root_list = []
        self.moov_boxes = {}  # noqa
        self.moov_list = []  # noqa
        self.creation = None
        self.copyright = None
        self.udta_boxes = {}  # noqa
        self.udta_list = []  # noqa
        self.cprt = None  # noqa

        with open(filename, 'rb') as f:
            self.root_boxes, self.root_list = self.find_boxes(f, None)

            if "ftyp" not in self.root_boxes or self.root_boxes["ftyp"].offset != 0:  # noqa
                raise PwpError("wrong MP4 structure: offset(ftyp) not 0", filename)  # noqa

            if "moov" not in self.root_boxes:  # noqa
                raise PwpError("wrong MP4 structure: no moov box ", filename)  # noqa

            self.moov_boxes, self.moov_list = self.find_boxes(f, self.root_boxes["moov"])  # noqa

            self.creation = self.get_creation(f, self.moov_boxes["mvhd"])  # noqa

            if "udta" in self.moov_boxes:  # noqa
                self.udta_boxes, self.udta_list = self.find_boxes(f, self.moov_boxes["udta"])  # noqa
                if "cprt" in self.udta_boxes:  # noqa
                    self.cprt = self.udta_boxes["cprt"]  # noqa
                    self.copyright = self.get_copyright(f, self.cprt)

    def print(self):
        LOGGER.msg(f"mp4       '{self.filename}'")
        LOGGER.msg(f"creation   {self.creation}")
        LOGGER.msg(f"Copyright '{self.copyright}'")
        for box in self.root_list:
            box.print("   ")

    @staticmethod
    def get_copyright(f, box: PwpMp4Box):
        f.seek(box.offset + box.header_length + 6, 0)  # skip header, lang
        char = 1
        res = bytes()
        while char != b'\x00':
            char = f.read(1)
            if char != b'\x00':
                res += char
        res_str = res.decode('utf8')
        return res_str

    @staticmethod
    def find_boxes(f, father: PwpMp4Box | None):
        """Returns a dictionary of all the data boxes and their absolute starting
        and ending offsets inside the mp4 file.

        when finished, the seek pointer is at end of data
        """
        if father is None:
            offset = 0
            end_offset = float("inf")
        else:
            offset = father.offset + father.header_length
            end_offset = father.offset + father.length

        boxes = {}
        boxes_list = []

        f.seek(offset, 0)
        while offset < end_offset - 8:
            box = PwpMp4Box(f, father, "parsing", offset)
            if box.length is None:
                return boxes, boxes_list
            # box.print()
            boxes[box.name] = box
            boxes_list.append(box)
            offset += box.length
        return boxes, boxes_list

    def add_box(self, filename, added_data: []):
        """Adds a box at the end of the current box described by the offset"""
        added_length = len(added_data)
        current = self.root_boxes["moov"]  # noqa
        udta_length = 0 if self.copyright is None else self.moov_boxes["udta"].length  # noqa

        insert = True
        with open(filename, "wb") as nf, open(self.filename, 'rb') as f:
            f_offset = 0
            n_offset = 0

            data = f.read(current.offset)
            f_offset += current.offset

            nf.write(data)
            n_offset += current.offset
            assert n_offset == f_offset  # noqa before the header of moov

            moov = PwpMp4Box(f, None, "Adding a box", current.offset, get_boxes=False)  # noqa
            f_offset += moov.length  # noqa after the moov box, because we read the entire box
            # noqa moov.print()
            assert current.equals(moov)

            if insert:
                moov.length += added_length - udta_length
                # noqa print(f"new length of moov {moov.length}")
            data = moov.pack_header()
            nf.write(data)
            n_offset += len(data)
            nf.write(moov.data)
            n_offset += len(moov.data)
            if insert and udta_length:
                nf.seek(-udta_length, 1)  # noqa go back to the start of udta
                n_offset -= udta_length
            assert n_offset == f_offset - udta_length  # noqa udta should be inserted

            # the new box must be inserted in the padding area reserved in the next box which must be "free"
            # and we lower the free zone for the same amount.

            if insert:
                nf.write(added_data)
                n_offset += len(added_data)
                assert n_offset == f_offset + (added_length - udta_length)  # noqa after udta

            # follow box should be 'free'
            free = PwpMp4Box(f, None, "next insert", f_offset, get_boxes=False)
            assert free.name == 'free'
            # free.print()
            initial_free_length = free.length

            if insert:
                free.offset = f_offset + (added_length - udta_length)
                free.length -= (added_length - udta_length)
                free.context = "modified for insert"
                # free.print()

            free_header = free.pack_header()
            nf.write(free_header)
            n_offset += len(free_header)
            assert len(free_header) == free.header_length

            assert n_offset == f_offset + (added_length - udta_length) + len(free_header)  # after the new free header

            f_offset += initial_free_length  # the real position of the seek index

            nf.write(bytes(1) * (free.length - free.header_length))
            # here free.length is the real length after removing added_length
            n_offset += (free.length - free.header_length)

            assert n_offset == f_offset

            # we should find here new boxes
            while True:
                mdat = PwpMp4Box(f, None, "after insert", f_offset, get_boxes=False)
                if mdat.length is None:
                    break  # EOF
                # free.print()

                data = mdat.pack_header()
                nf.write(data)
                nf.write(mdat.data)
                f_offset += mdat.length + mdat.header_length - 8
            return

    @staticmethod
    def get_creation(f, box: PwpMp4Box):

        f.seek(box.offset, 0)
        new_h = PwpMp4Box(f, None, "Getting creation date", box.offset, get_boxes=False)
        assert box.equals(new_h)

        f.seek(box.offset + box.header_length, 0)
        version = PwpMp4Box.get_unsigned(f, 1)
        word_size = 8 if version == 1 else 4

        # 3 bytes flags =  24-bit hex flags (current = 0)
        f.seek(3, 1)  # skip flags
        # 4 bytes created mac UTC date
        #          = long unsigned value in seconds since beginning 1904 to 2040
        created = PwpMp4Box.get_unsigned(f, word_size)
        utc_time = datetime.datetime(1904, 1, 1) + datetime.timedelta(seconds=created)
        return utc_time

    # noqa  * 8+ bytes optional user data (any custom info) box
    # noqa         = long unsigned offset + long ASCII text string 'udta'
    #
    # noqa        * 8+ bytes optional copyright notice box
    # noqa            = long unsigned offset + long ASCII text string 'cprt'
    # noqa          -> 4 bytes version/flags = byte hex version + 24-bit hex flags
    # noqa              (current = 0)
    # noqa          -> 1/8 byte ISO language padding = 1-bit value set to 0
    # noqa          -> 1 7/8 bytes content language = 3 * 5-bits ISO 639-2 language code less 0x60
    # noqa               ==> 1 + 15 bits = 2 bytes.
    # noqa            - example code for english = 0x15C7 qui fait très exactement 'eng'
    # noqa          -> annotation string = UTF text string
    # noqa          -> 1 byte annotation c string end = byte value set to zero
    # noqa        -> 4 bytes compatibility utda end = long value set to zero

    @staticmethod
    def build(annotation: str):  # noqa
        anno_len = len(annotation)
        # noqa                udta_length   cprt_length
        length = anno_len + 27  # 4
        descr = b'udta'  # noqa 4
        length_2 = anno_len + 15  # 4
        descr_2 = b'cprt'  # noqa          4
        version = 0  # 4
        lang: int = 0x15C7  # 2
        # annotation        #               l + 1
        com = 0  # 4
        # noqa                 Total cprt # l + 15
        # noqa  total udta  # l + 27

        s = struct.Struct(f"> I 4s I 4s I H {anno_len + 1}s I")
        data = s.pack(length, descr, length_2, descr_2, version, lang, annotation.encode(), com)
        assert len(data) == length
        # noqa print(f"udta length = {length} {len(data)}")
        return data

    def write_metadata(self, _new_author, copy_right, _new_special):
        copy_name = self.filename[:-4] + "_bak.mp4"
        ACTOR.copy(self.filename, copy_name)
        son = PwpMp4(copy_name)
        if son.copyright == copy_right:
            return False
        udta2 = self.build(copy_right)  # noqa
        son.add_box(self.filename, udta2)  # noqa
        return True


def diff(fn1, fn2):
    with open(fn1, 'rb') as f1, open(fn2, 'rb') as f2:
        index = 0
        u1 = 0
        u2 = 0
        print(f"comparing {fn1} and {fn2}")
        while u1 is not None and u2 is not None:
            if u1 != u2:
                print(f"{index:8}: {u1:08x} {u2:08x}")
            u1 = PwpMp4Box.get_unsigned(f1, 4)
            u2 = PwpMp4Box.get_unsigned(f2, 4)
            index += 4
        if u1 is not None:
            print(f"f1 is longer {index}")
        elif u2 is not None:
            print(f"f2 is longer {index}")
        else:
            print("done")


def mp4_main(arguments):
    parser = argparse.ArgumentParser(description='test copyright insertion in MP4 file')
    parser.add_argument('--file', '-f', help="source file",
                        action='store',
                        default="tests/sources/TRIAGE3/Vendée/Opéra-Paris.mp4")
    parser.add_argument('--output', '-o', help="output",
                        action='store',
                        default="tests/results/copyrighted.mp4")
    parser.add_argument('--diff', '-d', help="compare the file",
                        action='store_true')
    parser.add_argument('--print', '-p', help="print files",
                        action='store_true')

    args = parser.parse_args() if arguments is None else parser.parse_args(arguments)
    mp4 = PwpMp4(args.file)
    if args.print:
        mp4.print()
    if "moov" not in mp4.root_boxes is None:  # noqa
        raise PwpError("No moov box, exit", args.file)  # noqa

    c1 = "Copyright 2013 foo BAR"
    udta = mp4.build(c1)  # noqa
    mp4.add_box(args.output, udta)  # noqa

    son = PwpMp4(args.output)
    if son.copyright != c1:
        raise PwpError(f"wrong copyright '{c1}' != '{son.copyright}'")

    if args.print:
        son.print()
    if args.diff:
        diff(args.file, args.output)

    n2 = args.output[:-4] + "-v2.mp4"
    c2 = "Copyright 2013 lee-foo BAR-BAR"
    udta2 = son.build(c2)  # noqa
    son.add_box(n2, udta2)  # noqa

    son2 = PwpMp4(n2)
    if son2.copyright != c2:
        raise PwpError(f"wrong copyright '{c2}' != '{son2.copyright}'")

    if args.print:
        son2.print()
    if args.diff:
        diff(args.output, n2)


if __name__ == "__main__":
    mp4_main(sys.argv[1:])

# cf https://gpac.github.io/mp4box.js/test/filereader.html
