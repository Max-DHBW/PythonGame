from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(2000, 1200)
        self.win.requestProperties(properties)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

game = Game()
game.run()
