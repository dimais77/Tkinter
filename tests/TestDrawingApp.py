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

if __name__ == '__main__':
    unittest.main()
