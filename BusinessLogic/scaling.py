from typing import List, Optional

import numpy as np
from numpy import ndarray

from statics.constants import N


class Scaling:
    """Класс работы с масштабированием изображений"""
    @staticmethod
    def scalePixelMatrix(pixel_matrix: Optional[List[int]]) -> ndarray:
        """Масштабирование изображения под размер экрана"""
        tmp = np.zeros((N, N), dtype=int)

        # Находим границы изображения
        xmin, xmax, ymin, ymax = N, -1, N, -1
        for i in range(N):
            for j in range(N):
                if pixel_matrix[i][j] == 1:
                    if j < xmin:
                        xmin = j
                    if j > xmax:
                        xmax = j
                    if i < ymin:
                        ymin = i
                    if i > ymax:
                        ymax = i

        # Масштабируем изображение
        for i in range(N):
            for j in range(N):
                tmp[i][j] = pixel_matrix[ymin + int((i / N) * (ymax - ymin + 1))][xmin +
                                                                                  int((j / N) * (xmax - xmin + 1))]
        return tmp
