class Packet:
    def __init__(self, data):
        self._data = data

        # READ HEADER
        h = self.readBytes(2)
        self._pid = h >> 2
        self._len = self.readBytes(0b00000011 & h)

    def readBytes(self, len):
        '''return int value of the {len} first bytes'''
        extracted = self._data[:len * 2]
        self._data = self._data[len * 2:]
        return int(extracted, 16)

    def readByte(self):
        '''return int value of the first byte'''
        return self.readBytes(1)

    def skipBytes(self, len):
        self._data = self._data[len * 2:]

    def skipByte(self):
        self.skipBytes(1)

    def readBoolean(self):
        return self.readByte() != 0

    def readInt(self):
        return self.readBytes(4)

    def readShort(self):
        return self.readBytes(2)
