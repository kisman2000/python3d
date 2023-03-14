import graph
import math

KEY_W = 87
KEY_A = 65
KEY_S = 83
KEY_D = 68
KEY_LSHIFT = 16

fov = 2
a = (fov / 180) * math.pi
 
x0 = 0.5
y0 = 0.5
 
aspectX = 4
aspectY = 4
aspectZ = min(aspectX, aspectY) * 2
 
cameraX = 0
cameraY = 0
cameraZ = 40
 
speedX = 5
speedY = 5
speedZ = 5
 
class Point :
    def __init__(self, x, y, z, projectX, projectY) :
        self.x = x
        self.y = y
        self.z = z
        self.projectX = projectX
        self.projectY = projectY
 
 
class LineObject :
    def __init__(self, line, point1, point2) :
        self.line = line
        self.point1 = point1
        self.point2 = point2
 
class PolygonObject :
    def __init__(self, polygon, points, color) :
        self.polygon = polygon
        self.points = points
        self.color = color
 
 
lines = list()
polygons = list()
 
def modify(point) : 
    return [ point.projectX + x0 * graph.DEF_GRAPH_WIDTH, point.projectY + y0 * graph.DEF_GRAPH_HEIGHT ]
 
def project(x, y, z) :
    x = (x + cameraX) / ((z / aspectZ + cameraZ) * math.tan(a / aspectX))
    y = (y + cameraY) / ((z / aspectZ + cameraZ) * math.tan(a / aspectY))
 
    return [ x, y ]
 
def point(x, y, z) :
    projection = project(x, y, z)
    return Point(x, y, z, projection[0], projection[1])
 
def moveTo(point) :
    graph.moveTo(modify(point)[0], modify(point)[1])
 
def lineTo(point) :
    return graph.lineTo(modify(point)[0], modify(point)[1])
 
def line(point1, point2) :
    return graph.line(modify(point1)[0], modify(point1)[1], modify(point2)[0], modify(point2)[1])

def polygon(points) :
    points0 = [ ]

    for point in points :
        points0.append((modify(point)[0], modify(point)[1]))

    points0.append((modify(points[0])[0], modify(points[0])[1]))

    return graph.polygon(points0)
 
def update() :
    for polygon0 in polygons :
        points0 = list()

        for point1 in polygon0.points :
            points0.append(point(point1.x, point1.y, point1.z))

        polygon0.points = points0

        if polygon0.polygon != None :
            graph.deleteObject(polygon0.polygon)
 
        graph.brushColor(polygon0.color)
 
        polygon0.polygon = polygon(polygon0.points)

    for line0 in lines :
        point1 = point(line0.point1.x, line0.point1.y, line0.point1.z)
        point2 = point(line0.point2.x, line0.point2.y, line0.point2.z)
 
        graph.deleteObject(line0.line)
 
        line0.line = line(point1, point2)
 
def key(event) :
    global cameraX, cameraY, cameraZ
 
    if(event.keycode == KEY_W) :
        cameraZ += speedZ
 
    if(event.keycode == KEY_S) :
        cameraZ -= speedZ
 
    if(event.keycode == KEY_A) :
        cameraX -= speedX
 
    if(event.keycode == KEY_D) :
        cameraX += speedX
 
    if(event.keycode == graph.VK_SPACE) :
        cameraY -= speedY
 
    if(event.keycode == KEY_LSHIFT) :
        cameraY += speedY
 
    update()
 
def aabb(minX, minY, minZ, maxX, maxY, maxZ, color) :
    point1 = point(minX, minY, minZ)
    point2 = point(maxX, minY, minZ)
    point3 = point(maxX, minY, maxZ)
    point4 = point(minX, minY, maxZ)
    point5 = point(minX, maxY, minZ)
    point6 = point(maxX, maxY, minZ)
    point7 = point(maxX, maxY, maxZ)
    point8 = point(minX, maxY, maxZ)
 
    line1 = line(point1, point2)
    line2 = line(point2, point3)
    line3 = line(point3, point4)
    line4 = line(point4, point1)
    line5 = line(point5, point6)
    line6 = line(point6, point7)
    line7 = line(point7, point8)
    line8 = line(point8, point5)
    line9 = line(point1, point5)
    line10 = line(point2, point6)
    line11 = line(point3, point7)
    line12 = line(point4, point8)

    polygon1 = polygon([ point1, point2, point3, point4 ])
    polygon2 = polygon([ point5, point6, point7, point8 ])
    polygon3 = polygon([ point1, point2, point6, point5 ])
    polygon4 = polygon([ point3, point4, point8, point7 ])
    polygon5 = polygon([ point1, point4, point8, point5 ])
    polygon6 = polygon([ point2, point3, point7, point6 ])
 
    lines.append(LineObject(line1, point1, point2))
    lines.append(LineObject(line2, point2, point3))
    lines.append(LineObject(line3, point3, point4))
    lines.append(LineObject(line4, point4, point1))
    lines.append(LineObject(line5, point5, point6))
    lines.append(LineObject(line6, point6, point7))
    lines.append(LineObject(line7, point7, point8))
    lines.append(LineObject(line8, point8, point5))
    lines.append(LineObject(line9, point1, point5))
    lines.append(LineObject(line10, point2, point6))
    lines.append(LineObject(line11, point3, point7))
    lines.append(LineObject(line12, point4, point8))

    polygons.append(PolygonObject(polygon1, [ point1, point2, point3, point4 ], color))
    polygons.append(PolygonObject(polygon2, [ point5, point6, point7, point8 ], color))
    polygons.append(PolygonObject(polygon3, [ point1, point2, point6, point5 ], color))
    polygons.append(PolygonObject(polygon4, [ point3, point4, point8, point7 ], color))
    polygons.append(PolygonObject(polygon5, [ point1, point4, point8, point5 ], color))
    polygons.append(PolygonObject(polygon6, [ point2, point3, point7, point6 ], color))
 
def cube(centerX, centerY, centerZ, size, color) :
    aabb(centerX - size, centerY - size, centerZ - size, centerX + size, centerY + size, centerZ + size, color)
 
def pyramid(centerX, centerY, centerZ, height, size, color) :
    minX = centerX - size
    minZ = centerZ - size
    maxX = centerX + size
    maxZ = centerZ + size
 
    point1 = point(minX, centerY, minZ)
    point2 = point(maxX, centerY, minZ)
    point3 = point(maxX, centerY, maxZ)
    point4 = point(minX, centerY, maxZ)
 
    point5 = point(centerX, centerY - height, centerZ)
 
    line1 = line(point1, point2)
    line2 = line(point2, point3)
    line3 = line(point3, point4)
    line4 = line(point4, point1)
 
    line5 = line(point1, point5)
    line6 = line(point2, point5)
    line7 = line(point3, point5)
    line8 = line(point4, point5)

    polygon1 = polygon([ point1, point2, point3, point4 ])
    polygon2 = polygon([ point1, point2, point5 ])
    polygon3 = polygon([ point2, point3, point5 ])
    polygon4 = polygon([ point3, point4, point5 ])
    polygon5 = polygon([ point4, point1, point5 ])
 
    lines.append(LineObject(line1, point1, point2))
    lines.append(LineObject(line2, point2, point3))
    lines.append(LineObject(line3, point3, point4))
    lines.append(LineObject(line4, point4, point1))
    lines.append(LineObject(line5, point1, point5))
    lines.append(LineObject(line6, point2, point5))
    lines.append(LineObject(line7, point3, point5))
    lines.append(LineObject(line8, point4, point5))
 
    polygons.append(PolygonObject(polygon1, [ point1, point2, point3, point4 ], color))
    polygons.append(PolygonObject(polygon2, [ point1, point2, point5 ], color))
    polygons.append(PolygonObject(polygon3, [ point2, point3, point5 ], color))
    polygons.append(PolygonObject(polygon4, [ point3, point4, point5 ], color))
    polygons.append(PolygonObject(polygon5, [ point4, point1, point5 ], color))
 
graph.onKey(key)
graph.onTimer(update, 1)
 
graph.penColor("black")
 
 
aabb(-15, 0, -15, 15, 30, 15, "brown")
pyramid(0, 0, 0, 30, 50, "green")
pyramid(0, -30, 0, 30, 30, "green")
pyramid(0, -60, 0, 30, 20, "green")
 
 
# cube(0, 0, 1, 30)
# cube(0, 60, 1, 30)
# cube(80, 0, 1, 40)
# pyramid(-80, 40, 1, 80, 40)
 
 
graph.run()