import math

from ReplacementPolicy import RP
from StatFile import StatsFile

current_cycle = 0

dedBlockTime = 0

class Block:
    def __init__(self):
        self.valid = 0
        self.tag = 0
        self.data = 0
        self.touchTime = 0
    
    def touch(self):
        self.touchTime = current_cycle
    
    def write(self, tag, data):
        self.tag = tag
        self.data = data
        self.valid = 1
        self.touch()

class CacheSet:
    numberOfSet = 0
    replacementPolicy = RP.getRP("LRU")

    def __init__(self, numberOfWays, setRowID):
        self.blocks = []
        self.setRowID = setRowID
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
        if victim.valid:
            global dedBlockTime
            if current_cycle > self.numberOfSet * Cache.MAX_WAY: # for the time of warm up cache
                dedBlockTime += current_cycle - max(victim.touchTime, self.numberOfSet * Cache.MAX_WAY)
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
        self.MAX_WAY = numberOfWays
        for i in range(CacheSet.numberOfSet):
            self.tags.append(CacheSet(numberOfWays, i))
        
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
        global dedBlockTime
        print(f"avg of ded block:{round(dedBlockTime/(current_cycle - 1 - (CacheSet.numberOfSet * Cache.MAX_WAY)), 2)} ({round((dedBlockTime/(current_cycle - 1- (CacheSet.numberOfSet * Cache.MAX_WAY)))/(CacheSet.numberOfSet * self.MAX_WAY)*100, 2)}%)")
        StatsFile.printStates()