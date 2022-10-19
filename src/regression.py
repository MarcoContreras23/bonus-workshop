class Regression:

    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
        self.slope = 0
        self.intercept = 0
        self.x = 0
        self.y = 0
        self.xy = 0
        self.x2 = 0
    
    def start(self):
        self.calculate_data()
        self.calculate_slope()
        self.calculate_intercept()

    def calculate_data(self):
        self.x = sum(self.x_data)
        self.y = sum(self.y_data)
        self.xy = sum([self.x_data[i] * self.y_data[i] for i in range(len(self.x_data))])
        self.x2 = sum([self.x_data[i] * self.x_data[i] for i in range(len(self.x_data))])

    def calculate_slope(self):
        n = len(self.x_data)
        self.slope = (n * self.xy - self.x * self.y) / (n * self.x2 - self.x * self.x)

    def calculate_intercept(self):
        n = len(self.x_data)
        self.intercept = (self.y * self.x2 - self.x * self.xy) / (n * self.x2 - self.x * self.x)

    def predict(self, data_to_predict):
        return self.slope * data_to_predict + self.intercept

    def predict_list(self, data_to_predict):
        return [self.slope * data + self.intercept for data in data_to_predict]
