import numpy
import random
from collections import deque

def tuple_sub(t1, t2):
    return tuple(a - b for a, b in zip(t1, t2))

def tuple_add(t1, t2):
    return tuple(a + b for a, b in zip(t1, t2))

def tuple_invert(t):
    return tuple(-a for a in t)

class Labyrinth:
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        self.map = numpy.zeros((self.width, self.height), dtype=numpy.uint8)

    directions = [
        (-1, 0), # left
        (1, 0),  # right
        (0, 1), # up
        (0, -1)   # down
    ]
    def strToDir(s):
        if s == 'left':
            return 0
        elif s == 'right':
            return 1
        elif s == 'up':
            return 2
        elif s == 'down':
            return 3

    def reverseDir(dir):
        if dir == 0:
            return 1
        if dir == 1:
            return 0
        if dir == 2:
            return 3
        if dir == 3:
            return 2
            
    def isWall(self, p1, p2):
        point_dist = tuple_sub(p1, p2)
        return (self.map[p1] & (1 << (Labyrinth.directions.index(point_dist)))) == 0

    def isWallDir(self, p1, dir):
        dir = Labyrinth.strToDir(dir)
        return (self.map[p1] & (1 << (dir))) == 0
    
    def addWall(self, p1, p2):
        point_dist = tuple_sub(p1, p2)
        self.map[p1] = self.map[p1] & ~(1 << Labyrinth.directions.index(point_dist))
        point_dist = tuple_invert(point_dist)
        self.map[p2] = self.map[p2] & ~(1 << Labyrinth.directions.index(point_dist))

    def addWallDir(self, p1, dir):
        dir = strToDir(dir)
        self.map[p1] = self.map[p1] & ~(1 << dir)
        dir = reverseDir(dir)
        self.map[p2] = self.map[p2] & ~(1 << dir)

    def removeWall(self, p1, p2):
        try:
            point_dist = tuple_sub(p1, p2)
            self.map[p1] = self.map[p1] | (1 << Labyrinth.directions.index(point_dist))
            point_dist = tuple_invert(point_dist)
            self.map[p2] = self.map[p2] | (1 << Labyrinth.directions.index(point_dist))
        except:
            pass
        
    def generate(self, starting_point):
        stack = deque()
        stack.append(starting_point)
        visited = set([starting_point])

        while len(stack) != 0:
            current_cell = stack.pop()
            cells = []
            for i in range(4):
                cell = tuple_add(current_cell, Labyrinth.directions[i])
                if not cell in visited and cell[0] in range(self.width) and cell[1] in range(self.height):
                    cells.append(cell)
            if len(cells) != 0:
                stack.append(current_cell)
                next_cell = random.choice(cells)
                self.removeWall(current_cell, next_cell)
                visited.add(next_cell)
                stack.append(next_cell)

        number_of_wall_to_destroy = int(self.width*self.height/10)
        for i in range(number_of_wall_to_destroy):
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            for j in range(4):
                to_delete = random.randint(0, 2)
                if to_delete in range(2):
                    self.removeWall((x,y), tuple_add((x,y), Labyrinth.directions[to_delete]))
            
    def printMap(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.map[j][i], end=' ')
            print()

