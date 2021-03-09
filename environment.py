from warehouse.game import Game
from warehouse.game import Vehicle
from warehouse.game import Item
from server.firebase import Firebase
from algorithm.dijktra import Dijkstra
import pygame as p
from itertools import chain
# store the task list , work as FIFO
import queue as task
import random

task_list = task.Queue()
FPS = 50


def remove_path(vehicle_to_be_removed, item_to_be_removed, list_temp_all_best_path):
    for cp in list_temp_all_best_path[:]:
        if vehicle_to_be_removed in cp or item_to_be_removed in cp:
            list_temp_all_best_path.remove(cp)
    return list_temp_all_best_path


def main():
    # initial ##############################
    game = Game()
    # TODO: remove firebase for simuation
    # firebase = Firebase()
    # TODO: remove firebase for simuation ###

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
    vehicle_move = [] # for animation

    # hasItem = False
    # add Item task
    numberOfItems = 2
    # simple form
    item = []
    # test assign nearly robot
    item.append(Item("12", game.my_dict))

    # item.append(Item("30", game.my_dict))
    item.append(Item("32", game.my_dict))
    # item.append(Item("34", game.my_dict))
    #
    # item.append(Item("04", game.my_dict))
    # item.append(Item("14", game.my_dict))
    # item.append(Item("44", game.my_dict))

    # queue form
    # test assign nearly robot
    task_list.put(Item("12", game.my_dict))

    # task_list.put(Item("30", game.my_dict))
    task_list.put(Item("32", game.my_dict))
    # task_list.put(Item("34", game.my_dict))
    #
    # task_list.put(Item("04", game.my_dict))
    # task_list.put(Item("14", game.my_dict))
    # task_list.put(Item("44", game.my_dict))

    while game.running == 1:
        for event in p.event.get():
            if event.type == p.QUIT:
                game.running = 0
            if event.type == p.KEYDOWN:
                key = p.key.get_pressed()
                if key[p.K_0]:
                    flag_path = True

                    # TODO: find free vehicles to assign task

                    # TODO: find free vehicles to assign task ###

                    # TODO: get the best path for all free robot
                    # clear path after press 0

                    sourceNode = []
                    # get all free robot
                    for i in range(0, numberOfVehicles):
                        if not vehicle1[i].hasTask:
                            print("Vehicle init position {}".format(vehicle1[i].currentCoorPos))
                            sourceNode.append(vehicle1[i])

                    temp_all_best_path = []  # list
                    path = []

                    # explain in notebook
                    # for i in range(0, numberOfVehicles):
                    #     for j in range(0, numberOfItems):
                    #         # temp_all_best_path = dj.getBestPath(sourceNode[i], item[j].initValue)
                    #         if temp_all_best_path not in path:
                    #             path.append(temp_all_best_path)
                    # print("len of sourNode {} ".format(len(sourceNode)))
                    # for i in range(0, len(sourceNode)):
                    #     if not task_list.empty():
                    #         temp_all_best_path = dj.getBestPath(sourceNode[i], task_list.get().initValue)
                    #         if temp_all_best_path not in path:
                    #             path.append(temp_all_best_path)

                    # probability: path is the combination (freeRobot, number_task)
                    process_task = []
                    for i in range(0, len(sourceNode)):  # number of free robot
                        if not task_list.empty():
                            process_task.append(task_list.get())

                    # conduct the combination
                    for i in range(0, len(sourceNode)):
                        for j in range(0, len(process_task)):
                            print("Number of task{}{}".format(i, j))
                            path = dj.getBestPath(sourceNode[i].initValue, process_task[j].initValue)
                            # if path not in temp_all_best_path.values(): #  remove this line???
                            # temp_all_best_path.update({path: vehicle1[i]})
                            temp_all_best_path.append((vehicle1[i], process_task[j], path))

                    print("get best path for all sourceNode(vehicles)")
                    print(temp_all_best_path)
                    # TODO: get the best path for all free robot ###

                    # TODO: robot will move to object
                    # pick random
                    list_temp_all_best_path = temp_all_best_path  # should remove

                    print(list_temp_all_best_path)
                    current_path = []  # this is the array of object (Vehicle, path)
                    for i in range(0, len(sourceNode)):  # number of free robot
                        if list_temp_all_best_path != []:
                            current_choice = random.choice(list_temp_all_best_path)  # get random robot for given item path
                            print("current path {}".format(list_temp_all_best_path))
                            if current_choice not in current_path:
                                current_path.append(current_choice)  # add to array
                                # vehicle to be removed
                                vehicle_to_be_removed = current_choice[0]
                                item_to_be_removed = current_choice[1]
                                list_temp_all_best_path = remove_path(vehicle_to_be_removed, item_to_be_removed, list_temp_all_best_path)

                    # convert to node
                    # print(current_path)
                    new_path = []

                    for cp in current_path:
                        print(cp)
                        if game.map_path(cp[2]) not in new_path:  # remove this line???
                            new_path.append([cp[0], cp[1], game.map_path(cp[2])])


                    temp_path = new_path


                    # TODO: robot will move to object ###

                # TODO:  stupid reset
                if key[p.K_9]:
                    print("Reset")
                    main()
                # TODO:  stupid reset ###

        if flag_path:
            if not temp_path:
                flag_path = False
                print('false')
            else:
                for current_object in temp_path:
                    # for i in current_object[2]:
                    print(type(current_object))
                    game.color_shortest_path(current_object[2])
                    current_object[0].x, current_object[0].y, current_object[2], current_node = current_object[0].move(current_object[0].x,
                                                                                                current_object[0].y,
                                                                                                current_object[2],
                                                                                                game.my_dict)
                    # print(len(current_object[2]))
                # for i in temp_path:
                #
                #     # print("temp_path {}".format(temp_path[tp]))
                #     game.color_shortest_path(temp_path[i])
                #
                #     # moving robot in grid
                #     vehicle1[i].x, vehicle1[i].y, temp_path[i], current_node = vehicle1[i].move(vehicle1[i].x,
                #                                                                                 vehicle1[i].y,
                #                                                                                 temp_path[i],
                #                                                                                 game.my_dict)
                    # firebase.update_node_data(current_node)
        game.update()
        game.draw_board()
        for i in range(0, numberOfVehicles):
            game.load_vehicles(vehicle1[i])

        # if hasItem:
        for i in range(0, numberOfItems):
            game.load_item(item[i])
        game.tick(FPS)



if __name__ == "__main__":
    main()
