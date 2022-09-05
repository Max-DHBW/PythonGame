from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(2000, 1200)
        self.win.requestProperties(properties)
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -700, 60)

        self.floor = self.loader.loadModel("../Models/ground")
        self.floor.reparentTo(self.render)

        #Koordinaten Eckpunkte
        #print(self.floor.getTightBounds())

game = Game()
game.run()
