from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from light_setup import setup_point_light
from direct.task import Task
from panda3d.core import Vec3, Vec2
from GameObjects import *

from GameObjects import *

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Kamera und Background
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -275, 150)
        self.cam.setP(-30)

        # Grundplatte
        self.floor = self.loader.loadModel("../Models/ground")
        self.floor.setPos(0, 0, -0.5)
        self.floor.setScale(0.5)
        self.floor.reparentTo(self.render)

        # Window
        properties = WindowProperties()
        properties.setSize(2000, 1200)
        self.win.requestProperties(properties)

        # Licht
        setup_point_light(self.render, (30, 0, 100))

        #Koordinaten Eckpunkte (Test)
        print(self.floor.getTightBounds())

        # Update Loop Registrierung
        self.updateTask = self.taskMgr.add(self.update, "update")

        # Objekte Spawnen
        self.rabbits = []
        self.spawn_rabbits(10)

    def update(self, task):
        [rabbit.update() for rabbit in self.rabbits]
        return task.cont

    def spawn_rabbits(self, count):
        while count != 0:
            self.rabbits.append(Rabbit(Vec3(5, 0, 0), 0.1))
            count = count - 1

game = Game()
game.run()
