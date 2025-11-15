import time
from pygame import *
from random import randint
font.init()
font2 = font.SysFont('Arial', 40)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Astroshoot")
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"
max_lost = randint(10,15)
lost = 0
score = 0
goal = randint(10,15)
font1 = font.SysFont('Arial', 40)
background = transform.scale(image.load(img_back), (win_width, win_height))
finish = False
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x,self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y =0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
    

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed  

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
spaceship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
game = True
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                spaceship.fire()
    if finish != True:
        window.blit(background,(0,0))
        text_lose = font2.render("ufo's that are invading earth because of you:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text = font2.render("murders(humans literally eat everything):" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        asteroids.update()
        spaceship.update()
        spaceship.reset()
        bullets.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        win = font1.render('YOU Are A Murderer!', True, (255,255,255))
        lose = font1.render('YOUr Home Planet Is Destroyed!!!', True, (255,255,255))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy,randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add (monster)

        if sprite.spritecollide(spaceship, monsters, False) or sprite.spritecollide(spaceship, asteroids, False) :
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    else:
        finish = False
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
    clock.tick(FPS)

