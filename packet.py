class Packet:
    def __init__(self, data):
        data = ''.join(data.split(' '))
        self._init_data = data
        self._data = data

        # READ HEADER
        h = self.readBytes(2)
        self._len = self.readBytes(0b00000011 & h)
        self._pid = str(h >> 2)

    def readBytes(self, len):
        '''return int value of the {len} first bytes'''
        if len == 0:
            return 0
        extracted = self._data[:len * 2]
        if extracted == '':
            return 0
        self._data = self._data[len * 2:]
        return int(extracted, 16)

    def readUnsignedByte(self):
        '''return int value of the first byte'''
        return self.readBytes(1)

    def readByte(self):
        value = self.readBytes(1)
        if (value > 127):
            value -= 256
        return value

    def skipBytes(self, len):
        self._data = self._data[len * 2:]

    def skipByte(self):
        self.skipBytes(1)

    def readBoolean(self):
        return self.readByte() != 0

    def readInt(self):
        return self.readBytes(4)

    def readUnsignedInt(self):
        return self.readBytes(4)

    def readVarInt(self):
        offset = 0
        value = 0
        hasNext = False
        while offset < 32:
            b = self.readByte()
            hasNext = (b & 0b10000000) == 0b10000000
            value = value + ((b & 0b01111111) << offset)
            offset = offset + 7
            if not hasNext:
                return value

    def readVarShort(self):
        offset = 0
        value = 0
        hasNext = False
        while offset < 16:
            b = self.readByte()
            hasNext = (b & 0b10000000) == 0b10000000
            value = value + ((b & 0b01111111) << offset)
            offset = offset + 7
            if not hasNext:
                if value > 32767:
                    value = value - 65536
                return value

    def readVarLong(self):
        b = 0
        result = 0
        i = 0
        while True:
            b = self.readUnsignedByte()
            if (i == 28):
                break
            if (b < 128):
                result.low = result.low | b << i
            continue

        if (b >= 128):
            b = b & 127
            result.low = result.low | b << i
            result.high = b >> 4
            i = 3
            while (True):
                b = input.readUnsignedByte()
                if (i < 32):
                    if (b < 128):
                        break
                    result.high = result.high | (b & 127) << i
                i = i + 7
            result.high = result.high | b << i
            return result

        result.low = result.low | b << i
        result.high = b >> 4
        return result

    def readUnsignedShort(self):
        return self.readBytes(2)

    def readLong(self):
        return self.readBytes(8)

    def readDouble(self):
        b = self.readBytes(8)
        if b == 0x7ff0000000000000:
            return '+infinity'
        elif b == 0xfff0000000000000:
            return '-infinity'
        elif (b >= 0x7ff0000000000001
              and b <= 0x7fffffffffffffff) or (b >= 0xfff0000000000001
                                               and b <= 0xffffffffffffffff):
            return 'NaN'
        else:
            s = 1 if ((b >> 63) == 0) else -1
            e = (b >> 52) & 0x7ff
            m = (b & 0xfffffffffffff) << 1 if (
                e == 0) else (b & 0xfffffffffffff) | 0x10000000000000
            return s * m * pow(2, e - 1075)

    def readFloat(self):
        b = self.readBytes(4)
        if b == 0x7f800000:
            return '+infinity'
        elif b == 0xff800000:
            return '-infinity'
        elif (b >= 0x7f800001 and b <= 0x7fffffff) or (b >= 0xff800001
                                                       and b <= 0xffffffff):
            return 'NaN'
        else:
            s = 1 if ((b >> 31) == 0) else -1
            e = ((b >> 23) & 0xff)
            m = (b & 0x7fffff) << 1 if (e == 0) else (b & 0x7fffff) | 0x800000
            return s * m * pow(2, e - 150)

    def readUTF(self):
        UTF_length = self.readUnsignedShort()
        out = ''
        i = 0
        while (i < UTF_length):
            b = self.readByte()
            if b & 0b10000000 == 0b00000000:  # 1 byte
                i = i + 1
                out = out + chr(b)
            elif b & 0b11100000 == 0b11000000:  # 2 byte
                i = i + 2
                out = out + chr((b & 0x1F) << 6 | (self.readByte() & 0x3F))
            elif b & 0b11110000 == 0b11100000:  # 3 byte
                i = i + 3
                out = out + chr(((b & 0x0F) << 12) | (
                    (self.readByte() & 0x3F) << 6) | (self.readByte() & 0x3F))
        return out


if __name__ == "__main__":
    p = Packet(
        "00010072656372757465206b6f7272692073636f7265203330322063726120686162697475c3a92066756c6c206368616c6c206e6f206661696c20657420636f6d626174207261706969696964652c2036356b2f636d6274203220706c61637320646973706f"
    )

    print(p._data)
    print(p.readUTF())
