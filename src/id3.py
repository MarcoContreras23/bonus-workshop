from math import log2
from src.Algorithm import Algorithm


class Id3(Algorithm):

    def __init__(self, data):
        Algorithm.__init__(self, data)
        self.resumed_data = {}
        self.entropies = {}
        self.result = {}
    
    def start(self):
        self.categories = self.get_categories()
        self.resumed_data = self.get_resumed_data()
        self.entropies = self.get_entropies()
        self.result = self.get_result()

        self.print_result()
    
    def get_resumed_data(self):
        resumed_data = {}
        index = 0

        for (key, value) in self.data.items():
            if key != list(self.data.keys())[-1] and key not in resumed_data.keys():
                resumed_data[key] = {data: {category: 0 for category in self.categories[list(self.categories)[0]].keys()} for data in value}
            
            if key in resumed_data.keys():
                for data in value:
                    category = self.data[list(self.data.keys())[-1]][index]
                    resumed_data[key][data][category] += 1
                    index += 1
                
            index = 0
        
        return resumed_data
    
    def get_entropies(self):
        entropies = {data: 0 for data in self.resumed_data.keys()}

        for (key, value) in self.resumed_data.items():
            entropies[key] = self.get_entropy(value)
        
        return dict(sorted(entropies.items(), key=lambda x: x[1]))

    def get_entropy(self, data):
        entropy = 0

        for (key, value) in sorted(data.items()):
            entropy += (sum(value.values()) / (len(self.data) + 1)) * self.get_entropy_value(value)
        
        return entropy

    def get_entropy_value(self, data):
        entropy_value = 0

        for value in data.values():
            if value != 0:
                entropy_value += -(value / sum(data.values())) * log2(value / sum(data.values()))
        
        return entropy_value

    def get_result(self):
        current_category = list(self.entropies.keys())[0]
        result = {}
        ordered_result = {current_category: {}}

        for (key, value) in self.resumed_data[current_category].items():
            for (category, count) in value.items():
                if count == sum(value.values()):
                    result[key] = category
                    break
        
        for (key, value) in self.resumed_data[current_category].items():
            for (category, count) in value.items():
                if count != sum(value.values()) and key not in result.keys() and len(result.keys()) > 0:
                    result[key] = self.update_data(current_category, result.keys())
                    break
        
        if len(result.keys()) == 0:
            for (key, value) in self.resumed_data[current_category].items():
                for (category, count) in value.items():
                    if count == max(value.values()) and key not in result.keys():
                        result[key] = category
                        break
                    
        ordered_result[current_category] = dict(sorted(result.items(), key=lambda x: x[0]))
        return ordered_result
          
    def update_data(self, current_category, data_to_remove):
        index_to_remove = []
        data = {}

        for i in range(len(self.data[current_category])):
            if self.data[current_category][i] in data_to_remove:
                index_to_remove.append(i)

        for (key, value) in self.data.items():
            if key != current_category:
                data[key] = [value[i] for i in range(len(value)) if i not in index_to_remove]
        
        id3 = Id3(data)
        id3.start()

        return id3.get_result()

    def print_result(self):
        print("Decision Tree\n")
        print("Data clasifications:\n {}\n".format(self.categories))
        print("Clasified data:\n {}\n".format(self.resumed_data))
        print("Entropy for each column:\n {}\n".format(self.entropies))
        print("Result: ", self.result)