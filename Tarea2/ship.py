import libs.scene_graph as sg
from OpenGL.GL import *
import libs.easy_shaders as es
import libs.transformations as tr
from libs.assets_path import getAssetPath
from libs.gpu_shape import createGPUShape
from libs.obj_handler import read_OBJ2

def createShip(pipeline) -> sg.SceneGraphNode:
    
    ship = createGPUShape(pipeline, read_OBJ2(getAssetPath('starfox.obj')))
    ship.texture = es.textureSimpleSetup(getAssetPath("body.png"), 
                                         GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    return ship

def createsombra(pipeline) -> sg.SceneGraphNode:
    
    ship = createGPUShape(pipeline, read_OBJ2(getAssetPath('starfox.obj')))
    ship.texture = es.textureSimpleSetup(getAssetPath("sombratextura.jpg"), 
                                         GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    return ship


#The Basic Model and SytarFox ASAULT are originally owned by Nintendo and NAMCO

#License
#CC Attribution