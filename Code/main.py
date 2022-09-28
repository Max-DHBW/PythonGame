from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from light_setup import setup_point_light

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -700, 60)

        self.floor = self.loader.loadModel("../Models/ground")
        self.floor.reparentTo(self.render)

        properties = WindowProperties()
        properties.setSize(2000, 1200)
        self.win.requestProperties(properties)

        setup_point_light(self.render, (30, 0, 100))

        #Koordinaten Eckpunkte
        #print(self.floor.getTightBounds())

game = Game()
game.run()
