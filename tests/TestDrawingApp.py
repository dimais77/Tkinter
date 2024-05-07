import unittest
from tkinter import Tk
from unittest.mock import MagicMock, patch
from main import DrawingApp

class TestDrawingApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = DrawingApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_clear_canvas(self):
        self.app.canvas.delete = MagicMock()
        self.app.clear_canvas()
        self.app.canvas.delete.assert_called_once_with("all")

    def test_choose_color(self):
        self.app.pen_color = 'black'
        with patch('tkinter.colorchooser.askcolor', return_value=(None, 'black')):
            self.app.choose_color()
        self.assertEqual(self.app.pen_color, 'black')

    @patch('tkinter.filedialog.asksaveasfilename', return_value="test.png")
    @patch('tkinter.messagebox.showinfo')
    def test_save_image(self, mock_showinfo, mock_asksaveasfilename):
        self.app.image.save = MagicMock()
        self.app.save_image()
        self.app.image.save.assert_called_once_with("test.png")
        mock_showinfo.assert_called_once()

    @patch('tkinter.filedialog.asksaveasfilename', return_value="test.jpg")
    @patch('tkinter.messagebox.showinfo')
    def test_save_image_with_extension(self, mock_showinfo, mock_asksaveasfilename):
        self.app.image.save = MagicMock()
        self.app.save_image()
        self.app.image.save.assert_called_once_with("test.jpg.png")
        mock_showinfo.assert_called_once()

    def test_paint(self):
        # Проверяем, что при вызове paint последние координаты корректно обновляются
        event = MagicMock(x=100, y=200)
        self.app.last_x, self.app.last_y = 50, 60
        self.app.paint(event)
        self.assertEqual(self.app.last_x, 100)
        self.assertEqual(self.app.last_y, 200)

    def test_reset(self):
        # Проверяем, что при вызове reset последние координаты сбрасываются
        self.app.last_x, self.app.last_y = 50, 60
        self.app.reset(None)
        self.assertIsNone(self.app.last_x)
        self.assertIsNone(self.app.last_y)

    def test_use_eraser(self):
        # Проверяем, что при вызове use_eraser цвет кисти становится белым
        self.app.pen_color = 'black'
        self.app.use_eraser()
        self.assertEqual(self.app.pen_color, 'white')

    def test_use_brush(self):
        # Проверяем, что при вызове use_brush цвет кисти возвращается к предыдущему цвету
        self.app.pen_color = 'black'
        self.app.last_color = 'red'
        self.app.use_brush()
        self.assertEqual(self.app.pen_color, 'red')
        self.assertEqual(self.app.last_color, 'red')

if __name__ == '__main__':
    unittest.main()
