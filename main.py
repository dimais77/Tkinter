import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.brush_size_scale = None
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)  # установка начального размера кисти

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        brush_size_label = tk.Label(control_frame, text="Размер кисти:")
        brush_size_label.pack(side=tk.LEFT, padx=(10, 2))

        brush_size_frame = tk.Frame(control_frame)
        brush_size_frame.pack(side=tk.LEFT)

        sizes = [1, 3, 5, 10]
        self.create_brush_size_menu(brush_size_frame, sizes)

    def create_brush_size_menu(self, parent, sizes):
        size_menu = tk.OptionMenu(parent, self.brush_size, *sizes, command=self.update_brush_size)
        size_menu.pack(side=tk.LEFT)

        tk.Label(parent, text="   ").pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(parent, from_=1, to=10, orient=tk.HORIZONTAL,
                                         variable=self.brush_size, length=100,
                                         command=self.update_brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

    def update_brush_size(self, value):
        self.brush_size.set(value)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", f"Изображение успешно сохранено {file_path}")


def main():
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
