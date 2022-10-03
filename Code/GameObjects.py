from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3, Vec2
import random as rand

class Rabbit():
    def __init__(self, pos, speed):
        self.rabbit = Actor("../Models/rabbit", {})
        self.rabbit.reparentTo(render)
        self.rabbit.setPos(pos)
        self.speed = speed

        # Initialisirung
        self.direction = Vec3(0, 0, 0)
        self.direction_next_direction = (0, 1, 2, 3)
        self.has_moved = rand.randint(20, 50)
        self.random_direction(self.direction_next_direction)


    def update(self):
        self.rabbit.setPos(self.move())

    def move(self):
        vector_pos = self.rabbit.getPos()

        if self.has_moved == 0:
            self.random_direction(self.direction_next_direction)
            self.has_moved = rand.randint(20, 50)
        else:
            self.has_moved = self.has_moved - 1

        vector_pos_destiny = vector_pos + self.direction
        return self.check_if_map_border(vector_pos_destiny, vector_pos)

    def check_if_map_border(self, vector, vector_pos):
        if vector.getX() >= 95:
            self.random_direction((1, 2, 3))
            self.has_moved = rand.randint(20, 50)
            return vector_pos + self.direction
        if vector.getX() <= -95:
            self.random_direction((0, 2, 3))
            self.has_moved = rand.randint(20, 50)
            return vector_pos + self.direction
        if vector.getY() >= 95:
            self.random_direction((0, 1, 2))
            self.has_moved = rand.randint(20, 50)
            return vector_pos + self.direction
        if vector.getY() <= -95:
            self.random_direction((0, 1, 3))
            self.has_moved = rand.randint(20, 50)
            return vector_pos + self.direction

        return vector

    def random_direction(self, choice):
        number = rand.choice(choice)
        match number:
            case 0:
                self.direction = Vec3(self.speed, 0, 0)
                self.direction_next_direction = (0, 2, 3)
                self.rabbit.setH(0)
            case 1:
                self.direction = Vec3(-self.speed, 0, 0)
                self.direction_next_direction = (1, 2, 3)
                self.rabbit.setH(180)
            case 2:
                self.direction = Vec3(0, -self.speed, 0)
                self.direction_next_direction = (2, 0, 1)
                self.rabbit.setH(-90)
            case 3:
                self.direction = Vec3(0, self.speed, 0)
                self.direction_next_direction = (3, 0, 1)
                self.rabbit.setH(90)

    def delete(self):
        if self.rabbit is not None:
            self.rabbit.cleanup()
            self.rabbit.removeNode()
            self.rabbit = None
