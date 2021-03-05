from warehouse.game import Game
from warehouse.game import Vehicle
from warehouse.game import Item
from server.firebase import Firebase
from algorithm.dijktra import Dijkstra
import pygame as p
from itertools import chain
import queue as q

FPS = 20
targetNode = 0
sourceNode = 0

if __name__ == "__main__":

    # initial ##############################
    game = Game()
    firebase = Firebase()

    init_pos_x = 30
    init_pos_y = 20

    numberOfVehicles = 2
    vehicle1 = []
    # vehicle = Vehicle(init_pos_x, init_pos_y)
    # vehicle1.append(vehicle)
    #
    # vehicle = Vehicle(30, 220)
    # vehicle1.append(vehicle)
    vehicle = Vehicle("00", game.my_dict)
    vehicle1.append(vehicle)
    vehicle = Vehicle("02", game.my_dict)
    vehicle1.append(vehicle)
    # vehicle = Vehicle("03", game.my_dict)
    # vehicle1.append(vehicle)
    #########################################

    # load multiple robot based on the give position
    for i in range(0, numberOfVehicles):
        game.load_vehicles(vehicle1[i])

    dj = Dijkstra(game.adjacency_matrix)
    dj.calculate()
    print(dj.path)


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
                # setup goal position with mouse
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
            # clear path after press 0
            path = []

            sourceNode = []
            for i in range(0, numberOfVehicles):
                print("Vehicle init position {}".format(vehicle1[i].currentCoorPos))
                sourceNode.append(vehicle1[i].initValue)

            temp_init_path = []
            for i in range(0, numberOfVehicles):
                temp_init_path = dj.getBestPath(sourceNode[i], targetNode)
                if temp_init_path not in path:
                    path.append(temp_init_path)

            print("get best path for all sourceNode(vehicles)")
            print(path)
            newpath = []
            for current_path in path:
                if game.map_path(current_path) not in newpath:
                    newpath.append(game.map_path(current_path))

            # print("After convert {}".format(newpath[0]))
            shortest_path = newpath

            temp_path = shortest_path
            # color_shortest_path(screen, shortest_path)
        if flag_path:
            if not temp_path:
                flag_path = False
            else:
                for i in range(0, len(temp_path)):
                    # print("temp_path {}".format(temp_path[tp]))
                    game.color_shortest_path(temp_path[i])

                    # moving robot in grid
                    # vehicle1[i].x, vehicle1[i].y, temp_path[i], current_node = vehicle1[i].move(vehicle1[i].x, vehicle1[i].y, temp_path[i], game.my_dict)

                # firebase.update_node_data(current_node)

        game.update()
        game.draw_board()
        for i in range(0, numberOfVehicles):
            game.load_vehicles(vehicle1[i])

        if hasItem:
            game.load_item(item1)

        game.tick(FPS)
