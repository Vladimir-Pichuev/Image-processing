from PIL import Image, ImageDraw
from math import sqrt

from tile import tile


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
