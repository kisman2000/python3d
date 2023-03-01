import graph
import math

KEY_W = 87
KEY_A = 65
KEY_S = 83
KEY_D = 68
KEY_LSHIFT = 16

fov = 10
a = (fov / 180) * math.pi

x0 = 300
y0 = 300

aspectX = 4
aspectY = 3

cameraX = 0
cameraY = 30
cameraZ = 40

objects = [ [ None, 0, 0, 0, 0, 0, 0 ] ]

def modify(point) : 
    return [ point[0] + x0, point[1] + y0 ]

def project(x, y, z) :
    x = (x + cameraX) / ((z + cameraZ) * math.tan(a / aspectX))
    y = (y + cameraY) / ((z + cameraZ) * math.tan(a / aspectY))

    return [ x, y ]

def point(x, y, z) :
    return project(x, y, z)

def moveTo(point) :
    graph.moveTo(modify(point)[0], modify(point)[1])

def lineTo(point) :
    return graph.lineTo(modify(point)[0], modify(point)[1])

def line(point1, point2) :
    return graph.line(modify(point1)[0], modify(point1)[1], modify(point2)[0], modify(point2)[1])

def key(event) :
    global cameraX, cameraY, cameraZ

    if(event.keycode == KEY_W) :
        cameraZ += 1

    if(event.keycode == KEY_S) :
        cameraZ -= 1

    if(event.keycode == KEY_A) :
        cameraX -= 1

    if(event.keycode == KEY_D) :
        cameraX += 1

    if(event.keycode == graph.VK_SPACE) :
        cameraY -= 1

    if(event.keycode == KEY_LSHIFT) :
        cameraY += 1

    for pair in objects :
        object1 = pair[0]
        x1 = pair[1]
        y1 = pair[2]
        z1 = pair[3]
        x2 = pair[4]
        y2 = pair[5]
        z2 = pair[6]
        
        point1 = point(x1, y1, z1)
        point2 = point(x2, y2, z2)

        graph.deleteObject(object1)

        objects.remove(pair)

        object2 = line(point1, point2)

        objects.append( [ object2, x1, y1, z1, x2, y2, z2 ] )

def aabb(minX, minY, minZ, maxX, maxY, maxZ) :
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
    line3 = line(point3, point3)
    line4 = line(point4, point1)
    line5 = line(point5, point6)
    line6 = line(point6, point7)
    line7 = line(point7, point8)
    line8 = line(point8, point5)
    line9 = line(point1, point5)
    line10 = line(point2, point6)
    line11 = line(point3, point7)
    line12 = line(point4, point8)

    objects.append( [ line1, minX, minY, minZ, maxX, minY, minZ ] )
    objects.append( [ line2, maxX, minY, minZ, maxX, minY, maxZ ] )
    objects.append( [ line3, maxX, minY, maxZ, minX, minY, maxZ ] )
    objects.append( [ line4, minX, minY, maxZ, minX, minY, minZ ] )
    objects.append( [ line5, minX, maxY, minZ, maxX, maxY, minZ ] )
    objects.append( [ line6, maxX, maxY, minZ, maxX, maxY, maxZ ] )
    objects.append( [ line7, maxX, maxY, maxZ, minX, maxY, maxZ ] )
    objects.append( [ line8, minX, maxY, maxZ, minX, maxY, minZ ] )
    objects.append( [ line9, minX, minY, minZ, minX, maxY, minZ ] )
    objects.append( [ line10, maxX, minY, minZ, maxX, maxY, minZ ] )
    objects.append( [ line11, maxX, minY, maxZ, maxX, maxY, maxZ ] )
    objects.append( [ line12, minX, minY, maxZ, minX, maxY, maxZ ] )

def cube(centerX, centerY, centerZ, size) :
    aabb(centerX - size, centerY - size, centerZ - size, centerX + size, centerY + size, centerZ + size)

graph.onKey(key)

graph.penColor("black")


cube(50, 50, 1, 30)
cube(50, 50 + 60, 1, 30)
cube(50 + 60, 50, 1, 30)


graph.run()