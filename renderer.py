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
cameraZ = 0 # 40
 
speedX = 5
speedY = 5
speedZ = 5

sensitivity = 0.5

prevMouseX = -1
prevMouseY = -1
deltaMouseX = -1
deltaMouseY = -1

yaw = 0
pitch = 0

def hypot(a, b) :
    return math.sqrt(a * a + b * b)
 
class Point :
    def __init__(self, x, y, z, projectX, projectY, center) :
        self.x = x
        self.y = y
        self.z = z
        self.projectX = projectX
        self.projectY = projectY
        self.center = center

    def centre(self) :
        return point(self.x + self.center.x, self.y + self.center.y, self.z + self.center.z, center(0, 0, 0))        
 
 
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
    
class Vector2 :
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def len(self) :
        return hypot(self.x, self.y)
    
    def norm(self) :
        len0 = self.len()

        if len0 == 0 :
            return self

        return Vector2(self.x / len0, self.y / len0)
    
    def mult(self, a) :
        return Vector2(self.x * a, self.y * a)
    
    def toComplex(self) :
        return complex(self.x, self.y)
 
lines = list()
polygons = list()
 
def modify(point) : 
    return [ point.projectX + x0 * graph.DEF_GRAPH_WIDTH, point.projectY + y0 * graph.DEF_GRAPH_HEIGHT ]

def rad(degrees) :
    return degrees / 180 * math.pi

def deg(radians) :
    return radians * 180 / math.pi

def max0(a, b) : 
    if(abs(a) > abs(b)) :
        return a
    else :
        return b

def rotate(a, b, degree, centerA, centerB) :
    # a0 = a - centerA
    # b0 = b - centerB
    # hypot0 = hypot(a0, b0)

    # if hypot0 != 0 :
    #     cos = a0 / hypot0
    #     sin = b0 / hypot0

    #     a0 = math.cos(rad(degree) + math.acos(cos)) * hypot0
    #     b0 = math.sin(rad(degree) + math.asin(sin)) * hypot0

    # return [ a0 + centerA, b0 + centerB ]
    # print(degree)
    # complex0 = complex(a - centerA, b - centerB) * complex(math.cos(degree), math.sin(degree))# Vector2(0, degree / 90).norm().toComplex()# complex(0, degree / 90)

    lengthA = math.fabs(a - centerA)
    lengthB = math.fabs(b - centerB)
    # hypotAB = hypot(lengthA, lengthB)
    vec = Vector2(lengthA, lengthB)
    len = vec.len()

    # print(len)

    complex0 = complex(vec.x, vec.y) * complex(math.sin(rad(90 - degree)), math.sin(rad(degree)))

    # print(math.cos(rad(degree)),math.sin(rad(degree)))
    # print(complex0.real,complex0.imag)
    result = Vector2(complex0.real, complex0.imag).norm().mult(len)
    # vec1 = Vector2(complex0.real, complex0.imag)
    # mult = vec1.mult(hypotAB)

    return [ result.x + centerA, result.y + centerB ]
    

def max0(a, b) :
    if(a > b) :
        return a
    else :
        return b

def project(x, y, z) :
    # x = max0(x, cameraX)
    # z = max0(z, cameraZ)

    # print(z)

    

    x = (x + cameraX) / max(((z / aspectZ + cameraZ) * math.tan(a / aspectX)), 0.000000000001)
    y = (y + cameraY) / max(((z / aspectZ + cameraZ) * math.tan(a / aspectY)), 0.000000000001)
 
    return [ x, y ]
 
def point(x, y, z, center) :
    # vector = Vector3(math.asin(pitch), math.asin(yaw), 0)

    # rotateY = rotate(x, z, yaw, cameraX, cameraZ)
    # rotateX = rotate(y, rotateY[1], pitch, cameraY, cameraZ)

    # rotatedX = rotateY[0]
    # rotatedY = rotateX[0]
    # rotatedZ = rotateX[1]

    # print("prev x",x,"x",rotatedX,"yaw",yaw)

    # print(x,center.x)

    rotateY = rotate(x, z, yaw, cameraX, cameraZ)
    rotateX = rotate(y, rotateY[1], pitch, cameraY, cameraZ)
    


    rotatedX = rotateY[0]
    rotatedY = rotateX[0]
    rotatedZ = rotateX[1]

    projection = project(rotatedX, rotatedY, rotatedZ)
    # projection = project(x + center.x, y + center.y, z + center.z)

    return Point(x, y, z, projection[0], projection[1], center)

    # center0 = center(x, y, z)
    # center0.center = center1

    # return center0 # Point(x, y, z, center0.)

def center(x, y, z) :
    # rotateX = rotate(y, z, pitch, cameraY, cameraZ)
    # rotateY = rotate(x, rotateX[1], yaw, cameraX, cameraZ)

    # rotatedX = rotateY[0]
    # rotatedY = rotateX[0]
    # rotatedZ = rotateY[1]
    rotateY = rotate(x, z, yaw, cameraX, cameraZ)
    rotateX = rotate(y, z, pitch, cameraY, cameraZ)

    rotatedX = rotateY[0]
    rotatedY = rotateX[0]
    rotatedZ = rotateY[1]

    # print(x,rotatedX)

    # print("prev x",x,"x",rotatedX,"yaw",yaw)
    # print("prev y",y,"y",rotatedY,"pitch",pitch)

    projection = project(rotatedX, rotatedY, rotatedZ)

    return Point(rotatedX, rotatedY, rotatedZ, projection[0], projection[1], None)

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
        points1 = list()

        for point0 in polygon0.points :
            point1 = point(point0.x, point0.y, point0.z, center(point0.center.x, point0.center.y, point0.center.z))
            points1.append(point1.centre())

        if polygon0.polygon != None :
            graph.deleteObject(polygon0.polygon)
 
        if polygon0.color != "" :
            graph.brushColor(polygon0.color)
 
        polygon0.polygon = polygon(points1)

    for line0 in lines :
        if (line0.point1.z <= cameraZ or line0.point2.z <= cameraZ) and (line0.point1.z > cameraZ or line0.point2.z > cameraZ) :
            if line0.point1.z < cameraZ :
                point0 = line0.point1
                line0.point1 = point(point0.x, point0.y, 1, point0.center)
            else :
                point0 = line0.point2
                line0.point2 = point(point0.x, point0.y, 1, point0.center)

        graph.deleteObject(line0.line)

        if line0.point1.z >= cameraZ and line0.point2.z >= cameraZ :
            point1 = point(line0.point1.x, line0.point1.y, line0.point1.z, center(line0.point1.center.x, line0.point1.center.y, line0.point1.center.z)).centre()
            point2 = point(line0.point2.x, line0.point2.y, line0.point2.z, center(line0.point2.center.x, line0.point2.center.y, line0.point2.center.z)).centre()
 
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

def wrap(angle) :
    if(angle > 180) :
        angle = -180

    if(angle < -180) :
        angle = 180

    return angle

def mouse(event) :
    global prevMouseX, prevMouseY, deltaMouseX, deltaMouseY, yaw, pitch

    deltaMouseX = int(event.x - prevMouseX)
    deltaMouseY = int(event.y - prevMouseY)

    prevMouseX = event.x
    prevMouseY = event.y

    yaw = wrap(yaw + deltaMouseX * sensitivity)
    pitch = max(-90, min(90, wrap(pitch + deltaMouseY * sensitivity)))

    # print(pitch)
 
def aabb(minX, minY, minZ, maxX, maxY, maxZ, color) :
    center0 = center(min(minX, maxX) + math.fabs(minX - maxX) / 2, min(minY, maxY) + math.fabs(minY - maxY) / 2, min(minZ, maxZ) + math.fabs(minZ - maxZ) / 2)

    minX = 0
    minY = 0
    minZ = 0
    maxX = math.fabs(maxX - minX)
    maxY = math.fabs(maxY - minY)
    maxZ = math.fabs(maxZ - minZ)

    point1 = point(minX, minY, minZ, center0)
    point2 = point(maxX, minY, minZ, center0)
    point3 = point(maxX, minY, maxZ, center0)
    point4 = point(minX, minY, maxZ, center0)
    point5 = point(minX, maxY, minZ, center0)
    point6 = point(maxX, maxY, minZ, center0)
    point7 = point(maxX, maxY, maxZ, center0)
    point8 = point(minX, maxY, maxZ, center0)
 
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

    center0 = center(centerX, centerY - height / 2, centerZ)

    minX -= centerX
    minZ -= centerZ
    maxX -= centerX
    maxZ -= centerZ

    centerY = 0
 
    point1 = point(minX, centerY, minZ, center0)
    point2 = point(maxX, centerY, minZ, center0)
    point3 = point(maxX, centerY, maxZ, center0)
    point4 = point(minX, centerY, maxZ, center0)
 
    point5 = point(0, -height, 0, center0)
 
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

def start() :
    graph.onKey(key)
    graph.onMouseButtonMove(mouse)
    graph.onTimer(update, 1)
    
    graph.penColor("black")
    
    
    # aabb(-15, 0, -15, 15, 30, 15, "brown")
    # pyramid(0, 0, 0, 30, 50, "green")
    # pyramid(0, -30, 0, 30, 30, "green")
    # pyramid(0, -60, 0, 30, 20, "green")
    
    
    # cube(0, 0, 1, 30, "red")
    cube(50, 0, 1, 30, "red")
    pyramid(-50, 0, 1, 30, 30, "blue")
    aabb(0, 0, 0, 100, 0, 0, "")
    aabb(0, 0, 0, 0, 100, 0, "")
    aabb(0, 0, 0, 0, 0, 100, "")
    # cube(0, 60, 1, 30, "green")
    # cube(80, 0, 1, 40, "blue")
    # pyramid(-80, 40, 1, 80, 40, "white")
    
    
    graph.run()

start()