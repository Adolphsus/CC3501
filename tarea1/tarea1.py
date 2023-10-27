import pyglet
import numpy as np
import random
import ae

window = pyglet.window.Window(1200,900, 'Tarea 1: Star Fox 2D - AAP', vsync = True, resizable= False)
icon2 = pyglet.image.load('Sflogo32.png')
window.set_icon(icon2)
batch = pyglet.graphics.Batch()
pyglet.options['audio'] = ('openal', 'pulse', 'xaudio2', 'directsound', 'silent')
bg = pyglet.media.load('corneria.wav') #recomiendo bajar el sonido

class Ship:
    def __init__(self):
        self.body1 = pyglet.shapes.Triangle(x=575, y=475, x2=625, y2= 475, x3=600, y3= 587.5,
                                       color=(229, 229, 229), batch=batch)
        self.body2 = pyglet.shapes.Triangle(x=575, y=425, x2=625, y2= 425, x3=600, y3= 350,
                                        color=(229, 229, 229), batch=batch)
        self.body3 = pyglet.shapes.Rectangle(x=575, y=425, width=50, height=50,
                                        color=(229, 229, 229), batch=batch)
        self.cabin = pyglet.shapes.Rectangle(x=582.5, y=425, width=35, height=15, 
                                        color=(0, 0, 0, 200), batch=batch)
        self.cabin2 = pyglet.shapes.Triangle(x=582.5, y=440, x2=617.5, y2=440, x3=600, y3=507.5,
                                        color=(0, 0, 0, 200), batch=batch)
        self.union_right = pyglet.shapes.Rectangle(x=625, y=425, width=25, height=50,
                                        color=(100,100,100), batch=batch)
        self.union_left= pyglet.shapes.Rectangle(x=550, y=425, width=25, height=50,
                                        color=(100,100,100), batch=batch) 
        self.wing_right1 = pyglet.shapes.Rectangle(x=637.5, y=412.5, width=25, height=75,
                                        color=(0,53,255), batch=batch)
        self.wing_right2 = pyglet.shapes.Triangle(x=637.5, y=487.5, x2=662.5, y2=487.5, x3=662.5, y3= 562.5,
                                        color=(0,53,255),batch=batch)
        self.wing_right3 = pyglet.shapes.Triangle(x=637.5, y=412.5, x2=662.5, y2=412.5, x3=662.5, y3= 350,
                                        color=(0,53,255),batch=batch)
        self.wing_left1 = pyglet.shapes.Rectangle(x=537.5, y=412.5, width=25, height=75,
                                        color=(0,53,255), batch=batch)
        self.wing_left2 = pyglet.shapes.Triangle(x=537.5, y=412.5, x2=562.5, y2=412.5, x3=537.5, y3= 350,
                                        color=(0,53,255),batch=batch)
        self.wing_left3 = pyglet.shapes.Triangle(x=537.5, y=487.5, x2=562.5, y2=487.5, x3=537.5, y3= 562.5,
                                        color=(0,53,255), batch=batch)
        self.wing_right4= pyglet.shapes.Triangle(x=662.5, y=412.5, x2=662.5, y2=487.5, x3= 712.5, y3= 412.5,
                                        color=(229, 229, 229),batch=batch)
        self.wing_right5= pyglet.shapes.Rectangle(x=662.5, y=412.5, width=50, height=37.5,
                                        color=(229,229,229),batch=batch)
        self.wing_right6= pyglet.shapes.Triangle(x=712.5, y=412.5, x2=712.5, y2=450, x3=762.5, y3= 400,
                                        color=(255,223,0),batch=batch)
        self.wing_left4= pyglet.shapes.Triangle(x=537.5, y=412.5, x2=537.5, y2=487.5, x3= 487.5, y3= 412.5,
                                        color=(229, 229, 229),batch=batch)
        self.wing_left5= pyglet.shapes.Rectangle(x=487.5, y=412.5, width=50, height=37.5,
                                        color=(229,229,229),batch=batch)
        self.wing_left6= pyglet.shapes.Triangle(x=487.5, y=412.5, x2=487.5, y2=450, x3=437.5, y3= 400,
                                        color=(255,223,0),batch=batch)
        self.detail = pyglet.shapes.Circle(600, 400, radius=12, 
                                        color=(220,31,0, 150), batch=batch)

class Ship1:
    def __init__(self):
        self.body1 = pyglet.shapes.Triangle(x=275, y=175, x2=325, y2= 175, x3=300, y3= 287.5,
                                       color=(229, 229, 229), batch=batch)
        self.body2 = pyglet.shapes.Triangle(x=275, y=125, x2=325, y2= 125, x3=300, y3= 50,
                                        color=(229, 229, 229), batch=batch)
        self.body3 = pyglet.shapes.Rectangle(x=275, y=125, width=50, height=50,
                                        color=(229, 229, 229), batch=batch)
        self.cabin = pyglet.shapes.Rectangle(x=282.5, y=125, width=35, height=15, 
                                        color=(0, 0, 0, 200), batch=batch)
        self.cabin2 = pyglet.shapes.Triangle(x=282.5, y=140, x2=317.5, y2=140, x3=300, y3=200,
                                        color=(0, 0, 0, 200), batch=batch)
        self.union_right = pyglet.shapes.Rectangle(x=325, y=125, width=25, height=50,
                                        color=(100,100,100), batch=batch)
        self.union_left= pyglet.shapes.Rectangle(x=250, y=125, width=25, height=50,
                                        color=(100,100,100), batch=batch) 
        self.wing_right1 = pyglet.shapes.Rectangle(x=337.5, y=112.5, width=25, height=75,
                                        color=(0,53,255), batch=batch)
        self.wing_right2 = pyglet.shapes.Triangle(x=337.5, y=187.5, x2=362.5, y2=187.5, x3=362.5, y3= 262.5,
                                        color=(0,53,255),batch=batch)
        self.wing_right3 = pyglet.shapes.Triangle(x=337.5, y=112.5, x2=362.5, y2=112.5, x3=362.5, y3= 50,
                                        color=(0,53,255),batch=batch)
        self.wing_left1 = pyglet.shapes.Rectangle(x=237.5, y=112.5, width=25, height=75,
                                        color=(0,53,255), batch=batch)
        self.wing_left2 = pyglet.shapes.Triangle(x=237.5, y=187.5, x2=262.5, y2=187.5, x3=237.5, y3= 262.5,
                                        color=(0,53,255),batch=batch)
        self.wing_left3 = pyglet.shapes.Triangle(x=237.5, y=112.5, x2=262.5, y2=112.5, x3=237.5, y3= 50,
                                        color=(0,53,255), batch=batch)
        self.wing_right4= pyglet.shapes.Triangle(x=237.5, y=112.5, x2=187.5, y2=112.5, x3= 237.5, y3= 187.5,
                                        color=(229, 229, 229),batch=batch)
        self.wing_right5= pyglet.shapes.Rectangle(x=187.5, y=112.5, width=50, height=37.5,
                                        color=(229,229,229),batch=batch)
        self.wing_right6= pyglet.shapes.Triangle(x=137.5, y=100, x2=187.5, y2=112.5, x3=187.5, y3= 150,
                                        color=(255,223,0),batch=batch)
        self.wing_left4= pyglet.shapes.Triangle(x=362.5, y=112.5, x2=362.5, y2=187.5, x3= 412.5, y3= 112.5,
                                        color=(229, 229, 229),batch=batch)
        self.wing_left5= pyglet.shapes.Rectangle(x=362.5, y=112.5, width=50, height=37.5,
                                        color=(229,229,229),batch=batch)
        self.wing_left6= pyglet.shapes.Triangle(x=412.5, y=112.5, x2=412.5, y2=150, x3=462.5, y3= 100,
                                        color=(255,223,0),batch=batch)
        self.detail = pyglet.shapes.Circle(300, 100, radius=12, 
                                        color=(73,255,0, 150), batch=batch)  

class Ship2:
    def __init__(self):
        self.body1 = pyglet.shapes.Triangle(x=875, y=175, x2=925, y2= 175, x3=900, y3= 287.5,
                                       color=(229, 229, 229), batch=batch)
        self.body2 = pyglet.shapes.Triangle(x=875, y=125, x2=925, y2= 125, x3=900, y3= 50,
                                        color=(229, 229, 229), batch=batch)
        self.body3 = pyglet.shapes.Rectangle(x=875, y=125, width=50, height=50,
                                        color=(229, 229, 229), batch=batch)
        self.cabin = pyglet.shapes.Rectangle(x=882.5, y=125, width=35, height=15, 
                                        color=(0, 0, 0, 200), batch=batch)
        self.cabin2 = pyglet.shapes.Triangle(x=882.5, y=140, x2=917.5, y2=140, x3=900, y3=200,
                                        color=(0, 0, 0, 200), batch=batch)
        self.union_right = pyglet.shapes.Rectangle(x=925, y=125, width=25, height=50,
                                        color=(100,100,100), batch=batch)
        self.union_left= pyglet.shapes.Rectangle(x=850, y=125, width=25, height=50,
                                        color=(100,100,100), batch=batch) 
        self.wing_right1 = pyglet.shapes.Rectangle(x=937.5, y=112.5, width=25, height=75,
                                        color=(0,53,255), batch=batch)
        self.wing_right2 = pyglet.shapes.Triangle(x=937.5, y=187.5, x2=962.5, y2=187.5, x3=962.5, y3= 262.5,
                                        color=(0,53,255),batch=batch)
        self.wing_right3 = pyglet.shapes.Triangle(x=937.5, y=112.5, x2=962.5, y2=112.5, x3=962.5, y3= 50,
                                        color=(0,53,255),batch=batch)
        self.wing_left1 = pyglet.shapes.Rectangle(x=837.5, y=112.5, width=25, height=75,
                                        color=(0,53,255), batch=batch)
        self.wing_left2 = pyglet.shapes.Triangle(x=837.5, y=187.5, x2=862.5, y2=187.5, x3=837.5, y3= 262.5,
                                        color=(0,53,255),batch=batch)
        self.wing_left3 = pyglet.shapes.Triangle(x=837.5, y=112.5, x2=862.5, y2=112.5, x3=837.5, y3= 50,
                                        color=(0,53,255), batch=batch)
        self.wing_right4= pyglet.shapes.Triangle(x=837.5, y=112.5, x2=787.5, y2=112.5, x3= 837.5, y3= 187.5,
                                        color=(229, 229, 229),batch=batch)
        self.wing_right5= pyglet.shapes.Rectangle(x=787.5, y=112.5, width=50, height=37.5,
                                        color=(229,229,229),batch=batch)
        self.wing_right6= pyglet.shapes.Triangle(x=737.5, y=100, x2=787.5, y2=112.5, x3=787.5, y3= 150,
                                        color=(255,223,0),batch=batch)
        self.wing_left4= pyglet.shapes.Triangle(x=962.5, y=112.5, x2=962.5, y2=187.5, x3= 1012.5, y3= 112.5,
                                        color=(229, 229, 229),batch=batch)
        self.wing_left5= pyglet.shapes.Rectangle(x=962.5, y=112.5, width=50, height=37.5,
                                        color=(229,229,229),batch=batch)
        self.wing_left6= pyglet.shapes.Triangle(x=1012.5, y=112.5, x2=1012.5, y2=150, x3=1062.5, y3= 100,
                                        color=(255,223,0),batch=batch)
        self.detail = pyglet.shapes.Circle(900, 100, radius=12, 
                                        color=(0,131,255, 150), batch=batch)          

def stars(num_stars): #para crear las estrellas me base en la documentacion de pyglet, mas especificamente en la que se crea un juego
    star = []         #y se hace uso de asteroides que caen hacia la nave
    for i in range(num_stars):
        star_x = random.randint(0, 1200)
        star_y = random.randint(1000, 1200)
        new_star = ae.PhysicalObject(x=star_x, y= star_y, x2=star_x, y2=star_y - 50, width=4, batch=batch)
        new_star.velocity_y = 5
        star.append(new_star)
    return star

cosmos = stars(20)

def update():
    for obj in cosmos:
        obj.x = random.randint(0, 1200)
        obj.update()

  
ship = Ship()
ship1 = Ship1()
ship2 = Ship2()

@window.event
def on_draw():
    window.clear()
    update()
    batch.draw()


if __name__ == '__main__':
    bg.play()
    pyglet.app.run() 