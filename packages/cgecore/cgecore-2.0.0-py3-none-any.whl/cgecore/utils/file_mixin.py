# Created by Alfred Ferrer Florensa
"""Contains objects for reading files"""

import os
import sys
import gzip
import signal
from cgecore.utils.format_mixin import FormatFile


class CGELibFileError(Exception):
    """ Raised when a file produced by CGELib has not been created and does not
        exists or is incompatible with other CGELib produced files.
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGELibFileError, self).__init__(message, *args)


class CGELibFileParseError(StopIteration):
    """ Raised when the iterator has arrived to the end.
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGELibFileParseError, self).__init__(message, *args)


class _File:
    """Generic interface for taking information from files"""

    def __init__(self, file_path=None, is_empty=None, compression=None,
                 extension=None):
        self.file_path = file_path
        self.is_empty = is_empty
        self.compression = compression
        if extension is None:
            split_extension = os.path.splitext(file_path)[1]
            self.extension = split_extension
        else:
            self.extension = extension

    def define_file(self, file_path=None):

        if file_path is not None:
            self.file_path = "%s%s" % (file_path, self.extension)

        if not os.path.isfile(self.file_path):
            raise OSError("File %s does not exists" % (self.file_path))

        self.compression = FormatFile.is_gzipped(self.file_path)

        if not os.access(self.file_path, os.R_OK):
            raise OSError("File's %s permissions do not allow to read it")

    def __str__(self):
        """TODO: Truncated files"""
        self.define_file()

        return self.file_path

    def __repr__(self):
        """Represent file as a string"""
        self.define_file()
        return "File(file=%s, compression=%s)" % (self.file_path,
                                                  self.compression)


class _Parse_File(object):
    """A generator that iterates through a CC-CEDICT formatted file, returning
    a tuple of parsed results (Traditional, Simplified, Pinyin, English)"""

    def __init__(self, path, is_gzip=False):
        self.path = path
        if is_gzip:
            self.file = gzip.open(path, "rt")
        else:
            self.file = open(path, "r")
        signal.signal(signal.SIGINT, self.signal_term_handler)

    def signal_term_handler(self, signal, frame):
        """ Make sure to close handle if app closes prematurely """
        try:
            self.close()
        except ValueError:
            pass
        sys.exit()

    def parse_line(self, file_type="line"):
        self.opened_file()
        if file_type=="xml":
            try:
                line = next(self.iterator_XML)
            except StopIteration:
                raise CGELibFileParseError(
                    """The iterator of the file %s has arrived to the end """
                    """of the file""" % self.path)
        else:
            try:
                line = self.file.readline()
            except ValueError:
                raise CGELibFileParseError(
                    """The iterator of the file %s has arrived to the end """
                    """of the file""" % self.path)
        return line

    def opened_file(self):
        if self.file.closed:
            raise CGELibFileParseError(
                """The iterator of the file %s has arrived to the end """
                """of the file""" % self.path)

    def close(self):
        self.file.close()


class ResultFile(_File):

    def __init__(
        self,
        type,
        file_path,
        name=None,
        read_method=None,
        extension=None,
        compression=None,
        translate_read=None,
        options_read=None,
    ):
        self.type = type
        if os.path.splitext(file_path)[-1] == "":
            if extension is None:
                raise ValueError("The file does not have an extension")
            else:
                resultfile_path = "%s%s" % (file_path, extension)
        else:
            resultfile_path = file_path

        if name is None:
            self.name = os.path.splitext(os.path.basename(file_path))[0]
        else:
            self.name = name
        self.read_method = read_method
        if options_read is None:
            self.options_read = {}
        else:
            if not isinstance(options_read, dict):
                raise TypeError("The parameters for a reading the results file"
                                " have to be in a dictionary")
            else:
                self.options_read = options_read
        _File.__init__(self, file_path=resultfile_path,
                       compression=compression, extension=extension)

    def __str__(self):
        return self.file_path

    def __repr__(self):
        return "%s(file=%s, compression=%s, read_method=%s)" % (
                self.type.capitalize(), self.file_path, self.compression,
                self.read_method)

    def read(self, **kwargs):

        _File.define_file(self)
        if self.read_method is None:
            read_function = None
        else:
            if bool(self.options_read):
                read_function = self.read_method(self.file_path,
                                                 **self.options_read)
            else:
                read_function = self.read_method(self.file_path)
        return read_function

    def dump_json(self):
        pass


class Iterator_BioFiles:

    BioFiles = ["fasta", "paired_end_reads", "single_end_reads"]

    def __init__(self, dir_paths, extension, type_file):

        if isinstance(dir_paths, list):
            self.dir_paths = iter(dir_paths)
        else:
            self.dir_paths = iter([dir_paths])

        if type_file not in Iterator_BioFiles.BioFiles:
            raise TypeError("The only types of data accepted by the class %s"
                            " are %s" % (self.__name__,
                                        ", ".join(Iterator_BioFiles.BioFiles)))
        self.extension = extension
        self.type_file = type_file
        self.folder_files = None
        self.path = None

    def __iter__(self):
        return self

    def __iter__(self):

        if self.folder is None:
            folder = next(self.dir_paths)
            if os.path.isdir(folder):
                self.folder_files = os.listdir(folder)
                self.path = folder
            else:
                raise OSError("The path %s is not a folder" % folder)
        check_files = True
        while check_files:
            if self.type_file:
                continue
