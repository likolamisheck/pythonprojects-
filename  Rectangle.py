class Rectangle:
    """
    A class representing a rectangle with independent width and height.
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
            raise ValueError("Width must be a positive number.")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be a positive number.")
        self._height = value

    def area(self):
        return self._width * self._height

    def __str__(self):
        return f"Rectangle(width={self._width}, height={self._height})"


class Square:
    """
    A class representing a square where width and height are always equal.
    """
    def __init__(self, side_length):
        self._side_length = side_length

    @property
    def side_length(self):
        return self._side_length

    @side_length.setter
    def side_length(self, value):
        if value <= 0:
            raise ValueError("Side length must be a positive number.")
        self._side_length = value

    def area(self):
        return self._side_length ** 2

    def __str__(self):
        return f"Square(side_length={self._side_length})"


# TESTING THE CLASSES
if __name__ == "__main__":
    # Testing Rectangle
    rectangle = Rectangle(4, 5)
    print(rectangle)  # Rectangle(width=4, height=5)
    print(f"Area of rectangle: {rectangle.area()}")  # Area of rectangle: 20

    # Testing Square
    square = Square(4)
    print(square)  # Square(side_length=4)
    print(f"Area of square: {square.area()}")  # Area of square: 16

    # Modifying dimensions
    rectangle.width = 6
    rectangle.height = 7
    print(rectangle)  # Rectangle(width=6, height=7)
    print(f"New area of rectangle: {rectangle.area()}")  # New area of rectangle: 42

    square.side_length = 5
    print(square)  # Square(side_length=5)
    print(f"New area of square: {square.area()}")  # New area of square: 25
