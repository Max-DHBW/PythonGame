import math
from direct.actor.Actor import Actor
from panda3d.core import Vec3, Vec2
import random as rand

class Grass():
    def __init__(self, pos):
        self.grass = Actor("../Models/grass", {})
        self.grass.reparentTo(render)
        self.grass.setPos(pos)

        self.was_eaten = False

    def return_pos(self):
        return self.grass.getPos()

    def delete(self):
        if self.grass is not None:
            self.grass.cleanup()
            self.grass.removeNode()
            self.grass = None

class Rabbit():
    def __init__(self, pos, speed, health):
        self.rabbit = Actor("../Models/rabbit", {})
        self.rabbit.reparentTo(render)
        self.rabbit.setPos(pos)

        self.speed = speed
        self.health = health
        self.max_health = health
        self.visibility_range = 50

        # Initialisirung
        self.direction = Vec3(0, 0, 0)
        self.direction_next_direction = (0, 1, 2, 3)
        self.has_moved = rand.randint(20, 50)
        self.random_direction(self.direction_next_direction)


    def update(self, food_sources):

        distance_min = 10000
        index = -1

        for i in range(len(food_sources)):
            pos_rabbit = self.rabbit.getPos()
            pos_grass = food_sources[i].return_pos()
            connection_vektor = pos_grass - pos_rabbit
            distance = math.sqrt(connection_vektor.getX()**2 + connection_vektor.getY()**2)

            if distance < distance_min:
                if not food_sources[i].was_eaten:
                    index = i
                    distance_min = distance

        # Rabbit sieht kein Grass wegen der Sichtweite
        if distance_min > 20 or index < 0:
            self.rabbit.setPos(self.move())
            self.health = self.health - 1
            return

        # Rabbit steht auf dem Grass und isst das Grass
        if distance_min == 0:
            self.health = self.max_health
            food_sources[index].was_eaten = True
        # Rabbit steht nicht auf dem Grass, sieht das Grass aber
        else:
            self.health = self.health - 1
            # Distanz ist kleiner als der Schritt, führt dazu, dass Rabbit auf die Position vom Grass geht
            if distance_min <= self.speed:
                self.rabbit.setPos(food_sources[index].return_pos())
            # Rabbit läuft in die Richtung des Grasses
            else:
                pos_rabbit = self.rabbit.getPos()
                pos_grass = food_sources[index].return_pos()

                vektor = pos_grass - pos_rabbit
                norm_fac = self.speed / distance_min

                x = vektor.getX() * norm_fac
                y = vektor.getY() * norm_fac
                vektor_norm = Vec3(x, y, 0)

                self.rabbit.setPos(self.rabbit.getPos() + vektor_norm)

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
