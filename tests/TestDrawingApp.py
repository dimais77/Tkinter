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
        event = MagicMock(x=100, y=200)
        self.app.last_x, self.app.last_y = 50, 60
        self.app.paint(event)
        self.assertEqual(self.app.last_x, 100)
        self.assertEqual(self.app.last_y, 200)

    def test_reset(self):
        self.app.last_x, self.app.last_y = 50, 60
        self.app.reset(None)
        self.assertIsNone(self.app.last_x)
        self.assertIsNone(self.app.last_y)

    def test_use_eraser(self):
        self.app.pen_color = 'black'
        self.app.use_eraser()
        self.assertEqual(self.app.pen_color, 'white')

    def test_use_brush(self):
        self.app.pen_color = 'black'
        self.app.last_color = 'red'
        self.app.use_brush()
        self.assertEqual(self.app.pen_color, 'red')
        self.assertEqual(self.app.last_color, 'red')

    def test_update_brush_size(self):
        self.app.brush_size.set(5)
        self.app.update_brush_size(10)
        self.assertEqual(self.app.brush_size.get(), 10)

    def test_update_color_preview(self):
        self.app.pen_color = 'blue'
        self.app.update_color_preview()
        self.assertEqual(self.app.color_preview.cget('bg'), 'blue')

    def test_resize_canvas(self):
        with patch('tkinter.simpledialog.askinteger', side_effect=[800, 600]):
            self.app.resize_canvas()
        self.assertEqual(int(self.app.canvas.cget('width')), 800)
        self.assertEqual(int(self.app.canvas.cget('height')), 600)
        self.assertEqual(self.app.image.size, (800, 600))

    def test_style_menu(self):
        self.app.style_var.set('butt')
        self.assertEqual(self.app.style_var.get(), 'butt')

    @patch('main.DrawingApp.rgb_to_hex', return_value='#ffffff')
    def test_pick_color(self, mock_rgb_to_hex):
        event = MagicMock(x=10, y=10)
        self.app.image.getpixel = MagicMock(return_value=(255, 255, 255))
        self.app.pick_color(event)
        self.assertEqual(self.app.pen_color, '#ffffff')
        self.assertEqual(self.app.last_color, '#ffffff')
        self.assertEqual(self.app.color_preview.cget('bg'), '#ffffff')


if __name__ == '__main__':
    unittest.main()
