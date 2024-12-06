# This is a backpropagation-free Artificial Neural Network algorithm developed by Sapiens Technology®.
# The algorithm is a simplified reduction without hidden layers to an example application of a HurNet-type Neural Network.
# This version of the network works only with tabular numerical data, that is, two-dimensional numerical arrays distributed between rows and columns.
# HurNet networks are a technological creation of Sapiens Technology® and their distribution or copying without our permission is strictly prohibited.
# We do not permit copying, distribution or back-engineering of this or other versions of the HurNet network or any other code developed by Sapiens Technology®.
# We will prosecute anyone who fails to comply with the rules set out here or who discloses any details about this code.
class SingleLayerHurNetCore:
    def __init__(self):
        try: self.__weights, self.__input_layer = None, None
        except Exception as error: print('ERROR in class construction: ' + str(error))
    def __sum_axis1(self, data=[]): return [sum(row) for row in data]
    def __sum_keepdims(self, data=[]): return [[sum(row)] for row in data]
    def __sum_list(self, data=[]): return sum(data)
    def __mean_axis0(self, data=[]):
        if not data: return []
        number_of_columns, means = len(data[0]), []
        for column in range(number_of_columns):
            sum_of_columns, count = 0, 0
            for row in data:
                if column < len(row):
                    sum_of_columns += row[column]
                    count += 1
            mean = sum_of_columns / count if count > 0 else 0
            means.append(mean)
        return means
    def __linalg_norm(self, vector): return sum(x ** 2 for x in vector) ** .5
    def __euclidean_distance(self, vector1=[], vector2=[]): return sum((a - b) ** 2 for a, b in zip(vector1, vector2)) ** .5
    def __argmin(self, data=[]):
        if not data: return -1
        minimum_value, minimum_index = data[0], 0
        for index, value in enumerate(data):
            if value < minimum_value: minimum_value, minimum_index = value, index
        return minimum_index
    def __proximity_calculation(self, input_layer=[]):
        distances = []
        for stored_input in self.__input_layer:
            distance = self.__euclidean_distance(stored_input, input_layer)
            distances.append(distance)
        return self.__argmin(distances)
    def saveModel(self, path=''):
        try:
            if not path: filename = 'model.hur'
            else:
                filename = str(path).strip()
                if not filename.endswith('.hur'): filename += '.hur'
            data = {'input_layer': self.__input_layer, 'weights': self.__weights}
            from pickle import dump
            with open(filename, 'wb') as file: dump(data, file)
            from os import path as path_exists
            return path_exists.exists(filename)
        except Exception as error:
            print('ERROR in saveModel: ' + str(error))
            return False
    def loadModel(self, path=''):
        try:
            if not path: filename = 'model.hur'
            else:
                filename = str(path).strip()
                if not filename.endswith('.hur'): filename += '.hur'
            from os import path as path_exists
            if not path_exists.exists(filename):
                print(f'The {filename} file does not exist!!')
                return False
            from pickle import load
            with open(filename, 'rb') as file:
                data = load(file)
                self.__input_layer = data.get('input_layer', None)
                self.__weights = data.get('weights', None)
            return True
        except Exception as error:
            print(f'ERROR in loadModel: ' + str(error))
            return False
    def train(self, input_layer=[], output_layer=[], linear=False):
        try:
            if not input_layer or not output_layer:
                print('Input and output layers must not be empty.')
                return False
            if not all(isinstance(x, list) for x in input_layer): input_layer = [list(row) for row in input_layer]
            if not all(isinstance(y, list) for y in output_layer): output_layer = [list(row) for row in output_layer]
            input_array, output_array = input_layer, output_layer
            summation_function = self.__sum_axis1(input_array)
            sum_of_entries, weights_per_sample = [x if x != 0 else 1 for x in summation_function], []
            for output, sum_result in zip(output_array, sum_of_entries):
                weights = [y / sum_result for y in output]
                weights_per_sample.append(weights)
            if linear: self.__weights = self.__mean_axis0(weights_per_sample)
            else: self.__weights = weights_per_sample
            self.__input_layer = input_array
            return True
        except Exception as error:
            print(f'ERROR in train: ' + str(error))
            return False
    def predict(self, input_layer=[]):
        try:
            if self.__weights is None:
                print('No training has been carried out yet!!')
                return []
            if not input_layer:
                print('Input layer is empty.')
                return []
            if not all(isinstance(row, list) for row in input_layer): input_layer = [list(row) for row in input_layer]
            input_array, outputs = input_layer, []
            if isinstance(self.__weights[0], (int, float)):
                sum_inputs = self.__sum_axis1(input_array)
                sum_inputs = [x if x != 0 else 1 for x in sum_inputs]
                for x in sum_inputs:
                    output = [x * w for w in self.__weights]
                    outputs.append(output)
            else:
                for inputs in input_array:
                    nearest_index = self.__proximity_calculation(inputs)
                    weights = self.__weights[nearest_index]
                    sum_inputs = sum(inputs)
                    sum_inputs = sum_inputs if sum_inputs != 0 else 1
                    output = [sum_inputs * w for w in weights]
                    outputs.append(output)
            return outputs
        except Exception as error:
            print(f'ERROR in predict: ' + str(error))
            return []
# This is a backpropagation-free Artificial Neural Network algorithm developed by Sapiens Technology®.
# The algorithm is a simplified reduction without hidden layers to an example application of a HurNet-type Neural Network.
# This version of the network works only with tabular numerical data, that is, two-dimensional numerical arrays distributed between rows and columns.
# HurNet networks are a technological creation of Sapiens Technology® and their distribution or copying without our permission is strictly prohibited.
# We do not permit copying, distribution or back-engineering of this or other versions of the HurNet network or any other code developed by Sapiens Technology®.
# We will prosecute anyone who fails to comply with the rules set out here or who discloses any details about this code.
