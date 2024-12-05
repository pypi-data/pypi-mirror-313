"""
magic is a wrapper around the libmagic file identification library.

See README for more information.

Usage:

>>> import magicfile
>>> magicfile.from_file("testdata/test.pdf")
'PDF document, version 1.2'
>>> magicfile.from_file("testdata/test.pdf", mime=True)
'application/pdf'
>>> magicfile.from_buffer(open("testdata/test.pdf").read(1024))
'PDF document, version 1.2'
>>>


"""

import os
import sys
import glob
import threading

from ._libmagic import ffi as _ffi
from ._libmagic import lib as _lib


PY2 = sys.version_info.major == 2
if PY2:
    text_type = unicode
else:
    text_type = str


_CURR_PATH = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault('MAGIC', os.path.join(_CURR_PATH, 'magic.mgc'))


class MagicException(Exception):
    def __init__(self, message):
        super(MagicException, self).__init__(message)
        self.message = message


class Magic(object):
    """
    Magic is a wrapper around the libmagic C library.

    """

    def __init__(self, mime=False, magic_file=None, mime_encoding=False,
                 keep_going=False, uncompress=False):
        """
        Create a new libmagic wrapper.

        mime - if True, mimetypes are returned instead of textual descriptions
        mime_encoding - if True, codec is returned
        magic_file - use a mime database other than the system default
        keep_going - don't stop at the first match, keep going
        uncompress - Try to look inside compressed files.
        """
        self.flags = MAGIC_NONE
        if mime:
            self.flags |= MAGIC_MIME
        if mime_encoding:
            self.flags |= MAGIC_MIME_ENCODING
        if keep_going:
            self.flags |= MAGIC_CONTINUE

        if uncompress:
            self.flags |= MAGIC_COMPRESS

        self.cookie = _ffi.gc(magic_open(self.flags), _lib.magic_close)
        self.lock = threading.Lock()
        magic_load(self.cookie, maybe_encode(magic_file))

    def from_buffer(self, buf):
        """
        Identify the contents of `buf`
        """
        with self.lock:
            # if we're on python3, convert buf to bytes
            # otherwise this string is passed as wchar*
            # which is not what libmagic expects
            if type(buf) == str and str != bytes:
                buf = buf.encode('utf-8', errors='replace')
            return magic_buffer(self.cookie, buf)

    def from_file(self, filename):
        # raise FileNotFoundException or IOError if the file does not exist
        with open(filename):
            pass
        with self.lock:
            return magic_file(self.cookie, filename)

_instances = {}


def _get_magic_type(mime):
    i = _instances.get(mime)
    if i is None:
        i = _instances[mime] = Magic(mime=mime)
    return i


def from_file(filename, mime=False):
    """"
    Accepts a filename and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_file("testdata/test.pdf", mime=True)
    'application/pdf'
    """
    m = _get_magic_type(mime)
    return m.from_file(filename)


def from_buffer(buffer, mime=False):
    """
    Accepts a binary string and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'
    """
    m = _get_magic_type(mime)
    return m.from_buffer(buffer)


def maybe_encode(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s


def magic_setflags(cookie, flags):
    status = _lib.magic_setflags(cookie, flags)
    if status != 0:
        raise MagicException(magic_error(cookie))


def magic_error(cookie):
    return _ffi.string(_lib.magic_error(cookie))


def magic_open(flags):
    cookie = _lib.magic_open(flags)
    if cookie == _ffi.NULL:
        raise MagicException(magic_error(cookie))
    else:
        return cookie


def magic_close(cookie):
    _lib.magic_close(cookie)


def magic_load(cookie, path=None):
    if path is None:
        path = _ffi.NULL
    status = _lib.magic_load(cookie, path)
    if status != 0:
        raise MagicException(magic_error(cookie))


def magic_file(cookie, path):
    if not isinstance(path, bytes):
        path = path.encode(sys.getfilesystemencoding())
    result = _lib.magic_file(cookie, path)
    if result == _ffi.NULL:
        raise MagicException(magic_error(cookie))
    else:
        return _ffi.string(result).decode('utf8')


def magic_buffer(cookie, value):
    result = _lib.magic_buffer(cookie, value, len(value))
    if result == _ffi.NULL:
        raise MagicException(magic_error(cookie))
    else:
        return _ffi.string(result).decode('utf8')


def version():
    return _lib.magic_version()


MAGIC_NONE = 0x000000 # No flags
MAGIC_DEBUG = 0x000001 # Turn on debugging
MAGIC_SYMLINK = 0x000002 # Follow symlinks
MAGIC_COMPRESS = 0x000004 # Check inside compressed files
MAGIC_DEVICES = 0x000008 # Look at the contents of devices
MAGIC_MIME = 0x000010 # Return a mime string
MAGIC_MIME_ENCODING = 0x000400 # Return the MIME encoding
MAGIC_CONTINUE = 0x000020 # Return all matches
MAGIC_CHECK = 0x000040 # Print warnings to stderr
MAGIC_PRESERVE_ATIME = 0x000080 # Restore access time on exit
MAGIC_RAW = 0x000100 # Don't translate unprintable chars
MAGIC_ERROR = 0x000200 # Handle ENOENT etc as real errors

MAGIC_NO_CHECK_COMPRESS = 0x001000 # Don't check for compressed files
MAGIC_NO_CHECK_TAR = 0x002000 # Don't check for tar files
MAGIC_NO_CHECK_SOFT = 0x004000 # Don't check magic entries
MAGIC_NO_CHECK_APPTYPE = 0x008000 # Don't check application type
MAGIC_NO_CHECK_ELF = 0x010000 # Don't check for elf details
MAGIC_NO_CHECK_ASCII = 0x020000 # Don't check for ascii files
MAGIC_NO_CHECK_TROFF = 0x040000 # Don't check ascii/troff
MAGIC_NO_CHECK_FORTRAN = 0x080000 # Don't check ascii/fortran
MAGIC_NO_CHECK_TOKENS = 0x100000 # Don't check ascii/tokens
