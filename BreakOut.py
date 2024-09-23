import pygame
import pygame
import random

from pygame import Color

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

class Player (pygame.Rect): # saying our player is Rect
# inheritance!
    def __init__(self, x, y):
        super().__init__(x, y,  70, 10) # arbitrary values
        # TODO tweak?
        self.vx = 0

    def draw (self):
        pygame.draw.rect(screen, 'white', self, 0) # fill
        pygame.draw.rect(screen, 'white', self, 1) # outline

    def update(self):
        self.x += self.vx
        if self.x<0:
            self.x = 0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball (pygame.Rect):
    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(2,5) * random.choice ([1, -1])
        self.vy = random.randint(2, 5) # arbitrary values
        #TODO tweak?

    def draw(self):
        pygame.draw.ellipse(screen, 'white', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 and self.vx < 0:
            self.vx *=-1
        if self.x + self.w > screen.get_width() and self.vx > 0:
            self.vx *=-1
        if self.y < 0 and self.vy < 0:
            self.vy *= -1
        elif self.y > screen.get_height():
            self.y = 100

class Brick (pygame.Rect):
    w = 128 # width
    h = 20 # height
    def __init__(self, x, y):
        super().__init__(x, y, Brick.w, Brick.h)
        color1 = (255, 241,186)
        color2 = (255, 230, 230)
        color3 = (255, 233, 143)
        color4 = (245, 196, 215)
        colors = [color1, color2, color3, color4]
        self.color = (colors[random.randint(0,3)])


    def draw (self):
        pygame.draw.rect(screen, self.color, self, 0)# fill
        pygame.draw.rect(screen, (30,35,50), self, 1) # outline

bricks = []
for x in range(0, screen.get_width(), Brick.w):
    for y in range(0, 100, Brick.h):
        bricks.append(Brick(x, y))



player = Player(screen.get_width()/2-50, screen.get_height() - 20)
ball = Ball(screen.get_width()/2-10, screen.get_height()/2 + 20, 20)



while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: # pressing left or a will change the x
                player.vx +=-6
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # pressing left or a will change the x
                    player.vx += 6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # pressing left or a will change the x
                player.vx += 6
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # pressing left or a will change the x
                player.vx += -6

    # Do logical updates here.

    player.update()
    ball.update()
    if ball.colliderect(player):
        ball.vy*=-1
        ball.y = player.y - ball.width # makes collision on rect's side look better?
        diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        ball.vx += diff//10

    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball.vy *=-1



    screen.fill(Color(30,35,50))  # Fill the display with a solid color

    # Render the graphics here.

    player.draw()
    ball.draw()
    for b in bricks:
        b.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)