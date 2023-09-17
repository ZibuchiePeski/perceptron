import random
from typing import List, Optional, Any

from statics.constants import N, weights_filename


class Weights:
        """Класс работы с весовыми коэффициентами и кэшем"""

        def __init__(self):
            self.__weights = None
            self.loadWeights()

        def fillRandomValues(self) -> None:
            """Генерация случайных весов"""
            self.__weights = [[0] * N for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    self.__weights[i][j] = -0.3 + 0.6 * random.random()

        def saveWeights(self, filename: str = weights_filename) -> bool:
            """Сохранение весов в файл (кэш) по пути filename"""
            try:
                with open(filename, "w") as f:
                    for i in range(N):
                        for j in range(N):
                            f.write(str(self.__weights[i][j]) + "\n")
                return True
            except Exception as e:
                return False

        def loadWeights(self, filename: str = weights_filename) -> bool:
            """Выгрузка весов из файла (кэш) по пути filename"""
            self.__weights = [[0] * N for _ in range(N)]
            try:
                with open(filename, "r") as f:
                    for i in range(N):
                        for j in range(N):
                            self.__weights[i][j] = float(f.readline())
                return True
            except Exception as e:
                return False

        def setWeights(self, weights: Optional[List[float]]) -> None:
            """Установка весов weights"""
            self.__weights = weights
            self.saveWeights()

        @property
        def weights(self) -> Any:
            """Получение весов"""
            self.loadWeights()
            return self.__weights
