from ast import For
import operator as op
from itertools import takewhile, combinations


class FPGrowth:
    def __init__(self, data):
        self.support = 0
        self.items = data
        self.allItems = []
        self.itemNotRepet = []
        self.cleanItemSets = {}
        self.orderedItem = {}
        self.conditionalPatternBaseList = {}

    def start(self):
        self.supportItems()
        self.cleanItems()
        self.orderedItemSet()
        self.conditionalPatternBase()
        self.conditionalFpTree()

    def supportItems(self):
        for value in self.items.values():
            if type(value) is list:
                for letter in value:
                    if letter not in self.itemNotRepet:
                        self.itemNotRepet.append(letter)
                    self.allItems.append(letter)
        print("List items dont repeat")
        print(self.itemNotRepet)
        print("-----------------------")
        print("Frequency of items")
        for character in self.itemNotRepet:

            print(
                f"{character} has occurred {op.countOf(self.allItems, character)} times")
            self.cleanItemSets[character] = op.countOf(
                self.allItems, character)
        print("-----------------------")
        print("List of items with their frequency")
        print(self.cleanItemSets)

    def cleanItems(self):
        for value in self.items.values():
            if type(value) is int:
                self.support = value
        listCleanItemSets = {key: value for (
            key, value) in self.cleanItemSets.items()}
        for itemKey, itemValue in listCleanItemSets.items():
            if itemValue < self.support:

                del self.cleanItemSets[itemKey]
        print("-----------------------")
        print("List of items with their frequency that passed support")
        print(dict(sorted(self.cleanItemSets.items(), key=lambda x: x[1])))
        self.cleanItemSets = dict(
            sorted(self.cleanItemSets.items(), key=lambda x: x[1], reverse=True))
        print("-----------------------")
        print("List of items with their frequency that passed the ordered support")
        print(self.cleanItemSets)

    def orderedItemSet(self):

        self.orderedItem = {
            key: [] for key in self.items.keys() if key is not "support"
        }

        for character in self.cleanItemSets.keys():
            for key, value in self.items.items():
                if type(value) is list:
                    for letter in value:
                        if letter is character:
                            self.orderedItem[key].append(letter)

        print("-----------------------")
        print("Ordered item set")
        print(self.orderedItem)

    def conditionalPatternBase(self):
        reversedList = {list(self.cleanItemSets.keys())[i]: list(self.cleanItemSets.values())[
            i] for i in range(len(self.cleanItemSets) - 1, -1, -1)}
        print("-----------------------")
        print("List of items sorted in descending order")
        print(reversedList)
        listLetter = {key: [[]] for key in reversedList.keys()}
        for letter in reversedList.keys():
            for value in self.orderedItem.values():
                if letter in value:
                    val = list(takewhile(lambda x: x != letter, value))
                    if val not in listLetter[letter][0]:
                        if len(listLetter[letter][0]) == 0:
                            listLetter[letter].pop(0)
                        listLetter[letter].append([val, 1])
                    else:
                        listLetter[letter][0][1] += 1
        self.conditionalPatternBaseList = listLetter
        print("-----------------------")
        print("Conditional pattern base")
        print(self.conditionalPatternBaseList)

    def conditionalFpTree(self):

        workListCompare = {
            key: [["", array[1]] for array in value] for (key, value) in self.conditionalPatternBaseList.items()
        }

        for key, value in self.conditionalPatternBaseList.items():
            i = 0
            for array in value:
                if i == 0 or (i > 0 and ''.join(array[0]) != workListCompare[key][i - 1][0]):
                    workListCompare[key][i][0] = ''.join(array[0])
                elif i > 0:
                    workListCompare[key][i - 1][1] += array[1]
                    del workListCompare[key][i]
                i += 1
        self.getItemsCombination(workListCompare)

    def getItemsCombination(self, workListCompare):
        listResult = {key: {}
                      for (key) in self.conditionalPatternBaseList.keys()}
        listResult2 = {key: {}
                       for (key) in self.conditionalPatternBaseList.keys()}
        listCharacter = {}
        for key, value in workListCompare.items():
            for array in value:
                for i in range(len(array[0])):
                    combinaciones = combinations(array[0], i + 1)
                    for valueCombinations in combinaciones:
                        if ''.join(valueCombinations) not in listCharacter.keys():
                            listCharacter[''.join(
                                valueCombinations)] = array[1]
                        else:
                            listCharacter[''.join(
                                valueCombinations)] += array[1]
            listResult = self.patternGenerated(
                listCharacter, key, 0, listResult)

            listResult2 = self.patternGenerated(
                listCharacter, key, 1, listResult2)
            listCharacter = {}
        print("-----------------------")
        print("Conditional FP tree")
        print(listResult2)
        print("-----------------------")
        print("Freq pattern generated")
        print(listResult)

    def patternGenerated(self, listCharacter, key, number, listResult):

        addToResult = True
        for key2, value2 in listCharacter.items():
            if number is 1:
                listGreatherResult = [
                    key for key in listCharacter.keys() if len(key) > 1]
                for result in listGreatherResult:
                    if key2 in result and len(key2) < len(result) and listCharacter[result] >= self.support:
                        addToResult = False
                        break
            if value2 >= self.support and addToResult:
                listResult[key][key2] = value2
            addToResult = True

        return listResult
