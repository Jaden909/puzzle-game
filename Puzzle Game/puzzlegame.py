import pygame,PyEngine
screen=pygame.display.set_mode((512,512))
#level0=pygame.image.load('levelPlan.png')
#level1=pygame.image.load('levelPlan.png')
ground=pygame.image.load('ground.png')
playerImg=pygame.image.load('player.png')
enemy=pygame.image.load('enemy.png')
goal=pygame.image.load('cat.png')
air=pygame.image.load('air.png')
c0=pygame.image.load('cat\\cat0.png')
c1=pygame.image.load('cat\\cat1.png')
c2=pygame.image.load('cat\\cat2.png')
c3=pygame.image.load('cat\\cat3.png')
c4=pygame.image.load('cat\\cat4.png')
c5=pygame.image.load('cat\\cat5.png')
c6=pygame.image.load('cat\\cat6.png')
fade=pygame.image.load('fade.png').convert_alpha()
fade.set_alpha(0)
levels=[pygame.image.load('levelPlan.png'),pygame.image.load('level1.png')]
Rvalue=0
enemies=[]
tiles=[]
tileRects=[]
unfading=False
clock=pygame.time.Clock()
leaving=False
left=False
currentLevel=0
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.frames=50
        self.jumping=False
    def listenInputs(self):
            keys=pygame.key.get_pressed()
            #print('fhbvdgh')
            if keys[pygame.K_d]:
                self.x+=1
                screen.blit(playerImg,(self.x,self.y))
            if keys[pygame.K_a]:
                self.x-=1
                screen.blit(playerImg,(self.x,self.y))
            if keys[pygame.K_w]:
                self.jumping=True
            if self.jumping:
                if self.frames>0:
                    self.y-=2
                    self.frames-=1
                elif self.frames<0:
                    self.y+=1
                    self.frames-=1
                if self.frames==0:
                    self.frames=-2
                elif self.frames==-51:
                    self.frames=50
                    self.jumping=False
                screen.blit(playerImg,(self.x,self.y))
    def checkCollisions(self):
        #print(tileRects)
        global goalRect,leaving
        self.playerRect=pygame.Rect(self.x,self.y,32,32)
        #print(self.playerRect.collidelist(tileRects))
        #Check if player rect is lower to prevent tping up
        collision=self.playerRect.collidelist(tileRects)
        if collision!=-1 and self.playerRect.top<tileRects[collision].top:
            self.y-=2
        elif collision!=-1 and self.playerRect.top>tileRects[collision].top:
            self.y+=1
        if self.playerRect.colliderect(goalRect):
            #print('meow')
            leaving=True
            moveList=[c0,c0,c0,c0,c0,c0,c0,c0,c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c1,c1,c2,c2,c2,c2,c2,c2,c2,c2,c2,c2,c3,c3,c3,c3,c3,c3,c3,c3,c3,c3,c4,c4,c4,c4,c4,c4,c4,c4,c4,c4,c5,c5,c5,c5,c5,c5,c5,c5,c5,c5,c6,c6,c6,c6,c6,c6,c6,c6,c6,c6]
            #print(moveList)
            
            global Rvalue,curentSprite,clock
            #clock.tick(60)
            curentSprite=moveList[Rvalue]
            Rvalue+=1
            if Rvalue>=len(moveList):
                Rvalue=0
            screen.blit(curentSprite,goalRect)
    pygame.display.update()
class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.frames=50
        self.jumping=False
#class Goal:
#    def __init__(self,x,y):
#        self.x=x
#        self.y=y
class Tile:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tileRect=pygame.Rect(self.x,self.y,32,32)
        tileRects.append(self.tileRect)
    def collisionCheck(self):
        print(player.y)
        if player.x>self.x and player.x<self.x+32:
                if player.y>self.y and player.y<self.y+32:
                    player.y=self.y+1
def readLevel(level:pygame.Surface):
    global player,goalRect
    levelMap=[]
    j=pygame.PixelArray(level)
    x=0
    y=0
    screen.fill('white')
    for i in range(42069):
        #print(i)
        #print(x,y)
        #Scale each pixel up to 32x32
        #Store level in a list
        if j[x,y] == level.map_rgb(0,255,10):
            #print('green')
            levelMap.append('g')
            goalRect=pygame.Rect(x*32,y*32,32,32)
            #goalObj=Goal(x*32,x*32)
            screen.blit(goal,(x*32,y*32))
        if j[x,y] == level.map_rgb(255,0,0):
            #print('red')
            levelMap.append('r')
            enemies.append(Enemy(x*32,y*32))
            screen.blit(enemy,(x*32,y*32))
        if j[x,y] == level.map_rgb(0,107,255):
            #print('blue')
            player=Player(x*32,y*32)
            
            levelMap.append('b')
            screen.blit(playerImg,(x*32,y*32))
        if j[x,y] == level.map_rgb(0,0,0):
            #print('black')
            levelMap.append('bk')
            tiles.append(Tile(x*32,y*32))
            
            screen.blit(ground,(x*32,y*32))
        if j[x,y] == level.map_rgb(255,255,255):
            #print('white')
            levelMap.append('w')
        if x==15:
            y+=1
            x=0
            if y==16:
                break 
            continue
        x+=1
    return levelMap
def loadLevel(level):
    global player,leaving
    x=0
    y=0
    screen.fill('white')
    for i in level:
        if i=='g' and not leaving:
            screen.blit(goal,(x*32,y*32))
        
        if i=='r':
            screen.blit(enemy,(x*32,y*32))
        if i=='bk':
            screen.blit(ground,(x*32,y*32))
        if i=='b':
            screen.blit(playerImg,(player.x,player.y))    
        if i=='w':
            pass
        if x==15:
            y+=1
            x=0
            if y==16:
                break 
            continue
        x+=1
level=readLevel(levels[currentLevel])

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
    #print(level)
    loadLevel(level)
    player.listenInputs()
    player.checkCollisions()
    #for tile in tiles:
    #    tile.collisionCheck()
    if leaving:
        goalRect.left-=1
        screen.blit(curentSprite,goalRect)
        if goalRect.x<-32:
            left=True
    if left:
        if not unfading:
            fade.set_alpha(fade.get_alpha()+5)
        if fade.get_alpha()==255:
            unfading=True
            currentLevel+=1
            tileRects.clear()
            tiles.clear()
            level=readLevel(levels[currentLevel])
            leaving=False
        if unfading:
            fade.set_alpha(fade.get_alpha()-5)
        if fade.get_alpha()==0:
            unfading=False
            left=False
            #print(currentLevel)
            
    player.y+=1
    screen.blit(fade,(0,0))
    pygame.display.update()
    clock.tick(60)
