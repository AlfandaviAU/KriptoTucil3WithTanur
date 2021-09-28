import PIL.Image
from math import log
import numpy as np

class PureStegImage:
    def __init__(self, input : str, output : str):
        self.srcImage       = PIL.Image.open(input)
        self.srcPixels      = self.srcImage.load()
        self.outputName     = output
        self.pixelCount     = self.srcImage.size[0] * self.srcImage.size[1]
        self.maxPayloadSize = self.pixelCount * 3 // 8

    def payloadToStegBinary(self, payload : str) -> str:
        result = ""
        for c in payload:
            result += bin(ord(c))[2:].zfill(8)

        # Padding
        while len(result) % 3 != 0:
            result += "0"
        return result

    def lcg(self, a : int, b: int, m : int):
        i = 0
        if m is None:
            i = 3
            while True:
                yield (a*i + b)
                i += 1
        else:
            while True:
                nextgen = (a*i + b) % m
                while nextgen in [0, 1, 2]:
                    i += 1
                    nextgen = (a*i + b) % m
                yield nextgen
                i += 1

    def encode(self, payload : str, key : str = None) -> bool:
        if self.maxPayloadSize < len(payload):
            return False

        # LSB wiping
        for i in range(self.pixelCount):
            x = i %  self.srcImage.size[0]
            y = i // self.srcImage.size[0]
            self.srcPixels[x, y] = (
                (self.srcPixels[x, y][0] & 0xFE),
                (self.srcPixels[x, y][1] & 0xFE),
                (self.srcPixels[x, y][2] & 0xFE)
                )

        # Payload processing
        stegpayload = self.payloadToStegBinary(payload)
        if key is None:
            indexgenerator = self.lcg(1, 0, None)
            stegheader    = "001000000"
        else:
            # 3 bit for a, 6 bit for b
            a = ord(key[0]) % 8
            b = sum([ord(c) for c in key]) % 64
            if b == 0:
                b = 1
            indexgenerator = self.lcg(a, b, self.pixelCount)
            stegheader     = bin(a)[2:].zfill(3) + bin(b)[2:].zfill(6)

        # Insertion
        for i in range(3):
            self.srcPixels[i, 0] = (
                (self.srcPixels[i, 0][0] & 0xFE) | int(stegheader[3*i]),
                (self.srcPixels[i, 0][1] & 0xFE) | int(stegheader[3*i+1]),
                (self.srcPixels[i, 0][2] & 0xFE) | int(stegheader[3*i+2])
                )

        img_idx = next(indexgenerator)
        for i in range(0, len(stegpayload), 3):
            x = img_idx %  self.srcImage.size[0]
            y = img_idx // self.srcImage.size[0]
            img_idx = next(indexgenerator)
            self.srcPixels[x, y] = (
                (self.srcPixels[x, y][0] & 0xFE) | int(stegpayload[i]),
                (self.srcPixels[x, y][1] & 0xFE) | int(stegpayload[i+1]),
                (self.srcPixels[x, y][2] & 0xFE) | int(stegpayload[i+2])
                )

        self.srcImage.save(self.outputName)
        return True

    def decode(self):
        resultbin = ""

        stegheader = ""
        for i in range(3):
            stegheader += str(self.srcPixels[i, 0][0] & 1) + str(self.srcPixels[i, 0][1] & 1) + str(self.srcPixels[i, 0][2] & 1)
        a = int("0b" + stegheader[0:3], 2)
        b = int("0b" + stegheader[3:9], 2)

        iter = 0
        for i in self.lcg(a, b, self.pixelCount):
            if iter > self.pixelCount - 3:
                break
            x = i %  self.srcImage.size[0]
            y = i // self.srcImage.size[0]
            resultbin += str(self.srcPixels[x, y][0] & 0x1)
            resultbin += str(self.srcPixels[x, y][1] & 0x1)
            resultbin += str(self.srcPixels[x, y][2] & 0x1)
            iter += 1

        resultpayload = []
        for i in range(0, len(resultbin), 8):
            binstr = resultbin[i:i+8]
            if len(binstr) < 8:
                binstr = binstr.ljust(8, "0")

            binstr = "0b" + binstr
            resultpayload.append(int(binstr, 2))

        with open(self.outputName, "wb") as file:
            file.write(bytearray(resultpayload))


def psnr(cover : str, stego : str) -> float:
    buf1 = np.asarray(PIL.Image.open(cover))
    buf2 = np.asarray(PIL.Image.open(stego))
    rms  = np.mean((buf1-buf2)**2)
    return 20 * log(255/rms, 10)




# q = PureStegImage("other/eve.png", "hehe.png")
# q.encode("hehe", "uwu")
#
# #
# p = PureStegImage("hehe.png", "uwu.txt")
# p.decode()
