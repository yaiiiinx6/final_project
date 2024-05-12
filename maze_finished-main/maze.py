from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x =65, size_y = 65):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        # картинка стіни - прямокутник потрібних розмірів та кольору
        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))
        # кожен спрайт повинен зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load('lawn.png'), (win_width, win_height ))

player = Player('flower.png', 5, win_height - 80, 3)
monster = Enemy('zombie.png', win_width - 80, 280, 2)
monster2 = Enemy('zombie2.png', win_height - 90, 140, 3)
final = GameSprite('win.png', win_width - 120, win_height - 80, 0)
help = GameSprite('apple.png', win_height - 80, 60, 0)
small = GameSprite('small.png',400, 350, 1)
# help = GameSprite('apple.png',100, 350, 0)

w1 = Wall(150, 100, 60, 110, 10, 430, 15)
w2 = Wall(150, 100, 60, 110, 440, 300, 15)
w3 = Wall(150, 100, 60, 110, 10, 20, 330)
w4 = Wall( 150, 100, 60, 110, 150, 200, 15)
w5 = Wall( 150, 100, 60, 110, 330, 300, 15)
w6 = Wall(150, 100, 60, 210, 240, 400, 15)
w7 = Wall(150, 100, 60, 500, 230, 15, 350)

# написи
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (225, 0, 0))
lose = font.render('YOU LOSE!', True, (220, 0, 0))


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

game = True
finish = False
clock = time.Clock()
FPS = 66

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()
        monster2.update()
        help.update()
        small.update()


        player.reset()
        monster.reset()
        monster2.reset()
        final.reset()
        help.reset()
        small.reset()


        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()


    # Ситуація "Програш"
    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7):
        finish = True
        window.blit(lose, (210, 210))
        kick.play()

    if sprite.collide_rect(player, help):
        player.speed = 5
        help.image = Surface((0, 0), SRCALPHA)

    if sprite.collide_rect(player, small):
        player.image = transform.scale(image.load('flower.png'), (49, 49))
        player.rect = player.image.get_rect()
        player.rect.x = 400
        player.rect.y = 350
        small.image = Surface((0, 0), SRCALPHA)
        small.rect.x = 0
        small.rect.y = 0


    # Ситуація "Перемога"
    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (210, 210))
        money.play()


    display.update()
    clock.tick(FPS)
