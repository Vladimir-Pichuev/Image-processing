from PIL import Image, ImageDraw, ImageTk
from tkinter import Canvas, Tk, filedialog
from math import sqrt

# Глобальные переменные для хранения координат точки
image_height = None
image_width = None
get_image = None
selected_point = None


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


# (Функция из интернетa,
# в которой я конечно же не буду разбираться, описание ниже)
def tile(*images, vertical=False):
    """
Первый параметр в tile() использует оператор распаковки (*),
поэтому в качестве входных аргументов можно
использовать любое количество объектов типа PIL.Image.
Для параметра ключевого слова vertical можно установить значение True,
если вы хотите размещать изображения вертикально, а не горизонтально.
Эта функция предполагает, что все изображения имеют одинаковый размер.

Общий размер окончательного изображения рассчитывается исходя из размера
изображений и количества используемых изображений.
Затем вы создаете новый объект изображения с тем же режимом,
что и исходные изображения, и с размером общего экрана.

Цикл for вставляет изображения, которые вы вводите при вызове функции,
в окончательное изображение.
Функция возвращает окончательный объект Image,
содержащий все изображения рядом.

Изображение в данной статье, показывающее три цветовых режима для клубники,
было получено путем вызова функции tile() следующим образом:

strawberry_channels = tile(red_merge, green_merge, blue_merge)
Эта функция будет использоваться для создания всех изображений,
которые состоят из нескольких в текущем руководстве.
    """
    width, height = images[0].width, images[0].height
    tiled_size = (
        (width, height * len(images))
        if vertical
        else (width * len(images), height)
    )
    tiled_img = Image.new(images[0].mode, tiled_size)
    row, col = 0, 0
    for image in images:
        tiled_img.paste(image, (row, col))
        if vertical:
            col += height
        else:
            row += width

    return tiled_img


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


def create_circle(filename, selected_point):
    # Функция создания кружка, пока получается только квадрат
    # Круг тоже получился
    with Image.open(filename) as img:  # открываем файл
        # вырезаем объект с заданными координатами
        # cropped_image = img.crop(coordinates)
        draw = ImageDraw.Draw(img)
        # Получаем координаты из списка selected_point
        x1, y1 = selected_point[0]
        # Выбираем начальную точку вокруг которой рисовать
        x2, y2 = selected_point[1]
        # Вторая точка, необходима для определения радиуса
        radius = round(sqrt(((x1-x2)**2)+((y1-y2)**2)))
        draw.ellipse(
            (x1 - radius, y1 - radius, x1 + radius, y1 + radius)
        )
        # Рисование некоторой области с заданными координатами
        print(x1 - radius, y1 - radius, x1 + radius, y1 + radius)
        print(radius)
        mask = Image.new("L", img.size, 0)  # Создаем маску для
        # заливки черным цветом
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse(
            (x1 - radius, y1 - radius, x1 + radius, y1 + radius), fill=255
        )
        # Применяем маску к изображению
        masked_img = Image.new("RGBA", img.size)
        masked_img.paste(img, (0, 0), mask)
        # Обрезаем изображение с учетом маски
        cropped_image = masked_img.crop(
            (x1 - radius, y1 - radius, x1 + radius, y1 + radius)
        )
        # print(cropped_image.getbands())
        red, green, blue, alpha = cropped_image.split()
        # Разделим наше полученное обрезанное изображение
        # на красный, зеленый и голубой состовляющий
        print(alpha)
        red_pixels = 0
        green_pixels = 0
        blue_pixels = 0
        for x in range(cropped_image.width):
            for y in range(cropped_image.height):
                r, g, b, alpha = cropped_image.getpixel((x, y))
                red_pixels += r
                green_pixels += g
                blue_pixels += b
        zeroed_band = red.point(lambda _: 0)
        # выбираем все значения одного цвета и менеяем на 0
        red_merge = Image.merge("RGB", (red, zeroed_band, zeroed_band))
        green_merge = Image.merge("RGB", (zeroed_band, green, zeroed_band))
        blue_merge = Image.merge("RGB", (zeroed_band, zeroed_band, blue))
        cropped_image_show = tile(
            red_merge, green_merge, blue_merge, cropped_image
        )  # Объеденяем с помощью tile
        # все необходимые изображения
        print("Количество красных пикселей:", red_pixels)
        print("Количество зеленых пикселей:", green_pixels)
        print("Количество синих пикселей:", blue_pixels)
        cropped_image_show.show()


def main():
    choose_image_click()


if __name__ == "__main__":
    main()
