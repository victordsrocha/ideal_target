"""
Symbols Actuators Sensors Description Intrinsic  satisfaction
 ^    (^) Turn left True Turn 90Â° left toward adjacent empty square 0
      [^] False Turn 90Â° left toward adjacent wall -5
 >    (>) Forward True Move forward -1
      [>] False Bump wall -8
 v    (v) Turn right True Turn 90Â° right toward adjacent empty square 0
      [v] False Turn 90Â° right toward adjacent wall -5
      * Appear Target appears in distal sensor field 15
      + Closer Target approaches in distal sensor field 10
      x Reached Target reached according to distal sensor 15
      o  Disappear Target disappears from distal sensor field -15

a interação primitiva vai ser identifacada com 4 caracteres:

primeiro: '^', 'v', '>'

para identificar left, right or move

segundo: '.', 'w'

w para identificar se havia uma parede adjacente a frente ou batida na parede em caso de move

terceiro e quarto: '*', '+', 'x', 'o', '.'

para identificar o estado atual de cada olho

"""

from environment.state import State
from environment.environment import Environment
import random


class SimpleTarget(Environment):

    def __init__(self):
        self.ORIENTATION_UP = 0
        self.ORIENTATION_RIGHT = 1
        self.ORIENTATION_DOWN = 2
        self.ORIENTATION_LEFT = 3

        # acho que seria mais interessante as coords do agente ficarem em interface
        self.a_x = random.randint(1, 11)
        self.a_y = random.randint(1, 9)
        self.a_o = random.randint(0, 3)
        self.a_right_eye = '-'
        self.a_left_eye = '-'

        # estrutura para salvar os últimos passos e ser acessado por simularion
        self.last_state_list = []

        # board
        self.WIDTH = 13
        self.HEIGHT = 11
        self.board = [
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
        ]

        # food
        self.food_reached = False
        self.food_x, self.food_y = self.food_position()
        self.board[self.food_y][self.food_x] = 'f'

    def food_position(self):
        x_set = list(set([i for i in range(1, 11)]) - {self.a_x})
        y_set = list(set([i for i in range(1, 9)]) - {self.a_y})
        f_x = random.choice(x_set)
        f_y = random.choice(y_set)
        return f_x, f_y

    def update_food(self):
        if self.food_reached:
            self.board[self.food_y][self.food_x] = ' '
            self.food_x, self.food_y = self.food_position()
            self.board[self.food_y][self.food_x] = 'f'
            self.food_reached = False

    def tile_content(self, x, y):
        return self.board[y][x]

    def right_eye_update_state(self):
        food = False
        reached = False

        if self.a_o == 0:
            for i in range(self.a_x, self.WIDTH - 1):
                for j in range(self.a_y, 0, -1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        elif self.a_o == 1:
            for i in range(self.a_x, self.WIDTH - 1):
                for j in range(self.a_y, self.HEIGHT - 1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        elif self.a_o == 2:
            for i in range(1, self.a_x + 1):
                for j in range(self.a_y, self.HEIGHT - 1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        elif self.a_o == 3:
            for i in range(1, self.a_x + 1):
                for j in range(self.a_y, 0, -1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        if food:
            if self.a_right_eye == '-' or self.a_right_eye == 'o':
                new_state = '*'
            else:
                if reached:
                    new_state = 'x'
                    self.food_reached = True
                else:
                    new_state = '+'
        else:
            if self.a_right_eye == '+' or self.a_right_eye == '*' or self.a_right_eye == 'x':
                new_state = 'o'
            else:
                new_state = '-'

        self.a_right_eye = new_state
        return new_state

    def left_eye_update_state(self):
        food = False
        reached = False

        if self.a_o == 0:
            for i in range(1, self.a_x + 1):
                for j in range(self.a_y, 0, -1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        elif self.a_o == 1:
            for i in range(self.a_x, self.WIDTH - 1):
                for j in range(self.a_y, 0, -1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        elif self.a_o == 2:
            for i in range(self.a_x, self.WIDTH - 1):
                for j in range(self.a_y, self.HEIGHT - 1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        elif self.a_o == 3:
            for i in range(1, self.a_x + 1):
                for j in range(self.a_y, self.HEIGHT - 1):
                    if self.tile_content(i, j) == 'f':
                        food = True
                        if i == self.a_x and j == self.a_y:
                            reached = True
                        break

        if food:
            if self.a_right_eye == '-' or self.a_right_eye == 'o':
                new_state = '*'
            else:
                if reached:
                    new_state = 'x'
                    self.food_reached = True
                else:
                    new_state = '+'
        else:
            if self.a_right_eye == '+' or self.a_right_eye == '*' or self.a_right_eye == 'x':
                new_state = 'o'
            else:
                new_state = '-'

        self.a_left_eye = new_state
        return new_state

    def right(self):

        self.a_o += 1
        if self.a_o > self.ORIENTATION_LEFT:
            self.a_o = self.ORIENTATION_UP

        result = ['v']

        if self.a_o == self.ORIENTATION_UP and self.a_y == 1:
            result.append('w')
        elif self.a_o == self.ORIENTATION_RIGHT and self.a_x == self.WIDTH - 2:
            result.append('w')
        elif self.a_o == self.ORIENTATION_DOWN and self.a_y == self.HEIGHT - 2:
            result.append('w')
        elif self.a_o == self.ORIENTATION_LEFT and self.a_x == 1:
            result.append('w')
        else:
            result.append('.')

        result.append(self.left_eye_update_state())
        result.append(self.right_eye_update_state())

        # TODO pesquisar por forma mais prática de fazer list -> str
        result = str(result)[1:-1].replace("'", '').replace(',', '').replace(' ', '')

        self.save_state()
        return result

    def left(self):

        self.a_o -= 1
        if self.a_o < 0:
            self.a_o = self.ORIENTATION_LEFT

        result = ['^']

        if self.a_o == self.ORIENTATION_UP and self.a_y == 1:
            result.append('w')
        elif self.a_o == self.ORIENTATION_RIGHT and self.a_x == self.WIDTH - 2:
            result.append('w')
        elif self.a_o == self.ORIENTATION_DOWN and self.a_y == self.HEIGHT - 2:
            result.append('w')
        elif self.a_o == self.ORIENTATION_LEFT and self.a_x == 1:
            result.append('w')
        else:
            result.append('.')

        result.append(self.left_eye_update_state())
        result.append(self.right_eye_update_state())

        # TODO pesquisar por forma mais prática de fazer list -> str
        result = str(result)[1:-1].replace("'", '').replace(',', '').replace(' ', '')

        self.save_state()
        return result

    def move(self):
        result = ['>']

        # add 'w' to label if bump to Wall
        # else, add '.'
        if (self.a_o == self.ORIENTATION_UP) and (self.a_y > 0) and (
                (self.tile_content(self.a_x, self.a_y - 1) == ' ') or (
                self.tile_content(self.a_x, self.a_y - 1) == 'f')):
            self.a_y -= 1
            result.append('.')
        elif (self.a_o == self.ORIENTATION_DOWN) and (self.a_y < self.HEIGHT) and (
                (self.tile_content(self.a_x, self.a_y + 1) == ' ') or (
                self.tile_content(self.a_x, self.a_y + 1) == 'f')):
            self.a_y += 1
            result.append('.')
        elif (self.a_o == self.ORIENTATION_RIGHT) and (self.a_x < self.WIDTH) and (
                (self.board[self.a_y][self.a_x + 1] == ' ') or (self.board[self.a_y][self.a_x + 1] == 'f')):
            self.a_x += 1
            result.append('.')
        elif (self.a_o == self.ORIENTATION_LEFT) and (self.a_x > 0) and (
                (self.board[self.a_y][self.a_x - 1] == ' ') or (self.board[self.a_y][self.a_x - 1] == 'f')):
            self.a_x -= 1
            result.append('.')
        else:
            result.append('w')

        result.append(self.left_eye_update_state())
        result.append(self.right_eye_update_state())

        result = str(result)[1:-1].replace("'", '').replace(',', '').replace(' ', '')

        self.update_food()
        self.save_state()
        return result

    def save_state(self):
        last_action = State(
            self.a_x,
            self.a_y,
            self.a_o,
            self.a_right_eye,
            self.a_left_eye,
            self.food_x,
            self.food_y,
            self.food_reached
        )
        self.last_state_list.append(last_action)
