import math
from direct.actor.Actor import Actor
from panda3d.core import Vec3
import random as rand


# Grundklasse für alle Objekte die gespawnt werden
class Object():
    def __init__(self, pos, model):
        self.actor = Actor(model, {})
        # Rendern wird als Fehler angezeigt, ist aber keiner
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

    # Alle Referenzen werden gelöscht und die Nodes (Panda3D hat ein Nodesystem) werden ebenfalls gelöscht
    def delete(self):
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None


class Grass(Object):
    def __init__(self, pos):
        Object.__init__(self, pos, "../Models/grass")

        self.was_eaten = False

    def return_pos(self):
        return self.actor.getPos()


class Rabbit(Object):
    def __init__(self, pos, speed, health):
        Object.__init__(self, pos, "../Models/rabbit")

        self.speed = speed
        self.health = health
        self.max_health = health
        self.visibility_range = 50

        # Initialisierung
        self.direction = Vec3(0, 0, 0)
        self.direction_next_direction = (0, 1, 2, 3)
        self.has_moved = rand.randint(20, 50)
        self.random_direction(self.direction_next_direction)

    def update(self, food_sources):

        distance_min = 10000
        index = -1

        # Pathfinding Algorithmus sucht das nächste Grass-Objekt (Die ganze Mathematik ist selbst geschrieben)
        for i in range(len(food_sources)):
            pos_rabbit = self.actor.getPos()
            pos_grass = food_sources[i].return_pos()
            connection_vektor = pos_grass - pos_rabbit
            distance = math.sqrt(connection_vektor.getX() ** 2 + connection_vektor.getY() ** 2)

            if distance < distance_min:
                if not food_sources[i].was_eaten:
                    index = i
                    distance_min = distance

        # Rabbit sieht kein Grass wegen der Sichtweite
        if distance_min > 20 or index < 0:
            self.actor.setPos(self.move())
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
                self.actor.setPos(food_sources[index].return_pos())
            # Rabbit läuft in die Richtung des Grasses
            else:
                pos_rabbit = self.actor.getPos()
                pos_grass = food_sources[index].return_pos()

                # Der Vektor muss auf die Geschwindigkeit des Hasen normiert werden
                vektor = pos_grass - pos_rabbit
                norm_fac = self.speed / distance_min

                x = vektor.getX() * norm_fac
                y = vektor.getY() * norm_fac
                vektor_norm = Vec3(x, y, 0)

                self.actor.setPos(self.actor.getPos() + vektor_norm)

    def move(self):
        vector_pos = self.actor.getPos()

        # Logik damit nicht alle Updates die Richtung aktualisiert wird
        if self.has_moved == 0:
            self.random_direction(self.direction_next_direction)
            self.has_moved = rand.randint(20, 50)
        else:
            self.has_moved = self.has_moved - 1

        vector_pos_destiny = vector_pos + self.direction
        return self.check_if_map_border(vector_pos_destiny, vector_pos)

    # Logik damit der Hase nicht aus dem Feld rausläuft
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

    # Gibt eine Direction ausgehend von der jetzigen zurück (keine 180 Grad Drehungen)
    def random_direction(self, choice):
        number = rand.choice(choice)
        match number:
            case 0:
                self.direction = Vec3(self.speed, 0, 0)
                self.direction_next_direction = (0, 2, 3)
                self.actor.setH(0)
            case 1:
                self.direction = Vec3(-self.speed, 0, 0)
                self.direction_next_direction = (1, 2, 3)
                self.actor.setH(180)
            case 2:
                self.direction = Vec3(0, -self.speed, 0)
                self.direction_next_direction = (2, 0, 1)
                self.actor.setH(-90)
            case 3:
                self.direction = Vec3(0, self.speed, 0)
                self.direction_next_direction = (3, 0, 1)
                self.actor.setH(90)
