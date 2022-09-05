from panda3d.core import Vec3, Vec2
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode


class GameObject():
    def __init__(self, pos, modelName, modelAnims):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(self.render)
        self.actor.setPos(pos)

    def update(self):
        pass

    def delete(self):
        pass


class Plant(GameObject):
    pass


class Bunny(GameObject):
    pass
