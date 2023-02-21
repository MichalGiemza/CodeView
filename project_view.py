import wx


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False

    def contains_point(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class Canvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.rectangles = []
        self.dragging = False
        self.drag_start_pos = None
        self.selected_rectangle = None

        self.add_rectangle(50, 50, 100, 75)
        self.add_rectangle(200, 100, 75, 75)
        self.add_rectangle(150, 200, 50, 100)

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen('black', 2))
        for rectangle in self.rectangles:
            if rectangle.selected:
                dc.SetBrush(wx.Brush('red'))
            else:
                dc.SetBrush(wx.Brush('blue'))
            dc.DrawRectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        for i in range(len(self.rectangles)):
            for j in range(i+1, len(self.rectangles)):
                rect1 = self.rectangles[i]
                rect2 = self.rectangles[j]
                if self.is_connected(rect1, rect2):
                    dc.DrawLine(int(rect1.x + rect1.width/2), int(rect1.y + rect1.height/2), int(rect2.x + rect2.width/2), int(rect2.y + rect2.height/2))

    def is_connected(self, rect1, rect2):
        if rect1 is rect2:
            return False
        return (rect1.x <= rect2.x + rect2.width and rect1.x + rect1.width >= rect2.x and
                rect1.y <= rect2.y + rect2.height and rect1.y + rect1.height >= rect2.y)

    def on_left_down(self, event):
        x, y = event.GetPosition()
        for rectangle in reversed(self.rectangles):
            if rectangle.contains_point(x, y):
                self.selected_rectangle = rectangle
                self.dragging = True
                self.drag_start_pos = (x, y)
                break

    def on_left_up(self, event):
        self.dragging = False

    def on_motion(self, event):
        if self.dragging:
            dx, dy = event.GetPosition() - self.drag_start_pos
            self.selected_rectangle.x += dx
            self.selected_rectangle.y += dy
            self.drag_start_pos = event.GetPosition()
            self.Refresh()

    def add_rectangle(self, x, y, width, height):
        self.rectangles.append(Rectangle(x, y, width, height))
        self.Refresh()


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Rectangles on Canvas')
        self.canvas = Canvas(self)
        self.SetClientSize((800, 600))
        self.Show()


def setup_editor(project_dir: str):
    app = wx.App()
    MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    setup_editor("C:\\Projekty\\LushLandsGithub\\LushLands\\")
