import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        """
        Инициализирует приложение для рисования.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создаем изображение и объект для рисования
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создаем холст
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Настройки кисти
        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        self.style_var = tk.StringVar()
        self.style_var.set('round')

        # Переменные для отслеживания состояния рисования
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.last_color = 'black'

        self.setup_ui()

        # Привязка событий
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-2>', self.pick_color)
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

        self.text_mode = False

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопки управления
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        self.color_preview = tk.Label(control_frame, text=" ", bg=self.pen_color, width=2, height=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 10))

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        brush_button = tk.Button(control_frame, text="Кисть", command=self.use_brush)
        brush_button.pack(side=tk.LEFT)

        text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        text_button.pack(side=tk.LEFT)

        bg_button = tk.Button(control_frame, text="Изменить фон", command=self.change_bg_color)
        bg_button.pack(side=tk.LEFT)

        style_label = tk.Label(control_frame, text="Стиль кисти:")
        style_label.pack(side=tk.LEFT, padx=(5, 2))

        style_menu = tk.OptionMenu(control_frame, self.style_var, 'round', 'butt', 'projecting')
        style_menu.pack(side=tk.LEFT)

        brush_size_label = tk.Label(control_frame, text="Размер кисти:")
        brush_size_label.pack(side=tk.LEFT, padx=(5, 2))

        brush_size_frame = tk.Frame(control_frame)
        brush_size_frame.pack(side=tk.LEFT)

        sizes = [1, 3, 5, 10]
        self.create_brush_size_menu(brush_size_frame, sizes)

    def create_brush_size_menu(self, parent, sizes):
        """
        Создает меню для выбора размера кисти.
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
        """
        self.brush_size.set(value)

    def paint(self, event):
        """
        Рисует линии при движении мыши с зажатой левой кнопкой.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=self.style_var.get(), smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает координаты последней точки.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), "white")
        self.draw = ImageDraw.Draw(self.image)

    def resize_canvas(self):
        """
        Изменяет размер холста.
        """
        new_width = simpledialog.askinteger("Размер холста", "Введите новую ширину (min=100, max=1800):", minvalue=100,
                                            maxvalue=1800)
        new_height = simpledialog.askinteger("Размер холста", "Введите новую высоту (min=100, max=900):", minvalue=90,
                                             maxvalue=900)

        self.canvas.config(width=new_width, height=new_height)
        self.image = Image.new("RGB", (new_width, new_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """
        Открывает диалоговое окно для выбора цвета.
        """
        color = colorchooser.askcolor(color=self.last_color)
        if color[1]:
            self.pen_color = color[1]
            self.last_color = self.pen_color
            self.update_color_preview()

    def use_eraser(self):
        """
        Включает режим ластика.
        """
        self.last_color = self.pen_color
        self.pen_color = 'white'
        self.update_color_preview()

    def use_brush(self):
        """
        Включает режим кисти.
        """
        self.pen_color = self.last_color
        self.last_color = self.pen_color
        self.update_color_preview()

    def save_image(self, event=None):
        """
        Сохраняет изображение в файл.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", f"Изображение успешно сохранено {file_path}")

    def rgb_to_hex(self, rgb):
        """
        Преобразует RGB в шестнадцатеричный код цвета.
        """
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def pick_color(self, event):
        """
        Выбирает цвет из пикселя на холсте.
        """
        if 0 <= event.x < self.image.width and 0 <= event.y < self.image.height:
            pixel_color = self.image.getpixel((event.x, event.y))
            self.pen_color = self.rgb_to_hex(pixel_color)
            self.last_color = self.pen_color
            self.update_color_preview()

    def update_color_preview(self):
        """
        Обновляет цвет предварительного просмотра.
        """
        self.color_preview.config(bg=self.pen_color)

    def add_text(self):
        """
        Добавляет текст на холст.
        """
        text = simpledialog.askstring("Ввод текста", "Введите текст:")
        if text:
            self.text_mode = True
            self.current_text = text
            self.canvas.bind('<Button-1>', self.place_text)

    def add_text(self, event):
        """
        Размещает введенный текст на холсте.
        """
        if self.text_mode:
            x, y = event.x, event.y
            self.canvas.create_text(x, y, text=self.current_text, fill=self.pen_color, anchor='nw')
            self.draw.text((x, y), self.current_text, fill=self.pen_color)
            self.text_mode = False
            self.canvas.unbind('<Button-1>')

    def change_bg_color(self):
        """
        Изменяет цвет фона холста.
        """
        color = colorchooser.askcolor(title="Выбрать цвет фона")
        if color[1]:
            self.canvas.config(bg=color[1])
            self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), color[1])
            self.draw = ImageDraw.Draw(self.image)


def main():
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
