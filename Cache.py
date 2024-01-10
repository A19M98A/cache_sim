import math

from ReplacementPolicy import RP
from Prefetcher import PF
from StatFile import StatsFile

current_cycle = 0


class Block:
    def __init__(self):
        self.isPF = 0
        self.isCountedPF = 0
        self.valid = 0
        self.tag = 0
        self.data = 0
        self.touchTime = 0
    
    def touch(self):
        self.touchTime = current_cycle
    
    def write(self, tag, data, isPF):
        self.tag = tag
        self.data = data
        self.valid = 1
        self.isPF = isPF
        self.isCountedPF = 0
        self.touch()

class CacheSet:
    numberOfSet = 0
    replacementPolicy = RP.getRP("LRU")

    def __init__(self, numberOfWays, setRowID):
        self.blocks = []
        self.setRowID = setRowID
        for i in range(numberOfWays):
            self.blocks.append(Block())
    
    def access(self, tag, isPF, PCIn):
        for blk in self.blocks:
            if blk.tag == tag:
                blk.touch()
                if isPF:
                    blk.isPF = isPF
                elif blk.isPF:
                    if not blk.isCountedPF:
                        StatsFile.onPFHit()
                        blk.isCountedPF = 1
                    addr = (self.setRowID << Cache.setShiftSize) + (blk.tag << Cache.tagShiftSize)
                    Cache.access(Cache.prefetcherMethod.prefetch(addr, Cache.setShiftSize, PCIn), 1, PCIn)
                    # blk.isPF = 0
                
                return 1
        
        return 0
    
    def insert(self, tag, isPF):
        victim = self.replacementPolicy.getVictim(self.blocks)
        victim.write(tag, 0, isPF)
    
    def printState(self):
        blk_tags = []
        for blk in self.blocks:
            blk_tags.append(blk.tag)
        print(blk_tags)


class Cache:
    tags = []
    MAX_SET_ADDR = 0
    MAX_WAY = 0
    tagShiftSize = 0
    setShiftSize = 0
    prefetcherMethod = PF.getPF("no_PF")

    def __init__(self, cacheSize, blkSize, numberOfWays, replacementPolicy, prefetcherMethod):
        CacheSet.numberOfSet = int((cacheSize / blkSize) / numberOfWays)
        CacheSet.replacementPolicy = RP.getRP(replacementPolicy)
        Cache.tagShiftSize = int(math.log(blkSize, 2) + math.log(CacheSet.numberOfSet, 2))
        Cache.setShiftSize = int(math.log(blkSize, 2))
        Cache.MAX_WAY = numberOfWays
        Cache.prefetcherMethod = PF.getPF(prefetcherMethod)
        for i in range(CacheSet.numberOfSet):
            Cache.tags.append(CacheSet(numberOfWays, i))
        
        print(f"Cache created by {CacheSet.numberOfSet} sets.")
        print(f"tag shift:{Cache.tagShiftSize}, set shift:{Cache.setShiftSize}")

    @staticmethod
    def access(addressIN, isPF, PCIn):
        if not addressIN:
            return
        global current_cycle
        if not isPF:
            current_cycle += 1
        _set = addressIN >> Cache.setShiftSize & (CacheSet.numberOfSet - 1)
        satisfy = Cache.tags[_set].access(addressIN >> Cache.tagShiftSize, isPF, PCIn)
        if satisfy:
            if not isPF:
                StatsFile.onHit()
        else:
            Cache.tags[_set].insert(addressIN >> Cache.tagShiftSize, isPF)
            if not isPF:
                Cache.access(Cache.prefetcherMethod.prefetch(addressIN, Cache.setShiftSize, PCIn), 1, PCIn)
                StatsFile.onPFCount()
                StatsFile.onMiss()
            else:
                StatsFile.onPFCount()

    @staticmethod
    def printFinallyState():
        StatsFile.printStates()