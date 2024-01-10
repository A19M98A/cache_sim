

class NoPF:
    @staticmethod
    def prefetch(accessed, setShiftSize, PCIn):
        return

class NextLine:
    @staticmethod
    def prefetch(accessed, setShiftSize, PCIn):
        return ((accessed >> setShiftSize) + 1) << setShiftSize

class Stride:
    strideHistory = {0: (0, 0, 0)}
    @staticmethod
    def prefetch(accessed, setShiftSize, PCIn):
        if PCIn in Stride.strideHistory:
            stride = Stride.strideHistory[PCIn][0]
            preDist = Stride.strideHistory[PCIn][1]
            if stride - (accessed >> setShiftSize) == 0:
                return ((accessed >> setShiftSize) + 1) << setShiftSize
            dist = stride - (accessed >> setShiftSize)
            if preDist != 0:
                powDist = int(abs(dist) / abs(preDist))
            else:
                powDist = 1
            Stride.strideHistory[PCIn] = ((accessed >> setShiftSize), dist)
            if stride != 0:
                return ((accessed >> setShiftSize) + (dist * powDist)) << setShiftSize
            else:
                return ((accessed >> setShiftSize) + 1) << setShiftSize
        else:
            Stride.strideHistory[PCIn] = ((accessed >> setShiftSize), 0, 0)
            return ((accessed >> setShiftSize) + 1) << setShiftSize

class PF:
    @staticmethod
    def getPF(prefetcherMethod):
        if prefetcherMethod == "no_PF":
            return NoPF
        elif prefetcherMethod == "next_line":
            return NextLine
        elif prefetcherMethod == "Stride":
            return Stride
