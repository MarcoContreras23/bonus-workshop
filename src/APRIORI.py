import itertools

class APRIORI:

    def __init__(self, data):
        self.data = data
        self.minConfidence = 0
        self.minSupport = 0
        self.frecuentItemset = []
        self.inicialItemset = []

    def start(self, minConfidence, minSupport):
        self.minConfidence = minConfidence
        self.minSupport = minSupport
        rules = self.apriori()

    # Generate algorithm APRIORI
    def apriori(self):
        print("data: ", self.data)
        print("support percent", self.minSupport, " -- confidence percent", self.minConfidence)
        occurence = self.generateCombination(self.data)
        print("____________________________________________________________________________________")
        print("Frecuent itemset: ", self.frecuentItemset[-1])
        print("____________________________________________________________________________________")
        rules = self.generateRules(self.frecuentItemset[-1])

    #Generate all possible combination of items without repetition and without elimination of items
    def generateCombination(self, data):
        combination = []
        for transaction in data:
            for i in range(0, len(transaction)):
                combination.append(list(itertools.combinations(transaction, i + 1)))
        for i in range(len(combination)):
            print("____________________________________________________________________________________")
            print("Itemset", i + 1)
            print("K", i + 1, ":", combination[i])
            newCombination = self.generateOccurence(combination[i])
            if newCombination == False:
                break
        return combination

    #Generate occurence and support of each item
    def generateOccurence(self, data):
        occurence = {}
        for transaction in data:
            for item in self.data:
                if set(transaction).issubset(set(item)):
                    if transaction in occurence:
                        occurence[transaction] += 1
                    else:
                        occurence[transaction] = 1
        print("Occurence: ",occurence)
        newOccurence = self.filterPhase(occurence)
        if (newOccurence == False):
            return False
        else:
            self.frecuentItemset.append(newOccurence)
        return occurence
    
    # Filter phase of APRIORI
    def filterPhase(self, occurence):
        deloccurence = {}
        for key, value in occurence.items():
            occurence[key] = round(value / len(self.data),2)
            if occurence[key] >= self.minSupport:
                deloccurence[key] = occurence[key]
        print("Support: ", occurence)
        self.inicialItemset.append(occurence)
        if len(deloccurence) == 0:
            print("No itemset found")
            return False
        print("Delete post validate support percent")
        print(deloccurence)
        return deloccurence

    def generateRules(self, data):
        print("Generate rules -->")
        newList = []
        rulesOver = []
        print("data: ", data)
        for key, value in data:
            newList.append((key , value))
            newList.append((value , key))
        for key, value in newList:
            for key2 in self.inicialItemset[0]:
                if key in key2:
                    for supportData in data:
                        result = round(data[supportData] / self.inicialItemset[0][key2],2)
                    print(key , " => ", value, "--> confidence: ", result)
                    if result >= self.minConfidence:
                        rule=(key , " => ", value, "--> confidence: ", result)
                        rulesOver.append(rule)
        print("____________________________________________________________________________________")
        print("Rules over confidence percent: ")
        for rule in rulesOver:
            print(rule)