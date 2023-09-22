"""Game Engine for Python. Requires Pygame."""
import pygame,json,os,sys,importlib
_mouseDown=False
buttons=[]
messages=[]
def animation(moveList:list,fps:int,frames:int,screen,x,y):
    """Pygame animation."""
    for i in range(frames):    
        if i>len(moveList):
            i=0
        clock=pygame.time.Clock()
        clock.tick(fps)
        currentSprite=moveList[i]
        screen.blit(currentSprite,(x,y))
        pygame.display.update()
def wasdInput(WFunction=None,AFunction=None,SFunction=None,DFunction=None):
    """Simple WASD/arrow keys input listener. Also supports arrow keys. Args are functions to run when respective key is pressed"""
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]or keys[pygame.K_a]and AFunction is not None:
        AFunction()
    if keys[pygame.K_RIGHT]or keys[pygame.K_d]and DFunction is not None:
        DFunction()
    if keys[pygame.K_DOWN]or keys[pygame.K_s]and SFunction is not None:
        SFunction()
    if keys[pygame.K_UP]or keys[pygame.K_w]and WFunction is not None:
        WFunction()
class Message:
    "Creates a message that can be sent and recieved"
    def __init__(self,name):
        self.name=name
        message={'name':self.name,'state':False}
        messages.append(message)
    def send(self):
        for message in messages:
            if message.get('name')==self.name:
                message.update(state=True)
    def unsend(self):
        for message in messages:
            if message.get('name')==self.name:
                message.update(state=False)
    def listen(self):
        for message in messages:
            if message.get('state'):
                return True
            else:
                return False
class GameButton:
    """Create a button that can trigger a function if clicked on or a message is recieved (if one is provided)"""
    def __init__(self,x:int=0,y:int=0,function=None,notHoverSprite:pygame.Surface='default',hover:bool=True,active:bool=True,hoverSprite:pygame.Surface='default',imageRes:int=64,image:str='Defaults\\DEFAULTBUTTON.png',imageResX:int=0,imageResY:int=0,message:Message=None):
        self.hovering=False
        #REQUIRED ARGS  
        self.x=x
        self.y=y    
        self.imageResX=imageResX
        self.imageResY=imageResY
        if imageResX !=0 or imageResY !=0:
            self.square=False
        else:
            self.square=True
        if image is not None:
            self.image=pygame.image.load(image).convert()
        self.imageRes=imageRes
        self.function=function
        self.hover=hover
        self.hoverSprite=hoverSprite
        self.notHoverSprite=notHoverSprite
        if hoverSprite=='default':
            self.hoverCursor=pygame.SYSTEM_CURSOR_HAND
        else:
            self.hoverCursor=pygame.cursors.Cursor((0,0),self.hoverSprite)
        if notHoverSprite=='default':
            self.notHoverCursor=pygame.SYSTEM_CURSOR_ARROW    
        else:
            self.notHoverCursor=pygame.cursors.Cursor((0,0),self.notHoverSprite) 
        self.active=active
        self.message=message
        buttons.append(self)    
    #Blits button to screen provided
    def show(self,**kwargs):
        'Blit button to screen. Screen to blit to required. Requires defined image'
        screen=kwargs.get('screen')
        screen.blit(self.image,(self.x,self.y))
    
    #Listens for mouse clicks: should be in a loop to work properly
    def listen(self):    
        "Listens for clicks on the button. Should be in a loop."
        global _mouseDown
        if self.active:
            left,middle,right=pygame.mouse.get_pressed()
            #Hover
            if self.hover:    
                if self.square:
                    mouseX,mouseY=pygame.mouse.get_pos()
                    if mouseX>self.x and mouseX<self.x+self.imageRes and mouseY>self.y and mouseY<self.y+self.imageRes:
                        pygame.mouse.set_cursor(self.hoverCursor)
                        self.hovering=True
                    elif self.hovering:
                        pygame.mouse.set_cursor(self.notHoverCursor)
                        self.hovering=False
                else:
                    mouseX,mouseY=pygame.mouse.get_pos()
                    if mouseX>self.x and mouseX<self.x+self.imageResX and mouseY>self.y and mouseY<self.y+self.imageResY:
                        pygame.mouse.set_cursor(self.hoverCursor)
                        self.hovering=True
                    elif self.hovering:
                        pygame.mouse.set_cursor(self.notHoverCursor)
                        self.hovering=False
            #CLick Event
            if left and self.function:
                if self.square:    
                    mouseX,mouseY=pygame.mouse.get_pos()
                    if mouseX>self.x and mouseX<self.x+self.imageRes and mouseY>self.y and mouseY<self.y+self.imageRes and _mouseDown==False:
                        self.function()
                        _mouseDown=True
                else:
                    mouseX,mouseY=pygame.mouse.get_pos()
                    if mouseX>self.x and mouseX<self.x+self.imageResX and mouseY>self.y and mouseY<self.y+self.imageResY and _mouseDown==False:
                        self.function()
                        _mouseDown=True
            else: _mouseDown=False
            if self.message and self.function:
                if self.message.listen():
                    self.function()
    def listenPulse(self):
        "Listens for hover once. Should NOT be used in a loop. Useful for controllers."
        if self.active and self.function:
            if self.square:    
                mouseX,mouseY=pygame.mouse.get_pos()
                if mouseX>self.x and mouseX<self.x+self.imageRes and mouseY>self.y and mouseY<self.y+self.imageRes:
                    self.function()
            else:
                mouseX,mouseY=pygame.mouse.get_pos()
                if mouseX>self.x and mouseX<self.x+self.imageResX and mouseY>self.y and mouseY<self.y+self.imageResY:
                    self.function()   
def listenAll():
    "Listen on all created buttons at once"
    global buttons
    for button in buttons:
        button.listen()
def listenPulseAll():
    "Listen pulse on all created buttons at once"
    global buttons
    for button in buttons:
        button.listenPulse()
class Vector2:
    def __init__(self,x:int|float,y:int|float):
        self.value=(x,y)
    def translate(self,x=0,y=0):
        self.x=self.value.__getitem__(0)
        self.y=self.value.__getitem__(1)
        self.x+=x
        self.y+=y
        self.value=(self.x,self.y)
class staticImage:
    "Static Graphic that doesn't move. Requires x,y and image"
    def __init__(self,x:int,y:int,image:str):
        self.x=x
        self.y=y     
        self.image=pygame.image.load(image).convert()
    def show(self,screen):
        screen.blit(self.image,(self.x,self.y))

#Save/Load system
def save(saveFile:str,save):
    "Save a dictionary of variables to a json file"
    _save=save
    with open(saveFile,'w') as f:
        json.dump(_save,f)
def load(saveFile:str)-> dict:
    "Load a dictionary of variables from a json file and return it"
    _save=json.load(open(saveFile))
    return _save
def checkHover(x1:int,x2:int,y1:int,y2:int,function):
    "Runs a function if mouse is in given area"
    mouseX,mouseY=pygame.mouse.get_pos()
    if mouseX>x1 and mouseX<x2 and mouseY>y1 and mouseY<y2:
        function()
def loadMods(modDir:str,loadingScreen:pygame.Surface=None,screen:pygame.Surface=None):
    "Load mods in given directory. Returns list of loaded mods as Module objects. The folder containing each mod's files must start with an uppercase letter and the .py file must be the same name but lowercase."
    loadedMods=[]
    logList=[]
    log={}
    class Mod:
        def __init__(self,name,title,description,version,id,author,modified,script,icon):
            self.name=name
            self.title=title
            self.description=description
            self.version=version
            self.id=id
            self.author=author
            self.modified=modified
            self.script=script
            self.icon=icon
        def loop(self):
            self.script.loop()
        def init(self):
            self.script.init()
        def config(self):
            self.script.config() 
    for root, dirs, files in os.walk(f'{modDir}'):
            for name in dirs:
                if name[0].isupper():
                    
                    print('________________________________________________________________________________________')
                    logList.append('________________________________________________________________________________________')
                    print(f'Mod named {name} found.')
                    logList.append(f'Mod named {name} found.')
                    sys.path.insert(1,f'{modDir}\\{name}')
                    print(f'Folder named {name} successfully added to sys.path.')
                    logList.append(f'Folder named {name} successfully added to sys.path.')
                    meta=load(f'{modDir}\\{name}\\meta.json')
                    print(f'meta data of {name} successfully loaded.')
                    logList.append(f'meta data of {name} successfully loaded.')
                    mod=Mod(name,meta.get('title'),meta.get('description'),meta.get('version'),meta.get('id'),meta.get('author'),meta.get('modified'),importlib.import_module(name.lower()),None)
                    print(f'Mod object successfully created using the meta data of {name}.')
                    logList.append(f'Mod object successfully created using the meta data of {name}.')
                    loadedMods.append(mod)
                    print(f'{name}\'s mod object succesfully added to list of mods.')
                    print(f'Mod named {name} successfully loaded.')
                    logList.append(f'{name}\'s mod object succesfully added to list of mods.')
                    logList.append(f'Mod named {name} successfully loaded.')
                    if not loadingScreen is None:
                        screen.blit(loadingScreen,(0,0))    
    log.update(log=logList)
    save('log.json',log)
    print('Log saved to log.json file.')
    return loadedMods
if __name__=='__main__':
    print('This script doesn\'t work on its own. Import it into a project to use the functions and classes defined here')
else:
    print('Using PyEngine v0.3 APLHA') 