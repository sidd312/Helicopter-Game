from Tkinter import *
import random
import time

def keyPressed(canvas,event):
    if(event.keysym=="r"):
        init(canvas)
    redrawAll(canvas)

def mousePressed(canvas, event): 
    canvas.data.alist.append(1)
    redrawAll(canvas)

def leftMouseReleased(canvas,event):
    if(len(canvas.data.alist)>0):
        canvas.data.alist.pop()
    redrawAll(canvas)

def leftMouseMoved(canvas,event):
    if(canvas.data.gameOver==False):
        canvas.data.cy-=canvas.data.speed+5
    redrawAll(canvas)

def movecloud(canvas):
    if(canvas.data.cloudx>0):
        canvas.data.cloudx-=canvas.data.speed
    else:
        canvas.data.cloudx=canvas.data.width\
        *random.randint(2,6)
        canvas.data.cloudy=random.randint(canvas.data.height/6,canvas.data.height*0.6)

def timerFired(canvas):
    #here you determine which level you are and canvas.data.increase would be determined by that
    if(canvas.data.buttonPressed==True):
        helicoptercollision(canvas)
        if(canvas.data.help==False):
            if(canvas.data.showscore==False):
                if(canvas.data.gameOver==True):
                    cx = canvas.data.width/2
                    cy = canvas.data.height/2
                    canvas.create_text(cx, cy, text="Game Over!", \
                        font=("Helvetica", 32, "bold"),fill="red")
                else:
                    """
                    if((int(round(time.time()-canvas.data.starttime)))%abs(canvas.data.timeinterval)==0):
                        canvas.data.levelincrease=True
                    """
                    canvas.data.timercounter+=1
                    if(canvas.data.timercounter>400):
                        canvas.data.levelincrease=True
                    if(canvas.data.timercounter%400==0):
                        canvas.data.increase+=25
                        canvas.data.level+=1
                        canvas.data.obstacleincrease+=5
                    #print "level increase",canvas.data.increase
                    #print canvas.data.level
                    canvas.data.index+=1
                    canvas.data.index%=len(canvas.data.imagelist)
                    canvas.data.cy+=10
                    canvas.data.distance+=1     
                    #if((int(round(time.time()-canvas.data.starttime)))%4==0):
                    canvas.data.a.moveFirstObstacle(canvas)
                    if(canvas.data.levelincrease):
                        canvas.data.a.moveSecondObstacle(canvas)
                    moveUpBlocks(canvas)
                    moveDownBlocks(canvas)
                    movecloud(canvas)
                    if(time.time()-canvas.data.collisiontime)>2.5:  
                        canvas.data.helicoptervisible=True
                    if(len(canvas.data.alist)>0):
                        canvas.data.cy-=20
                    if(canvas.data.gameOver==False):
                        redrawAll(canvas)
    
    delay =40 # milliseconds
    def f():
        timerFired(canvas)
    canvas.after(delay, f)

def moveUpBlocks(canvas):
    blockwidth=canvas.data.width/4
    for ublock in canvas.data.UpblockList:
        ublock.x0-=canvas.data.speed
        ublock.x1-=canvas.data.speed
    #just checking bounds for the first block 
    if(canvas.data.UpblockList[0].x1<0):
        exitUBlock=canvas.data.UpblockList.pop(0)
        exitUBlock.x0=canvas.data.\
        UpblockList[len(canvas.data.UpblockList)-1].x1
        exitUBlock.x1=exitUBlock.x0+blockwidth
        exitUBlock.y0=0
        exitUBlock.y1=random.randrange(20,\
            canvas.data.height/6, 1)
        canvas.data.UpblockList.append(exitUBlock)

def moveDownBlocks(canvas):
    blockwidth=canvas.data.width/4
    for dblock in canvas.data.DownblockList:
        dblock.x0-=canvas.data.speed
        dblock.x1-=canvas.data.speed
    #just checking bounds for the first block 
    if(canvas.data.DownblockList[0].x1<0):
        exitDBlock=canvas.data.DownblockList.pop(0)
        exitDBlock.x0=canvas.data.\
        DownblockList[len(canvas.data.DownblockList)-1].x1
        exitDBlock.x1=exitDBlock.x0+blockwidth
        exitDBlock.y0=random.randrange\
        (canvas.data.height*0.7,canvas.data.height-20,1)
        exitDBlock.y1=canvas.data.height
        canvas.data.DownblockList.append(exitDBlock)
    

def helicoptercollision(canvas):
    #all sides of the helicopter
    if(canvas.data.gameOver==False):
        x0=canvas.data.cx
        y0=canvas.data.cy   
        x1=canvas.data.cx+canvas.data.image.width()
        y1=canvas.data.cy+canvas.data.image.height() 
        ids = canvas.find_overlapping(x0,y0,x1,y1)
        if(canvas.data.helicoptervisible==True):
            if(len(ids)>1):
                for i in xrange(len(ids)):
                    if(canvas.type(ids[i])!='image'):
                        fill=canvas.itemcget(ids[i],"fill")
                        if(fill=="green" or fill=="cyan" or fill=="orange"):
                            saveScore((str(canvas.data.distance)+"\n")\
                                ,"Helicopter Game Scores.txt")
                            canvas.data.gameOver=True
                    else:
                        try:
                            if(canvas.type(ids[i+1])=='image'):
                                canvas.data.helicoptervisible=False
                                canvas.data.collisiontime=\
                                time.time()
                        except:
                            pass
                                    

def redrawAll(canvas):
    canvas.delete(ALL)
    offset=60
    buttonoffset=80
    if(canvas.data.buttonPressed==False):
        canvas.create_image(0,0,anchor=NW,image=canvas.data.back)
        cx = canvas.data.width/2
        cy = canvas.data.height/2
        canvas.create_text(cx, cy, text="Helicopter Game!", \
                font=("Helvetica", 40, "bold"),fill="red")
        canvas.create_window(canvas.data.width/2,\
            canvas.data.height*2/3,window=canvas.data.b1)
        canvas.create_window(canvas.data.width/2,\
            (canvas.data.height*2/3)+buttonoffset,window=canvas.data.b2)
        canvas.create_window(canvas.data.width/2,\
            (canvas.data.height*2/3)+buttonoffset+buttonoffset,window=canvas.data.b3)

    else: 
        if(canvas.data.help==False):
            if(canvas.data.showscore==False):
                width=canvas.data.width
                height=canvas.data.height
                canvas.create_rectangle(0,0,width,\
                height,width=5,fill="black")#initial background
                # Draw the original size image on the left
                image = canvas.data.image
                offset=60
                cx=canvas.data.cx
                cy=canvas.data.cy   
                font = ("Arial", 16, "bold")
                canvas.data.a.drawFirstObstacle(canvas)
                if(canvas.data.levelincrease==True):
                    canvas.data.a.drawSecondObstacle(canvas)
                for ublock in canvas.data.UpblockList:
                    canvas.create_rectangle(ublock.x0,ublock.y0,\
                        ublock.x1,ublock.y1,fill="cyan",width=0)
                for dblock in canvas.data.DownblockList:
                    canvas.create_rectangle(dblock.x0,dblock.y0,\
                        dblock.x1,dblock.y1,fill="orange",width=0)
                canvas.create_image(canvas.data.cloudx,canvas.data.cloudy,\
                    image=canvas.data.cloud)
                for imagefile in canvas.data.imagelist:
                    photo = PhotoImage(file=imagefile)
                    canvas.data.giflist.append(photo)
                if(canvas.data.helicoptervisible==True):        
                    canvas.create_image(cx, cy, anchor=NW, \
                        image=canvas.data.giflist[canvas.data.index])        
                msg = "Helicoptor Game" 
                canvas.create_text(width/2, 25, text=msg, font=font,fill="white")
                msg1="Score:",canvas.data.distance
                canvas.create_text(width*3.5/5,25,text=msg1,\
                    font=font,fill="magenta")
                loadscore("Helicopter Game Scores.txt")
                msg2="Best:"+loadscore("Helicopter Game Scores.txt")#should return string
                canvas.create_text(width*4/5+offset,25,text=msg2,\
                    font=font,fill="yellow")
                msg3="Level:",canvas.data.level
                canvas.create_text(width/5+offset,25,text=msg3,\
                    font=font,fill="black")
            else:
                msg4=loadTextString("Helicopter Game Scores.txt")
                canvas.create_text(offset,0,text=msg4,fill="black")

        else:
            cx = canvas.data.width/2
            cy = canvas.data.height/4
            offsetx=canvas.data.height*0.44
            offsety=canvas.data.height/10
            textspace=100
            font=("Helvetica", 24, "bold")
            canvas.create_text(cx, cy, text="Instructions", \
                font=("Helvetica", 46, "bold"),fill="red")
            canvas.create_text(cx-offsetx,cy+offsety,\
                text="1. Press r to restart and also to go back",\
                font=font,anchor=NW,fill="blue")
            canvas.create_text(cx-offsetx,cy+offsety+textspace,\
                text="2. The helicopter is controlled by pressing the mouse",\
                font=font,anchor=NW,fill="blue")
            canvas.create_text(cx-offsetx,cy+offsety+textspace*2,\
                text="3. Clouds makes you invisible!!But you can't get rid of gravity!!!",font=font,anchor=NW,fill="blue")
            canvas.create_text(cx-offsetx,cy+offsety+textspace*3,\
                text="4. One way to escape immediate collision is to drag the mouse!!",font=font,anchor=NW,fill="blue")


def saveScore(text,filename):
    fin=open(filename,"a")
    fin.write(text)
    fin.close()

def loadscore(filename):#stack overflow
    lines=[line.strip() for line in open(filename)]
    scores=[]
    for line in lines:
        scores.append(int(line))
    return str(max(scores))


class Obstacle(object):
    def __init__(self,canvas):
        self.wallx=canvas.data.width
        self.wally=random.randint(134,canvas.data.height*0.21)
        self.wallwidth=canvas.data.width/14
        self.wallheight=canvas.data.height/6+\
        canvas.data.obstacleincrease
        self.wallx1=canvas.data.width*random.uniform(1,4)
        self.wally1=random.randint(canvas.data.height*0.325,\
            canvas.data.height*0.625)

    
    def drawFirstObstacle(self,canvas):
        canvas.create_rectangle(self.wallx,self.wally,\
            self.wallx+self.wallwidth,\
            self.wally+self.wallheight,fill="green")
    
    def drawSecondObstacle(self,canvas):
        canvas.create_rectangle(self.wallx1,self.wally1,\
            self.wallx1+self.wallwidth,\
            self.wally1+self.wallheight,fill="green")
        
    def moveFirstObstacle(self,canvas):
        if(self.wallx>0):
            self.wallx-=canvas.data.speed
        else:
            self.wallx=canvas.data.width
            self.wally=random.randint(134,canvas.data.height*0.21)

    def moveSecondObstacle(self,canvas):
        if(self.wallx1>0):
            self.wallx1-=canvas.data.speed
        else:
            self.wallx1=canvas.data.width*random.uniform(1,4)
            self.wally1=random.randint(canvas.data.height*0.325,\
                canvas.data.height*0.625)
        

class Wall(object):
    def __init__(self,x0,y0,x1,y1):
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1

def button1Pressed(canvas):
    canvas.data.buttonPressed=True
    redrawAll(canvas)

def button2Pressed(canvas):
    canvas.data.help=True
    canvas.data.buttonPressed=True
    redrawAll(canvas)

def loadTextString(fileName):#course website
    fileHandler = open(fileName, "rt") # rt stands for read text
    text = fileHandler.read() # read the entire file into a single string
    fileHandler.close() # close the file
    return text

def button3Pressed(canvas):
    canvas.data.buttonPressed=True
    canvas.data.showscore=True
    redrawAll(canvas)

def init(canvas):
    canvas.data.speed=10
    canvas.data.showscore=False
    canvas.data.obstacleincrease=0
    image = PhotoImage(file="frame_00.gif")
    imagelist=["frame_00.gif",\
    "frame_01.gif","frame_02.gif","frame_03.gif"]
    imagecloud=PhotoImage(file="cloud.gif")
    backimage=PhotoImage(file="back.gif")
    canvas.data.back=backimage
    canvas.data.imagelist=imagelist
    canvas.data.giflist=[]
    canvas.data.cloud=imagecloud
    canvas.data.image = image
    canvas.data.cx=canvas.data.width/3
    canvas.data.cy=canvas.data.height/3
    canvas.data.gameOver=False
    canvas.data.distance=0
    canvas.data.alist=[]
    canvas.data.a=Obstacle(canvas)
    canvas.data.gameOver=False
    canvas.data.increase=0
    makeUpwallList(canvas)
    makeDownwallList(canvas)
    canvas.data.highScore=[]
    canvas.data.cloudy=random.randint(\
        canvas.data.height/6,canvas.data.height*0.6)
    canvas.data.cloudx=canvas.data.width*\
    random.uniform(2,6)
    canvas.data.helicoptervisible=True
    canvas.data.collisiontime=0
    canvas.data.help=False
    canvas.data.index=1
    canvas.data.giflist=[]
    canvas.data.level=0
    canvas.data.timercounter=0
    canvas.data.buttonPressed=False
    def b1Pressed(): button1Pressed(canvas)
    b1 = Button(canvas, text="Play", command=b1Pressed)
    canvas.data.b1=b1
    def b2Pressed(): button2Pressed(canvas)
    b2=Button(canvas, text="Instructions", command=b2Pressed)
    canvas.data.b2=b2
    def b3Pressed(): button3Pressed(canvas)
    b3=Button(canvas, text="See All scores",command=b3Pressed)
    canvas.data.b3=b3
    canvas.data.levelincrease=False
    

def makeUpwallList(canvas):#helper function to make walls
    blockwidth=canvas.data.width/4
    maxUBlockHeight=canvas.data.height/6
    ux0=0
    uy0=0
    ux1=blockwidth
    uy1=(random.randrange(20,maxUBlockHeight, 1)+canvas.data.increase)
    canvas.data.UpblockList=[]
    for i in xrange(10):
        ublock=Wall(ux0,uy0,ux1,uy1)
        canvas.data.UpblockList.append(ublock)
        ux0=ux0+blockwidth
        uy0=0
        ux1=ux1+blockwidth
        uy1=(random.randrange(20, maxUBlockHeight, 1)\
            +canvas.data.increase)
    
def makeDownwallList(canvas):
    blockwidth=canvas.data.width/4
    offset=30
    dx0=0
    dx1=blockwidth
    dy0=(random.randrange(canvas.data.height*0.7,\
        canvas.data.height-offset,1)-canvas.data.increase)
    dy1=canvas.data.height
    canvas.data.DownblockList=[]
    for i in xrange(10):
        dblock=Wall(dx0,dy0,dx1,dy1)
        canvas.data.DownblockList.append(dblock)
        dx0=dx0+blockwidth
        dy0=(random.randrange(canvas.data.height*0.7,\
            canvas.data.height-offset,1)-canvas.data.increase)
        dx1=dx1+blockwidth
        dy1=canvas.data.height
        
def run():
    # create the root and the canvas
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.title("Helicopter Game")
    canvasWidth=800
    canvasHeight=800
    canvas = Canvas(root, width=canvasWidth, \
        height=canvasHeight)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    init(canvas) # DK: init() --> init(canvas)
    def f(event): mousePressed(canvas, event)    
    root.bind("<Key>",\
        lambda event: keyPressed(canvas,event))
    root.bind("<Button-1>", f)
    root.bind("<B1-Motion>", \
        lambda event :leftMouseMoved(canvas,event))
    root.bind("<B1-ButtonRelease>", \
    lambda event:leftMouseReleased(canvas,event))#class website
    # DK: Or you can just use an anonymous lamdba function,
    # like this:
    timerFired(canvas) # DK: timerFired() --> timerFired(canvas)
    root.mainloop()

run()






