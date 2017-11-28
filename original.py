import pygame
import time
import random
import math

class Bullet:

    def draw(self):
        self.hitbox = pygame.draw.circle(screen,pygame.Color('black'),(int(self.x),int(self.y)),self.radius)

    def move(self):

        newx = self.x + self.x_change * self.speed * math.cos(self.angle)
        newy = self.y + self.y_change * self.speed * math.sin(self.angle)

        if newx - self.radius < 0 or newx + self.radius > display_width or newy - self.radius < 0 or newy + self.radius > display_height:
            self.dead = True
        else:
            self.x = newx
            self.y = newy

    def __init__(self,player):

        self.player = player

        self.x_change = 1
        self.y_change = 1

        self.speed = player.bullet_speed
        self.x = player.x
        self.y = player.y
        self.radius = player.bullet_radius
        self.angle = player.angle

        self.dead = False

class Player:

    def move(self):

        newx = self.x + self.x_change * self.speed
        newy = self.y + self.y_change * self.speed

        self.angle += self.angle_change

        if newx - self.radius >= 0 and newx + self.radius <= display_width:
            self.x = newx
        if newy - self.radius >= 0 and newy + self.radius <= display_height:
            self.y = newy


    def spawnBullet(self):
        #Issue with click from menu coming through
        if self.last_shot == 0:
            self.last_shot = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_shot > self.shot_delay:
            self.last_shot = pygame.time.get_ticks()
            self.bullets.append(Bullet(self))

    def handleKeys(self):

        if pygame.mouse.get_pressed()[0]:
            self.spawnBullet()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.x_change = -1
                elif event.key == pygame.K_d:
                    self.x_change = 1
                elif event.key == pygame.K_w:
                    self.y_change = -1
                elif event.key == pygame.K_s:
                    self.y_change = 1
                elif event.key == pygame.K_LEFT:
                    self.angle_change = -math.radians(1)
                elif event.key == pygame.K_RIGHT:
                    self.angle_change = math.radians(1)
                elif event.key == pygame.K_SPACE:
                    self.spawnBullet()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.x_change = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.y_change = 0
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    self.angle_change = 0
    def draw(self):

        #Draw the player
        self.hitbox = pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

        #Get mouse position, if it's on the screen, otherwise we're doing the arrow keys
        if pygame.mouse.get_focused() and self.local:
            (self.mx,self.my) = pygame.mouse.get_pos()

            #Handling division by zero in a terrible way
            if self.mx-self.x == 0:
                self.angle = math.atan((self.my-self.y)/.0001)
            else:
                self.angle = math.atan((self.my-self.y)/(self.mx-self.x))

            #If we are to the left of the player, make sure the gun is facing the right way
            if self.mx < self.x:
                self.angle+=math.radians(180)
        elif self.local:
            #Draw a raycast for aiming assist
            pygame.draw.line(screen,pygame.Color('red'),(self.x,self.y),(display_width * 2 *math.cos(self.angle) + self.x,display_height * 2 * math.sin(self.angle) + self.y))
        #Figure out the gun's position
        gx = self.gun_size * math.cos(self.angle) + self.x
        gy = self.gun_size * math.sin(self.angle) + self.y

        #Draw the gun
        pygame.draw.polygon(screen,self.color,[(self.x,self.y),(gx,gy)],self.gun_width)

        #Draw health

        r = self.radius * .6

        pygame.draw.circle(screen,pygame.Color('red'),(self.x,self.y),int(r))
        if self.hp != 0:
            pygame.draw.circle(screen,pygame.Color('green'),(self.x,self.y),int(r-(self.max_hp-self.hp)*r/self.max_hp))

        #Manage bullets
        for b in self.bullets:
            #Clean up used bullets
            if b.dead:
                self.bullets.remove(b)
            #Move/Draw Bullets
            b.move()
            b.draw()

    def __init__(self, name, local):

        #Player's private variables

        #Start off with no bullets
        self.bullets = []

        self.mx = 0
        self.my = 0

        self.angle = 0

        self.radius = 20
        self.bullet_radius = 10

        self.gun_width = 10
        self.gun_size = self.radius + 10

        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.name = name

        self.x = random.randint(0,display_width - self.radius)
        self.y = random.randint(0,display_height + self.radius)

        self.x_change = 0
        self.y_change = 0

        self.look_x = 0
        self.look_y = 0

        self.speed = 3
        self.bullet_speed = 5

        self.hp = 10
        self.max_hp = self.hp

        self.shot_delay = 500
        self.last_shot = 0

        self.angle_change = 0

        self.local = local

def Menu():
    inmenu = True
    while inmenu:
        header = myfont.render('Welcome to Justin\'s 2D Shooter!',False,(0,0,0))
        screen.blit(header,header.get_rect(center=(display_width/2, display_height/ 25)))

        local = myfont.render('Local Game',False,(0,0,0))
        local_box = screen.blit(local,local.get_rect(center=(display_width/2, display_height/ 4)))

        online = myfont.render('Online Game',False,(0,0,0))
        online_box = screen.blit(online,online.get_rect(center=(display_width/2, display_height/ 3)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and local_box.collidepoint(pygame.mouse.get_pos()):
                inmenu = False

def gameLoop():
    #Create players - player[0] is local
    players = []
    players.append(Player('Justin',True))
    players.append(Player('Bob',False))
    running = True
    while running:
        #Clear the screen
        screen.fill(white)

        #Character handling
        players[0].handleKeys()
        players[0].move()
        for player in players:
            player.draw()

        #Collision detection

        #For every player
        for player in players:
            #Get their bullets
            for bullet in player.bullets:
                #For every other player that isn't us, see if we hit
                for p in players:
                    if bullet.hitbox.colliderect(p.hitbox) and p != bullet.player:
                        print (bullet.player.name + '\'s bullet hit ' + p.name)
                        bullet.dead = True

                        if p.hp > 0:
                            p.hp-=1
                        if p.hp <= 0:
                            #print ('Game over!\n' + player.name + ' Wins!')
                            winner = myfont.render('Game over! ' + player.name + ' Wins!',False,(0,0,0))
                            screen.blit(winner,winner.get_rect(center=(display_width/2, display_height/ 25)))
                            running = False
        #Update display
        pygame.display.update()

        #Advance gametime
        clock.tick(60)

#######MAIN######

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS',30)

display_width = 1280
display_height = 720

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Justin\'s 2D Shooter')
clock = pygame.time.Clock()

start_time = time.time()
running = True
screen.fill(white)

Menu()
while True:
    gameLoop()
    time.sleep(3)
pygame.quit()
quit()
