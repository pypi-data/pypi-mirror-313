from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from PIL import ImageDraw, Image, ImageFont
from PIL.Image import Image as PILImage
from .types import Grid, LatticePoint, Vector


# ----------------------------------------------

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class EditableImage:
    def __init__(self, img : PILImage, mapper : PixelMapper):
        self.pil_image : PILImage = img.convert('RGBA')

        ImageDraw.Draw(self.pil_image)
        self.mapper : PixelMapper = mapper
        self.overlay = Image.new('RGBA', self.pil_image.size, (255, 255, 255, 0))
        self.overlay = self.overlay.convert('RGBA')
        self.overlay_draw = ImageDraw.Draw(self.overlay)


    def get_grid_overlay(self) -> PILImage:
        self.draw_cell_labels()
        self.draw_grid_lines()
        return Image.alpha_composite(self.pil_image, self.overlay)


    def draw_cell_labels(self):
        grid = self.mapper.input_grid
        for pt in grid.get_lattice_points():
            input_vector = pt.to_vector() + Vector(x=0.5, y=0.5)
            output_vector = self.mapper.map_vector(vector=input_vector)
            output_pt = output_vector.to_lattice()
            text = str(grid.get_num(pt=pt))
            self.draw_text(text=text, point=output_pt, font_size=int(400 / grid.x_size))


    def draw_grid_lines(self):
        for x in range(0, self.mapper.input_grid.x_size + 1):
            x_px = self.mapper.map_horizontal(x=x)
            self.draw_line(coordinate=x_px, orientation=Orientation.VERTICAL)
        for y in range(0, self.mapper.input_grid.y_size + 1):
            y_px = self.mapper.map_vertical(y=y)
            self.draw_line(coordinate=y_px, orientation=Orientation.HORIZONTAL)


    def draw_line(self, coordinate : int, orientation : Orientation, opacity=128):
        color_vector = (255,0,0, opacity)
        if orientation == Orientation.HORIZONTAL:
            start_pos = (0, coordinate)
            end_pos = (self.overlay.width, coordinate)
        else:
            start_pos = (coordinate, 0)
            end_pos = (coordinate, self.overlay.height)

        self.overlay_draw.line([start_pos, end_pos], fill=color_vector, width=1)


    def draw_text(self, text: str, point: LatticePoint, font_size=20, opacity=255):
        font = ImageFont.load_default(size=font_size)
        delta = LatticePoint(font_size // 2, font_size // 2)
        centered_point = point - delta

        background_color = self.pil_image.getpixel(centered_point.as_tuple())
        brightness = sum(background_color[:3]) / (3 * 255)
        if brightness < 0.5:
            color = (255, 255,255 , opacity)
        else:
            color = (0, 0, 0, opacity)
        self.overlay_draw.text(centered_point.as_tuple(), text=text, fill=color, font=font)


@dataclass
class PixelMapper:
    input_grid : Grid
    output_grid : Grid

    def map_vector(self, vector : Vector):
        if not self.input_grid.is_in_bounds(vec=vector):
            raise ValueError(f"Vector {vector} is outside of the grid bounds")

        return Vector(x=self.map_horizontal(vector.x), y=self.map_vertical(vector.y))

    def map_pt(self, point : LatticePoint) -> LatticePoint:
        if not self.input_grid.is_in_bounds(vec=point):
            raise ValueError(f"Lattice point {point} is outside of the grid bounds")
        return LatticePoint(x=self.map_horizontal(point.x), y=self.map_vertical(point.y))

    def map_horizontal(self, x : float) -> int:
        if not self.input_grid.in_horizontal_bounds(x=round(x)):
            raise ValueError(f"X value {x} is outside of the grid bounds")
        return round(x * self.output_grid.x_size / self.input_grid.x_size)

    def map_vertical(self, y : float) -> int:
        if not self.input_grid.is_in_vertical_bounds(y=round(y)):
            raise ValueError(f"Y value {y} is outside of the grid bounds")
        return round(y * self.output_grid.y_size / self.input_grid.y_size)
