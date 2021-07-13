import random
import pygame
import os
import math
import sys
from pygame.locals import*
pygame.init()
win=pygame.display.set_mode((800,447))
pygame.display.set_caption('first game')
# This goes outside the while loop, near the top of the program
walkRight=[pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft=[pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.png').convert()
bgx=0
p=8
#saw=[pygame.image.load(os.path.join('icon/saw','SAW0.png')),pygame.image.load(os.path.join('icon/saw','SAW1.png')),pygame.image.load(os.path.join('icon/saw','SAW2.png')),pygame.image.load(os.path.join('icon/saw','SAW3.png'))]

bgx2=bg.get_width()
char = pygame.image.load('standing.png')
clock=pygame.time.Clock()
score=0
music=pygame.mixer.music.load('music.mp3')           #back ground music
pygame.mixer.music.play(-1)
count_level=1
new_goblin=0
class player(object):
    def __init__(self,x,y,width,height):
        self.isjump=False
        self.jump_count=10
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.run=True
        self.left=False
        self.right=False
        self.walkcount=0
        self.standing=True
        self.hitbox=(self.x+20,self.y,28,60)
    def draw(self,win):
        if self.walkcount +1>=27:
            self.walkcount=0
  
       # if not(self.standing):
        if self.left:
            win.blit(walkLeft[self.walkcount//3],(self.x,self.y))
            self.walkcount+=1
        elif self.right:
            win.blit(walkRight[self.walkcount//3],(self.x,self.y))
            self.walkcount+=1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox=(self.x+20,self.y,28,60)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        hit_sound=pygame.mixer.music.load('hit.mp3')         #hit sound
        pygame.mixer.music.play(0)
        self.isjump=False
        self.jumpcount=10
        self.x=100
        self.y=310
        self.walkcount=0
        font1=pygame.font.SysFont('comicsans',50)
        text=font1.render('-5',1,(255,0,0))
        win.blit(text,(250-(text.get_width()/2),200))
        pygame.display.update()
        i=0
        while i<300:
            pygame.time.delay(1)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()
                    run=False
                    quit()
        
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
    
class enemy(object):
    walkRight=[pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft=[pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkcount=0
        self.vel=2
        self.path=(self.x-300,self.y+450)
        self.hitbox=(self.x+20,self.y,28,60)
        self.health=10
        self.visible=True
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkcount+1>=33:
                self.walkcount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            else:
                win.blit(self.walkLeft[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50+new_goblin,10))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,50+new_goblin -(5*(10-self.health)),10))
            self.hitbox=(self.x+20,self.y,28,60)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def move(self):
        if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkcount=0
        else:
            if self.x-self.vel>self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkcount=0
    def hit(self):
        if self.health>0:
            hit_sound=pygame.mixer.music.load('hit.mp3')         #hit sound
            pygame.mixer.music.play(0)
            self.health-=1
        else:
            self.visible=False

       
    
# for draw character on the window
def redrawGameWindow():
    #win.blit(bg,(-985,0)) #for set Background window with bg pic
    win.blit(bg,(bgx,0))
    win.blit(bg,(bgx2,0))
    text=font.render('SCORE:'+str(score),1,(0,0,0))  #put font on the screen
    text_level=font.render('LEVEL:'+str(count_level),1,(0,0,0))
    win.blit(text,(350,10))
    win.blit(text_level,(200,10))
    man.draw(win)
    #win.blit(saw[f],(400,320))
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

speed=30


#main loop
font=pygame.font.SysFont('comicscans',30,True) #create font
bullets=[]
man=player(200,310,64,64)
goblin=enemy(300,310,64,64,450)
size=10

    
    
shootloop=0

        
while man.run:
    p-=1
    f=7%p
    if p==4:
        p=8

    
    while not goblin.visible:
        goblin=enemy(100,310,64,64,450)
        font2=pygame.font.SysFont('comicsans',30,True)
        size+=2
        count_level+=1
        goblin.vel+=2
        goblin.health+=2
        new_goblin+=2
        pygame.display.update()
    clock.tick(27)#fps =frame rate per second
    if goblin.visible==True:
        if man.hitbox[1]<goblin.hitbox[1] +goblin.hitbox[3] and man.hitbox[3]+man.hitbox[1]>goblin.hitbox[1]:
            if man.hitbox[0]+man.hitbox[2] >goblin.hitbox[0] and man.hitbox[0]<goblin.hitbox[0]+goblin.hitbox[2]:
                #hitsound.play()   #hit sound
                if not man.isjump:  #for jumping BUG
                    man.hit()
                    score-=5
    keys=pygame.key.get_pressed()           #for user interative mode keys pressed
    if shootloop>0:
        shootloop+=1
    if shootloop>3:
        shootloop=0
    redrawGameWindow()
    clock.tick(speed)   #slow fps
    speed=man.vel+900000
    if keys[pygame.K_LEFT]:
        bgx+=1.4
        bgx2+=1.4
    elif keys[pygame.K_RIGHT]:
        bgx-=1.4
        bgx2-=1.4
    
    if bgx<bg.get_width()*-1:
        bgx=bg.get_width()
    if bgx2<bg.get_width()*-1:
        bgx2=bg.get_width()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
            pygame.quit()
            quit()
    for bullet in bullets:
        if bullet.y-bullet.radius<goblin.hitbox[1] +goblin.hitbox[3] and bullet.y+bullet.radius>goblin.hitbox[1]:
            if bullet.x+bullet.radius>goblin.hitbox[0] and bullet.x -bullet.radius<goblin.hitbox[0]+goblin.hitbox[2]:
                #hitsound.play()   #hit sound
                goblin.hit()
                if goblin.visible:
                    score+=1
                    bullets.pop(bullets.index(bullet))
        if bullet.x<800 and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    
    if keys[pygame.K_SPACE] and shootloop==0:
        bullet_sound=pygame.mixer.music.load('bullet.mp3')   #bullet sound
        pygame.mixer.music.play(0)
        #bulletsound.play()   #bullet sound
        if man.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),6,(0,0,0),facing))
        shootloop=1
    if keys[pygame.K_LEFT] and man.x +30>man.vel:
        man.x-=man.vel
        man.left=True
        man.right=False
        man.standng=False
    elif keys[pygame.K_RIGHT] and man.x <760-man.vel:
        man.x+=man.vel
        man.right=True
        man.left=False
        man.standing=False
    else:
        man.standing=True
        man.walkcount=0
    if not(man.isjump):
        if keys[pygame.K_UP]:
            man.isjump=True
            man.right=False
            man.left=False
            man.walkcount=0
    else:
        if man.jump_count>=-10:
            neg=1
            if man.jump_count<0:
                neg=-1
            man.y-=(man.jump_count**2)*0.5*neg
            man.jump_count-=1
        else:
            man.isjump=False
            man.jump_count=10
            
    
            

pygame.quit()
   
