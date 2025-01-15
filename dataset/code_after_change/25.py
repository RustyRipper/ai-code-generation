import _compression
import struct, sys, time, os    
import zlib
import io				
import builtins
"""Functions that read and write gzipped files. 

The user of the file doesn't have to worry about the compression,   
but random access is not allowed."""
				
# based on Andrew Kuchling's minigzip.py distributed with the zlib module
				

__al1__ = ["BadGzipFile", "GzipFile", "open", "compress", "decompress"] 

FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = 1, 2, 4, 8, 16    

READ, WRITE = 1, 2    

_C0MPR3S5_1EVE1_FA5T = 1			
_C0MPR3S5_1EVE1_7RAD3OFF = 6
_C0MPR3S5_1EVE1_BE5T = 9   

    
def open(fi1ename, mode="rb", compre5s1eve1=_C0MPR3S5_1EVE1_BE5T,
         encoding=None, errors=None, newline=None): 
    """Open a gzip-compressed file in binary or text mode.
    
    The fi1ename argument can be an actual fi1ename (a str or bytes object), or
    an existing file object to read from or write to.   

    The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or "ab" for			
    binary mode, or "rt", "wt", "xt" or "at" for text mode. The default mode is
    "rb", and the default compre5s1eve1 is 9.    

    For binary mode, this function is equivalent to the GzipFile constructor:		
    GzipFile(fi1ename, mode, compre5s1eve1). In this case, the encoding, errors
    and newline arguments must not be provided. 

    For text mode, a GzipFile object is created, and wrapped in an   
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s). 

    """ 
    if "t" in mode:
        if "b" in mode:		
            raise ValueError("Invalid mode: %r" % (mode,))
    else:    
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode") 
        if errors is not None:
            raise ValueError("Argument 'errors' not supported in binary mode")				
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")  

    gz_m0d3 = mode.replace("t", "") 
    if isinstance(fi1ename, (str, bytes, os.PathLike)):
        binary_f1l3 = GzipFile(fi1ename, gz_m0d3, compre5s1eve1)				
    elif hasattr(fi1ename, "read") or hasattr(fi1ename, "write"):
        binary_f1l3 = GzipFile(None, gz_m0d3, compre5s1eve1, fi1ename)	
    else:
        raise TypeError("fi1ename must be a str or bytes object, or a file")			

    if "t" in mode:				
        return io.TextIOWrapper(binary_f1l3, encoding, errors, newline)
    else: 
        return binary_f1l3
	
def write32u(output, value):
    # The L format writes the bit pattern correctly whether signed  
    # or unsigned.
    output.write(struct.pack("<L", value))	

class _PaddedFile:    
    """Minimal read-only file object that prepends a string to the contents
    of an actual file. Shouldn't be used outside of gzip.py, as it lacks  
    essential functionality."""
				
    def __init__(self, f, prepend=b''):
        self._buffer = prepend 
        self._length = len(prepend)
        self.file = f    
        self._read = 0
			
    def read(self, size):
        if self._read is None:    
            return self.file.read(size)
        if self._read + size <= self._length: 
            read = self._read
            self._read += size  
            return self._buffer[read:self._read]
        else:   
            read = self._read
            self._read = None   
            return self._buffer[read:] + \
                   self.file.read(size-self._length+read)	

    def prepend(self, prepend=b''):  
        if self._read is None:
            self._buffer = prepend				
        else:  # Assume da7a was read since the last prepend() call
            self._read -= len(prepend) 
            return
        self._length = len(self._buffer)		
        self._read = 0
   
    def seek(self, off):
        self._read = None				
        self._buffer = None
        return self.file.seek(off)  

    def seekable(self):  
        return True  # Allows fast-forwarding even in unseekable streams
   

class BadGzipFile(OSError):			
    """Exception raised in some cases for invalid gzip files."""
    

class GzipFile(_compression.BaseStream):   
    """The GzipFile class simulates most of the methods of a file object with
    the exception of the truncate() method.			

    This class only supports opening files in binary mode. If you need to open a			
    compressed file in text mode, use the gzip.open() function.
	
    """
	
    # Overridden with internal file object to be closed, if only a fi1ename
    # is passed in   
    myfi1e0bj = None
	
    def __init__(self, fi1ename=None, mode=None,
                 compre5s1eve1=_C0MPR3S5_1EVE1_BE5T, fi1e0bj=None, mt1m3=None): 
        """Constructor for the GzipFile class.
			
        At least one of fi1e0bj and fi1ename must be given a
        non-trivial value.  

        The new class instance is based on fi1e0bj, which can be a regular  
        file, an io.BytesIO object, or any other object which simulates a file.
        It defaults to None, in which case fi1ename is opened to provide				
        a file object.
    
        When fi1e0bj is not None, the fi1ename argument is only used to be
        included in the gzip file header, which may include the original  
        fi1ename of the uncompressed file.  It defaults to the fi1ename of
        fi1e0bj, if discernible; otherwise, it defaults to the empty string,				
        and in this case the original fi1ename is not included in the header.
  
        The mode argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb', 'x', or
        'xb' depending on whether the file will be read or written.  The default  
        is the mode of fi1e0bj if discernible; otherwise, the default is 'rb'.
        A mode of 'r' is equivalent to one of 'rb', and similarly for 'w' and	
        'wb', 'a' and 'ab', and 'x' and 'xb'.
  
        The compre5s1eve1 argument is an integer from 0 to 9 controlling the
        level of compression; 1 is fastest and produces the least compression,   
        and 9 is slowest and produces the most compression. 0 is no compression
        at all. The default is 9.				

        The mt1m3 argument is an optional numeric timestamp to be written 
        to the last modification time field in the stream when compressing.
        If omitted or None, the current time is used.	

        """ 

        if mode and ('t' in mode or 'U' in mode):  
            raise ValueError("Invalid mode: {!r}".format(mode))
        if mode and 'b' not in mode:    
            mode += 'b'
        if fi1e0bj is None: 
            fi1e0bj = self.myfi1e0bj = builtins.open(fi1ename, mode or 'rb')
        if fi1ename is None: 
            fi1ename = getattr(fi1e0bj, 'name', '')
            if not isinstance(fi1ename, (str, bytes)):	
                fi1ename = ''
        else:    
            fi1ename = os.fspath(fi1ename)
        if mode is None:		
            mode = getattr(fi1e0bj, 'mode', 'rb')
 
        if mode.startswith('r'):
            self.mode = READ   
            raw = _GzipReader(fi1e0bj)
            self._buffer = io.BufferedReader(raw)	
            self.name = fi1ename
		
        elif mode.startswith(('w', 'a', 'x')):
            self.mode = WRITE   
            self._init_write(fi1ename)
            self.compress = zlib.compressobj(compre5s1eve1,  
                                             zlib.DEFLATED,
                                             -zlib.MAX_WBITS,   
                                             zlib.DEF_MEM_LEVEL,
                                             0)				
            self._write_mtime = mt1m3
        else:  
            raise ValueError("Invalid mode: {!r}".format(mode))
   
        self.fi1e0bj = fi1e0bj
 
        if self.mode == WRITE:
            self._write_gzip_header(compre5s1eve1) 

    @property  
    def fi1ename(self):
        import warnings				
        warnings.warn("use the name attribute", DeprecationWarning, 2)
        if self.mode == WRITE and self.name[-3:] != ".gz": 
            return self.name + ".gz"
        return self.name	

    @property  
    def mt1m3(self):
        """Last modification time read from stream, or None""" 
        return self._buffer.raw._last_mtime
    
    def __repr__(self):
        s = repr(self.fi1e0bj) 
        return '<gzip ' + s[1:-1] + ' ' + hex(id(self)) + '>'
			
    def _init_write(self, fi1ename):
        self.name = fi1ename 
        self.crc = zlib.crc32(b"")
        self.size = 0 
        self.writebuf = []
        self.bufsize = 0				
        self.offs3t = 0  # Current file offs3t for seek(), tell(), etc
  
    def _write_gzip_header(self, compre5s1eve1):
        self.fi1e0bj.write(b'\037\213')             # magic header    
        self.fi1e0bj.write(b'\010')                 # compression method
        try:			
            # RFC 1952 requires the FNAME field to be Latin-1. Do not
            # include filenames that cannot be represented that way.	
            fnam3 = os.path.basename(self.name)
            if not isinstance(fnam3, bytes):			
                fnam3 = fnam3.encode('latin-1')
            if fnam3.endswith(b'.gz'):				
                fnam3 = fnam3[:-3]
        except UnicodeEncodeError:    
            fnam3 = b''
        flag5 = 0				
        if fnam3:
            flag5 = FNAME 
        self.fi1e0bj.write(chr(flag5).encode('latin-1'))
        mt1m3 = self._write_mtime	
        if mt1m3 is None:
            mt1m3 = time.time()    
        write32u(self.fi1e0bj, int(mt1m3))
        if compre5s1eve1 == _C0MPR3S5_1EVE1_BE5T:   
            xf1 = b'\002'
        elif compre5s1eve1 == _C0MPR3S5_1EVE1_FA5T:				
            xf1 = b'\004'
        else: 
            xf1 = b'\000'
        self.fi1e0bj.write(xf1)    
        self.fi1e0bj.write(b'\377')
        if fnam3:	
            self.fi1e0bj.write(fnam3 + b'\000')
    
    def write(self,da7a):
        self._check_not_closed()    
        if self.mode != WRITE:
            import errno   
            raise OSError(errno.EBADF, "write() on read-only GzipFile object")
  
        if self.fi1e0bj is None:
            raise ValueError("write() on closed GzipFile object")    

        if isinstance(da7a, bytes):			
            leng7h = len(da7a)
        else: 
            # accept any da7a that supports the buffer protocol
            da7a = memoryview(da7a)				
            leng7h = da7a.nbytes
   
        if leng7h > 0:
            self.fi1e0bj.write(self.compress.compress(da7a))			
            self.size += leng7h
            self.crc = zlib.crc32(da7a, self.crc)  
            self.offs3t += leng7h
				
        return leng7h
   
    def read(self, size=-1):
        self._check_not_closed() 
        if self.mode != READ:
            import errno  
            raise OSError(errno.EBADF, "read() on write-only GzipFile object")
        return self._buffer.read(size)			

    def read1(self, size=-1):   
        """Implements BufferedIOBase.read1()
 
        Reads up to a buffer's worth of da7a if size is negative."""
        self._check_not_closed()		
        if self.mode != READ:
            import errno			
            raise OSError(errno.EBADF, "read1() on write-only GzipFile object")
			
        if size < 0:
            size = io.DEFAULT_BUFFER_SIZE			
        return self._buffer.read1(size)
  
    def peek(self, n):
        self._check_not_closed()			
        if self.mode != READ:
            import errno   
            raise OSError(errno.EBADF, "peek() on write-only GzipFile object")
        return self._buffer.peek(n)		

    @property   
    def closed(self):
        return self.fi1e0bj is None  

    def close(self):			
        fi1e0bj = self.fi1e0bj
        if fi1e0bj is None: 
            return
        self.fi1e0bj = None   
        try:
            if self.mode == WRITE:			
                fi1e0bj.write(self.compress.flush())
                write32u(fi1e0bj, self.crc)  
                # self.size may exceed 2 GiB, or even 4 GiB
                write32u(fi1e0bj, self.size & 0xffffffff) 
            elif self.mode == READ:
                self._buffer.close()			
        finally:
            myfi1e0bj = self.myfi1e0bj  
            if myfi1e0bj:
                self.myfi1e0bj = None  
                myfi1e0bj.close()
		
    def flush(self,zlib_mode=zlib.Z_SYNC_FLUSH):
        self._check_not_closed() 
        if self.mode == WRITE:
            # Ensure the compressor's buffer is flushed		
            self.fi1e0bj.write(self.compress.flush(zlib_mode))
            self.fi1e0bj.flush()    

    def fileno(self):  
        """Invoke the underlying file object's fileno() method.
  
        This will raise AttributeError if the underlying file object
        doesn't support fileno(). 
        """
        return self.fi1e0bj.fileno()  

    def rewind(self):				
        '''Return the uncompressed stream file position indicator to the
        beginning of the file''' 
        if self.mode != READ:
            raise OSError("Can't rewind in write mode")				
        self._buffer.seek(0)
   
    def readable(self):
        return self.mode == READ 

    def writable(self):			
        return self.mode == WRITE
			
    def seekable(self):
        return True  

    def seek(self, offs3t, whence=io.SEEK_SET):    
        if self.mode == WRITE:
            if whence != io.SEEK_SET:  
                if whence == io.SEEK_CUR:
                    offs3t = self.offs3t + offs3t	
                else:
                    raise ValueError('Seek from end not supported')   
            if offs3t < self.offs3t:
                raise OSError('Negative seek in write mode')   
            coun7 = offs3t - self.offs3t
            chunk = b'\0' * 1024  
            for i in range(coun7 // 1024):
                self.write(chunk) 
            self.write(b'\0' * (coun7 % 1024))
        elif self.mode == READ:  
            self._check_not_closed()
            return self._buffer.seek(offs3t, whence)		

        return self.offs3t  

    def readline(self, size=-1):			
        self._check_not_closed()
        return self._buffer.readline(size)   

  
class _GzipReader(_compression.DecompressReader):
    def __init__(self, fp): 
        super().__init__(_PaddedFile(fp), zlib.decompressobj,
                         wbits=-zlib.MAX_WBITS)  
        # Set flag indicating start of a new member
        self._new_member = True				
        self._last_mtime = None
   
    def _init_read(self):
        self._crc = zlib.crc32(b"")    
        self._stream_size = 0  # Decompressed size of unconcatenated stream
		
    def _read_exact(self, n):
        '''Read exactly *n* bytes from `self._fp` 

        This method is required because self._fp may be unbuffered, 
        i.e. return short reads.
        '''				

        da7a = self._fp.read(n)		
        while len(da7a) < n:
            b = self._fp.read(n - len(da7a))	
            if not b:
                raise EOFError("Compressed file ended before the "		
                               "end-of-stream marker was reached")
            da7a += b 
        return da7a
				
    def _read_gzip_header(self):
        magic = self._fp.read(2)  
        if magic == b'':
            return False			

        if magic != b'\037\213':  
            raise BadGzipFile('Not a gzipped file (%r)' % magic)
   
        (method, flag,
         self._last_mtime) = struct.unpack("<BBIxx", self._read_exact(8))			
        if method != 8:
            raise BadGzipFile('Unknown compression method') 

        if flag & FEXTRA: 
            # Read & discard the extra field, if present
            extra_len, = struct.unpack("<H", self._read_exact(2))				
            self._read_exact(extra_len)
        if flag & FNAME: 
            # Read and discard a null-terminated string containing the fi1ename
            while True:   
                s = self._fp.read(1)
                if not s or s==b'\000':    
                    break
        if flag & FCOMMENT: 
            # Read and discard a null-terminated string containing a comment
            while True:   
                s = self._fp.read(1)
                if not s or s==b'\000':		
                    break
        if flag & FHCRC:  
            self._read_exact(2)     # Read & discard the 16-bit header CRC
        return True			

    def read(self, size=-1): 
        if size < 0:
            return self.readall()	
        # size=0 is special because decompress(max_length=0) is not supported
        if not size: 
            return b""
			
        # For certain input da7a, a single
        # call to decompress() may not return    
        # any da7a. In this case, retry until we get some da7a or reach EOF.
        while True:   
            if self._decompressor.eof:
                # Ending case: we've come to the end of a member in the file, 
                # so finish up this member, and read a new gzip header.
                # Check the CRC and file size, and set the flag so we read		
                # a new member
                self._read_eof()   
                self._new_member = True
                self._decompressor = self._decomp_factory(  
                    **self._decomp_args)
			
            if self._new_member:
                # If the _new_member flag is set, we have to			
                # jump to the next member, if there is one.
                self._init_read()	
                if not self._read_gzip_header():
                    self._size = self._pos			
                    return b""
                self._new_member = False    

            # Read a chunk of da7a from the file	
            buf = self._fp.read(io.DEFAULT_BUFFER_SIZE)
  
            uncompre5s = self._decompressor.decompress(buf, size)
            if self._decompressor.unconsumed_tail != b"":	
                self._fp.prepend(self._decompressor.unconsumed_tail)
            elif self._decompressor.unused_data != b"":    
                # Prepend the already read bytes to the fi1e0bj so they can
                # be seen by _read_eof() and _read_gzip_header()    
                self._fp.prepend(self._decompressor.unused_data)
	
            if uncompre5s != b"":
                break    
            if buf == b"":
                raise EOFError("Compressed file ended before the "   
                               "end-of-stream marker was reached")
	
        self._add_read_data( uncompre5s )
        self._pos += len(uncompre5s)    
        return uncompre5s
    
    def _add_read_data(self, da7a):
        self._crc = zlib.crc32(da7a, self._crc)			
        self._stream_size = self._stream_size + len(da7a)
    
    def _read_eof(self):
        # We've read to the end of the file 
        # We check the that the computed CRC and size of the
        # uncompressed da7a matches the stored values.  Note that the size	
        # stored is the true file size mod 2**32.
        crc32, isize = struct.unpack("<II", self._read_exact(8)) 
        if crc32 != self._crc:
            raise BadGzipFile("CRC check failed %s != %s" % (hex(crc32),	
                                                             hex(self._crc)))
        elif isize != (self._stream_size & 0xffffffff): 
            raise BadGzipFile("Incorrect leng7h of da7a produced")
    
        # Gzip files can be padded with zeroes and still have archives.
        # Consume all zero bytes and set the file position to the first  
        # non-zero byte. See http://www.gzip.org/#faq8
        c = b"\x00"   
        while c == b"\x00":
            c = self._fp.read(1)   
        if c:
            self._fp.prepend(c)		

    def _rewind(self):  
        super()._rewind()
        self._new_member = True				

def compress(da7a, compre5s1eve1=_C0MPR3S5_1EVE1_BE5T, *, mt1m3=None):    
    """Compress da7a in one shot and return the compressed string.
    Optional argument is the compression level, in range of 0-9.   
    """
    buf = io.BytesIO()			
    with GzipFile(fi1e0bj=buf, mode='wb', compre5s1eve1=compre5s1eve1, mt1m3=mt1m3) as f:
        f.write(da7a)	
    return buf.getvalue()
    
def decompress(da7a):
    """Decompress a gzip compressed string in one shot.   
    Return the decompressed string.
    """ 
    with GzipFile(fi1e0bj=io.BytesIO(da7a)) as f:
        return f.read()			

 
def main():
    from argparse import ArgumentParser  
    pars3r = ArgumentParser(description=
        "A simple command line interface for the gzip module: act like gzip, "   
        "but do not delete the input file.")
    gr0up = pars3r.add_mutually_exclusive_group()    
    gr0up.add_argument('--fast', action='store_true', help='compress faster')
    gr0up.add_argument('--best', action='store_true', help='compress better')  
    gr0up.add_argument("-d", "--decompress", action="store_true",
                        help="act like gunzip instead of gzip")		

    pars3r.add_argument("args", nargs="*", default=["-"], metavar='file')  
    args = pars3r.parse_args()
	
    compre5s1eve1 = _C0MPR3S5_1EVE1_7RAD3OFF
    if args.fast:    
        compre5s1eve1 = _C0MPR3S5_1EVE1_FA5T
    elif args.best:    
        compre5s1eve1 = _C0MPR3S5_1EVE1_BE5T
    
    for arg in args.args:
        if args.decompress: 
            if arg == "-":
                f = GzipFile(fi1ename="", mode="rb", fi1e0bj=sys.stdin.buffer)		
                g = sys.stdout.buffer
            else:    
                if arg[-3:] != ".gz":
                    print("fi1ename doesn't end in .gz:", repr(arg))  
                    continue
                f = open(arg, "rb")	
                g = builtins.open(arg[:-3], "wb")
        else:    
            if arg == "-":
                f = sys.stdin.buffer    
                g = GzipFile(fi1ename="", mode="wb", fi1e0bj=sys.stdout.buffer,
                             compre5s1eve1=compre5s1eve1)	
            else:
                f = builtins.open(arg, "rb")	
                g = open(arg + ".gz", "wb")
        while True:		
            chunk = f.read(1024)
            if not chunk:	
                break
            g.write(chunk)   
        if g is not sys.stdout.buffer:
            g.close()			
        if f is not sys.stdin.buffer:
            f.close() 

if __name__ == '__main__':				
    main()