from PIL import Image, ImageTk
from tkinter import Canvas, Tk, filedialog

from create_circle import create_circle


# Глобальные переменные для хранения координат точки
get_image = None
selected_point = None
image_height = None
image_width = None


def process_image(filename):
    global image_height, image_width
    # Загрузка изображения
    with Image.open(filename) as img:
        img.load()
        print(
            f'Размер изображения: {img.size}. '
            f'Формат: {img.format}. Тип изображения: {img.mode}'
        )
        # Определение ширины и высоты изображения
        image_width, image_height = img.size
        # Масштабирование изображения до размеров окна
        img.thumbnail((image_width, image_height))
        # Сохраняем как типа PIL.ImageTk.PhotoImage.
        # Это специфический тип данных из библиотеки Pillow (PIL),
        # который используется для хранения изображений,
        # готовых к отображению в графическом интерфейсе Tkinter.
        get_image = ImageTk.PhotoImage(img)
    return (get_image)  # Возвращаем этот объект


def choose_image_click():
    global image_width, image_height
    root = Tk()  # Создание корневого объкта - окна
    # root.withdraw()  # Скрыть основное окно Tkinter
    root.title('Выбор изображения')  # Устанавливаем заголовок окна
    # Открыть диалоговое окно для выбора файла
    filename = filedialog.askopenfilename()
    if filename:
        img = process_image(filename)  # Выполняем функцию
        root.geometry(f'{image_width}x{image_height}')  # Установка размеров
        # root.attributes("-fullscreen", True)  # Это можно использовать позже,
        # чтобы изображение вытягивалось на весь экран
        # и была возможность не подстраивать размер окна
        # а сразу выбирать 2 точки
        root.maxsize(1024, 768)  # Опционально установлен максимальный размер
        # потому что у меня разъебало на весь экран это всплывающее
        # ебучее окно что пришлось перезапускать программу
        root.update_idletasks()
        # Необходимо чтобы до метода mainloop применился размер окна
        canvas = Canvas(root, width=image_width, height=image_height)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=img)
        # root.after(100, on_image_click, img)
        # Создаем список для хранения выбранных точек
        selected_point = []

        def on_image_click(event):
            # Получение координат щелчка мыши
            x = event.x
            y = event.y
            # Запоминание выбранной точки
            selected_point.append((x, y))
            if len(selected_point) == 2:
                root.quit()
                # coordinates = tuple(
                #   [coord for point in selected_point for coord in point]
                # )  # преобразование кортежа в систему координат, используемую
                # в функции crop
                print("Выбранные точки:", selected_point)
            create_circle(filename, selected_point)  # Выполнение функции по
            # вырезанию объекта
            # create_circle(filename, coordinates)  # Выполнение функции по
            # вырезанию объекта
            return selected_point
        # Тыкаем и получаем координаты
        canvas.bind("<Button-1>", on_image_click)

        root.mainloop()


def main():
    choose_image_click()


if __name__ == "__main__":
    main()
