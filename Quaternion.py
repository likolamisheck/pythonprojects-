#Task 2.1

import math

class Quaternion:
    def __init__(self, a, b, c, d):
        self.a = a  # Scalar part
        self.b = b  # i coefficient
        self.c = c  # j coefficient
        self.d = d  # k coefficient

    def __repr__(self):
        return f"{self.a} + {self.b}i + {self.c}j + {self.d}k"
    
    def __add__(self, other):
        return Quaternion(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)

    def __mul__(self, other):
        a = self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d
        b = self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c
        c = self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b
        d = self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a
        return Quaternion(a, b, c, d)

    def conjugate(self):
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def norm(self):
        norm = math.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)
        return Quaternion(self.a / norm, self.b / norm, self.c / norm, self.d / norm)


    def rotate_vector(self, vector):
        if len(vector) != 3:
            raise ValueError("Vector must have exactly 3 components")
        q_vec = Quaternion(0, *vector) # Chuyển vector thành quaternion (phần thực = 0)
        rotated = self * q_vec * self.conjugate() # Xoay vector: Q * Q_vector * Q_conjugate
        return [rotated.b, rotated.c, rotated.d] # Phần tưởng tượng của quaternion chứa vector đã xoay


def create_rotation_quaternion(theta, axis):
    
    if len(axis) != 3:
        raise ValueError("Vector must have exactly 3 components")
        
    # Chuẩn hóa trục xoay
    u_x, u_y, u_z = axis
    norm = math.sqrt(u_x**2 + u_y**2 + u_z**2)
    u_x, u_y, u_z = u_x / norm, u_y / norm, u_z / norm

    # Tính toán các thành phần của quaternion
    a = math.cos(theta / 2)
    b = math.sin(theta / 2) * u_x
    c = math.sin(theta / 2) * u_y
    d = math.sin(theta / 2) * u_z

    return Quaternion(a, b, c, d)

    
if __name__ == "__main__":
    # Tạo quaternion xoay 90 độ quanh trục z
    theta = math.pi / 2  # 90 độ
    axis = [0, 0, 1]     # Trục z
    rotation_quaternion = create_rotation_quaternion(theta, axis)

    # Vector ban đầu
    vector = [1, 0, 0]

    # Xoay vector
    rotated_vector = rotation_quaternion.rotate_vector(vector)
    print("vector after rotation:", rotated_vector)
