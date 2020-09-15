import turtle
import math
import random


class Line:

    def __init__(self, p1, p2):
        self.points = [p1, p2]
        self.mpo = None

    def share_point(self, other):
        if self.points[0] in other.points:
            return self.points[0]
        if self.points[1] in other.points:
            return self.points[1]
        return None

    def __eq__(self, other):
        return set(self.points) == set(other.points)

    def __repr__(self):
        return "{points}".format(points=self.points)

class Triangle:

    def __init__(self, l1=None, l2=None, l3=None):
        self.lines = [l for l in [l1, l2, l3] if l is not None]

    def add_line(self, line):
        self.lines.append(line)

    def __repr__(self):
        return "Triangle with lines {lines}".format(lines=self.lines)

def omp(line, off):
    if line.mpo is None:
        p1, p2 = line.points
        midoff = ((p1[2] + p2[2]) / 2) + 2 * random.random() * off
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1])/2, midoff
    return line.mpo

def fractal(tl, off, rough, itr):
    new_triangles = []
    line_list = []
    for t in tl:
        for line in t.lines:
            if line not in line_list:
                line.mpo = omp(line, off)
                line_list.append(line)
            else:
                line.mpo = line_list[line_list.index(line)].mpo

        l1 = Line(t.lines[0].mpo, t.lines[1].mpo)
        l2 = Line(t.lines[1].mpo, t.lines[2].mpo)
        l3 = Line(t.lines[2].mpo, t.lines[0].mpo)

        new_triangles.append(Triangle(l1 = l1, l2 = l2, l3 = l3))

        point1 = t.lines[0].share_point(t.lines[1])
        point2 = t.lines[1].share_point(t.lines[2])
        point3 = t.lines[2].share_point(t.lines[0])

        new_triangles.append(Triangle(l1 = l1, l2 = Line(point1, t.lines[0].mpo), l3 = Line(point1, t.lines[1].mpo)))
        new_triangles.append(Triangle(l1 = l2, l2 = Line(point2, t.lines[1].mpo), l3 = Line(point2, t.lines[2].mpo)))
        new_triangles.append(Triangle(l1 = l3, l2 = Line(point3, t.lines[2].mpo), l3 = Line(point3, t.lines[0].mpo)))

    if itr > 0:
        return fractal(new_triangles, off * (2 ** -rough), rough, itr-1)
    else:
        return new_triangles


def transform(x, y, z, angle, tilt):
    #Animation control (around y-axis)
    s, c = math.sin(angle), math.cos(angle)
    x, y = x * c - y * s, x * s + y * c

    #Camera tilt  (around x-axis)
    s, c = math.sin(tilt), math.cos(tilt)
    z, y = z * c - y * s, z * s + y * c

    # Setting up View Parameters
    y += 150 #Fixed Distance from top
    FOV = 16000 #Fixed Field of view
    f = FOV / y
    sx, sy = x * f, z * f
    return sx, sy

def get_color(points):
    maxz = max(points[0][2], points[1][2])
    if maxz < 1:
        return "black"
    if maxz >= 1 and maxz <= 1.5:
        return "dark blue"
    if maxz > 1.5 and maxz <= 2:
        return "medium blue"
    return "royal blue"


def main():
    wn = turtle.Screen()
    wn.bgcolor("white")
    wn.title("Turtle")
    skk = turtle.Turtle()

    # draw triangle is for 2D drawing, the comment triangle below works well with 2D
    """def draw_triangle(triangle):
        for line3 in triangle.lines:
            skk.penup()
            skk.goto((line3.points[0][0]*200, line3.points[0][2]*200))
            skk.pendown()
            skk.goto((line3.points[1][0]*200, line3.points[1][2]*200))

    tl1 = Line((0, 0, 1.5), (-2, 0, -1.5))
    tl2 = Line((-2, 0, -1.5), (2, 0, -1.5))
    tl3 = Line((2, 0, -1.5), (0, 0, 1.5))"""

    tl1 = Line((0, 1.5, .4), (-2, -1.5, -.1))
    tl2 = Line((-2, -1.5, -.1), (2, -1.5, 0))
    tl3 = Line((2, -1.5, 0), (0, 1.5, .4))

    fT = Triangle(l1 = tl1, l2 = tl2, l3 = tl3)
    allT = [fT,]
    offset = 1.5
    roughness = 2
    itr1 = 3
    skk.speed(0)
    turtle.tracer(0,  0)
    angl = 0



    tester = fractal(allT, offset, roughness, itr1)

    # comment below is for 2D drawing
    """for t in tester:
        draw_triangle(t)"""

    while True:
        skk.clear()
        for t in tester:
            for line in t.lines:
                if len(line.points[0]) == 3:
                    skk.pencolor(get_color(line.points))
                    p1 = transform(line.points[0][0], line.points[0][1], line.points[0][2], angl, 0.25)
                    p2 = transform(line.points[1][0], line.points[1][1], line.points[1][2], angl, 0.25)
                    skk.penup()
                    skk.goto(*p1)
                    skk.pendown()
                    skk.goto(*p2)

        turtle.update()

        angl += .01

    turtle.done()

if __name__ == "__main__":
    main()
