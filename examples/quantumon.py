import pew
import random
from aether import *

quantumon = [
    [
        [2,2,2,2,2,0,0,0],
        [2,0,0,3,0,0,0,3],
        [2,0,0,3,3,3,3,3],
        [2,0,0,3,1,1,1,3],
        [2,0,0,3,1,1,1,3],
        [2,0,0,3,1,3,1,3],
        [2,0,0,3,1,3,1,3],
        [2,2,3,3,1,3,1,3]
    ],
    [
        [2,0,0,0,0,3,0,0],
        [3,0,0,1,3,3,3,1],
        [2,0,0,3,1,3,1,3],
        [3,0,0,1,3,3,3,1],
        [2,2,2,3,1,1,1,3],
        [3,3,3,3,3,3,3,1],
        [3,1,1,3,3,1,3,3],
        [2,2,0,0,0,0,2,2]
    ],
    [
        [3,2,3,0,0,3,2,3],
        [2,1,3,1,1,3,1,2],
        [3,1,2,1,1,2,1,3],
        [0,3,0,0,0,0,3,0],
        [0,3,2,2,2,2,3,0],
        [3,3,1,2,2,1,3,3],
        [0,0,3,0,0,3,0,0],
        [0,3,3,0,0,3,3,0]
    ],
    [
        [0,0,0,0,0,0,0,0],
        [0,3,3,0,0,0,0,2],
        [3,0,0,3,0,0,2,0],
        [3,2,2,3,0,0,0,2],
        [0,3,3,0,0,0,2,0],
        [3,2,2,3,3,3,3,3],
        [3,1,3,1,3,1,1,3],
        [1,0,1,0,1,0,0,1]
    ],
    [
        [0,0,0,0,0,0,0,0],
        [0,2,2,2,0,0,0,0],
        [2,3,3,3,2,0,0,0],
        [2,1,3,1,3,2,0,1],
        [2,2,3,2,3,3,1,3],
        [2,3,3,3,3,2,0,1],
        [2,3,2,3,2,0,0,0],
        [0,2,2,2,0,0,0,0]
    ],
    [
        [0,3,3,2,2,2,3,3],
        [0,3,0,1,0,1,0,3],
        [0,0,3,0,2,0,3,0],
        [0,0,0,3,0,3,0,0],
        [0,0,0,1,1,1,0,0],
        [0,0,0,1,3,1,0,0],
        [0,0,1,3,3,3,1,0],
        [0,0,2,2,2,2,2,0]
    ],
    [
        [0,0,1,3,3,3,2,0],
        [0,1,0,1,3,1,2,2],
        [0,1,1,3,3,3,2,2],
        [0,1,1,3,1,3,2,2],
        [0,1,1,3,3,3,2,2],
        [0,1,1,3,3,3,0,2],
        [0,0,1,3,3,3,2,0],
        [0,0,0,0,0,0,0,0]
    ],
]

sad = [
    [0,0,3,3,3,3,0,0],
    [0,3,3,3,3,3,3,0],
    [3,3,1,3,3,1,3,3],
    [3,3,1,3,3,1,3,3],
    [3,3,3,3,3,3,3,3],
    [3,3,2,2,2,2,3,3],
    [0,2,3,3,3,3,2,0],
    [0,0,3,3,3,3,0,0],
]

happy = [
    [0,0,3,3,3,3,0,0],
    [0,3,3,3,3,3,3,0],
    [3,3,1,3,3,1,3,3],
    [3,3,1,3,3,1,3,3],
    [3,3,3,3,3,3,3,3],
    [3,2,3,3,3,3,2,3],
    [0,3,2,2,2,2,3,0],
    [0,0,3,3,3,3,0,0],
]

def get_prob(x,y,X,Y,seed):
    qc.data.clear()
    xx = (x+X) % period
    yy = (y+Y) % period
    hash  = [False]*(period-xx)+[True]*xx + [False]*(period-yy)+[True]*yy
    for j in range(2*period):
        if hash[j] ^ seed[j]:
            qc.rx(pi/4,0)
        else:
            qc.h(0)
            qc.rx(pi/4,0)
            qc.h(0)
    return (1 + execute(qc,get='E')['Z'])/2

def get_colour(x,y,X,Y,seed):
    p = get_prob(x,y,X,Y,seed)
    if p>0.75:
        return rock
    elif p<0.01:
        return animal        
    return 0
  
def teleport(x,y):
    x += random.randint(-3,3)
    y += random.randint(-3,3)
    while get_colour(x,y,0,0,seed)!=0:
        x += random.randint(-3,3)
        y += random.randint(-3,3)
    return x,y

pew.init()
screen = pew.Pix()

rock = 3
player = 2
animal = 1

period = 50
seed = [ (random.random()<0.5) for _ in range(2*period)]

qc = QuantumCircuit(1)
(x,y) = teleport(0,0)
pressing = False
caught = []
escaped = []
dex = [False]*len(quantumon)
while False in dex:
    for X in range(-3,5):
        for Y in range(-3,5):
            if (x+X,y+Y) in caught+escaped:
                screen.pixel(X+3,Y+3,0)
            else:
                screen.pixel(X+3,Y+3,get_colour(x,y,X,Y,seed))
    screen.pixel(3,3,player)
    
    (dx,dy) = (0,0)
    collect = False
    jump = False
    keys = pew.keys()
    if not pressing:
        if keys & pew.K_UP:
            dy = -1
        elif keys & pew.K_DOWN:
            dy = +1
        if keys & pew.K_LEFT:
            dx = -1
        elif keys & pew.K_RIGHT:
            dx = +1
        if keys & pew.K_O:
            jump = True
        if keys & pew.K_X:
            collect = True
        if keys:
            pressing = True
    else:
        if not keys:
            pressing = False

    if get_colour(x+dx,y+dy,0,0,seed)!=rock:
        x += dx
        y += dy
    if jump:
        x,y = teleport(x,y)

    if collect:
        for (X,Y) in [(0,1),(0,-1),(1,0),(-1,0)]:
            if get_colour(x,y,X,Y,seed)==animal:
                if (x+X,y+Y) not in caught+escaped:
                    caught.append( (x+X,y+Y) )
                    type = random.randint(0,len(quantumon)-1)
                    dex[type] = True
                    screen.blit(pew.Pix.from_iter(quantumon[type]))
                    pew.show(screen)
                    pew.tick(1)

    if get_colour(x,y,0,0,seed)==animal:
        if (x,y) not in caught+escaped:
            escaped.append( (x,y) )
            screen.blit(pew.Pix.from_iter(sad))
            pew.show(screen)
            pew.tick(1)

    pew.show(screen)
    pew.tick(1/12)

    if False not in dex:
        screen.blit(pew.Pix.from_iter(happy))
        pew.show(screen)
        pew.tick(5)
