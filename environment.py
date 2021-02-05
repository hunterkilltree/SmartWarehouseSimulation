from warehouse.game import Game
import pygame as p

game = Game()

while game.running == 1:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    game.tick(90)
    game.screen.fill((0, 0, 0))
    game.reDraw()
