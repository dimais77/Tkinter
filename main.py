import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        """
        Инициализирует приложение для рисования.

        Параметры:
            root (tk.Tk): Корневой виджет Tkinter.
        """
        self.brush_size_scale = None
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.last_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-2>',
                         self.pick_color)  # На MacOS <Button-3> (правая кнопка мыши/трекпада) не срабатывает,
        # заменил на <Button-2> - особенность MacOS

    def setup_ui(self):
        """
        Настраивает интерфейс приложения.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        brush_button = tk.Button(control_frame, text="Кисть", command=self.use_brush)
        brush_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        brush_size_label = tk.Label(control_frame, text="Размер кисти:")
        brush_size_label.pack(side=tk.LEFT, padx=(10, 2))

        brush_size_frame = tk.Frame(control_frame)
        brush_size_frame.pack(side=tk.LEFT)

        sizes = [1, 3, 5, 10]
        self.create_brush_size_menu(brush_size_frame, sizes)

    def create_brush_size_menu(self, parent, sizes):
        """
        Создает меню выбора размера кисти.

        Параметры:
            parent (tk.Frame): Родительский фрейм для размещения меню.
            sizes (list): Список размеров кисти.
        """
        size_menu = tk.OptionMenu(parent, self.brush_size, *sizes, command=self.update_brush_size)
        size_menu.pack(side=tk.LEFT)

        tk.Label(parent, text="   ").pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(parent, from_=1, to=10, orient=tk.HORIZONTAL,
                                         variable=self.brush_size, length=100,
                                         command=self.update_brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

    def update_brush_size(self, value):
        """
        Обновляет размер кисти.

        Параметры:
            value: Новое значение размера кисти.
        """
        self.brush_size.set(value)

    def paint(self, event):
        """
        Рисует на холсте при движении мыши.

        Параметры:
            event: Событие мыши.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает последние координаты.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Позволяет выбрать цвет кисти.
        """
        color = colorchooser.askcolor(color=self.last_color)
        if color[1]:
            self.pen_color = color[1]
            self.last_color = self.pen_color

    def use_eraser(self):
        """
        Переключает режим на ластика.
        """
        self.last_color = self.pen_color
        self.pen_color = 'white'

    def use_brush(self):
        """
        Переключает режим на кисть.
        """
        self.pen_color = self.last_color
        self.last_color = self.pen_color

    def save_image(self):
        """
        Сохраняет изображение в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", f"Изображение успешно сохранено {file_path}")

    def rgb_to_hex(self, rgb):
        """Преобразует кортеж RGB в шестнадцатеричный код цвета."""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def pick_color(self, event):
        """
        Извлекает цвет пикселя в месте клика правой кнопкой мыши и устанавливает его в качестве текущего цвета кисти.
        Параметры:
            event: Событие мыши.
        """
        if 0 <= event.x < self.image.width and 0 <= event.y < self.image.height:
            pixel_color = self.image.getpixel((event.x, event.y))
            self.pen_color = self.rgb_to_hex(pixel_color)  # Преобразование в шестнадцатеричный цвет
            self.last_color = self.pen_color  # Обновляем последний выбранный цвет


def main():
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
