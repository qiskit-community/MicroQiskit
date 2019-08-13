import pew
from aether import *
from random import random

sad = [[ (j in [i,7-i]) for j in range(8) ] for i in [0,1,2,3,3,2,1,0]]

clock = [
    [0,0,0,2,2,0,0,0],
    [0,1,2,3,0,2,1,0],
    [0,2,0,3,0,0,2,0],
    [2,0,0,3,0,0,0,2],
    [2,0,0,3,3,3,0,2],
    [0,2,0,0,0,0,2,0],
    [0,1,2,0,0,2,1,0],
    [0,0,0,2,2,0,0,0],
]

pew.init()
screen = pew.Pix()

screen.blit(pew.Pix.from_iter(clock))
pew.show(screen)

(x,y) = (0,0)
(X,Y) = (3,3)
pressing = False
qc = QuantumCircuit(1,1)
seed = [(2*(random()<0.5)-1)*(1+random())/2 for _ in range(4)]

def get_pixel(xx,yy):
    qc.data.clear()
    qc.rx((2*pi/360)*(seed[2]*(xx+yy)+seed[3]*(xx-yy))*45,0)
    qc.h(0)
    qc.rx((2*pi/360)*(seed[0]*xx+seed[1]*yy)*45,0)
    qc.measure(0,0)
    if execute(qc,shots=1000,get='counts')['1']>600:
        return 2
    else:
        return 0

def get_screen(x,y):
    scr = []
    for Y in range(8):
        scr.append([])
        for X in range(8):
            xx = x*8 + X
            yy = y*8 + Y
            scr[Y].append(get_pixel(xx,yy))

    return scr

scr = get_screen(x,y)
if scr[Y][X]!=0:
    for dX in [+1,0,-1]:
        for dY in [+1,0,-1]:
            scr[Y+dY][X+dX]=0
screen.pixel(X,Y,3)
screen.blit(pew.Pix.from_iter(scr))



pew.show(screen)

while True:

    screen.pixel(X,Y,3)

    (dX,dY) = (0,0)
    keys = pew.keys()
    if not pressing:
        if keys & pew.K_UP:
            dY = -1
        elif keys & pew.K_DOWN:
            dY = +1
        if keys & pew.K_LEFT:
            dX = -1
        elif keys & pew.K_RIGHT:
            dX = +1
        if keys & pew.K_O:
            pass
        if keys & pew.K_X:
            pass
        if keys:
            pressing = True
    else:
        if not keys:
            pressing = False

    if (X+dX in range(8)) and (Y+dY in range(8)):
        if (scr[Y+dY][X+dX]==0):
           screen.pixel(X,Y,0)
           X+=dX
           Y+=dY
           screen.pixel(X,Y,3)
    else:
        dx=((X+dX)==8)-((X+dX)==-1)
        dy=((Y+dY)==8)-((Y+dY)==-1)
        nX=(X+dX)%8
        nY=(Y+dY)%8
        if get_pixel( (x+dx)*8+nX,(y+dy)*8+nY )==0:
            (x,y) = (x+dx,y+dy)
            (X,Y) = (nX,nY)
            screen.blit(pew.Pix.from_iter(clock))
            pew.show(screen)
            scr = get_screen(x,y)
            screen.blit(pew.Pix.from_iter(scr))
            screen.pixel(X,Y,3)
        else:
            screen.blit(pew.Pix.from_iter(sad))
            pew.show(screen)
            pew.tick(1)
            screen.blit(pew.Pix.from_iter(scr))

    pew.show(screen)