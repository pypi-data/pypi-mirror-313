

class Lock:
    """
    A lock on a stream.
    """
    def __init__(self, stream, start, end):
        self.stream = stream
        self.start = start
        self.end = end

    def __enter__(self):
        self.stream.locks.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.locks.remove(self)


class Stream:
    """
    A double buffered stream of data.
    """

    def __init__(self, buffer_size):
        self.start = 0
        self.end = 0
        self.buffers = []
        self.buffer = None
        self.locks = {}

    def write(self, data):
        """
        Write data to the stream.
        """
        if len(data) > len(self.buffers[self.current]):
            self.swap()
        self.buffers[self.current].write(data)

    def swap(self):
        """
        Swap the current buffer.
        """
        pass

    def lock(self, start, end=None):
        """
        Get a read lock. Data past `start` is available.
        """
        return Lock(self, start, end or self.end)


class Buffer:
    """
    A buffer of data.
    """
    def __init__(self, size):
        self.size = size
        self.data = self.allocate(size)
        self.start = 0
        self.end = 0

    def write(self, data):
        """
        Write data to the buffer.
        """

# buffer types:
# numpy array
# torch
# bytes
# dicts
# tree?
