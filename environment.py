from warehouse.game import Game
from warehouse.game import Vehicle
from warehouse.game import Item
import pygame as p

FPS = 90

if __name__ == "__main__":
    game = Game()

    init_pos_x = 30
    init_pos_y = 20

    vehicle1 = Vehicle(init_pos_x, init_pos_y)
    game.load_vehicles(vehicle1)

    shortest_path = ["10", "11", "12", "02"]  # test
    # shortest_path = dijkstra (adjacency_matrix)
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
