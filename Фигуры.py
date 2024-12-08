#Task 2.3 About shapes

class Rectangle:
    """
    A class to represent a rectangle.
    Attributes:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.
    """
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive.")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive.")
        self._height = value

    def area(self):
        """Calculates the area of the rectangle."""
        return self.width * self.height


class Square:
    """
    A class to represent a square. It does not inherit from Rectangle to maintain Liskov substitution principle.
    Attributes:
        side (float): The side length of the square.
    """
    def __init__(self, side):
        self._side = side

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value <= 0:
            raise ValueError("Side length must be positive.")
        self._side = value

    @property
    def width(self):
        return self._side

    @width.setter
    def width(self, value):
        self.side = value

    @property
    def height(self):
        return self._side

    @height.setter
    def height(self, value):
        self.side = value

    def area(self):
        """Calculates the area of the square."""
        return self.side ** 2

# Example Usage
rectangle = Rectangle(5, 10)
print("Rectangle area:", rectangle.area())

square = Square(4)
print("Square area:", square.area())

# Updating dimensions
rectangle.width = 7
square.side = 5

print("Updated Rectangle area:", rectangle.area())
print("Updated Square area:", square.area())




