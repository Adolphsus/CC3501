import pyglet
import random
from OpenGL.GL import *

from math import *
from collections import deque
from itertools import chain
from pathlib import Path
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))

import libs.transformations as tr
import libs.basic_shapes as bs
import libs.scene_graph as sg
import libs.easy_shaders as es
import libs.lighting_shaders as ls
import libs.curves as cs

from libs.gpu_shape import createGPUShape
from libs.obj_handler import read_OBJ2
from libs.assets_path import getAssetPath
from utils import createOFFShape
from ship import createShip, createsombra
from pyglet.graphics.shader import Shader, ShaderProgram
from pathlib import Path
from itertools import chain

class Controller(pyglet.window.Window):

    def __init__(self, width, height, tittle=f"Tarea 3 - Adolfo Arenas P"):
        super().__init__(width, height, tittle)
        self.pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
        self.pipeline2 = es.SimpleModelViewProjectionShaderProgram()
        self.check_points = []
        self.check_points_tograph = []
        self.step = 0
        self.curve = []
        self.show_route = False
        self.path= []

width = 1280
height = 960
N = 100
controller = Controller(width, height)
PERSPECTIVE_PROJECTION = 1
ORTOGRAPHIC_PROJECTION = 0

PROJECTIONS = [tr.ortho(-8, 8, -8, 8, 0.0001, 1000),
    tr.perspective(80, float(width)/float(height), 0.0001, 100)]

with open(Path(os.path.dirname(__file__)) / "point_vertex_program.glsl") as f:
    vertex_program = f.read()

with open(Path(os.path.dirname(__file__)) / "point_fragment_program.glsl") as f:
    fragment_program = f.read()

vert_shader = Shader(vertex_program, "vertex")
frag_shader = Shader(fragment_program, "fragment")
pipeline = ShaderProgram(vert_shader, frag_shader)


class Ship():

    def __init__(self):
        self.shape = createShip(controller.pipeline)
        self.shapesombra = createsombra(controller.pipeline)
        self.x = 0
        self.y = 5
        self.z = 0
        self.velocity = 0
        self.rotationylocal = 0
        self.altitude = 0
        self.route = []
        self.start_route = False
        self.linex = 0
        self.liney = 0
        self.linez = 0

ship = Ship()

class Camera:

    def __init__(self, at=np.array([ship.x, ship.y, ship.z],dtype=float), 
                 eye=np.array([5 , 7, 5],dtype=float), 
                 up=np.array([0, 1, 0],dtype=float)) -> None:
        
        #Parametros de la camara
        self.at = at
        self.eye = eye
        self.up = up

        self.available_projections = PROJECTIONS
        self.projection = self.available_projections[ORTOGRAPHIC_PROJECTION]

    def set_projection(self, projection_name):
        self.projection = self.available_projections[projection_name]
 #siga a nuestra nave y no se rote

camera = Camera()

class Point():
    
    def __init__(self, position):
        self.ex_shape = createGPUShape(controller.pipeline2,bs.createColorCube(1.0, 0.5, 0.0))
        self.position =  np.array(position, dtype=np.float32)

#Aqui agregamos hijos de la clase Ship que creamos para formar nuestro escuadron
def crearEscuadron():

    shipNode1 = sg.SceneGraphNode('ship')
    shipNode1.transform = tr.matmul([tr.rotationY(np.deg2rad(180)), tr.uniformScale(0.8)])
    shipNode1.childs += [ship.shape]

    shipNode2 = sg.SceneGraphNode('ship2')
    shipNode2.transform = tr.translate(2,0,3)
    shipNode2.childs += [shipNode1]

    shipNode3 = sg.SceneGraphNode('ship3')
    shipNode3.transform = tr.translate(-2,0,3)
    shipNode3.childs += [shipNode1]

    Escuadron = sg.SceneGraphNode('Escuadron')
    Escuadron.transform = tr.translate(0,0.1,0)
    Escuadron.childs += [shipNode1]
    Escuadron.childs += [shipNode2]
    Escuadron.childs += [shipNode3]

    return Escuadron
#Separe sombras de la nave para que las sombras no subieran tambien, ya que daba un efecto raro. Ahora las sombras siempre estan a la altura del piso.
def crearSombra():
    sombra = sg.SceneGraphNode('sombra')
    sombra.transform = tr.matmul([tr.translate(0,0.1,0), tr.scale(0.6,0.01,0.6), tr.rotationY(np.deg2rad(180))])
    sombra.childs += [ship.shapesombra]

    sombra1 = sg.SceneGraphNode('sombra1')
    sombra1.transform = tr.translate(ship.x, 0, ship.z)
    sombra1.childs += [sombra]

    sombra2 = sg.SceneGraphNode('sombra2')
    sombra2.transform = tr.translate(ship.x+2, 0, ship.z+3)
    sombra2.childs += [sombra]

    sombra3 = sg.SceneGraphNode('sombra3')
    sombra3.transform = tr.translate(ship.x-2, 0, ship.z+3)
    sombra3.childs += [sombra]

    Sombras = sg.SceneGraphNode('Sombras')
    Sombras.transform = tr.translate(0,0,0)
    Sombras.childs += [sombra1]
    Sombras.childs += [sombra2]
    Sombras.childs += [sombra3]

    return Sombras

#Con ayuda del auxiliar 3 ponemos un piso a la escena
def createFloor() -> sg.SceneGraphNode:

    Floor = bs.createMinecraftFloor(1.5)
    gpuFloor = es.GPUShape().initBuffers()
    controller.pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(Floor.vertices,Floor.indices,GL_STATIC_DRAW)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("floorTexture.png"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    
    Piso = sg.SceneGraphNode('Piso')
    Piso.transform = tr.scale(20,20,100)
    Piso.childs += [gpuFloor]

    totalFloor = sg.SceneGraphNode('totalFloor')
    totalFloor.transform = tr.matmul([tr.translate(0, 0, 0), tr.rotationX(np.deg2rad(90))])
    totalFloor.childs += [Piso]

    return totalFloor

#Con esto ponemos los objetos de la escena (lo quise hacer separado del piso para una futura tarea) 
def createScene() -> sg.SceneGraphNode:

    Cube = bs.createMinecraftCube(1)
    gpuCube = es.GPUShape().initBuffers()
    controller.pipeline.setupVAO(gpuCube)
    gpuCube.fillBuffers(Cube.vertices, Cube.indices, GL_STATIC_DRAW)
    gpuCube.texture = es.textureSimpleSetup(
        getAssetPath('circuit.jpg'), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    
    turret = createGPUShape(controller.pipeline, read_OBJ2(getAssetPath("Laser_turret.obj")))
    turret.texture = es.textureSimpleSetup(getAssetPath("laser_turret_BaseColor.png"), 
                                         GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    Torreta = sg.SceneGraphNode('Torreta')
    Torreta.transform = tr.uniformScale(1)
    Torreta.childs += [turret]

    Torreta1 = sg.SceneGraphNode('Torreta1')
    Torreta1.transform = tr.translate(0, 0, -9)
    Torreta1.childs += [Torreta]

    Torreta2 = sg.SceneGraphNode('Torreta2')
    Torreta2.transform = tr.translate(-5,0, 5)
    Torreta2.childs += [Torreta]

    Torreta3 = sg.SceneGraphNode('Torreta3')
    Torreta3.transform = tr.translate(8,0,8)
    Torreta3.childs += [Torreta]
    
    Condensador = sg.SceneGraphNode('condensador')
    Condensador.transform = tr.uniformScale(0.8)
    Condensador.childs += [gpuCube]

    Condensador1 = sg.SceneGraphNode('condesador1')
    Condensador1.transform = tr.matmul([tr.translate(-4, 1, 3), tr.scale(1,5,1)])
    Condensador1.childs += [Condensador]

    Condensador2 = sg.SceneGraphNode('condesador2')
    Condensador2.transform = tr.matmul([tr.translate(4, 1, -3), tr.scale(7,2,1)])
    Condensador2.childs += [Condensador]

    scene = sg.SceneGraphNode('scene')
    scene.childs += [Condensador1]
    scene.childs += [Condensador2]
    scene.childs += [Torreta1]
    scene.childs += [Torreta2]
    scene.childs += [Torreta3]

    return scene

#con esta funcion vamos moviendo el escuadron, segun la propiedades que le pusimos a la nave                                                                  
def add_points(position, orientation):
    controller.check_points_tograph.append(Point((position[0],position[1],position[2])))
    controller.check_points.append([position[0],position[1],position[2],orientation])

@controller.event
def on_key_press(symbol, modifiers):
    global vector
    if symbol == pyglet.window.key.P: #Esto nos permite cambiar a una vista en perspectiva
        camera.set_projection(PERSPECTIVE_PROJECTION)
    if symbol == pyglet.window.key.O: #Esto nos permite cambiar a una vista ortografica
        camera.set_projection(ORTOGRAPHIC_PROJECTION)
    if symbol == pyglet.window.key.W: #avanzar
        ship.velocity = -0.3
    if symbol == pyglet.window.key.S: #retroceder
        ship.velocity = 0.1
    if symbol == pyglet.window.key.A: #rotar antihorario
        ship.rotationylocal = 0.1
    if symbol == pyglet.window.key.D: #rotar horario
        ship.rotationylocal = -0.1   
    if symbol == pyglet.window.key.R: #Aqui se graban puntos y ademas se crean las matrices y la curva final de hermite
        Yrotation = sg.findTransform(escuadron, 'Escuadron')
        add_points([ship.x,ship.y,ship.z],[Yrotation[0][0],Yrotation[0][2],Yrotation[2][0],Yrotation[2][2]])
        controller.curve = []
        if len(controller.check_points) == 0:
            pass
        if len(controller.check_points) == 1:
            pass
        else:
            for i in range(1, len(controller.check_points)):
                P1 = np.array([[controller.check_points[i-1][0],
                            controller.check_points[i-1][1],      
                            controller.check_points[i-1][2]]]).T 
                P2 = np.array([[controller.check_points[i][0],
                            controller.check_points[i][1],
                            controller.check_points[i][2]]]).T   
                T1 = np.array([[30, 0,30]]).T
                T2 = np.array([[30, 0,30]]).T#  #la idea es crear una matriz de hermite para los puntos de control
                matrix = cs.hermiteMatrix(P1, P2, T1, T2)
                controller.curve.append(cs.evalCurve(matrix, N))
            if len(controller.curve) == 0:
                pass
            if len(controller.curve) == 1:
                ship.route = controller.curve[0]
            else:
                ship.route = controller.curve[0]
                for j in range(1, len(controller.curve)):             #luego aqui abajo quiero concatenar la lista para crear una sola curva final
                    ship.route =  np.concatenate((ship.route, controller.curve[j]))                                             
        controller.step = 0
    if symbol == pyglet.window.key.L: #Nos hace comenzar a recorrer la ruta (debe mantenerse apretado L)
        if len(controller.curve) == 0: #Esto es para asegurarnos de que almenos haya una curva, la cantidad de curvas siempre sera un numero natural.
                pass
        else:
            ship.start_route = True  #este booleano le indica a update que debe cambiar la transformacion de la nave
    if symbol == pyglet.window.key.V:  #Nos permite visualizar la ruta  (debe mantenerse apretado V)
        controller.show_route = True
    if symbol == pyglet.window.key.ESCAPE:
        controller.close()

@controller.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        ship.velocity = 0
    if symbol == pyglet.window.key.S:
        ship.velocity = 0
    if symbol == pyglet.window.key.A:
        ship.rotationylocal = 0
    if symbol == pyglet.window.key.D:
        ship.rotationylocal = 0
    if symbol == pyglet.window.key.Q: 
        ship.rotationzlocal = 0
    if symbol == pyglet.window.key.E:
        ship.rotationzlocal = 0
    if symbol == pyglet.window.key.L:
        ship.start_route = False
    if symbol == pyglet.window.key.V:
        controller.show_route = False

@controller.event
def on_mouse_drag(x,y,dx,dy, buttons, modifiers):
    if buttons == pyglet.window.mouse.LEFT:            #pense que al apretar el left click y luego permitir que la nave se moviera
        if y > 460:                                    #era mas natural que se moviera siempre
            ship.altitude = 20*dy/960
        if y == 0:
            ship.altitude = 0
        elif y < 0:
            ship.altitude = -10*dy/960

escuadron = crearEscuadron()
sombras = crearSombra()
piso = createFloor()
escenario = createScene()
punto = createGPUShape(controller.pipeline2, bs.createAxis(0.0001))

def update(dt):
    global vector
    escuadron.transform = tr.matmul([escuadron.transform, tr.rotationY(ship.rotationylocal), tr.translate(0, ship.altitude, ship.velocity)]) #esta se encarga de rotar mi nave sobre su eje y, ademas de trasladarla
    ship.x = sg.findPosition(escuadron,'Escuadron')[0][0]    #actualizamos los parametros de la posicion de la nave
    ship.y = sg.findPosition(escuadron, 'Escuadron')[1][0]
    ship.z = sg.findPosition(escuadron, 'Escuadron')[2][0]
    sombras.transform = tr.matmul([sombras.transform, tr.rotationY(ship.rotationylocal), tr.translate(0, 0, ship.velocity)])
    camera.eye[1] = ship.y+7
    camera.at[1] = ship.y
    camera.eye[0] = ship.x+5 
    camera.at[0] = ship.x
    camera.eye[2] = ship.z+5   
    camera.at[2] = ship.z

    if controller.step == (N*len(controller.curve))-1:
        pass
    else:
        controller.step += 1

    if controller.step >= 1 and len(ship.route) >=1: 
        vector = [ship.route[controller.step][0]-ship.route[controller.step-1][0],           #este es un vector que toma tiene como coordernadas xf-xi para cada instante,
                            ship.route[controller.step][1]-ship.route[controller.step-1][1], #esto permite darle orientacion a la nave mientras recorre
                            ship.route[controller.step][2]-ship.route[controller.step-1][2]]
        angle=pi+atan2(vector[0],vector[2]) #aca sacamos la arcotangente, en un principio queda dado vuelta pero para esto se le suma pi
    
    if ship.start_route:
        transformEscuadron =  tr.matmul([       #Este transform permite a la nave recorrer la curva de hermite
            tr.translate(ship.route[controller.step, 0],
                        ship.route[controller.step, 1],
                        ship.route[controller.step, 2]), tr.rotationY(angle)])
        escuadron.transform = transformEscuadron
        sombras.transform = transformEscuadron
        ship.linex = ship.route[controller.step][0]
        ship.liney = ship.route[controller.step][1]
        ship.linez = ship.route[controller.step][2]

@controller.event
def on_draw():
    controller.clear()

    glClearColor(1.0, 1.0, 1.0, 0.8)

    view = tr.lookAt(
        camera.eye,
        camera.at,
        camera.up
    )

    for points in controller.check_points_tograph:                                            #Aca dibujamos los puntos de control
            transform = tr.matmul([
                tr.translate(points.position[0],points.position[1],points.position[2]), 
                tr.uniformScale(0.25)]
                )
            glUseProgram(controller.pipeline2.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(controller.pipeline2.shaderProgram, "projection"), 1, GL_TRUE, camera.projection)
            glUniformMatrix4fv(glGetUniformLocation(controller.pipeline2.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(controller.pipeline2.shaderProgram, "model"), 1, GL_TRUE, transform)
            controller.pipeline2.drawCall(points.ex_shape)

    
    glUseProgram(controller.pipeline2.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline2.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
    controller.pipeline2.drawCall(punto)

    if controller.show_route and len(controller.curve)>=1: #basados en cloth.py aqui dibujamos las lineas de la ruta
            lines = pipeline.vertex_list(                  #creamos una lista de vertices
            len(ship.route),
            pyglet.gl.GL_LINES,position="f",)
            tupla = ()
            for i in range(0, len(ship.route)):            #Aqui creamos la posicion de los vertices en base a nuestra curva
                tupla += (ship.route[i][0], ship.route[i][1], ship.route[i][2])
            lines.position[:] = tupla                      #asignamos las tuplas creadas como la posicion
            lines.draw(pyglet.gl.GL_LINES)                           

    glUseProgram(controller.pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "projection"), 1, GL_TRUE, camera.projection)
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "viewPosition"), camera.at[0], camera.at[1], camera.at[2])
    glEnable(GL_DEPTH_TEST)
    sg.drawSceneGraphNode(escenario, controller.pipeline, "model")
    sg.drawSceneGraphNode(piso, controller.pipeline, "model")
    sg.drawSceneGraphNode(sombras, controller.pipeline, "model")
    sg.drawSceneGraphNode(escuadron, controller.pipeline, "model")

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()