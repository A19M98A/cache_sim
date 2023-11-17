import math

from ReplacementPolicy import RP
from StatFile import StatsFile

current_cycle = 0

class Block:
    def __init__(self):
        self.tag = 0
        self.data = 0
        self.touchTime = 0
    
    def touch(self):
        self.touchTime = current_cycle
    
    def write(self, tag, data):
        self.tag = tag
        self.data = data
        self.touch()

class CacheSet:
    numberOfSet = 0
    replacementPolicy = RP.getRP("LRU")

    def __init__(self, numberOfWays):
        self.blocks = []
        for i in range(numberOfWays):
            self.blocks.append(Block())
    
    def access(self, tag):
        for blk in self.blocks:
            if blk.tag == tag:
                blk.touch()
                return 1
        
        return 0
    
    def insert(self, tag):
        victim = self.replacementPolicy.getVictim(self.blocks)
        victim.write(tag, 0)
    
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

    def __init__(self, cacheSize, blkSize, numberOfWays, replacementPolicy):
        CacheSet.numberOfSet = int((cacheSize / blkSize) / numberOfWays)
        CacheSet.replacementPolicy = RP.getRP(replacementPolicy)
        self.tagShiftSize = int(math.log(blkSize, 2) + math.log(CacheSet.numberOfSet, 2))
        self.setShiftSize = int(math.log(blkSize, 2))
        for i in range(CacheSet.numberOfSet):
            self.tags.append(CacheSet(numberOfWays))
        
        print(f"Cache created by {CacheSet.numberOfSet} sets.")
        print(f"tag shift:{self.tagShiftSize}, set shift:{self.setShiftSize}")

    def access(self, addressIN):
        global current_cycle
        current_cycle += 1
        _set = addressIN >> self.setShiftSize & (CacheSet.numberOfSet - 1)
        satisfy = self.tags[_set].access(addressIN >> self.tagShiftSize)
        if satisfy:
            StatsFile.onHit()
        else:
            self.tags[_set].insert(addressIN >> self.tagShiftSize)
            StatsFile.onMiss()
    
    def printFinallyState(self):
        StatsFile.printStates()