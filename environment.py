from warehouse.game import Game
from warehouse.game import Vehicle
from warehouse.game import Item
from server.firebase import Firebase
import pygame as p
from itertools import chain
import queue as q

FPS = 50


class Dijkstra:

    def __init__(self, input):
        self.input = input
        self.path = []

    def calculate(self):
        return [self.calculateFromOrigin(i) for i, v in enumerate(self.input)]

    def calculateFromOrigin(self, origin):
        distance = [-1 for i in range(len(self.input))]
        path = [-1 for i in range(len(self.input))]  # vector to get the best path

        # Distance from origin to itself is always 0
        distance.pop(origin)
        distance.insert(origin, 0)
        priority = list(range(len(self.input)))

        while True:
            if len(priority) == 0: break
            frm = self.getSmallestPossibleVertex(distance, priority)
            priority.remove(frm)
            options = self.getOptionList(self.input[frm])
            for [position, weight] in options:
                dist = distance[frm] + weight
                if distance[position] == -1 or dist < distance[position]:
                    distance.pop(position)
                    distance.insert(position, dist)
                    path.pop(position)
                    path.insert(position, frm)

        self.path.insert(origin, path)
        return distance

    def getSmallestPossibleVertex(self, distances, priority):
        smallestKey = -1
        smallestValue = -1
        for i, item in enumerate(distances):
            if (smallestValue == -1 or (item >= 0 and item < smallestValue)) and i in priority:
                smallestValue = item
                smallestKey = i
        return smallestKey

    def getOptionList(self, vector):
        return [[i, weight] for i, weight in enumerate(vector) if weight > 0]

    def getPath(self):
        return self.path

    def getBestPath(self, frm, to):
        return [i for i in reversed(self._getBestPath(frm, to, [to]))]

    def _getBestPath(self, frm, to, path):
        path_ = self.path[frm]
        lastNode = path_[to]
        path.append(lastNode)
        if (lastNode == frm):
            return path
        else:
            return self._getBestPath(frm, lastNode, path)


targetNode = 0
sourceNode = 0

if __name__ == "__main__":
    game = Game()
    firebase = Firebase()

    init_pos_x = 30
    init_pos_y = 20

    vehicle1 = Vehicle(init_pos_x, init_pos_y)
    game.load_vehicles(vehicle1)

    # shortest_path = ["10", "11", "12", "02"]  # test
    # shortest_path = dijkstra (adjacency_matrix)
    # dijkstra(adjacency_matrix)
    # shortest_path = warm_up(game, game.adjacency_matrix, 0)

    dj = Dijkstra(game.adjacency_matrix)
    dj.calculate()
    print(dj.path)
    # path = dj.getBestPath(0, targetNode)
    # newpath = game.map_path(path)
    # shortest_path = newpath
    path = []
    newpath = []
    shortest_path = []

    flag_path = False
    temp_path = []

    hasItem = False
    col = 0
    row = 0
    item1 = 0

    while game.running == 1:
        for event in p.event.get():
            if event.type == p.QUIT:
                game.running = 0
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] - 10
                row = location[1] - 10

                item1 = Item(location[0] - 10, location[1] - 10)
                print(item1.pos)

                # set target node
                index = 0
                posNearValue = 0
                for value in game.my_dict.values():
                    # sure bug here
                    if 0 <= abs(location[0] - value.x) <= 30 and \
                            0 <= abs(location[1] - value.y) <= 30:
                        targetNode = index
                    index = index + 1
                print(targetNode)
                hasItem = True

        key = p.key.get_pressed()

        if key[p.K_0]:
            flag_path = True
            ind = 0
            sourceNode = 0
            for value in game.my_dict.values():
                # sure bug here
                if 0 <= abs(vehicle1.x - value.x) <= 30 and \
                        0 <= abs(vehicle1.y - value.y) <= 30:
                    sourceNode = ind
                ind = ind + 1
            print(sourceNode)

            path = dj.getBestPath(sourceNode, targetNode)
            newpath = game.map_path(path)
            shortest_path = newpath

            temp_path = shortest_path
            # color_shortest_path(screen, shortest_path)
        if flag_path:
            if not temp_path:
                flag_path = False
            else:
                game.color_shortest_path(temp_path)


                vehicle1.x, vehicle1.y, temp_path, current_node = vehicle1.move(vehicle1.x, vehicle1.y, temp_path, game.my_dict)

                # firebase.update_node_data(current_node)

        game.update()
        game.draw_board()
        game.load_vehicles(vehicle1)
        if hasItem:
            game.load_item(item1)

        game.tick(FPS)
