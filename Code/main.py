from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from light_setup import setup_point_light

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

        # Update Loop Registrierung
        self.updateTask = self.taskMgr.add(self.update, "update")

        # Objekte Spawnen
        self.rabbits = []
        self.grasses = []
        # Anzahl der Rabbits und Grasses
        self.spawn_objects(40, 25)

    def update(self, task):
        for rabbit in self.rabbits:
            rabbit.update(self.grasses)
            if rabbit.health <= 0:
                rabbit.delete()
                self.rabbits.remove(rabbit)

        for grass in self.grasses:
            if grass.was_eaten:
                # Wenn etwas gegessen wurde, wird ein neuer Rabbit erzeugt
                speed = rand.choice((0.1, 0.15, 0.05))
                self.rabbits.append(Rabbit(grass.return_pos(), speed, rand.randint(200, 1000)))

                grass.delete()
                self.grasses.remove(grass)

                # Begrenzung damit nicht zu viel Grass auf der Fläche ist (zu viel Grass => viele Hasen => Lag)
                if len(self.grasses) < 15:
                    self.grasses.append(Grass(Vec3(rand.randint(-90, 90), rand.randint(-90, 90), 0)))

        return task.cont

    # Spawnt alle Hasen- und Grass-Objekte
    def spawn_objects(self, count_rabbits, count_grass):
        while count_rabbits != 0:
            speed = rand.choice((0.1, 0.15, 0.05))
            self.rabbits.append(Rabbit(Vec3(0, 0, 0), speed, rand.randint(200, 1000)))
            count_rabbits = count_rabbits - 1

        while count_grass != 0:
            self.grasses.append(Grass(Vec3(rand.randint(-90, 90), rand.randint(-90, 90), 0)))
            count_grass = count_grass - 1


# Startet das Programm
game = Game()
game.run()
