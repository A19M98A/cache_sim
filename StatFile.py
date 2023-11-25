

class StatsFile:
    numberOfHit = 0
    numberOfMiss = 0
    numberOfTotal = 0

    @classmethod
    def onHit(cls):
        cls.numberOfHit += 1
        cls.numberOfTotal += 1
    
    @classmethod
    def onMiss(cls):
        cls.numberOfMiss += 1
        cls.numberOfTotal += 1
    
    @classmethod
    def printStates(cls):
        print(f"Number of Hit:{cls.numberOfHit}, Number of Miss:{cls.numberOfMiss}, Hit rate:{round((cls.numberOfHit/cls.numberOfTotal) * 100, 2)}")