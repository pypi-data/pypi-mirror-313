from io import StringIO, BytesIO

from azureml.core import Run


class WriteBuffer:

    def __init__(self, iotype, encoding='utf-8'):
        if iotype not in {StringIO, BytesIO}:
            raise Exception(f"Unsupported IO type: {iotype}")
        self._io = iotype()
        self._encoding = encoding
        self.data = b''

    def __enter__(self):
        return self._io.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.store_data()
        return self._io.__exit__(exc_type, exc_value, traceback)

    def write(self, *args, **kargs):
        return self._io.write(*args, **kargs)

    def close(self, *args, **kargs):
        self.store_data()
        return self._io.close(*args, **kargs)

    def store_data(self):
        # Store written data before close the io instance
        if isinstance(self._io, StringIO):
            self.data = self._io.getvalue().encode(self._encoding)
        elif isinstance(self._io, BytesIO):
            self.data = self._io.getvalue()


class RWBufferManager:
    """A buffer manager that can write data first, then read the written data.

    >>> mng = RWBufferManager()
    >>> data = 'some string'
    >>> with mng.open('w') as fout:
    ...     fout.write(data)
    11
    >>> with mng.open('r') as fin:
    ...     fin.read()
    'some string'
    """

    def __init__(self, encoding='utf-8'):
        self.buf = None
        self.encoding = encoding

    @property
    def data(self):
        if self.buf is None:
            return b''
        return self.buf.data

    def open(self, mode):
        # Return an IO instance with stored data when mode is 'r' or 'rb'
        if mode in {'rb', 'r'}:
            if mode == 'rb':
                buf = BytesIO(self.data)
            else:
                buf = StringIO(self.data.decode(self.encoding))
            self.buf = None
        # Return a WriteBuffer to store data when mode is 'w' or 'wb'
        elif mode == 'w':
            buf = self.buf = WriteBuffer(StringIO, self.encoding)
        elif mode == 'wb':
            buf = self.buf = WriteBuffer(BytesIO)
        else:
            raise Exception(f"Unsupported IO mode: {mode}")
        return buf


def pipeline_io(write_func, write_mode, read_func, read_mode):
    """Write some data with write_func, then redirect the data to read_func."""

    mng = RWBufferManager()
    with mng.open(write_mode) as fout:
        write_func(fout)
    with mng.open(read_mode) as fin:
        read_func(fin)


class AzureMLOutput:
    """An interface that can upload data to azureml."""

    @staticmethod
    def open(path, write_mode, run=None):
        """Return an AzureMLOutput object for writing data and uploading to azureml.

        :param run: an azureml Run object for uploading file.
        :param path: the path to upload in azureml.
        :param write_mode: the write mode(w/wb) for writing data.
        :return:
        """
        return AzureMLOutput(path, write_mode, run)

    def __init__(self, path, write_mode, run=None):
        if write_mode not in {'w', 'wb'}:
            raise Exception(f"Unsupported IO mode: {write_mode}")
        self.run = run
        if run is None:
            self.run = Run.get_context()
        self.path = path
        self.mng = RWBufferManager()
        self.fout = self.mng.open(write_mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write(self, *args, **kargs):
        return self.fout.write(*args, **kargs)

    def close(self):
        result = self.fout.close()
        with self.mng.open('rb') as fin:
            self.run.upload_file(self.path, fin)
        return result
