import tkinter as tk
from tkinter import messagebox, filedialog
from statics.constants import *
from BusinessLogic.weights import *
from BusinessLogic.scaling import *
from BusinessLogic.perceptron import *


class Draw:
    def __init__(self):
        self.__pixel_matrix = [[0] * N for _ in range(N)]
        self.__root = tk.Tk()
        self.__root.title("Рисование пикселей")
        self.__weights = Weights()
        self.__perceptron = Perceptron()
        self.__setUI()

    def __setUI(self):
        # Создание холста для рисования
        self.canvas = tk.Canvas(self.__root, width=window_width, height=window_height, bg="white")
        self.canvas.pack()

        # Обработка движения мыши с зажатой ЛКМ
        self.canvas.bind("<B1-Motion>", self.__drawPixel)
        self.save_button = tk.Button(self.__root, text="Сохранить матрицу", command=self.__saveMatrixClick)
        self.save_button.pack()

        self.clear_button = tk.Button(self.__root, text="Очистить холст", command=self.__clearCanvasClick)
        self.clear_button.pack()

        self.random_weights_button = tk.Button(self.__root, text="Случайные веса", command=self.__weightsInitializeClick)
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

    def __drawPixel(self, event):
        x, y = event.x, event.y
        row, col = y // cell_height, x // cell_width
        if 0 <= row <= N - 1 and 0 <= col <= N - 1:
            self.__pixel_matrix[row][col] = 1
            self.canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width,
                                         (row + 1) * cell_height,
                                         fill="black")

    def __saveMatrixClick(self):
        with open("pixel_matrix.txt", "w") as file:
            for row in self.__pixel_matrix:
                file.write(" ".join(map(str, row)) + "\n")

    def __clearCanvasClick(self):
        self.canvas.delete("all")
        self.__pixel_matrix = [[0] * N for _ in range(N)]

    def __weightsInitializeClick(self):
        self.__weights.fillRandomValues()
        message = "Веса инициализированы случаным образом!"
        messagebox.showinfo("Диалоговое окно", message)

    def __saveWeightsClick(self):
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

    def __loadWeightsClick(self):
        file_dialog = filedialog.askopenfile(filetypes=[("Text Files", "*.txt")])
        if file_dialog:
            filename = file_dialog.name
            if self.__weights.loadWeights(filename):
                message = 'Веса загружены'
            else:
                message = 'Ошибка загрузки весов'
            messagebox.showinfo("Диалоговое окно", message)
            file_dialog.close()

    def __scaleImageClick(self):
        self.__pixel_matrix = Scaling.scalePixelMatrix(self.__pixel_matrix)
        self.canvas.delete("all")
        for row in range(N):
            for col in range(N):
                if self.__pixel_matrix[row][col] == 1:
                    self.canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width,
                                                 (row + 1) * cell_height,
                                                 fill="black")

    def __perceptronCheckClick(self):
        output = self.__perceptron.perceptronOutput(self.__pixel_matrix, self.__weights)
        output_text = "крестик" if output == 1 else "нолик"
        message = "Это {output_text}?".format(output_text=output_text)
        answer = messagebox.askquestion("Диалоговое окно", message)
        self.__perceptron.perceptronTrain(answer, output)

    @property
    def pixel_matrix(self):
        return self.__pixel_matrix
