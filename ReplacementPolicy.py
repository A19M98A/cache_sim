import random

class LRU_RP:
    @staticmethod
    def getVictim(candidate):
        victim = -1
        for blk in candidate:
            if victim == -1 or victim.touchTime < blk.touchTime:
                victim = blk
        
        return victim

class NMRU_RP:
    @staticmethod
    def getVictim(candidate):
        MRU = -1
        for blk in candidate:
            if MRU == -1 or MRU.touchTime < blk.touchTime:
                MRU = blk
        victim = candidate[random.randint(0, len(candidate) - 1)]
        while victim == MRU:
            victim = candidate[random.randint(0, len(candidate) - 1)]
        return victim

class Random_RP:
    @staticmethod
    def getVictim(candidate):
        victim = candidate[random.randint(0, len(candidate) - 1)]
        return victim

class RP:
    @staticmethod
    def getRP(RP):
        if RP == "LRU" or RP == "":
            return LRU_RP
        elif RP == "NMRU":
            return NMRU_RP
        elif RP == "Random":
            return Random_RP