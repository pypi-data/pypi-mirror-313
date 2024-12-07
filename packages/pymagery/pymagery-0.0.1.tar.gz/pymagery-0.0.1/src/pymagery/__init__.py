import random
from PIL import Image
import os
from pyperclip import copy

def clamp(val, min, max):
    if val > max:
        return max
    elif val < min:
        return min
    else:
        return val

class map:
    def __init__(self, width, height, colormode: str = "RGBA"):
        self.width = width
        self.height = height
        self.color_mode = colormode
        self.pixels = {}
        for y in range(height):
            row = {}
            for x in range(width):
                row[x] = (0, 0, 0, 255)  # Default to opaque black
            self.pixels[y] = row

    def set_pixel(self, x: int, y: int, color: tuple):
        x = int(x)
        y = int(y)
        
        if self.color_mode == "RGBA":
            r = int(clamp(color[0], 0, 255))
            g = int(clamp(color[1], 0, 255))
            b = int(clamp(color[2], 0, 255))
            a = int(clamp(color[3], 0, 255)) if len(color) == 4 else 255
            color = (r, g, b, a)
        
        if (x < 0 or x >= self.width) or (y < 0 or y >= self.height):
            raise ValueError(f"The position {x}/{y} cannot be written onto the map.")
        else:
            self.pixels[y][x] = color

    def get_pixel(self, x, y):
        if (x < 0 or x >= self.width) or (y < 0 or y >= self.height):
            raise ValueError("The position provided is not on the map.")
        else:
            return self.pixels[y][x]

    def resize(self, width: int, height: int, blur: bool=False):
        if self.width == 0 or self.height == 0:
            raise ValueError("Original image has no size.")
        
        row_factor = self.height / height
        col_factor = self.width / width
        _new_image_dict = {}

        for i in range(height):
            _new_image_dict[i] = {}
            for j in range(width):
                orig_i = int(i * row_factor)
                orig_j = int(j * col_factor)
                _new_image_dict[i][j] = self.pixels[orig_i][orig_j]

        self.pixels = _new_image_dict
        self.width = width
        self.height = height
    
    def write_to_file(self, path: str = "exported_map.png"):
        _image = Image.new(self.color_mode, (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                _image.putpixel((x, y), self.pixels[y][x])
        
        _path = ""
        for item in path.split("/")[0:-1]:
            _path += item
            _path += "/"
        try:
            os.makedirs(_path, exist_ok=True)
        except:
            pass
        
        _image.save(path) 

    def combine_with(self, other: map, occupancy: float = 1):
        other.resize(self.width, self.height)
        
        _data = map(self.width, self.height)
        
        for y in range(self.height):
            for x in range(self.width):
                r = self.get_pixel(x, y)[0] + (other.get_pixel(x, y)[0] * occupancy)
                r /= 1 + occupancy
                r = int(r)
                g = self.get_pixel(x, y)[1] + (other.get_pixel(x, y)[1] * occupancy)
                g /= 1 + occupancy
                g = int(g)
                b = self.get_pixel(x, y)[2] + (other.get_pixel(x, y)[2] * occupancy)
                b /= 1 + occupancy
                b = int(b)
                a = self.get_pixel(x, y)[3] + (other.get_pixel(x, y)[3] * occupancy)
                a /= 1 + occupancy
                a = int(a)
                _data.set_pixel(x, y, (r, g, b, a))
        
        self.pixels = _data.pixels
    
    def modify(self, mod):
        for x in range(self.width):
            for y in range(self.height):
                val1 = self.get_pixel(x, y)[0] + mod
                val2 = self.get_pixel(x, y)[1] + mod
                val3 = self.get_pixel(x, y)[2] + mod
                self.set_pixel(x, y, (val1, val2, val3, self.get_pixel(x, y)[3]))

    def remove_color(self, color: tuple):
        """
        Remove a specific color from the map by making it transparent.

        :param color: A tuple containing the RGB color to remove. For example (255, 255, 255).
        :return: None
        """
        if self.color_mode != "RGBA":
            print("Warning! RGBA must be used to use transparency")

        for y in range(self.height):
            for x in range(self.width):
                if self.get_pixel(x, y)[:3] == color:
                    self.set_pixel(x, y, (color[0], color[1], color[2], 0))  # Set alpha to 0 for transparency
class colormap:
    def __init__(self):
        self.colors = {}
        for i in range(0,256):
            self.colors[i] = gray(i)
            
    def value(self, input_value = int):
        val = int(input_value)
        val = clamp(val, 0, 255)
        return self.colors[val]
    
    def gradient(self, val_from, val_to, color_start, color_end):
        dV = val_from - val_to
        
        dR = color_start[0]-color_end[0]
        dG = color_start[1]-color_end[1]
        dB = color_start[2]-color_end[2]
        
        i=0
        for val in range(val_from, val_to):
            self.colors[val] = (color_start[0]+(dR*(i/dV)), color_start[1]+(dG*(i/dV)), color_start[2]+(dB*(i/dV)))
            i+=1

    def import_gradient(self, colors: dict):
        prev_key = 0
        last_color = (0,0,0)
        for key in colors:
            self.gradient(prev_key,int(key),last_color,colors[key])
            last_color = colors[key]
            prev_key = int(key)

def gray(val):
    return (val, val, val)


