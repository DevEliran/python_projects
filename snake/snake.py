import math
import pygame
import tkinter as tk
import random
from tkinter import messagebox
import os
import imghdr
import cv2
from pygame.mixer import Sound
import datetime
from dateutil.parser import parse


class stats():
    def __init__(self):
        with open("high_score.txt",'r') as file:
            self.high_score=int(file.read())

        self.max_time_played=0

class cube(object):
    rows=20
    w=500
    def __init__(self,start,dirnx=1,dirny=0,color=(37,210,229)):
        self.pos=start
        self.dirnx=1
        self.dirny=0
        self.color=color

    def move(self,dirnx,dirny):
        self.dirnx=dirnx
        self.dirny=dirny
        self.pos=(self.pos[0]+self.dirnx,self.pos[1]+self.dirny)

    def draw(self,surface,eyes=False):
        dis=self.w//self.rows
        i=self.pos[0]
        j=self.pos[1]

        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))

        if eyes:
            center=dis//2
            raduis=3
            circleMiddle=(i*dis+center-raduis,j*dis+8)
            circleMiddle2=(i*dis+dis-raduis*2,j*dis+8)
            pygame.draw.circle(surface,(0,0,0),circleMiddle,raduis)
            pygame.draw.circle(surface,(0,0,0),circleMiddle2,raduis)

class snake(object):
    body=[]
    turns={}
    def __init__(self,color,pos):
        self.color=color
        self.head=cube(pos)
        self.body.append(self.head)
        self.dirnx=0
        self.dirny=0

    def move(self):
        global start_stamp , time_played
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            keys=pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx=-1
                    self.dirny=0
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx=1
                    self.dirny=0
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx=0
                    self.dirny=-1
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx=0
                    self.dirny=1
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]

        for i , c in enumerate(self.body):
            p=c.pos[:]
            if p in self.turns:
                turn=self.turns[p]
                c.move(turn[0],turn[1])
                if i==len(self.body)-1:
                    self.turns.pop(p)
            else: # checking if the snake is about to hit the walls
                if c.dirnx==-1 and c.pos[0]<=0:
                    c.pos=(c.rows-1,c.pos[1])
                elif c.dirnx==1 and c.pos[0]>=c.rows-1:
                    c.pos=(0,c.pos[1])
                elif c.dirny==1 and c.pos[1]>=c.rows-1:
                    c.pos=(c.pos[0],0)
                elif c.dirny==-1 and c.pos[1]<=0:
                    c.pos=(c.pos[0],c.rows-1)
                else:
                    c.move(c.dirnx,c.dirny)    # keep moving in the same direction


    def reset(self,pos):
        self.head=cube(pos)
        self.body=[]
        self.body.append(self.head)
        self.turns={}
        self.dirnx=0
        self.dirny=1

    def addCube(self):
        tail=self.body[-1]
        dx,dy=tail.dirnx,tail.dirny

        if dx==1 and dy==0:#moving right
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))#adding cube left
        elif dx==-1 and dy==0:#moving left
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))#adding cube right
        elif dx==0 and dy==1:#moving down
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))#adding cube up
        elif dx==0 and dy==-1:#moving up
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))#adding cube down

        self.body[-1].dirnx=dx
        self.body[-1].dirny=dy

    def draw(self,surface):
        for i ,c in enumerate(self.body):
            if i==0:
                c.draw(surface,True)
            else:
                c.draw(surface)

def drawGrid(w,rows,surface):
    size=w//rows
    x=0
    y=0
    for l in range(rows):
        x=x+size
        y=y+size
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y))

def redrawWindow(surface):
    global rows , width,snake,snack
    surface.fill((100,100,100))
    snake.draw(surface)
    snack.draw(surface)
    #drawGrid(width,rows,surface)
    pygame.display.update()

def randomSnack(rows,item):
    positions=item.body

    while True:
        x=random.randrange(rows)
        y=random.randrange(rows)

        if len(list(filter(lambda z:z.pos==(x,y),positions)))>0:
            continue
        else:
            break
    return (x,y)

def message_box(subject,content):
    root=tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def update_highscore():
    pygame.display.set_caption("Snake | Highest Score : "+str(st.high_score)+" | Current Score :"+ str(len(snake.body)))

def open_meme(n):
    n=random.randint(1,8)
    s="secret//"+str(n)+".jpg"
    img=cv2.imread(s,cv2.IMREAD_COLOR)
    cv2.imshow('MEME FOR YOU',img)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

def total_time_played():
    global time_played
    with open ('time.txt','r') as f :
        content=f.readlines()
def avg_score():
    avg,count=0,0
    with open('scores.txt','r') as f:
        content=f.readlines()
        print(content)
    for i in content:
        count+=1
        avg+=int(i)
    print(avg/count)
    return avg/count

def main():
    global width , rows,snake,snack,st,active,start_stamp,time_played
    width=500
    rows=20
    random_insults=["Can you breath by yourself ? ", "Guess monkeys didn't evovle that much ! ", "NOOB","I wasn't expecting that low score !","Are you already ashamed ? ","Douchebaggette "]
    k=random.randint(1,2)
    n=random.randint(1,8)
    path="secret//"+str(k)+".mp3"
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.20)
    pygame.mixer.music.play(-1)

    window=pygame.display.set_mode((width,width))


    snake=snake((37,210,229),(10,10))
    st=stats()
    snack=cube(randomSnack(rows,snake),color=(233,53,17))
    clock=pygame.time.Clock()
    start_stamp=datetime.datetime.now()

    while True:
        pygame.mouse.set_visible(False)
        clock.tick(20)
        snake.move()
        update_highscore()
        if snake.body[0].pos==snack.pos:
            snake.addCube()
            snack=cube(randomSnack(rows,snake),color=(233,53,17))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos,snake.body[x+1:])) :
                end_stamp=datetime.datetime.now()
                time_played=end_stamp-start_stamp
                print(time_played)

                with open ('time.txt','a+') as f:
                    f.write(str(time_played)+'\n')
                print('score',len(snake.body))
                with open ('scores.txt','a+') as f:
                    f.write(str(len(snake.body))+'\n')
                message_box('GAME OVER',random.choice(random_insults) +' \nYOU GOT ONLY '+str(len(snake.body))+' POINTS' + '\nYOUR LOUSY AVERAGE SCORE IS :'+str(avg_score())+'\nIT TOOK YOU :'+str(time_played))
                print(avg_score())
                if st.high_score < int(len(snake.body)):
                    st.high_score=len(snake.body)
                    with open ("high_score.txt",'w+') as file:
                        file.seek(0)
                        file.write(str(len(snake.body)))

                    message_box('NAICU ','YOU GOT YOURSELF A TREAT BOI')
                    #mail()
                    open_meme(n)

                snake.reset((10,10))
                start_stamp=datetime.datetime.now()
                n=random.randint(1,8)
                break

        redrawWindow(window)
        update_highscore()


main()
