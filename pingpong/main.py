import pygame
from random import randint
class Hitbox():
    def __init__(self,screen,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
    
    def draw_hitbox(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 3)
    
class Picture(Hitbox):
    def __init__(self,screen,x,y,width,height,color,img_path):
        Hitbox.__init__(self,screen,x,y,width,height,color)
        self.img_path = img_path
        self.image = pygame.transform.scale(pygame.image.load(self.img_path).convert_alpha(), (self.width, self.height))
        
    def draw_picture(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(Picture):
    def __init__(self,screen,x,y,width,height,color,img_path,speed,has_damage):
        Picture.__init__(self,screen,x,y,width,height,color,img_path)
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.has_damage = False

    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy
    
    def controller(self,player_id):
        global seven,bullets
        
        keys = pygame.key.get_pressed()
        if player_id == 1:
            if keys[pygame.K_a] and  not keys[pygame.K_d]:
                self.dx = -1
            elif keys[pygame.K_d] and  not keys[pygame.K_a]:
                self.dx = 1
            else:
                self.dx = 0
            if keys[pygame.K_w] and  not keys[pygame.K_s]:
                self.dy = -1
            elif keys[pygame.K_s] and  not keys[pygame.K_w]:
                self.dy = 1
            else:
                self.dy = 0
            
                



            
        if player_id == 2:
            if keys[pygame.K_LEFT] and  not keys[pygame.K_RIGHT]:
                self.dx = -1
            elif keys[pygame.K_RIGHT] and  not keys[pygame.K_LEFT]:
                self.dx = 1
            else:
                self.dx = 0
            if keys[pygame.K_UP] and  not keys[pygame.K_DOWN]:
                self.dy = -1
            elif keys[pygame.K_DOWN] and  not keys[pygame.K_UP]:
                self.dy = 1
            else:
                self.dy = 0
           
    def collide_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_hight:
            self.rect.bottom = screen_hight

    def collide_wall(self,player_id):
        if self.rect.colliderect(red_zone.rect):
            if player_id == 2:
                self.rect.left = red_zone.rect.right
            if player_id == 1:
                self.rect.right = red_zone.rect.left

    def collide_ball(self, sprite, player_id):
        if self.rect.colliderect(sprite.rect):
            if player_id == 1:
                sprite.rect.left = self.rect.right + 5
                sprite.dx *= -1
            elif player_id == 2:
                sprite.rect.right = self.rect.left - 5
                sprite.dx *= -1
            sprite.dy = self.dy


red_points = 0
blue_points = 0
    
class Ball(Picture):
    def __init__(self,screen,x,y,width,height,color,img_path,speed):
        Picture.__init__(self,screen,x,y,width,height,color,img_path)
        self.speed = speed
        self.dx = 0
        self.dy = 0

    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy
    
    def start_move(self):
        random_number = randint(1,2)
        if random_number == 1:
            self.dx = -1
        elif random_number == 2:
            self.dx = 1
class Bullet(Picture):
    def __init__(self,screen,x,y,width,height,color,img_path,speed):
        Picture.__init__(self,screen,x,y,width,height,color,img_path)
        self.speed = speed
        self.dx = 1
        
        self.image = pygame.transform.rotate(self.image, 270)
    def move(self):
        self.rect.x += self.speed * self.dx




screen_title = 'Pingpong'
screen_width = 1800
screen_hight = 900
screen_color = (0, 200, 0)
screen = pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption(screen_title)

background = Picture(screen,0,0,1800,900,(0,0,0),'galaxy.jpg')
player1 = Player(screen,50,450,150,200,(0,0,0),'ufo.png',6,False)
player2 = Player(screen,1600,450,150,200,(0,0,0),'ufo.png',6,False)
red_zone = Picture(screen,850,0,50,900,(0,0,0),'square.png')
ball = Ball(screen,900,450,75,75,(0,0,0),'medicine-ball.png',7)



ball = Ball(screen,900,450,75,75,(0,0,0),'medicine-ball.png',6)
ball.start_move()


is_on = True
fps = 60
clock = pygame.time.Clock()
pygame.init()


ball.start_move()


damage_counter = 0
damage_delay = 2
bullets = list()
while is_on == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                bullet = Bullet(screen,0,0,25,25,(0,0,0),'bullet.png',7)
                bullet.rect.left = player1.rect.right
                bullet.rect.centery = player1.rect.centery
                bullets.append(bullet)
    
    
        
  
                
    


        
    screen.fill(screen_color)
    background.draw_picture()

   

    for bullet in bullets:
        bullet.move()
        bullet.draw_picture()
        if bullet.rect.right >= 1800:
            bullets.remove(bullet)
        if player2.rect.colliderect(bullet.rect):
            if player2.has_damage == False:
                player2.has_damage = True
            bullets.remove(bullet)

            
    
        
    if player2.has_damage == True:
        if damage_counter >= fps * damage_delay:
            player2.has_damage = False
            damage_counter = 0
        else:
            damage_counter += 1
        
    if player2.has_damage == True:
        player2.dx, player2.dy = 0, 0
               






    


    red_zone.draw_picture()

    player1.draw_picture()
    player2.draw_picture()
    player1.move()
    player2.move()
    player1.controller(1)
    player2.controller(2)
    player1.collide_wall(1)
    player2.collide_wall(2)
    player1.collide_screen()
    player2.collide_screen()
    ball.draw_picture()
    ball.move()
    player1.collide_ball(ball,1)
    player2.collide_ball(ball,2)
    screen.blit(pygame.font.SysFont(None,60).render('POINTS:'+ str(red_points), True, (100,0,0)), (60,60))
    screen.blit(pygame.font.SysFont(None,60).render('POINTS:'+ str(blue_points), True, (0,200,0)), (1500,60))

    if ball.rect.bottom > screen_hight:
        if ball.rect.x < 900:
            blue_points += 1
            ball.rect.x = 900
            ball.rect.y = randint(100,600)
            ball.dx = 1
            ball.dy = 0
        elif ball.rect.x > 900:
            red_points += 1
            ball.rect.x = 900
            ball.rect.y = randint(100,600)
            ball.dx = -1
            ball.dy = 0

    if ball.rect.top < 0:
        if ball.rect.x < 900:
            blue_points += 1
            ball.rect.x = 900
            ball.rect.y = randint(100,600)
            ball.dx = 1
            ball.dy = 0
        elif ball.x > 900:
            red_points += 1
            ball.rect.x = 900
            ball.rect.y = randint(100,600)
            ball.dx = -1
            ball.dy = 0
            
    if ball.rect.right > screen_width:

        red_points += 1
        ball.rect.x = 900
        ball.rect.y = randint(100,600)
        ball.dx = -1
        ball.dy = 0
        
    if ball.rect.left < 0:
        blue_points += 1
        ball.rect.x = 900
        ball.rect.y = randint(100,600)
        ball.dx = 1
        ball.dy = 0

    


    
    
    
        
    
        



    



    






















































    pygame.display.update()
    clock.tick(fps)

