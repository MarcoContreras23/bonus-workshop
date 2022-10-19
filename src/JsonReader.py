import json


class Json:

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as file:
            data = json.load(file)
            dataToAsign = None
            dataToReturn = data

            if "axis_x" in data.keys():
                dataToReturn = (data["axis_x"]["name"],
                                data["axis_y"]["name"],
                                data["axis_x"]["data"],
                                data["axis_y"]["data"],
                                data["data_to_predict"])
            elif "k" in data.keys():
                dataToAsign = data["dataToAsign"]
                k = data["k"]
                del data["dataToAsign"]
                del data["k"]

                dataToReturn = (dataToAsign, data, k)
            elif "dataToAsign" in data.keys():
                dataToAsign = data["dataToAsign"]
                del data["dataToAsign"]

                dataToReturn = (dataToAsign, data)
            return dataToReturn