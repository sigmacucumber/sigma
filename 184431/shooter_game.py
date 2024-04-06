from pygame import *
from pygame import draw as py_draw
from random import randint
from time import sleep
gamemode = 0 
kills = 0
font.init()
font1 = font.Font(None, 36)
bigfont = font.Font(None, 60)
life = 1
r = 30
h = 700
w = 1000
window = display.set_mode((w, h))
display.set_caption('чиназес')
enemy = transform.scale(image.load('enemy.png').convert_alpha(), (80, 90))
#starimage = image.load('star.png').convert_alpha()
#bullet = image.load('shot.png').convert_alpha()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w = 50, h = 60):
        super().__init__()
        self.image = transform.scale(image.load(player_image).convert_alpha(), (w, h))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    reload = r
    health = 100
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.player_speed
        if keys[K_RIGHT] and self.rect.x < (w - 60):
            self.rect.x += self.player_speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.player_speed
        if keys[K_DOWN] and self.rect.y < (h - 120):
            self.rect.y += self.player_speed
        if keys[K_SPACE]:
            self.fire()
        if self.reload < r:
            self.reload += 1
    def fire(self):
        if self.reload >= r:
            
            if bonus > 0:
                powershot.play()
                shot = Shot('shot.png', self.rect.x - 5, self.rect.y, 20, 40, 40)
                shots.add(shot)
                shot = Shot('shot.png', self.rect.x + 45, self.rect.y, 20, 40, 40)
                shots.add(shot)
            else:
                shotsound.play()
                shot = Shot('shot.png', self.rect.x + 20, self.rect.y, 20, 40, 40)
                shots.add(shot)
            

            self.reload = 0
        if self.rect.y < -50:
            self.kill()

    def draw(self):
        if self.health > 0:
            super().reset()
            rect1 = Rect(self.rect.x, self.rect.bottom, self.rect.w * self.health/100, 5)
            rect2 = Rect(self.rect.x, self.rect.bottom, self.rect.w, 5)
            color = (255 - int(255*self.health/100), int(255*self.health/100), 0)
            py_draw.rect(window, color, rect1)
            py_draw.rect(window, color, rect2, 2)
        if self.health == 0:
            global gamemode
            gamemode = 'loose'
            lox_center = lox.rect.center
            Boom(lox_center, loose_boom, booms)
            self.health -= 1


    
    def health_damage(self):
        self.health -= 20

    
        

class Star(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y > h:
            stars.remove(self)


class Ufo(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w = 50, h = 60):
        super().__init__()
        self.image = player_image
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y > h:
            ufos.remove(self)
            global mistakes
            mistakes += 1
            mistakesound.play()
        if self.rect.y > h:
            self.kill()

class Shot(GameSprite):
    def update(self):
        self.rect.y -= self.player_speed
        if self.rect.y < -50:
            shots.remove(self)

class Skins(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, pic_name):
        super().__init__()
        self.pic_name = pic_name
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def return_picname(self):
        return self.pic_name


class Boom(sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms, loops_amount = 0) -> None:
        super().__init__() 
        #global booms, boom_sprites 
        self.loops_amount = loops_amount
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1  
        
    
    def update(self):
        if self.loops_amount == 0:
            self.next_frame()
            if self.frame_num == len(self.frames)-1:
                self.kill()
        else:
            self.rect.y += 2
            if self.rect.y > h:
                self.kill()
            else:
                self.next_frame()
                if self.frame_num == len(self.frames)-1:
                    self.frame_num = 0
                



            
def sprites_load(folder, file_name, size, colorkey):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = image.load(f'{folder}\\{file_name}{num}.png')
            spr = transform.scale(spr,size)
            if colorkey: spr.set_colorkey((0,0,0))
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites





background = transform.scale(image.load('galaxy.png'), (w, h))
loosebg = transform.scale(image.load('loose.png'), (w, h))
#good = transform.scale(image.load('win.jpg'), (w, h))

is_skin = 0
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
kick = mixer.Sound('fire.ogg')
shotsound = mixer.Sound('shot.ogg')
powershot = mixer.Sound('powershot.ogg')
boom1 = mixer.Sound('boom1.ogg')
boom1.set_volume(0.5)
boom2 = mixer.Sound('boom2.ogg')
boom2.set_volume(0.5)
boom3 = mixer.Sound('boom3.ogg')
boom3.set_volume(0.5)
boom4 = mixer.Sound('boom4.ogg')
boom4.set_volume(0.5)
bonuscoin = mixer.Sound('coin.ogg')
mistakesound = mixer.Sound('mistake.ogg')
bonus = 0
ticks = 0

mistakes = 0

play_but = GameSprite('play.png', 435, 450, 0, 100, 50)
skin_but = GameSprite('skin_ch.png', 435, 500, 0, 100, 50)
menu_but = GameSprite('menu_but.png', 900, 0, 0, 100, 70)
exit_but = GameSprite('exit_but.png', 400, 300, 0, 200, 100)
cont_but = GameSprite('cont_but.png', 400, 400, 0, 205, 100) 
start_text = GameSprite('text.png', 300, 100, 0, 400, 200)

chosen_skin = 'skin1.png'
lox = Hero(chosen_skin, 500, 500, 10, 80, 100)




boom_sprites = sprites_load('boom4', 'boom', (150, 150), (0, 0, 0))
loose_boom = sprites_load('boom4', 'boom', (300, 300), (0, 0, 0))
coin_sprites = sprites_load('coin', 'i', (50, 50), (255,255,255) )

stars = []

skins = ['skin1', 'skin2', 'skin3', 'skin4', 'skin5', 'skin6']
skin_choise = sprite.Group()
x = 1
for s in skins:
    skinpic = transform.scale(image.load('skin' + str(x) + '.png').convert_alpha(), (100, 150))
    skin = Skins(skinpic, -70 + x*150, h-150, 'skin' + str(x) + '.png')
    skin_choise.add(skin)
    x += 1



coins = sprite.Group()

ufos = sprite.Group()

collides = []

shots = sprite.Group()

booms = sprite.Group()

hero = sprite.Group()
hero.add(lox)

clock = time.Clock()

play = True

finish = False
win = False
while play:
    
    for e in event.get():
        if e.type == QUIT:
            play = False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                play = False
        
        

    
    if not finish:


        if mistakes >= 3:
            gamemode = 'loose'
        if gamemode != 'loose':
            window.blit(background, (0,0))
        if gamemode == 1:
            
            for star in stars:
                star.reset()
                star.update()
            shots.update()
            ufos.update()
            
            booms.update()
            coins.update()
            lox.draw()

            ufos.draw(window)
            shots.draw(window)
            booms.draw(window)
            coins.draw(window)
            if life == 1:
                lox.update()
                lox.reset()
            menu_but.reset()

            window.blit(font1.render(f'Время бонуса: {round((bonus/60) , 1)}', True, (255, 0, 0)), (20,h - 50))
            window.blit(font1.render(f'Пропущено врагов: {mistakes}', True, (255, 0, 0)), (20,20))
            window.blit(font1.render(f'Уничтожено врагов: {kills}', True, (255, 0, 0)), (20,70))

        
            if ticks % 5 == 0:
                size = randint(10, 30)
                x = randint(0, w)
                speed = int(size/2)
                star = Star('star.png',x , -10, speed, size, size)
                stars.append(star)

            if ticks % 60 == 0:
                x = randint(0, w- 100)
                speed = randint(2, 7)
                ufo = Ufo(enemy, x , -100, speed, 100, 100)
                ufos.add(ufo)
                


            collides = sprite.groupcollide(ufos, shots, True, True)
            if collides:
                for ufo, shot in collides.items():
                    kills += 1
                    boomnum = randint(1, 4)
                    if boomnum == 1:
                        boom1.play()
                    if boomnum == 2:
                        boom2.play()
                    if boomnum == 3:
                        boom3.play()
                    if boomnum == 4:
                        boom4.play()
                

                ufo_center = ufo.rect.center
                Boom(ufo_center, boom_sprites, booms)
                luck = randint(1, 10)
                if luck == 10:
                    Boom(ufo_center, coin_sprites, coins, 200)

            damage = sprite.spritecollide(lox, ufos, True)
            if damage:
                kills += 1
                boomnum = randint(1, 4)
                if boomnum == 1:
                    boom1.play()
                if boomnum == 2:
                    boom2.play()
                if boomnum == 3:
                    boom3.play()
                if boomnum == 4:
                    boom4.play()

                lox.health_damage()
            
            for ufo in damage:
                ufo_center = ufo.rect.center
                Boom(ufo_center, boom_sprites, booms)

            farms = sprite.groupcollide(coins, hero, True, False)
            if farms:
                bonus += 600
                bonuscoin.play()

        
            ticks += 1
            if bonus > 0:
                bonus -= 1
                
            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                menu_click = menu_but.rect.collidepoint(mouse_pos)
                if menu_click:
                    gamemode = 2
        if gamemode == 0:
            skin_but.reset()
            play_but.reset()
            start_text.reset()
            if is_skin == 1:
                skin_choise.draw(window)

            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                for curskin in skin_choise:
                    click_onskin = curskin.rect.collidepoint(mouse_pos)
                    if click_onskin:
                        chosen_skin = curskin.return_picname()
                        lox = Hero(chosen_skin, 500, 500, 10, 80, 100)
                        hero.add(lox)


            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                click = play_but.rect.collidepoint(mouse_pos)
                if click:

                    gamemode = 1
                    lox = Hero(chosen_skin, 500, 500, 10, 80, 100)
                    hero.add(lox)
                    for ufo in ufos:
                        ufo.kill()
                    is_skin = 0
                    bonus = 0
                    mistakes = 0
                    kills = 0

            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                skin_click = skin_but.rect.collidepoint(mouse_pos)
                if skin_click: 
                    is_skin = 1
                    

        
        if gamemode == 2:
            ufos.draw(window)
            shots.draw(window)
            booms.draw(window)
            coins.draw(window)
            if life == 1:
                lox.reset()
            menu_but.reset()
            exit_but.reset()

            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                exit_click = exit_but.rect.collidepoint(mouse_pos)
                if exit_click:
                    gamemode = 0
                    lox = Hero(chosen_skin, 500, 500, 10, 80, 100)
                    hero.add(lox)
                    for ufo in ufos:
                        ufo.kill()
                    bonus = 0
                    mistakes = 0
                    kills = 0
                    #тут надо чтоб все пропали

            for star in stars:
                star.reset()



            cont_but.reset()

            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                cont_click = cont_but.rect.collidepoint(mouse_pos)
                if cont_click:
                    gamemode = 1


        if gamemode == 'loose':
            window.blit(loosebg, (0,0))
            skin_but.reset()
            play_but.reset()
            booms.update()
            booms.draw(window)
            window.blit(bigfont.render('Земля захвачена', True, (0, 255, 0)), (w/2 - 100,h/2 - 100))
            if is_skin == 1:
                skin_choise.draw(window)

            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                for curskin in skin_choise:
                    click_onskin = curskin.rect.collidepoint(mouse_pos)
                    if click_onskin:
                        chosen_skin = curskin.return_picname()
                        lox = Hero(chosen_skin, 500, 500, 10, 80, 100)
                        hero.add(lox)
                        


            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                click = play_but.rect.collidepoint(mouse_pos)
                if click:
                    gamemode = 1
                    is_skin = 0
                    lox = Hero(chosen_skin, 500, 500, 10, 80, 100)
                    hero.add(lox)
                    for ufo in ufos:
                        ufo.kill()
                    bonus = 0
                    mistakes = 0
                    kills = 0

            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                skin_click = skin_but.rect.collidepoint(mouse_pos)
                if skin_click: 
                    is_skin = 1




            
            
            
        display.update()
    clock.tick(60)
