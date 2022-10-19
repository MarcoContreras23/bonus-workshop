class Algorithm:

    def __init__(self, data):
        self.data = data
        self.categories = {}
    
    def get_categories(self):
        category = list(self.data.keys())[-1]
        categories = {category: {data: 0 for data in self.data[category]}}

        for data in self.data[category]:
            if data not in categories:
                categories[category][data] += 1
        
        return categories
    
