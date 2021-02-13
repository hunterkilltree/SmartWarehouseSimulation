import pygame as p
import random
from collections import namedtuple

WIDTH = HEIGHT = 600  # 512
DIMENSION = 50  # dimensions of a chess board are 8x8
SIZE = HEIGHT // DIMENSION
n = 6
Position = namedtuple('Position', ['x', 'y'])
top, left, space, lines = (20, 20, 100, n)

programIcon = p.image.load("image/Robot2.ico")
picture = p.image.load("image/Robot2.png")
station = p.image.load("image/Station.png")
itemPicture = p.image.load("image/Robot1.png")


# [
# [0, 4, 0, 9, 0, 0, 0, 0, 0],
#  [7, 0, 9, 0, 3, 0, 0, 0, 0],
#  [0, 8, 0, 0, 0, 10, 0, 0, 0],
#  [4, 0, 0, 0, 8, 0, 5, 0, 0],
#  [0, 9, 0, 9, 0, 9, 0, 6, 0],
#  [0, 0, 2, 0, 4, 0, 0, 0, 7],
#  [0, 0, 0, 9, 0, 0, 0, 5, 0],
#  [0, 0, 0, 0, 8, 0, 7, 0, 6],
#  [0, 0, 0, 0, 0, 5, 0, 7, 0]
#  ]

# 4 nodes
# [
# [0, 3, 10, 0], # tat ca lien quan den 00
#  [10, 0, 0, 4], # tat ca lien quan den 01
#  [9, 0, 0, 7], # tat ca lien quan den 10
#  [0, 3, 5, 0] # tat ca lien quan den 11
#  ]


class Game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        p.display.set_caption('SimuTool')
        p.display.set_icon(programIcon)

        self.screen.fill(p.Color("white"))

        self.running = True
        self.clock = p.time.Clock()

        self.default_font = p.font.get_default_font()
        self.font_renderer = p.font.Font(self.default_font, SIZE)

        # hash code
        self.points = [[] for i in range(lines)]
        for i in range(lines):
            for j in range(lines):
                self.points[i].append(Position(left + i * space, top + j * space))

        self.my_dict = {}  # store Node reference to the position in grip map
        for r in range(n):
            for c in range(n):
                coordinate = str(r) + str(c)
                temp = {coordinate: self.points[r][c]}
                self.my_dict.update(temp)
        #  Adjacency Matrix 6x6
        # self.adjacency_matrix = [
        #      [0, 3, 10, 0], # tat ca lien quan den 00
        #      [10, 0, 0, 4], # tat ca lien quan den 01
        #      [9, 0, 0, 7], # tat ca lien quan den 10
        #      [0, 3, 5, 0] # tat ca lien quan den 11
        # ]
        self.adjacency_matrix = []
        self.list_node = []

        for key in self.my_dict.keys():
            self.list_node.append(key)
        print(self.list_node)

        for r in self.my_dict:
            matrix = []
            for c in self.my_dict:
                if ((int(r[0]) == int(c[0]) or int(r[1]) == int(c[1]))
                        and
                        (abs(int(r[0]) - int(c[0])) == 1 or abs(int(r[1]) - int(c[1])) == 1)):
                    r1 = random.randint(2, 10)
                    matrix.append(r1)
                    # print(r + " " + c)
                else:
                    matrix.append(0)
            self.adjacency_matrix.append(matrix)

        print(self.adjacency_matrix)

    def update(self):
        p.display.flip()
        self.screen.fill(p.Color("white"))  # not good but it work :v
        self.screen.blit(p.transform.scale(station, (SIZE + 10, SIZE + 10)), p.Rect(10, 10, SIZE, SIZE))

    def tick(self, fps):
        self.clock.tick(fps)

    def load_vehicles(self, vehicle):
        self.screen.blit(vehicle.image, p.Rect(vehicle.x, vehicle.y, SIZE, SIZE))

    def load_item(self, item):
        self.screen.blit(item.image, p.Rect(item.x, item.y, SIZE, SIZE))

    def color_shortest_path(self, path):
        color = p.Color("red")
        for i in range(0, len(path) - 1):
            p.draw.line(self.screen, color, self.my_dict[path[i]], self.my_dict[path[i + 1]], 3)

    def map_path(self, path):
        new_path = []
        for i in path:
            if i == -1:
                new_path.append("None")
            else:
                new_path.append(self.list_node[i])
        return new_path

    # draw grid map
    def draw_board(self):
        # p.draw.line(screen, p.Color("gray"), (-1, -1), (512, 0), 5)
        color = (0, 0, 0)  # Checkerboard grid line color
        color_circle = p.Color("red")

        # Draw coordinate numbers
        for i in range(1, lines):
            coord_text = self.font_renderer.render(
                str(i),  # The font to render
                True,  # With anti aliasing
                (0, 0, 0))  # RGB Color

            self.screen.blit(
                coord_text,
                (
                    self.points[i][0].x - round(coord_text.get_width() / 2),
                    self.points[i][0].y - coord_text.get_height()))
            self.screen.blit(
                coord_text,
                (
                    self.points[0][i].x - coord_text.get_width(),
                    self.points[0][i].y - round(coord_text.get_height() / 2)))

        for x in range(lines):
            # Draw horizontal lines
            p.draw.line(self.screen, color, self.points[0][x], self.points[lines - 1][x])
            p.draw.circle(self.screen, color_circle, self.points[x][0], 2, 0)

            # Draw vertical lines
            p.draw.line(self.screen, color, self.points[x][0], self.points[x][lines - 1])
            p.draw.circle(self.screen, color_circle, self.points[0][x], 2, 0)


class Vehicle:
    def __init__(self, init_pos_x, init_pos_y):
        self.image = p.transform.scale(picture, (SIZE + 10, SIZE + 10))  # scale the given image fit the grid
        self.x = init_pos_x - 10
        self.y = init_pos_y - 10

        self.obstacle = False
        self.priority = 0  # 0 > 1 > 2 in multi robot

        # movement
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.angle = 0
        self.rotate_left = False
        self.rotate_right = False

        self.turn_speed = 0.5
        self.top_speed = 6
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.current_speed = 0
        self.move_x = 0
        self.move_y = 0
        self.speed = 1

    def move(self, x, y, path, my_dict):
        if path:
            if (x + 10) == my_dict[path[0]].x and (y + 10) == my_dict[path[0]].y:
                path.pop(0)
                return x, y, path
            if (x + 10) < my_dict[path[0]].x:
                x = x + self.speed
            if (x + 10) > my_dict[path[0]].x:
                x = x - self.speed

            if (y + 10) < my_dict[path[0]].y:
                y = y + self.speed
            if (y + 10) > my_dict[path[0]].y:
                y = y - self.speed

        return x, y, path


class Item:
    def __init__(self, x, y):
        self.image = p.transform.scale(itemPicture, (SIZE + 10, SIZE + 10))
        self.x = x
        self.y = y
        self.pos = Position(x, y)
