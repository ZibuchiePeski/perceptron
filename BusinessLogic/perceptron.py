from statics.constants import N, speed

from BusinessLogic.scaling import Scaling
from BusinessLogic.weights import Weights

from typing import List, Optional


class Perceptron:

    def __init__(self):
        self.__pixel_matrix: Optional[List[int]] = None
        self.__weights: Weights = None

    def __setPerceptronParams(self, pixel_matrix: Optional[List[int]], weights: Weights) -> None:
        self.__pixel_matrix = pixel_matrix
        self.__weights = weights
        self.__weights_matrix: Optional[List[float]] = weights.weights

    def perceptronOutput(self, pixel_matrix: Optional[List[int]], weights: Weights) -> bool:
        self.__setPerceptronParams(pixel_matrix, weights)

        total_sum = 0

        # Растягивание изображения на сетке до ее границ
        self.__pixel_matrix = Scaling.scalePixelMatrix(self.__pixel_matrix)

        # Вычисляем сумму входа персептрона
        for i in range(N):
            for j in range(N):
                total_sum += self.__pixel_matrix[i][j] * self.__weights_matrix[i][j]

        # Определяем выход персептрона
        # Пусть крестик - 1, а нолик - 0
        output = 1 if total_sum > 0 else 0

        return output

    def perceptronTrain(self, answer: str, output: bool) -> None:
        if answer == 'no':
            if output == 0:
                test = 1
            else:
                test = -1

            # Обучаем персептрон в случае неправильного ответа
            for i in range(N):
                for j in range(N):
                    # Корректируем веса по формуле
                    self.__weights_matrix[i][j] += speed * test * self.__pixel_matrix[i][j]

            # Сохраняем измененные веса в файл
            self.__weights.setWeights(self.__weights_matrix)