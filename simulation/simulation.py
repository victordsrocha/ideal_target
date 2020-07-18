from simulation import constants
import pygame
import sys


class Simulation:

    def __init__(self, agent):
        self.agent = agent

        # TODO
        # da forma abaixo não aponta para o mesmo obj
        # não entendi como resolver, vou acessar direto por agent por enquanto
        # self.last_state_list = agent.enacter.interface.env.last_state_list

        # TODO checar se faz sentido usar o convert_alpha
        # Agent img standard
        self.agent_img = pygame.image.load('simulation/images/ladybug.png')
        self.agent_img = pygame.transform.scale(self.agent_img,
                                                (int(1 * constants.BLOCK_WIDTH), int(1 * constants.BLOCK_HEIGHT)))
        # Agent img right
        self.agent_img_right = pygame.image.load('simulation/images/ladybug-right.png')
        self.agent_img_right = pygame.transform.scale(self.agent_img_right,
                                                      (int(1 * constants.BLOCK_WIDTH), int(1 * constants.BLOCK_HEIGHT)))
        # Agent img left
        self.agent_img_left = pygame.image.load('simulation/images/ladybug-left.png')
        self.agent_img_left = pygame.transform.scale(self.agent_img_left,
                                                     (int(1 * constants.BLOCK_WIDTH), int(1 * constants.BLOCK_HEIGHT)))
        # Agent img both eyes
        self.agent_img_both = pygame.image.load('simulation/images/ladybug-both.png')
        self.agent_img_both = pygame.transform.scale(self.agent_img_both,
                                                     (int(1 * constants.BLOCK_WIDTH), int(1 * constants.BLOCK_HEIGHT)))

        # food img
        food_img = pygame.image.load('simulation/images/leaf.png')
        self.food_img = pygame.transform.scale(food_img,
                                               (int(0.8 * constants.BLOCK_WIDTH), int(0.8 * constants.BLOCK_HEIGHT)))

    def get_tile_color(self, tile_contents):
        tile_color = (0, 0, 0)
        if tile_contents == 'w':
            tile_color = constants.GREY
        elif tile_contents == '-':
            tile_color = constants.BROWN
        return tile_color

    def draw_grid(self, surface):
        for i in range(constants.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * constants.BLOCK_HEIGHT)
            new_width = round(i * constants.BLOCK_WIDTH)
            pygame.draw.line(surface, constants.BLACK, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
            pygame.draw.line(surface, constants.BLACK, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)

    def draw_map(self, surface, map_tiles):
        for j, tile in enumerate(map_tiles):
            for i, tile_contents in enumerate(tile):
                # print(f'{i},{j}: {tile_contents}')
                my_rect = pygame.Rect(i * constants.BLOCK_WIDTH, j * constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH,
                                      constants.BLOCK_HEIGHT)
                pygame.draw.rect(surface, self.get_tile_color(tile_contents), my_rect)

    def game_loop(self, surface, world_map, agent):
        clock = pygame.time.Clock()
        current = 0
        t = 0
        while True:
            if t < 5000:
                clock.tick(500)
            else:
                clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if current == len(agent.enacter.interface.env.last_state_list):
                current = 0
                agent.enacter.interface.env.last_state_list = []
                agent.step()
                state = agent.enacter.interface.env.last_state_list[current]
            else:
                state = agent.enacter.interface.env.last_state_list[current]
            current += 1

            self.draw_map(surface, world_map)
            self.draw_grid(surface)
            self.draw_agent_food(surface, state)

            t += 1
            pygame.display.update()

    def initialize_game(self):
        pygame.init()
        surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption(constants.TITLE)
        surface.fill(constants.GREY)
        return surface

    def read_map(self, map_file):
        with open(map_file, 'r') as f:
            world_map = f.readlines()
        world_map = [line.strip() for line in world_map]
        return world_map

    def draw_agent_food(self, surface, state):

        def rot_center(image, angle):
            """rotate an image while keeping its center and size"""
            orig_rect = image.get_rect()
            rot_image = pygame.transform.rotate(image, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            return rot_image

        a_x = state.a_x
        a_y = state.a_y
        a_o = state.a_o

        rot = 0
        if a_o == 1:
            rot = -90
        elif a_o == 2:
            rot = -180
        elif a_o == 3:
            rot = -270

        a_x = a_x * constants.BLOCK_WIDTH
        a_y = a_y * constants.BLOCK_HEIGHT

        agent_img = self.agent_img
        if state.a_left_eye == '+' or state.a_left_eye == '*' or state.a_left_eye == 'x':
            if state.a_right_eye == '+' or state.a_right_eye == '*' or state.a_right_eye == 'x':
                agent_img = self.agent_img_both
            else:
                agent_img = self.agent_img_left
        elif state.a_right_eye == '+' or state.a_right_eye == '*' or state.a_right_eye == 'x':
            agent_img = self.agent_img_right

        surface.blit(rot_center(agent_img, rot), (a_x, a_y))
        surface.blit(self.food_img,
                     (state.food_x * constants.BLOCK_WIDTH + 5, state.food_y * constants.BLOCK_HEIGHT + 5))

    # criar update através da lista de state, a lista vai ser controlada no loop

    def run(self, clock_tick=60):
        surface = self.initialize_game()
        world_map = self.read_map(constants.MAPFILE)
        self.game_loop(surface, world_map, self.agent)
