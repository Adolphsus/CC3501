import pyglet
import random
from OpenGL.GL import *

from math import *
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))

import libs.transformations as tr
import libs.basic_shapes as bs
import libs.scene_graph as sg
import libs.easy_shaders as es
import libs.lighting_shaders as ls

from libs.gpu_shape import createGPUShape
from libs.obj_handler import read_OBJ2
from libs.assets_path import getAssetPath
from utils import createOFFShape
from ship import createShip, createsombra

class Controller(pyglet.window.Window):

    def __init__(self, width, height, tittle=f"Tarea 2 - Adolfo Arenas P"):
        super().__init__(width, height, tittle)
        self.pipeline = es.SimpleTextureModelViewProjectionShaderProgram()

width = 1280
height = 960
controller = Controller(width, height)
PERSPECTIVE_PROJECTION = 1
ORTOGRAPHIC_PROJECTION = 0

PROJECTIONS = [tr.ortho(-8, 8, -8, 8, 0.0001, 1000),
    tr.perspective(80, float(width)/float(height), 0.0001, 100)]

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

glClearColor(0.1, 0.1, 0.1, 1.0)

glUseProgram(controller.pipeline.shaderProgram)

#Aqui agregamos hijos de la clase Ship que creamos para formar nuestro escuadron
def crearEscuadron():

    shipNode1 = sg.SceneGraphNode('ship')
    shipNode1.transform = tr.matmul([tr.rotationY(np.deg2rad(180)), tr.uniformScale(0.8)])
    shipNode1.childs += [ship.shape]

    sombra = sg.SceneGraphNode('sombra')
    sombra.transform = tr.matmul([tr.translate(0,0.1,0), tr.scale(0.6,0.01,0.6), tr.rotationY(np.deg2rad(180))])
    sombra.childs += [ship.shapesombra]

    sombra1 = sg.SceneGraphNode('sombra1')
    sombra1.transform = tr.translate(ship.x, 0, ship.z)
    sombra1.childs += [sombra]

    shipNode2 = sg.SceneGraphNode('ship2')
    shipNode2.transform = tr.translate(2,0,3)
    shipNode2.childs += [shipNode1]

    sombra2 = sg.SceneGraphNode('sombra2')
    sombra2.transform = tr.translate(ship.x+2, 0, ship.z+3)
    sombra2.childs += [sombra]

    shipNode3 = sg.SceneGraphNode('ship3')
    shipNode3.transform = tr.translate(-2,0,3)
    shipNode3.childs += [shipNode1]

    sombra3 = sg.SceneGraphNode('sombra3')
    sombra3.transform = tr.translate(ship.x-2, 0, ship.z+3)
    sombra3.childs += [sombra]

    Escuadron = sg.SceneGraphNode('Escuadron')
    Escuadron.transform = tr.translate(0,0,0)
    Escuadron.childs += [shipNode1]
    Escuadron.childs += [sombra1]
    Escuadron.childs += [shipNode2]
    Escuadron.childs += [sombra2]
    Escuadron.childs += [shipNode3]
    Escuadron.childs += [sombra3]


    return Escuadron

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

#con esta funcion vamos moviendo el escuadron, segun la propiedades que le pusimos a la nave                                                                                             #¿como puedo combinar ambas para hacer traslacion mas rotacion y se mueva
                                                                                      # en el plano xz?
@controller.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        camera.set_projection(PERSPECTIVE_PROJECTION)
    if symbol == pyglet.window.key.O:
        camera.set_projection(ORTOGRAPHIC_PROJECTION)
    if symbol == pyglet.window.key.W:
        ship.velocity = -0.3
    if symbol == pyglet.window.key.S:
        ship.velocity = 0.1
    if symbol == pyglet.window.key.A:
        ship.rotationylocal = 0.2
    if symbol == pyglet.window.key.D:
        ship.rotationylocal = -0.2

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

@controller.event
def on_mouse_drag(x,y,dx,dy, buttons, modifiers):
    if buttons == pyglet.window.mouse.LEFT:            #pense que al apretar el left click y luego permitir que la nave se moviera
        if y > 460:                                    #era mas natural que me moviera siempre
            ship.altitude = 20*dy/960
        if y == 0:
            ship.altitude = 0
        elif y < 0:
            ship.altitude = -10*dy/960

escuadron = crearEscuadron()
piso = createFloor()
escenario = createScene()

def update(dt):
    escuadron.transform = tr.matmul([escuadron.transform, tr.rotationY(ship.rotationylocal), tr.translate(0, ship.altitude, ship.velocity)]) #esta se encarga de rotar mi nave sobre su eje y, ademas de trasladarla
    ship.x = sg.findPosition(escuadron,'Escuadron')[0][0]    #actualizamos los parametros de la posicion de la nave
    ship.y = sg.findPosition(escuadron, 'Escuadron')[1][0]
    ship.z = sg.findPosition(escuadron, 'Escuadron')[2][0]
    camera.eye[1] = ship.y+7
    camera.at[1] = ship.y
    camera.eye[0] = ship.x+5
    camera.at[0] = ship.x
    camera.eye[2] = ship.z+5 #Modificamos estos dos parametros para que la camara    
    camera.at[2] = ship.z 

@controller.event
def on_draw():
    controller.clear()
    view = tr.lookAt(
        camera.eye,
        camera.at,
        camera.up
    ) 
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "projection"), 1, GL_TRUE, camera.projection)
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "viewPosition"), camera.at[0], camera.at[1], camera.at[2])
    glEnable(GL_DEPTH_TEST)
    sg.drawSceneGraphNode(escuadron, controller.pipeline, "model")
    sg.drawSceneGraphNode(escenario, controller.pipeline, "model")
    sg.drawSceneGraphNode(piso, controller.pipeline, "model")

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()
