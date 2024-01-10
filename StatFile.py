from Prefetcher import PF

class StatsFile:
    numberOfHit = 0
    numberOfMiss = 0
    numberOfTotal = 0
    numberOfHitPF = 0
    numberOfPF = 0

    @staticmethod
    def onHit():
        StatsFile.numberOfHit += 1
        StatsFile.numberOfTotal += 1
    
    @staticmethod
    def onPFHit():
        StatsFile.numberOfHitPF += 1
    
    @staticmethod
    def onPFCount():
        StatsFile.numberOfPF += 1
    
    @staticmethod
    def onMiss():
        StatsFile.numberOfMiss += 1
        StatsFile.numberOfTotal += 1
    
    @staticmethod
    def printStates():
        print(f"Number of Hit:{StatsFile.numberOfHit}, Number of Miss:{StatsFile.numberOfMiss}, Hit rate:{round((StatsFile.numberOfHit/StatsFile.numberOfTotal) * 100, 2)}")
        print(f"Number of PF:{StatsFile.numberOfPF}, Number of PF Hit:{StatsFile.numberOfHitPF}, Hit rate on PF:{round((StatsFile.numberOfHitPF/StatsFile.numberOfPF) * 100, 2)}")