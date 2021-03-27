from warehouse.game import Game
from warehouse.game import Vehicle
from warehouse.game import Item
# from server.firebase import Firebase
from algorithm.dijktra import Dijkstra
from algorithm.dijktra import DijkstraModify
import pygame as p
from itertools import chain
# store the task list , work as FIFO
import queue as task
import random

task_list = task.Queue()
FPS = 50


def remove_path(vehicle_to_be_removed, item_to_be_removed, list_all_pair):
    for cp in list_all_pair[:]:
        if vehicle_to_be_removed in cp or item_to_be_removed in cp:
            list_all_pair.remove(cp)
    return list_all_pair


def main():
    # initial ##############################
    game = Game()
    # TODO: remove firebase for simuation
    # firebase = Firebase()
    # TODO: remove firebase for simuation ###

    init_pos_x = 30
    init_pos_y = 20
    max_number_of_step = 30
    numberOfVehicles = 5
    vehicle1 = []
    # vehicle = Vehicle(init_pos_x, init_pos_y)
    # vehicle1.append(vehicle)
    #
    # vehicle = Vehicle(30, 220)
    # vehicle1.append(vehicle)
    vehicle = Vehicle("00", game.my_dict, game.adjacency_matrix, 'red', 1)
    vehicle1.append(vehicle)
    vehicle = Vehicle("02", game.my_dict, game.adjacency_matrix, 'blue', 2)
    vehicle1.append(vehicle)
    vehicle = Vehicle("04", game.my_dict, game.adjacency_matrix, 'green', 3)
    vehicle1.append(vehicle)
    vehicle = Vehicle("00", game.my_dict, game.adjacency_matrix, 'red', 4)
    vehicle1.append(vehicle)
    vehicle = Vehicle("00", game.my_dict, game.adjacency_matrix, 'red', 5)
    vehicle1.append(vehicle)
    #########################################

    # load multiple robot based on the give position
    for i in range(0, numberOfVehicles):
        game.load_vehicles(vehicle1[i])

    # dj = Dijkstra(game.adjacency_matrix)
    # dj.calculate()
    # print(dj.path)

    path = []
    newpath = []
    shortest_path = []

    flag_path = False
    temp_path = []
    vehicle_move = []  # for animation

    # hasItem = False
    # add Item task
    numberOfItems = 3
    # simple form
    item = []
    # test assign nearly robot
    # item.append(Item("12", game.my_dict))

    item.append(Item("30", game.my_dict))
    item.append(Item("32", game.my_dict))
    # item.append(Item("34", game.my_dict))
    #
    # item.append(Item("04", game.my_dict))
    # item.append(Item("14", game.my_dict))
    item.append(Item("33", game.my_dict))

    # queue form
    # test assign nearly robot
    # task_list.put(Item("12", game.my_dict))

    task_list.put(Item("30", game.my_dict))
    task_list.put(Item("32", game.my_dict))
    # task_list.put(Item("34", game.my_dict))
    #
    # task_list.put(Item("04", game.my_dict))
    # task_list.put(Item("14", game.my_dict))
    task_list.put(Item("33", game.my_dict))

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
                    pair_robot_item = []  # list
                    path = []
                    # get all free robot
                    for i in range(0, numberOfVehicles):
                        if not vehicle1[i].hasTask:
                            print("Vehicle init position {}".format(vehicle1[i].currentCoorPos))
                            sourceNode.append(vehicle1[i])

                    # probability: path is the combination (freeRobot, number_task)
                    process_task = []
                    for i in range(0, len(sourceNode)):  # number of free robot
                        if not task_list.empty():
                            process_task.append(task_list.get())

                    # conduct the combination
                    for v in sourceNode:
                        for p_task in process_task:
                            # print("Number of task{}{}".format(i, j))
                            pair_robot_item.append((v, p_task))


                    # TODO: get the best path for all free robot ###

                    # TODO: robot will move to object
                    # pick random
                    list_all_pair = pair_robot_item  # should remove


                    current_pair = []  # this is the array of object (Vehicle, Item)
                    for i in range(0, len(sourceNode)):  # number of free robot
                        if list_all_pair:
                            current_choice = random.choice(list_all_pair)  # get random pair robot item
                            if current_choice not in current_pair:
                                current_pair.append(current_choice)  # add to array
                                # vehicle to be removed
                                vehicle_to_be_removed = current_choice[0]
                                item_to_be_removed = current_choice[1]
                                list_all_pair = remove_path(vehicle_to_be_removed, item_to_be_removed, list_all_pair)

                    # path finding
                    current_path = []
                    for pair in current_pair: # 0: vehicle, 1: item

                        # version 1
                        dj = Dijkstra(game.adjacency_matrix, game.occupy_node)
                        dj.calculate()
                        path = dj.getBestPath(pair[0].initValue, pair[1].initValue) # if path is null mean the task need put in the queue again
                        if path == []:
                            task_list.put(pair[1])
                            continue
                        else:
                            pair[0].hasTask = True # robot is in task

                        # version 2
                        # dj = DijkstraModify()
                        # dj.dijkstra(game.adjacency_matrix, pair[0].initValue)
                        # path = dj.getBestPath(pair[0].initValue, pair[1].initValue) # if path is null mean the task need put in the queue again

                        new_path = game.map_path(path)

                        # remove all path has the same position with the same value
                        # example
                        # 0 1 3  4 5 6
                        # 4 2 3  8 9 => 4 2

                        if new_path not in current_path:
                            current_path.append([pair[0], pair[1], new_path])

                            pair[0].update_occupy_node(new_path[:max_number_of_step], game) # add True if node is in the path

                            for i in range(0, len(pair[0].occupyEdge) - 1):
                                game.adjacency_matrix[pair[0].occupyEdge[i]][pair[0].occupyEdge[i + 1]] = 0  # zero mean no path
                                # game.adjacency_matrix[pair[0].occupyEdge[i + 1]][pair[0].occupyEdge[i]] = 0 #  no bi direction
                            print(game.adjacency_matrix)
                    # convert to node
                    print("this is current path {}".format(current_path))
                    temp_path = current_path

                    # TODO: robot will move to object ###

                # TODO:  stupid reset
                if key[p.K_9]:
                    print("Reset")
                    main()
                # TODO:  stupid reset ###

        if flag_path:
            if not temp_path:
                flag_path = False
                # print('false')
            else:


                for current_object in temp_path: # 0: vehicle, 1: item, 2: path
                    # current_object[0].update_occupy_node(current_object[2][:max_number_of_step], game)
                    # update data to map

                    for i in range(0, len(current_object[0].occupyEdge[:max_number_of_step]) - 1):
                        game.adjacency_matrix[current_object[0].occupyEdge[i]][
                            current_object[0].occupyEdge[i + 1]] = 0 # zero mean no path
                        # game.adjacency_matrix[current_object[0].occupyEdge[i + 1]][
                        #     current_object[0].occupyEdge[i]] = 0  # no bi direction
                        # print("hello {} {}".format(current_object[0].occupyEdge[i], current_object[0].occupyEdge[i + 1]))
                        # game.adjacency_matrix[current_object[0].occupyEdge[i + 1]][
                        #     current_object[0].occupyEdge[i]] = 0

                    # path here is the String value
                    game.color_shortest_path(current_object[2][:max_number_of_step-1], current_object[0].colorPath) #  color to max node number

                    if current_object[0].state == "Move":
                        current_object[0].x, current_object[0].y, current_object[2], current_node = current_object[0].move(
                            current_object[0].x,
                            current_object[0].y,
                            current_object[2],
                            game.my_dict)

                    if current_object[2] == []: # reach the item
                        current_object[0].state == "Stop"
                        for i in range(0, len(current_object[0].occupyEdge[:max_number_of_step]) - 1):
                            print(i)
                            value = current_object[0].returnMapValue.pop(0)  # return back value
                            game.adjacency_matrix[current_object[0].occupyEdge[i]][
                                current_object[0].occupyEdge[i + 1]] = value
                            print('{} to {} value {}'.format(current_object[0].occupyEdge[i], current_object[0].occupyEdge[i + 1], value))

                            # game.adjacency_matrix[current_object[0].occupyEdge[i]][
                            #     current_object[0].occupyEdge[i + 1]] = value
                        for i in current_object[0].occupyNode:
                            game.occupy_node[i] = False
                        current_object[0].free_occupy_node()



                    # if number of move greater than the max number of step then free previous location
                    if current_object[0].numberOfMovingStep >= max_number_of_step:
                        # print("start to find aother paht {}".format(current_object[0].numberOfMovingStep))
                        current_object[0].numberOfMovingStep = 0

                        # free all occupy node
                        print("this is current_object[0].occupyEdge")
                        print(current_object[0].occupyEdge)
                        for i in range(0, len(current_object[0].occupyEdge[:max_number_of_step]) - 1):
                            print(i)
                            value = current_object[0].returnMapValue.pop(0)  # return back value
                            game.adjacency_matrix[current_object[0].occupyEdge[i]][
                                current_object[0].occupyEdge[i + 1]] = value
                            print('{} to {} value {}'.format(current_object[0].occupyEdge[i], current_object[0].occupyEdge[i + 1], value))

                            # game.adjacency_matrix[current_object[0].occupyEdge[i]][
                            #     current_object[0].occupyEdge[i + 1]] = value
                        for i in current_object[0].occupyNode:
                            game.occupy_node[i] = False
                        current_object[0].free_occupy_node()

                        # version 1
                        dj = Dijkstra(game.adjacency_matrix, game.occupy_node)
                        dj.calculate()

                        print("this is occupy_node")
                        print(game.occupy_node)

                        if current_object[0].initValue != current_object[1].initValue:
                            next_path = dj.getBestPath(current_object[0].initValue, current_object[
                                1].initValue)  # if path is null mean the task need put in the queue again

                            if next_path != []:
                                convert_path = game.map_path(next_path)
                                current_object[2] = convert_path
                                current_object[0].update_occupy_node(current_object[2][:max_number_of_step+1], game)
                                # update data to map

                                for i in range(0, len(current_object[0].occupyEdge[:max_number_of_step]) - 1):
                                    game.adjacency_matrix[current_object[0].occupyEdge[i]][
                                        current_object[0].occupyEdge[i + 1]] = 0  # zero mean no path
                                    print("hello {} {}".format(current_object[0].occupyEdge[i],
                                                               current_object[0].occupyEdge[i + 1]))

                        # version 2
                        # dj = DijkstraModify()
                        # dj.dijkstra(game.adjacency_matrix, current_object[0].initValue)
                        #
                        # # TODO: update new path
                        # restart for current  robot
                        # for vehicle_item_path in temp_path:
                        #     next_path = []
                        #     if vehicle_item_path[0].initValue != vehicle_item_path[1].initValue:
                        #         print("This is bug {} {}".format(vehicle_item_path[0].initValue, vehicle_item_path[1].initValue))
                        #         # next_path = dj.getBestPath(vehicle_item_path[0].initValue, vehicle_item_path[1].initValue)
                        #
                        #         next_path = dj.getBestPath(current_object[0].initValue, current_object[1].initValue)  # if path is null mean the task need put in the queue again
                        #
                        #         if next_path != []:
                        #
                        #
                        #             vehicle_item_path[2] = game.map_path(next_path) #remember convert
                        #
                        #             vehicle_item_path[0].update_occupy_node(vehicle_item_path[2][:max_number_of_step])
                        #             for i in range(0, len(vehicle_item_path[0].occupyEdge[:max_number_of_step]) - 1):
                        #                 game.adjacency_matrix[vehicle_item_path[0].occupyEdge[i]][
                        #                     vehicle_item_path[0].occupyEdge[i + 1]] = 0  # zero mean no path
                        #                 # game.adjacency_matrix[vehicle_item_path[0].occupyEdge[i + 1]][
                        #                 #     vehicle_item_path[0].occupyEdge[i]] = 0  # no bi direction

                        #             # vehicle_item_path[0].state = "Move"
                        #         # else:
                        #             # vehicle_item_path[0].state = "Stop"

                        # if all vehicle is Stop, then random choice 1 move
                        # if "Move" not in temp_path
                        # count = 0
                        # for number_vehicle in temp_path:
                        #     if number_vehicle[0].state == "Stop":
                        #         count += 1
                        # print("This count {}".format(count))

                        # if current_object[0].numberOfMovingStep >= max_number_of_step:

                        # TODO: update new path

                    # firebase.update_node_data(current_node)


        game.update()
        game.draw_board()  # draw square and load cost on each path
        # loop for load all vehicle
        for i in range(0, numberOfVehicles):
            game.load_vehicles(vehicle1[i])

        # loop for load all exit item
        # if hasItem:
        for i in range(0, numberOfItems):
            game.load_item(item[i])


        game.tick(FPS)


if __name__ == "__main__":
    main()
