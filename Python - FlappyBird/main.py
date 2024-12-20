import pygame
from pygame.locals import *
import random

#alustetaan pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60
#Määritetään ruudun koko
screen_width = 800
screen_height = 800
#Luodaan näyttö
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#Määritetään fontti
font = pygame.font.SysFont('Bauhaus 93', 65)
white = (255, 255, 255)

#Luodaan tarvittavat muuttujat
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 175 #Putkien väli
pipe_fequency = 1500 #Kuinka usein uusia putia luodaan. ms
last_pipe = pygame.time.get_ticks() - pipe_fequency
score = 0
pass_pipe = False

#Ladataan tarvittavat kuvat
bg = pygame.image.load('img/bg.png')
bg = pygame.transform.scale(bg, (800, 610))
ground_img = pygame.image.load('img/ground.png')
ground_img = pygame.transform.scale(ground_img, (860, 200))
button_img = pygame.image.load('img/restart.png')
button_img = pygame.transform.scale(button_img, (120, 40))

#Tekstin piirtäminen ruudulle
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
#Pelin reset
def reset_game():
    pipe_group.empty() #Poistetaan putket ryhmästä
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2) #Asetetaan hahmo takaisin lähtöpisteeseen
    score = 0 #Nollataan pisteet
    return score

#Bird luokka hahmolle. 
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1,4): #Hahmon kuvat. Kuvia on kolme joita vaihdellaan nopeasti että näyttää että hahmo heiluttaa siipiä
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0 # Painovoima aluksi
        self.clicked = False

    def update(self):

        if flying == True: #jos peli on käynnissä
            
            self.vel += 0.5 #Painovoima kasvaa
            if self.vel > 8: # Painovoiman maksimi
                self.vel = 8
            if self.rect.bottom < 600:  #Estää linnun putoamisen maasta läpi
                self.rect.y += int(self.vel)

        if game_over == False:
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #Hyppy , Hiiren vasen
                self.clicked = True
                self.vel = -10 # Hypyn nopeus
            if pygame.mouse.get_pressed()[0] == 0: #Varmistaa, että hiirtä ei voi pitää pohjassa
                self.clicked = False

            #Hahmon animaatio
            self.counter += 1
            flappy_cooldown = 5
            if self.counter > flappy_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #Hypätessä hahmo pyörähtää haluttuun suuntaan
            self.image = pygame.transform.rotate(self.images[self.index],self.vel * -2 )

        else: 
            self.image = pygame.transform.rotate(self.images[self.index], -90 )

#Luokka putkille
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()

        #Asetetaan esteet. Positio 1 on ylhäältä ja -1 on alhaalta
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft =[x,y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_speed # Putki liikkuu vasemmalle
        if self.rect.right < 0:# Poistetaan putki kun se menee ruudun ulkopuolelle
            self.kill()  

#Nappi luokka jolla käynnistetään peli uudelleen
class Button():
    def __init__(self, x , y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos): #Hiiri menee napin päälle
            if pygame.mouse.get_pressed()[0] == 1: #Hiiren klikkaus napin päällä
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))  #Piirretään nappi näytölle   
        return action

#Luodaan ryhmät hahmolle ja putkille
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#Luodaan hahmo
flappy = Bird(100,int(screen_height / 2))
#Lisätään ryhmään
bird_group.add(flappy)

#Luodaan nappi
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


run = True
while run:
    clock.tick(fps)

    #Asetetaan tausta
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    

    #Asetetaan maa
    screen.blit(ground_img, (ground_scroll,600))

    #Tarkistetaan pistemäärä
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
            
    #Piirretään pisteet ruudulle
    draw_text(str(score), font, white, int(screen_width/2), 20)

    #Hahmon törmäys
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #Jos hahmo osuu maahan
    if flappy.rect.bottom >= 599:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #Luodaan uusia putkia
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_fequency:
            pipe_height = random.randint(-150, 25)
            btm_pipe = Pipe(screen_width, int(screen_height / 2)+pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2)+pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        #Scrollataan maata
        screen.blit(ground_img, (ground_scroll,600))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 60:
            ground_scroll = 0
        pipe_group.update()

    #Jos peli on ohi, näytetään reset nappi
    if game_over == True:
       if button.draw() == True:
           game_over = False
           score = reset_game() #Nollataan pisteet

    #Käsitellään pelin aloitus tai pelin lopetus
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
    
#Lopetetaan peli
pygame.quit()