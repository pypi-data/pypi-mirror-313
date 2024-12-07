import time

from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from holytools.hardware.display import Display, LatticePoint, Vector
from holytools.hardware.display import Grid
from typing import Optional

# ----------------------------------------------

class Mouse:
    def __init__(self):
        self._mouse : MouseController = MouseController()

    def click(self, pixel_x : int, pixel_y : int, on_primary_display: bool = True):
        point = LatticePoint(pixel_x, pixel_y)
        display = Display.get_primary() if on_primary_display else Display.get_secondary()
        if not display.in_bounds(point):
            raise ValueError(f"Point {point} is outside of the display bounds")
        rel_to_primary = display.to_virtual_display(pixel=point)

        self._mouse.position = (rel_to_primary.x, rel_to_primary.y)
        self._mouse.click(Button.left, 1)

class TextMouse:
    def __init__(self, input_grid: Grid = Grid(x_size=25, y_size=25)):
        self.mouse : Mouse = Mouse()
        self.input_grid : Grid = input_grid
        self.primary : Display = Display.get_primary()
        self.secondary : Optional[Display] = Display.get_secondary()

    def get_view(self, on_primary_display : bool = True):
        display = self.primary if on_primary_display else self.secondary
        return display.get_screenshot(grid=self.input_grid)

    def click(self, cell_num : int, on_primary_display : bool = True):
        left_corner = self.input_grid.get_pt(num=cell_num).to_vector()
        center = left_corner + Vector(0.5,0.5)

        display = self.primary if on_primary_display else self.secondary
        if not display:
            raise ValueError("There is no secondary display")

        mapper = display.get_mapper(grid=self.input_grid)
        center = mapper.map_vector(center).to_lattice()
        self.mouse.click(center.x, center.y, on_primary_display=on_primary_display)


if __name__ == "__main__":
    text_mouse = TextMouse()
    while True:
        view = text_mouse.get_view()
        view.show()
        num = int(input(f'Click on cell:'))
        text_mouse.click(num)
        time.sleep(1)
        
        
