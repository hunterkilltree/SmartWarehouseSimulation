from warehouse.game import Game
from warehouse.game import Vehicle
from warehouse.game import Item
import pygame as p
import queue as q

FPS = 90

MAX = 100
INF = int(1e9)
path = []
dist = []
graph = []


class Node:
    def __init__(self, id, dist, name):
        self.dist = dist
        self.id = id
        self.name = name

    def __lt__(self, other):
        return self.dist <= other.dist


def dijkstra(s):
    pq = q.PriorityQueue()
    pq.put(Node(s, 0, "init"))
    dist[s] = 0
    while not pq.empty():
        top = pq.get()
        u = top.id
        w = top.dist
        for neighbor in graph[u]:
            if w + neighbor.dist < dist[neighbor.id]:
                dist[neighbor.id] = w + neighbor.dist
                pq.put(Node(neighbor.id, dist[neighbor.id], neighbor.name))
                path[neighbor.id] = u


def get_path(int_to_node):
    newdict = {}
    for i in range(0, len(int_to_node)):
        newdict.update({int_to_node[i]: dist[i]})

    # finaldict = dict(sorted(newdict.items(), key=lambda item: item[1]))
    finaldict = newdict
    print(finaldict)

    mypath = []
    for key in finaldict.keys():
        mypath.append(key)

    return mypath


def _getBestPath(frm, to, th):
    print(th)
    path_ = th[frm]
    lastNode = path_[to]
    th.append(lastNode)
    if lastNode == frm:
        return th
    else:
        return _getBestPath(frm, lastNode, th)

def getBestPath(frm, to):
    return [i for i in reversed(_getBestPath(frm, to, [to]))]

def warm_up(game, matrix, s):
    n = len(matrix[0])
    global graph
    global dist
    global path

    graph = [[] for i in range(n + 5)]
    dist = [INF for i in range(n + 5)]
    path = [-1 for i in range(n + 5)]

    for i in range(0, n):
        for j in range(0, n):
            if matrix[i][j] > 0:
                name = str(i) + str(j)
                graph[i].append(Node(j, matrix[i][j], name))

    dijkstra(s)

    mypath = get_path(game.list_node)
    print("path")
    print(path)
    # from point to point
    getBestPath(0, 5)
    # print(testPath)

    # target = "21"
    # newpath1 = game.map_path(path, target)
    # print(newpath1)

    return mypath


if __name__ == "__main__":
    game = Game()

    init_pos_x = 30
    init_pos_y = 20

    vehicle1 = Vehicle(init_pos_x, init_pos_y)
    game.load_vehicles(vehicle1)

    # shortest_path = ["10", "11", "12", "02"]  # test
    # shortest_path = dijkstra (adjacency_matrix)
    # dijkstra(adjacency_matrix)
    shortest_path = warm_up(game, game.adjacency_matrix, 0)

    flag_path = False
    temp_path = []

    hasItem = False
    col = 0
    row = 0

    while game.running == 1:
        for event in p.event.get():
            if event.type == p.QUIT:
                game.running = 0
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] - 10
                row = location[1] - 10

                hasItem = True

        key = p.key.get_pressed()

        if key[p.K_0]:
            flag_path = True
            temp_path = shortest_path
            # color_shortest_path(screen, shortest_path)
        if flag_path:
            game.color_shortest_path(temp_path)
            vehicle1.x, vehicle1.y, temp_path = vehicle1.move(vehicle1.x, vehicle1.y, temp_path, game.my_dict)

            if not temp_path:
                flag_path = False

        game.update()
        game.draw_board()
        game.load_vehicles(vehicle1)
        if hasItem:
            game.load_item(Item(col, row))

        game.tick(FPS)
