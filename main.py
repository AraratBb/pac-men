from pygame import *
from random import choice, randint
display.set_caption('Pac-man')
window = display.set_mode((700, 500))
class Pacman(sprite.Sprite):
    def __init__(self, images, pacman_x, pacman_y, size_x, size_y, pacman_x_speed,pacman_y_speed):
        sprite.Sprite.__init__(self)
        self.direct="right"
        self.images = {
          "up": transform.scale(image.load(images["up"]), (size_x, size_y)),
          "down": transform.scale(image.load(images["down"]), (size_x, size_y)),
          "right": transform.scale(image.load(images["right"]), (size_x, size_y)),
          "left": transform.scale(image.load(images["left"]), (size_x, size_y))
        }
        self.rect = self.images[self.direct].get_rect()
        self.size_x = size_x
        self.size_y = size_y
        self.rect.x = pacman_x
        self.rect.y = pacman_y
        self.x_speed = pacman_x_speed
        self.y_speed = pacman_y_speed
    def update(self):
        if pacman.rect.x <= 700-30 and pacman.x_speed > 0 or pacman.rect.x >= 0 and pacman.x_speed < 0:
            self.rect.x += self.x_speed
        if self.x_speed > 0: # идем направо
           self.direct = "right"
        elif self.x_speed < 0: # идем налево
           self.direct = "left"
        if pacman.rect.y <= 500-30 and pacman.y_speed > 0 or pacman.rect.y >= 0 and pacman.y_speed < 0:
            self.rect.y += self.y_speed
        if self.y_speed > 0: # идем вниз
           self.direct= "down"
        elif self.y_speed < 0: # идем вверх
           self.direct = "up"
        if self.direct == 'right' and self.rect.x == 675 or self.direct == 'left' and self.rect.x == -5:
            self.x_speed = 0
        if self.direct == 'up' and self.rect.y == -5 or self.direct == 'down' and self.rect.y == 475:
            self.y_speed = 0
    def reset(self):
        window.blit(self.images[self.direct], (self.rect.x, self.rect.y))
        if time.get_ticks() % 7 < 4 and (self.x_speed != 0 or self.y_speed != 0):
            window.blit(transform.scale(image.load('Pclose.png'), (self.size_x, self.size_y)),(self.rect.x, self.rect.y))
pacman_images = {'up':'Pup.png', 'down':'Pdown.png', 'right':'Pright.png', 'left':'Pleft.png'}

class Ghost(sprite.Sprite):
    def __init__(self, ghost_image, ghost_x, ghost_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(ghost_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = ghost_x
        self.rect.y = ghost_y
        self.ghost_x_speed = choice([-4, 4])
        self.ghost_y_speed = choice([-4, 4])
        self.start = time.get_ticks()
    def update(self):
        if time.get_ticks() - self.start < 5000:
            if -5 <= self.rect.y and self.ghost_y_speed < 0:
                self.rect.y += self.ghost_y_speed
            if  self.rect.y <= 475 and self.ghost_y_speed > 0:
                self.rect.y += self.ghost_y_speed
            if -5 <= self.rect.x and self.ghost_x_speed < 0:
                self.rect.x += self.ghost_x_speed
            if self.rect.x <= 675 and self.ghost_x_speed > 0:
                self.rect.x += self.ghost_x_speed
            if self.rect.y >= 475 or self.rect.y <= -5:
                self.ghost_y_speed *= -1
            if self.rect.x >= 675 or self.rect.x <= -5:
                self.ghost_x_speed *= -1
        else:
            if choice([0,1]):
                self.ghost_y_speed = choice([-4,0,4])
                if self.ghost_y_speed == 0:
                    self.ghost_x_speed = choice([-4, 4])
                else:
                    self.ghost_x_speed = choice([-4, 0, 4])
            else:
                self.ghost_x_speed = choice([-4, 0, 4])
                if self.ghost_x_speed == 0:
                    self.ghost_y_speed = choice([-4, 4])
                else:
                    self.ghost_y_speed = choice([-4, 0, 4])
            self.start = time.get_ticks()
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
pacman = Pacman(pacman_images, 350 - 30, 250 - 30, 30, 30, 0, 0)
ghosts = sprite.Group()
ghosts_images = ['bghots.png','wghots.png','blueghots.png','rghots.png']
run = True
init()
while run:
    window.fill((120, 200, 120))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                pacman.x_speed = -5
            elif e.key == K_RIGHT:
                pacman.x_speed = 5
            elif e.key == K_UP:
                pacman.y_speed = -5
            elif e.key == K_DOWN:
                pacman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                pacman.x_speed = 0
            elif e.key == K_RIGHT:
                pacman.x_speed = 0
            elif e.key == K_UP:
                pacman.y_speed = 0
            elif e.key == K_DOWN:
                pacman.y_speed = 0
    pacman.reset()
    pacman.update()
    sprite.spritecollide(pacman, ghosts, True)
    if len(ghosts) == 0:
        for i in range(8):
            ghosts.add(Ghost(ghosts_images[i%4], randint(0, 670), randint(0, 470), 30, 30))
    ghosts.draw(window)
    ghosts.update()
    time.Clock().tick(50)
    display.update()

