from pygame import *
import time
import random

init()

window = display.set_mode((700, 500))
display.set_caption('Морские приключения')
picture = transform.scale(image.load('sea.jpg'), (700, 500)) #создание игрового окна


diver = 'submarine2_0.png'
wood = 'walls.png' #переменные с картинками
trident = 'torpedo.png'
monster = 'monster.png'
treasure = 'treasure.png'
explosion = 'explosion.png'

gameover = transform.scale(image.load('gameover.jpg'), (700, 500))
victory = transform.scale(image.load('victory.jpg'), (700, 500)) #Два конечных экрана

wait_picture = transform.scale(image.load('yes.jpg'), (700, 500))

class Pic(sprite.Sprite):
    def __init__(self, picture, x, y, w, h, x_speed, y_speed):
        super().__init__()
        self.picture = picture
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_speed = x_speed
        self.y_speed = x_speed

        self.sprite = transform.scale(image.load(picture), (w, h))
    
    def reset(self):
        window.blit(self.sprite, (self.x, self.y))


hero = Pic(diver, 120, 400, 100, 50, 0, 0) #создание главного героя

weapon = list() #создание списка с оружием

walls = list()
walls.append(Pic(wood, 300, 280, 50, 240, 0, 0))
walls.append(Pic(wood, 370, 85, 50, 200, 0, 0))
walls.append(Pic(wood, 160, 260, 400, 50, 0, 0)) #три стены

monster = Pic(monster, 200, 0, 150, 100, 0.2, 0) #противник

treasure = Pic(treasure, 350, 400, 100, 100, 0, 0) #конечная цель

run = True
finish = False
result = True
monster_alive = True
time1 = time.time() #взрыв должен идти около 0,15 секунд, поэтому я завел переменную time1, контролирующую это

window.blit(wait_picture, (0, 0)) #заставка
start_time = time.time()
display.update()
for wait in range(9999999):
    if time.time() - start_time > 2.5: #заставка идет две с половиной секунды
        break


wait_font = font.SysFont('arial', 40)
text_wait = wait_font.render('Press ENTER to play', False, (150, 255, 255)) #Начальный экран

advices = ('Если двигаться по диагонали, ваша скорость будет в 1,5 раза больше!', 'У нас также есть кликер!', 'Первоначально эта игра была про плохих людей!', '!', '', 'Ракета делает бом-бом!!!', 'А ведь у этого монстра могут быть дети...', 'Мы сейчас делаем пародию на Гугл-Динозаврика!')
random_advice = random.randint(1, len(advices)) #интересные факты и советы
random_advice = advices[random_advice - 1]

advice_font = font.SysFont('arial', 20)
text_advice = advice_font.render(random_advice, False, (220, 200, 200))
paint_time = 0
wait = True
start_time = time.time() #динаминый начальный экран
a = 1#по порядку то надпись, то темный экран
while wait:
    display.update()
    if time.time() - start_time> 0.5:
        if a ==1:
            window.fill((0, 100, 150))
            window.blit(text_advice, ((700 - (len(random_advice)*10))/2, 450))
            a = 0
        else:
            window.blit(text_wait, (165, 200))
            a = 1
        start_time = time.time()

    for i in event.get():
        if i.type == KEYDOWN:
            if i.key == 13:
                wait = False
        if i.type == QUIT:
            run = False
            wait = False



while run:
    
    if not(finish): #если герой не умер или не достиг цели
        window.blit(picture, (0, 0))

        if time.time() - time1 > 0.15 and len(weapon)>0 and weapon[0].x_speed == 0: #проверка времени с последнего взрыва
            weapon.remove(weapon[0]) 

        if len(weapon)>1:
            weapon.remove(weapon[0]) #последняя торпеда должна взорваться, чтобы пустить следующую
            
        if len(weapon) > 0: #движение торпеды
            weapon[0].x += weapon[0].x_speed
        
        monster.y += monster.y_speed #движение монстра

        hero.y += hero.y_speed
        hero.x += hero.x_speed #движение главного героя

        if monster.y+monster.h > 200 or monster.y<0:
            monster.y_speed = 0 -monster.y_speed #противник передвигается в определенной области
        
        if monster_alive:
            monster.reset() #отрисовка монстра

        for i in walls:
            i.reset() #отрисовка всех стен
        
        treasure.reset() #отрисовка сокровища

        for i in weapon:
            i.reset() #отрисовка торпеды
    
        hero.reset() #отрисовка главного героя
    
        for i in event.get(): 
        
            if i.type == QUIT: 
                run = False
        
            if i.type == KEYDOWN:
            
                k = i.key

                if k == 27:
                    run = False #выход на клавишу Escape
            
                if k == 1073741906:
                    hero.y_speed-=0.2
            
                if k == 1073741905:
                    hero.y_speed+=0.2
            
                if k == 1073741903:
                    hero.x_speed+=0.2
            
                if k == 1073741904:
                    hero.x_speed-=0.2
            
                if k == 32: #пуск оружия при нажатии на пробел
                
                    if len(weapon) == 0:
                        weapon.append(Pic(trident, hero.x+hero.w-50, hero.y, 40, 20, 0.3, 0)) #только одна торпеда может быть в полете
        
            if i.type == KEYUP:
            
                k = i.key 
            
                if k == 1073741906:
                    hero.y_speed+=0.2
            
                if k == 1073741905:
                    hero.y_speed-=0.2
            
                if k == 1073741903:
                    hero.x_speed-=0.2
            
                if k == 1073741904:
                    hero.x_speed+=0.2    
        for a in walls:
            for c in range(int(hero.y), int(hero.y) + hero.h):
                if int(hero.x) in range(a.x, a.x+a.w) or int(hero.x)+hero.w in range(a.x, a.x+a.w):
                    if c in range(a.y, a.y + a.h): #проверка для каждого y, не вошел ли герой в стену
                        result = False
                    
                        finish = True
                
                if int(hero.x) in range(treasure.x, treasure.x + treasure.w):
                    if c in range(treasure.y, treasure.y+treasure.h):
                        result = True

                        finish = True #не коснулся ли герой сокровища
                
                if monster_alive: #если монстр жив
                    if int(hero.x) + hero.w in range(monster.x, monster.x+monster.w):
                        if c in range(int(monster.y), int(monster.y) + monster.h): #коснулся ли главный герой живого монстра
                            result = False 

                            finish = True
            
            for c in range(int(hero.x), int(hero.x)+hero.w):
                if int(hero.y) in range(a.y, a.y+a.h) or int(hero.y)+ hero.h in range(a.y, a.y+a.h):
                    if c in range(a.x, a.x+a.w):
                        result = False #проверка для каждого х, не вошел ли в стену персонаж

                        finish = True


        if len(weapon)>0 and weapon[0].x_speed > 0:   
            for b in walls:
            
                if int(weapon[len(weapon)-1].x)+weapon[len(weapon)-1].w in range(b.x, b.x+b.w) and weapon[len(weapon)-1].x_speed != 0:

                    if int(weapon[len(weapon)-1].y+weapon[len(weapon)-1].h/2) in range(b.y, b.y+b.h):
                        weapon[len(weapon)-1].x_speed = 0
                        weapon[len(weapon)-1].sprite = transform.scale(image.load(explosion), (weapon[len(weapon)-1].w+100, weapon[len(weapon)-1].h+100))
                        weapon[len(weapon)-1].x += weapon[len(weapon)-1].w/4 #врезалась ли ракета в стену
                        weapon[len(weapon)-1].y -= weapon[len(weapon)-1].h*3 #взрыв торпеды

                        time1 = time.time()
            
            if monster_alive:
                    if int(weapon[len(weapon)-1].x)+weapon[len(weapon)-1].w in range(monster.x, monster.x+monster.w):

                        if int(weapon[len(weapon)-1].y+weapon[len(weapon)-1].h/2) in range(int(monster.y), int(monster.y)+monster.h):  #попала ли торпеда в монстра
                            
                            weapon[len(weapon)-1].x_speed = 0
                            monster.y_speed = 0
                            
                            weapon[len(weapon)-1].sprite = transform.scale(image.load(explosion), (weapon[len(weapon)-1].w+100, weapon[len(weapon)-1].h+100))
                            weapon[len(weapon)-1].x += weapon[len(weapon)-1].w/2
                            weapon[len(weapon)-1].y -= weapon[len(weapon)-1].h*3 #взрыв торпеды
                            
                            monster_alive = False

                            time1 = time.time()

            if weapon[0].x > 750:
                weapon.remove(weapon[0]) #при вылете за зону видимости, торпеда сама пропадает
                        
    
    if finish: #экран после поражения/победы
        for i in event.get():
            if i.type == QUIT:
                run = False
        
            if i.type == KEYDOWN:
            
                k = i.key

                if k == 27:
                    run = False 

        if time.time() - paint_time > 2000:
            paint_time = time.time()
        if time.time() - paint_time >= 1200:
            if not(result):
                window.fill((0, 0, 0))
            else:
                window.fill((255, 255, 255))
            display.update()
        elif time.time() - paint_time < 800:
            if result == False:
                window.blit(gameover, (0, 0))
            else:
                window.blit(victory, (0, 0))
            display.update()
        paint_time -= 1
    
    display.update()