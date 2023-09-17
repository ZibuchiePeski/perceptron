import tkinter as tk
from tkinter import messagebox, filedialog

from BusinessLogic.perceptron import *
from statics.constants import *


class Draw:
    """Класс для realtime рисования и отображения UI"""
    def __init__(self):
        self.__pixel_matrix = [[0] * N for _ in range(N)]
        self.__root = tk.Tk()
        self.__root.title("Рисование пикселей")
        self.__weights = Weights()
        self.__perceptron = Perceptron()
        self.__setUI()

    def __setUI(self) -> None:
        """Отрисовка каркаса экрана"""
        # Создание холста для рисования
        self.canvas = tk.Canvas(self.__root, width=window_width, height=window_height, bg="white")
        self.canvas.pack()

        # Обработка движения мыши с зажатой ЛКМ
        self.canvas.bind("<B1-Motion>", self.__drawPixel)

        self.clear_button = tk.Button(self.__root, text="Очистить холст", command=self.__clearCanvasClick)
        self.clear_button.pack()

        self.random_weights_button = tk.Button(self.__root, text="Случайные веса", command=self.__RandomWeightsClick)
        self.random_weights_button.pack()

        self.save_button = tk.Button(self.__root, text="Сохранить веса", command=self.__saveWeightsClick)
        self.save_button.pack()

        self.load_button = tk.Button(self.__root, text="Загрузить веса", command=self.__loadWeightsClick)
        self.load_button.pack()

        self.scale_button = tk.Button(self.__root, text="Масштабировать изображение", command=self.__scaleImageClick)
        self.scale_button.pack()

        self.perceptron_check_button = tk.Button(self.__root, text="Проверить", command=self.__perceptronCheckClick)
        self.perceptron_check_button.pack()

        self.__root.mainloop()

    def __drawPixel(self, event) -> None:
        """Метод отрисовки пикселей"""
        x, y = event.x, event.y
        row, col = y // cell_height, x // cell_width
        if 0 <= row <= N - 1 and 0 <= col <= N - 1:
            self.__pixel_matrix[row][col] = 1
            self.canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width,
                                         (row + 1) * cell_height,
                                         fill="black")

    def __clearCanvasClick(self) -> None:
        """Действие очистки области рисования"""
        self.canvas.delete("all")
        self.__pixel_matrix = [[0] * N for _ in range(N)]

    def __RandomWeightsClick(self) -> None:
        """Расчет матрицы случайных весов с значениями из [-0.3;0.3]"""
        self.__weights.fillRandomValues()
        message = "Веса инициализированы случаным образом!"
        messagebox.showinfo("Диалоговое окно", message)

    def __saveWeightsClick(self) -> None:
        """Действие сохранения весов в файл через системный обозреватель"""
        file_dialog = filedialog.asksaveasfile(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt")])
        if file_dialog:
            filename = file_dialog.name
            if self.__weights.saveWeights(filename):
                message = 'Веса сохранены'
            else:
                message = 'Веса не сохранены'
            messagebox.showinfo("Диалоговое окно", message)
            file_dialog.close()

    def __loadWeightsClick(self) -> None:
        """Действие выгрузки весов из файла через системный обозреватель"""
        file_dialog = filedialog.askopenfile(filetypes=[("Text Files", "*.txt")])
        if file_dialog:
            filename = file_dialog.name
            if self.__weights.loadWeights(filename):
                message = 'Веса загружены'
            else:
                message = 'Ошибка загрузки весов'
            messagebox.showinfo("Диалоговое окно", message)
            file_dialog.close()

    def __scaleImageClick(self) -> None:
        """Действие динамического масштабирвоания полотна"""
        self.__pixel_matrix = Scaling.scalePixelMatrix(self.__pixel_matrix)
        self.canvas.delete("all")
        for row in range(N):
            for col in range(N):
                if self.__pixel_matrix[row][col] == 1:
                    self.canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width,
                                                 (row + 1) * cell_height,
                                                 fill="black")

    def __perceptronCheckClick(self) -> None:
        """Действие работы с перцептроном"""
        output = self.__perceptron.perceptronOutput(self.__pixel_matrix, self.__weights)
        output_text = "крестик" if output == 1 else "нолик"
        message = "Это {output_text}?".format(output_text=output_text)
        answer = messagebox.askquestion("Диалоговое окно", message)
        self.__perceptron.perceptronTrain(answer, output)

