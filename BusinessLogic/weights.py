from statics.constants import N, weights_filename
import random

from typing import List, Optional

class Weights:

        def __init__(self):
            self.__weights = None
            self.loadWeights()

        def fillRandomValues(self):
            self.__weights = [[0] * N for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    self.__weights[i][j] = -0.3 + 0.6 * random.random()

        def saveWeights(self, filename=weights_filename):
            try:
                with open(filename, "w") as f:
                    for i in range(N):
                        for j in range(N):
                            f.write(str(self.__weights[i][j]) + "\n")
                return True
            except Exception as e:
                return False

        def loadWeights(self, filename=weights_filename):
            self.__weights = [[0] * N for _ in range(N)]
            try:
                with open(filename, "r") as f:
                    for i in range(N):
                        for j in range(N):
                            self.__weights[i][j] = float(f.readline())
                return True
            except Exception as e:
                return False

        @property
        def weights(self):
            self.loadWeights()
            return self.__weights

        def setWeights(self, weights: Optional[List[float]]):
            self.__weights = weights
            self.saveWeights()
