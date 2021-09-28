import PIL.Image

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

        while len(result) % 3 != 0:
            result += "0"
        return result

    def encode(self, payload : str) -> bool:
        if self.maxPayloadSize < len(payload):
            return False

        img_idx = 0
        stegpayload = self.payloadToStegBinary(payload)
        for i in range(0, len(stegpayload), 3):
            x = img_idx %  self.srcImage.size[0]
            y = img_idx // self.srcImage.size[0]
            img_idx += 1
            self.srcPixels[x, y] = (
                (self.srcPixels[x, y][0] & 0xFE) | int(stegpayload[i]),
                (self.srcPixels[x, y][1] & 0xFE) | int(stegpayload[i+1]),
                (self.srcPixels[x, y][2] & 0xFE) | int(stegpayload[i+2])
                )

        while img_idx < self.pixelCount:
            x = img_idx %  self.srcImage.size[0]
            y = img_idx // self.srcImage.size[0]
            self.srcPixels[x, y] = (
                (self.srcPixels[x, y][0] & 0xFE),
                (self.srcPixels[x, y][1] & 0xFE),
                (self.srcPixels[x, y][2] & 0xFE)
                )
            img_idx += 1

        self.srcImage.save(self.outputName)
        return True

    def decode(self):
        resultbin = ""
        for i in range(self.pixelCount):
            x = i %  self.srcImage.size[0]
            y = i // self.srcImage.size[0]
            resultbin += str(self.srcPixels[x, y][0] & 0x1)
            resultbin += str(self.srcPixels[x, y][1] & 0x1)
            resultbin += str(self.srcPixels[x, y][2] & 0x1)

        resultpayload = []
        for i in range(0, len(resultbin), 8):
            binstr = resultbin[i:i+8]
            if len(binstr) < 8:
                binstr = binstr.ljust(8, "0")

            binstr = "0b" + binstr
            resultpayload.append(int(binstr, 2))

        with open(self.outputName, "wb") as file:
            file.write(bytearray(resultpayload))


# q = PureStegImage("other/eve.png", "hehe.png")
# q.encode("hehe")
#
# p = PureStegImage("hehe.png", "uwu.txt")
# p.decode()
