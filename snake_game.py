"""Snake!"""
import pygame
from time import time
import numpy as np
from collections import deque

BG_COLOR = (0,0,0)
SNAKE_COLOR = (255,255,255)
DEAD_COLOR = (255,0,0),
FOOD_COLOR = (0,255,0)

DIAG_EYE_COLOR = (255,0,255)
DIAG_FOOD_COLOR = (255,255,0)

LEFT_TURN = np.array([[0,-1],[1,0]])
RIGHT_TURN = -LEFT_TURN

def check_pos_mult(a,b):
    """check if b is a positive multiple of a.
    not expected to work with floating points; integers only."""
    return ((a@a)*(b@b) == (a@b)**2) and (a@b>0)

print(pygame.init())

class SnakeGame:
    def __init__(
        self,
        blocks_width,
        blocks_height
    ):
        """Initialize snake game"""
        self.blocks_width = blocks_width
        self.blocks_height = blocks_height
        pos_x = np.random.randint(2,blocks_width-2)
        pos_y = np.random.randint(2,blocks_height-2)
        self.snake = deque([np.array([pos_x,pos_y])])
        directions = [
            np.array([0,1]),
            np.array([0,-1]),
            np.array([1,0]),
            np.array([-1,0])
        ]
        self.direc = directions[np.random.randint(0,4)]
        self.try_direc = self.direc
        self.food = self.snake[0]+self.direc
        self.dead = False

    def step(self):
        "Move the snake forward one step and handle conditions"
        self.direc = self.try_direc

        loc = (self.snake[0] + self.direc)
        if self.dead:
            raise ValueError("Game is over, cannot step")
        if (
            any((loc==sn).all() for sn in self.snake) or 
            loc[0]<0 or
            loc[0]>=self.blocks_width or
            loc[1]<0 or
            loc[1]>=self.blocks_height
        ): #if snake has hit self or a wall
            self.dead = True
            return False
        elif (loc == self.food).all(): #if the snake has run into food
            self.snake.appendleft(loc)
            while any((self.food==sn).all() for sn in self.snake):
                #currently the food is part of the snake; position it randomly until it's not
                self.food=np.array([
                    np.random.randint(0,self.blocks_width),
                    np.random.randint(0,self.blocks_height)
                ])
            return True
        else:
            self.snake.appendleft(loc)
            self.snake.pop()
            return True

    def turn(self, direction):
        """Check if direction is valid. if it is, set try_direc for next step()"""
        directions = {
            "north":np.array([0,-1]),
            "south":np.array([0,1]),
            "west":np.array([-1,0]),
            "east":np.array([1,0]),
            "forward":self.direc,
            "left":self.direc@LEFT_TURN,
            "right":self.direc@RIGHT_TURN
        }
        assert direction in directions
        try_direc = directions[direction]
        if (try_direc == -self.direc).all():
            return False
        else:
            self.try_direc = try_direc
            return True

    def get_values(self):
        """Get the sensor values for the current state, as a 5-tuple.
        empty space forward, left, right; relative food dist forward, right"""
        left = self.direc@LEFT_TURN
        right = self.direc@RIGHT_TURN
        a,b = self.snake[0]
        out = []
        #these are the edges of the screen at cardinal directions
        bounds = [
            np.array([a,-1]),
            np.array([a,self.blocks_height]),
            np.array([-1,b]),
            np.array([self.blocks_width,b])
        ]
        kill_spots = list(self.snake)[1:]+bounds
        rels = [sn - self.snake[0] for sn in kill_spots if np.prod(sn-self.snake[0])==0]
        for d in (self.direc, left, right):
            inline = [i for i in rels if check_pos_mult(i,d)]

            out.append(min(i@d for i in inline))
        if self.direc[1] == 0:
            k = (self.food - self.snake[0])*self.direc[0]
            out.append(k[0])
            out.append(k[1])
        elif self.direc[0] == 0:
            k = (self.food - self.snake[0])*self.direc[1]
            out.append(k[1])
            out.append(-k[0])
        else:
            raise ValueError(f"Invalid direction {self.direc} (not cardinal)")
        return out
    
    def score(self):
        return len(self.snake)

        

    
class GraphicalSnakeGame(SnakeGame):
    def __init__(
        self,
        blocks_width,
        blocks_height,
        block_size
    ):
        SnakeGame.__init__(self, blocks_width, blocks_height)
        self.block_size = block_size
        self.screen_width = self.blocks_width * self.block_size
        self.screen_height = self.blocks_height * self.block_size
        self.screen =  pygame.display.set_mode((self.screen_width, self.screen_height))
        self.draw_color = SNAKE_COLOR

    def draw(self, diagnostic = False):
        draw_color = DEAD_COLOR if self.dead else SNAKE_COLOR
        self.screen.fill(BG_COLOR)
        for sn in self.snake:
            pygame.draw.rect(
                self.screen,
                draw_color,
                pygame.Rect(
                    sn[0]*self.block_size,
                    sn[1]*self.block_size,
                    self.block_size,
                    self.block_size
                )
            )
        pygame.draw.ellipse(
            self.screen,
            FOOD_COLOR,
            pygame.Rect(
                self.food[0]*self.block_size,
                self.food[1]*self.block_size,
                self.block_size,
                self.block_size
            )
        )
        if diagnostic:
            k_f, k_l, k_r, f_f, f_r = self.get_values()
            left = self.direc@LEFT_TURN
            right = self.direc@RIGHT_TURN
            head = (self.snake[0]+0.5)*self.block_size
            food = (self.food+0.5)*self.block_size
            pygame.draw.line(
                self.screen,
                DIAG_EYE_COLOR,
                head,
                head + self.direc*k_f*self.block_size
            )

            pygame.draw.line(
                self.screen,
                DIAG_EYE_COLOR,
                head,
                head + left*k_l*self.block_size
            )

            pygame.draw.line(
                self.screen,
                DIAG_EYE_COLOR,
                head,
                head + right*k_r*self.block_size
            )

            pygame.draw.line(
                self.screen,
                DIAG_FOOD_COLOR,
                food,
                food - self.direc*f_f*self.block_size
            )

            pygame.draw.line(
                self.screen,
                DIAG_FOOD_COLOR,
                food,
                food - right*f_r*self.block_size
            )


        pygame.display.flip()


if __name__ == "__main__":

    BLOCK_SIZE = 30
    BLOCKS_WIDTH = 15
    BLOCKS_HEIGHT = 10

    TICK = .2

    game = GraphicalSnakeGame(
        blocks_width=BLOCKS_WIDTH,
        blocks_height=BLOCKS_HEIGHT,
        block_size=BLOCK_SIZE
    )

    running = True

    t_base = time()
    advance = False

    while running:
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    game.turn("south")
                elif event.key in (pygame.K_w, pygame.K_UP):
                    game.turn("north")
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    game.turn("west")
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    game.turn("east")
                elif event.key == pygame.K_SPACE:
                    advance = True


            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

        new_t = time()
        if (new_t-t_base > TICK or advance)  and not game.dead:
            t_base = new_t
            advance = False
            alive = game.step()
            game.draw(True)
            print(game.get_values())
            if not alive:
                game = GraphicalSnakeGame(
                    blocks_width=BLOCKS_WIDTH,
                    blocks_height=BLOCKS_HEIGHT,
                    block_size=BLOCK_SIZE
                )
