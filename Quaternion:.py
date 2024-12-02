class Quaternion:
    def __init__(self, w, x, y, z):
        """
        Initialize a quaternion with components w, x, y, z.
        """
        self.w, self.x, self.y, self.z = w, x, y, z

    def __repr__(self):
        """
        String representation of the quaternion.
        """
        return f"{self.w} + {self.x}i + {self.y}j + {self.z}k"

    def conjugate(self):
        """
        Compute the conjugate of the quaternion.
        :return: A new Quaternion object.
        """
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def magnitude(self):
        """
        Compute the magnitude of the quaternion.
        :return: The magnitude as a float.
        """
        return (self.w**2 + self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __add__(self, other):
        """
        Add two quaternions.
        """
        return Quaternion(
            self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z
        )

    def __sub__(self, other):
        """
        Subtract one quaternion from another.
        """
        return Quaternion(
            self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z
        )

    def __mul__(self, other):
        """
        Multiply two quaternions.
        Formula: q1 * q2 = (w1w2 - x1x2 - y1y2 - z1z2) 
                         + (w1x2 + x1w2 + y1z2 - z1y2)i
                         + (w1y2 - x1z2 + y1w2 + z1x2)j
                         + (w1z2 + x1y2 - y1x2 + z1w2)k
        """
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    def __truediv__(self, other):
        """
        Divide one quaternion by another (q1 / q2).
        Division: q1 * q2^-1 (multiplying by the inverse of q2).
        """
        conjugate = other.conjugate()
        denominator = other.magnitude()**2
        numerator = self * conjugate
        return Quaternion(
            numerator.w / denominator,
            numerator.x / denominator,
            numerator.y / denominator,
            numerator.z / denominator,
        )


# TESTING THE QUATERNION CLASS
if __name__ == "__main__":
    # Define two quaternions
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(0, -1, 2, -3)

    print("Quaternion 1:", q1)
    print("Quaternion 2:", q2)

    # Conjugate
    print("\nConjugate of q1:", q1.conjugate())

    # Magnitude
    print("Magnitude of q1:", q1.magnitude())

    # Addition
    print("\nAddition (q1 + q2):", q1 + q2)

    # Subtraction
    print("Subtraction (q1 - q2):", q1 - q2)

    # Multiplication
    print("Multiplication (q1 * q2):", q1 * q2)

    # Division
    print("Division (q1 / q2):", q1 / q2)
class Quaternion:
    def __init__(self, w, x, y, z):
        """
        Initialize a quaternion with components w, x, y, z.
        """
        self.w, self.x, self.y, self.z = w, x, y, z

    def __repr__(self):
        """
        String representation of the quaternion.
        """
        return f"{self.w} + {self.x}i + {self.y}j + {self.z}k"

    def conjugate(self):
        """
        Compute the conjugate of the quaternion.
        :return: A new Quaternion object.
        """
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def magnitude(self):
        """
        Compute the magnitude of the quaternion.
        :return: The magnitude as a float.
        """
        return (self.w**2 + self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __add__(self, other):
        """
        Add two quaternions.
        """
        return Quaternion(
            self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z
        )

    def __sub__(self, other):
        """
        Subtract one quaternion from another.
        """
        return Quaternion(
            self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z
        )

    def __mul__(self, other):
        """
        Multiply two quaternions.
        Formula: q1 * q2 = (w1w2 - x1x2 - y1y2 - z1z2) 
                         + (w1x2 + x1w2 + y1z2 - z1y2)i
                         + (w1y2 - x1z2 + y1w2 + z1x2)j
                         + (w1z2 + x1y2 - y1x2 + z1w2)k
        """
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    def __truediv__(self, other):
        """
        Divide one quaternion by another (q1 / q2).
        Division: q1 * q2^-1 (multiplying by the inverse of q2).
        """
        conjugate = other.conjugate()
        denominator = other.magnitude()**2
        numerator = self * conjugate
        return Quaternion(
            numerator.w / denominator,
            numerator.x / denominator,
            numerator.y / denominator,
            numerator.z / denominator,
        )


# TESTING THE QUATERNION CLASS
if __name__ == "__main__":
    # Define two quaternions
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(0, -1, 2, -3)

    print("Quaternion 1:", q1)
    print("Quaternion 2:", q2)

    # Conjugate
    print("\nConjugate of q1:", q1.conjugate())

    # Magnitude
    print("Magnitude of q1:", q1.magnitude())

    # Addition
    print("\nAddition (q1 + q2):", q1 + q2)

    # Subtraction
    print("Subtraction (q1 - q2):", q1 - q2)

    # Multiplication
    print("Multiplication (q1 * q2):", q1 * q2)

    # Division
    print("Division (q1 / q2):", q1 / q2)
