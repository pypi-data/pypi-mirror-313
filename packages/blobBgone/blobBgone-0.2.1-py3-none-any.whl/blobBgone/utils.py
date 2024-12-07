from __future__ import division
import tkinter as tk
from tkinter import filedialog

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    def norm(self):
        return self.dot(self)**0.5
    def normalized(self):
        norm = self.norm()
        return Vector(self.x / norm, self.y / norm)
    def perp(self):
        return Vector(1, -self.x / self.y)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    def __str__(self):
        return f'({self.x}, {self.y})'

class Helper():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def generate_perpendicular_vector(P1, P2, scale=1, direction='left'):
        A = Vector(*P1)
        B = Vector(*P2)
        AB = B - A  
        AB_perp_normed = AB.perp().normalized()
        if direction == 'left':
            P1 = B + AB_perp_normed * scale - AB
            P2 = B - AB_perp_normed * scale - AB
        elif direction == "center":
            P1 = B + AB_perp_normed * scale - AB/2
            P2 = B - AB_perp_normed * scale - AB/2
        elif direction == 'right':
            P1 = B + AB_perp_normed * scale
            P2 = B - AB_perp_normed * scale 
        return P1, P2

class pyDialogue():
    
    @staticmethod
    def askDIR():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        DIR_path = filedialog.askdirectory()
        return DIR_path

    @staticmethod
    def askFILE():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        FILE_path = filedialog.askopenfilename()
        return FILE_path

    @staticmethod
    def askFILES():
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        FILE_path = filedialog.askopenfilenames()
        return FILE_path
    
