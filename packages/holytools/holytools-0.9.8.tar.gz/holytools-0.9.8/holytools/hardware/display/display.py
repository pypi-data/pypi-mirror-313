from __future__ import annotations

from typing import Optional
from PIL import Image
from mss import mss
from screeninfo import get_monitors
from screeninfo import Monitor as BaseMonitor

from .grid_draw import EditableImage, PixelMapper
from .types import Grid, LatticePoint


# ----------------------------------------------


class Display(BaseMonitor):
    @classmethod
    def get_primary(cls) -> Optional[Display]:
        for monitor in get_monitors():
            if monitor.is_primary:
                return cls.from_base(base_monitor=monitor)
        return None

    @classmethod
    def get_secondary(cls) -> Optional[Display]:
        for monitor in get_monitors():
            if not monitor.is_primary:
                return cls.from_base(base_monitor=monitor)
        return None

    @classmethod
    def from_base(cls, base_monitor : BaseMonitor) -> Display:
        return cls(x=base_monitor.x, y=base_monitor.y, width=base_monitor.width, height=base_monitor.height, is_primary=base_monitor.is_primary)

    # ----------------------------------------------

    def get_screenshot(self, grid : Optional[Grid] = None):
        with mss() as sct:
            monitor_dict = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            sct_img = sct.grab(monitor_dict)
            img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        if grid:
            editable = EditableImage(img=img, mapper=self.get_mapper(grid=grid))
            img = editable.get_grid_overlay()

        return img

    def get_mapper(self, grid : Grid):
        pixel_grid = Grid(x_size=self.width, y_size=self.height)
        return PixelMapper(input_grid=grid, output_grid=pixel_grid)

    def to_virtual_display(self, pixel : LatticePoint) -> LatticePoint:
        origin = LatticePoint(x=self.x, y = self.y)
        return origin + pixel

    def in_bounds(self, pixel : LatticePoint):
        return 0 <= pixel.x <= self.width and 0 <= pixel.y <= self.height

    def is_horizontal(self):
        return self.width > self.height

    def is_vertical(self):
        return self.height > self.width
