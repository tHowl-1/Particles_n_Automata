"""Basic 3D Rendering using olc 3d graphics tutorial"""
from __future__ import annotations

from blanksim import BlankSimulation

from math import sqrt, sin, cos, tan, pi
import numpy as np
from typing import Tuple
from copy import deepcopy

from tcod import console, los

WIDTH, HEIGHT = 512, 288

class Vec3:
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z

class Tri:
    def __init__(
        self, 
        points: list[Vec3, Vec3, Vec3]
    ) -> None:
        self.points = points

class Mesh:
    def __init__(
        self,
        tris: list
    ) -> None:
        self.tris = tris

class Mat4x4:
    def __init__(
        self
    ) -> None:
        self.matrix = np.full(
            (4, 4), fill_value = 0.0, dtype = float
        )

def multiply_matrix_vector(i_v: Vec3, m: Mat4x4) -> Vec3:
    r_v     = Vec3(0, 0, 0)
    r_v.x   = i_v.x * m.matrix[0][0] + i_v.y * m.matrix[1][0] + i_v.z * m.matrix[2][0] + m.matrix[3][0]
    r_v.y   = i_v.x * m.matrix[0][1] + i_v.y * m.matrix[1][1] + i_v.z * m.matrix[2][1] + m.matrix[3][1]
    r_v.z   = i_v.x * m.matrix[0][2] + i_v.y * m.matrix[1][2] + i_v.z * m.matrix[2][2] + m.matrix[3][2]
    w       = i_v.x * m.matrix[0][3] + i_v.y * m.matrix[1][3] + i_v.z * m.matrix[2][3] + m.matrix[3][3]

    if w != 0:
        r_v.x /= w
        r_v.y /= w
        r_v.z /= w

    return r_v

def drawLine(x1: int, y1: int, x2: int, y2: int, color: Tuple[int, int, int], cons: console):
    for point in los.bresenham((x1, y1), (x2, y2)):
        if 0 <= point[0] < WIDTH and 0 <= point[1] < HEIGHT:
            cons.tiles_rgb[point[0], point[1]]["bg"] = color


def drawTri(tri: Tri, color: Tuple[int, int, int], cons: console):
    drawLine(int(tri.points[0].x), int(tri.points[0].y), int(tri.points[1].x), int(tri.points[1].y), color, cons)
    drawLine(int(tri.points[1].x), int(tri.points[1].y), int(tri.points[2].x), int(tri.points[2].y), color, cons)
    drawLine(int(tri.points[2].x), int(tri.points[2].y), int(tri.points[0].x), int(tri.points[0].y), color, cons)

def fillTri(tri: Tri, color: Tuple[int, int, int], cons: console):
    drawLine(int(tri.points[0].x), int(tri.points[0].y), int(tri.points[1].x), int(tri.points[1].y), color, cons)
    drawLine(int(tri.points[1].x), int(tri.points[1].y), int(tri.points[2].x), int(tri.points[2].y), color, cons)
    drawLine(int(tri.points[2].x), int(tri.points[2].y), int(tri.points[0].x), int(tri.points[0].y), color, cons)
    
    
    # Dumb bad implementation
    # itotal = 60
    # for i in range(0, itotal):
    #     drawLine(int(tri.points[0].x), int(tri.points[0].y), int(tri.points[2].x - ((tri.points[2].x - tri.points[1].x) * i / itotal)), int((tri.points[2].y - (tri.points[2].y - tri.points[1].y) * i / itotal)), color, cons)


class Render3d(BlankSimulation):
    def __init__(self) -> None:
        self.width = WIDTH
        self.height = HEIGHT

        # Initialize Cube Mesh
        self.meshCube = Mesh(
            [
                # South
                Tri([Vec3(0, 0, 0), Vec3(0, 1, 0), Vec3(1, 1, 0)]),
                Tri([Vec3(0, 0, 0), Vec3(1, 1, 0), Vec3(1, 0, 0)]),

                # East
                Tri([Vec3(1, 0, 0), Vec3(1, 1, 0), Vec3(1, 1, 1)]),
                Tri([Vec3(1, 0, 0), Vec3(1, 1, 1), Vec3(1, 0, 1)]),

                # North
                Tri([Vec3(1, 0, 1), Vec3(1, 1, 1), Vec3(0, 1, 1)]),
                Tri([Vec3(1, 0, 1), Vec3(0, 1, 1), Vec3(0, 0, 1)]),
            
                # West
                Tri([Vec3(0, 0, 1), Vec3(0, 1, 1), Vec3(0, 1, 0)]),
                Tri([Vec3(0, 0, 1), Vec3(0, 1, 0), Vec3(0, 0, 0)]),

                # Top
                Tri([Vec3(0, 1, 0), Vec3(0, 1, 1), Vec3(1, 1, 1)]),
                Tri([Vec3(0, 1, 0), Vec3(1, 1, 1), Vec3(1, 1, 0)]),

                # Bottom
                Tri([Vec3(1, 0, 1), Vec3(0, 0, 1), Vec3(0, 0, 0)]),
                Tri([Vec3(1, 0, 1), Vec3(0, 0, 0), Vec3(1, 0, 0)]),
            ]
        )


        # Initialize Projection Matrix
        f_near: float = 0.1
        f_far: float = 1000
        f_fov: float = 90
        f_ar: float = float(self.height / self.width)
        f_ftan: float = 1.0 / tan(f_fov * 0.5 / 180 * pi)

        self.matProj = Mat4x4()
        self.matProj.matrix[0][0] = f_ar * f_ftan
        self.matProj.matrix[1][1] = f_ftan
        self.matProj.matrix[2][2] = f_far / (f_far - f_near)
        self.matProj.matrix[3][2] = (-f_far * f_near) / (f_far - f_near)
        self.matProj.matrix[2][3] = 1.0
        self.matProj.matrix[3][3] = 0.0

        self.theta = 0.0

        self.v_camera = Vec3()

        self.matRotZ = Mat4x4()

        self.matRotX = Mat4x4()
        


    def on_update(self, dt: float) -> None:
        self.theta += dt

        # Modify rotation matrices by elapsed time
        self.matRotZ.matrix[0][0] = cos(self.theta)
        self.matRotZ.matrix[0][1] = sin(self.theta)
        self.matRotZ.matrix[1][0] = -sin(self.theta)
        self.matRotZ.matrix[1][1] = cos(self.theta)
        self.matRotZ.matrix[2][2] = 1
        self.matRotZ.matrix[3][3] = 1

        self.matRotX.matrix[0][0] = 1
        self.matRotX.matrix[1][1] = cos(self.theta / 2)
        self.matRotX.matrix[1][2] = sin(self.theta / 2)
        self.matRotX.matrix[2][1] = -sin(self.theta / 2)
        self.matRotX.matrix[2][2] = cos(self.theta / 2)
        self.matRotX.matrix[3][3] = 1

    def on_render(self, cons: console) -> None:
        super().on_render(cons)

        for tri in self.meshCube.tris:
            # Rotate Triangle on Z
            triRotZ = Tri([Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(0, 0, 0)])
            for i in range(0, 3):
                triRotZ.points[i] = multiply_matrix_vector(tri.points[i], self.matRotZ)

            # Rotate Triangle on X
            triRotX = Tri([Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(0, 0, 0)])
            for i in range(0, 3):
                triRotX.points[i] = multiply_matrix_vector(triRotZ.points[i], self.matRotX)

            # Translate on Z
            triTrans = deepcopy(triRotX)
            for i in range(0, 3):
                triTrans.points[i].z = triRotX.points[i].z + 3.0

            # Calculate Normal
            line1 = Vec3()
            line1.x = triTrans.points[1].x - triTrans.points[0].x
            line1.y = triTrans.points[1].y - triTrans.points[0].y
            line1.z = triTrans.points[1].z - triTrans.points[0].z

            line2 = Vec3()
            line2.x = triTrans.points[2].x - triTrans.points[0].x
            line2.y = triTrans.points[2].y - triTrans.points[0].y
            line2.z = triTrans.points[2].z - triTrans.points[0].z

            normal = Vec3()
            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x

            # Normalize Normal
            length: float = sqrt(normal.x**2 + normal.y**2 + normal.z**2)
            normal.x /= length
            normal.y /= length
            normal.z /= length

            dot = normal.x * (triTrans.points[0].x - self.v_camera.x) + normal.y * (triTrans.points[0].y - self.v_camera.y) + normal.z * (triTrans.points[0].z - self.v_camera.z)
            
            if dot < 0:
                # Apply Matrix Math
                triProj = Tri([Vec3(0, 0, 0), Vec3(0, 0, 0), Vec3(0, 0, 0)])
                for i in range(0, 3):
                    triProj.points[i] = multiply_matrix_vector(triTrans.points[i], self.matProj)
                    triProj.points[i].x = (triProj.points[i].x + 1) * (self.width / 2)
                    triProj.points[i].y = (triProj.points[i].y + 1) * (self.height / 2)

                # Draw Triangle
                fillTri(triProj, (255, 255, 255), cons)
