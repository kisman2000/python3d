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

objects = [ [ None, 0, 0, 0, 0, 0, 0 ] ]

def modify(point) : 
    return [ point[0] + x0 * graph.DEF_GRAPH_WIDTH, point[1] + y0 * graph.DEF_GRAPH_HEIGHT ]

def project(x, y, z) :
    x = (x + cameraX) / ((z / aspectZ + cameraZ) * math.tan(a / aspectX))
    y = (y + cameraY) / ((z / aspectZ + cameraZ) * math.tan(a / aspectY))

    return [ x, y ]

def point(x, y, z) :
    return project(x, y, z)

def moveTo(point) :
    graph.moveTo(modify(point)[0], modify(point)[1])

def lineTo(point) :
    return graph.lineTo(modify(point)[0], modify(point)[1])

def line(point1, point2) :
    return graph.line(modify(point1)[0], modify(point1)[1], modify(point2)[0], modify(point2)[1])

def update() :
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

    update()

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

def pyramid(centerX, centerY, centerZ, height, size) :
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
 
    objects.append( [ line1, minX, centerY, minZ, maxX, centerY, minZ ] )
    objects.append( [ line2, maxX, centerY, minZ, maxX, centerY, maxZ ] )
    objects.append( [ line3, maxX, centerY, maxZ, minX, centerY, maxZ ] )
    objects.append( [ line4, minX, centerY, maxZ, minX, centerY, minZ ] )
    objects.append( [ line5, minX, centerY, minZ, centerX, centerY - height, centerZ ] )
    objects.append( [ line6, maxX, centerY, minZ, centerX, centerY - height, centerZ ] )
    objects.append( [ line7, maxX, centerY, maxZ, centerX, centerY - height, centerZ ] )
    objects.append( [ line8, minX, centerY, maxZ, centerX, centerY - height, centerZ ] )

graph.onKey(key)
graph.onTimer(update, 1)

graph.penColor("black")

aabb(-15, 0, -15, 15, 30, 15)
pyramid(0, 0, 0, 30, 50)
pyramid(0, -30, 0, 30, 30)
pyramid(0, -60, 0, 30, 20)

# cube(0, 0, 1, 30)
# cube(0, 60, 1, 30)
# cube(80, 0, 1, 40)


graph.run()