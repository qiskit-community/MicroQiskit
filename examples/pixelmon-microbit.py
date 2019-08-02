from microbit import *
import random
pi=3.14159265359
def cos(t):
  t=t%(2*pi)
  c=1
  tm=1
  for j in range(1,16):
    tm=-tm*t**2/(2*j*(2*j-1))
    c+=tm
  return c
def sin(t):
  return cos(t-pi/2)
class QuantumCircuit:
  def __init__(qc,nq):
    qc._nq=nq
    qc.p2s=['I','X','Y','Z']*(qc._nq==2)+['']*(qc._nq==1)
    qc.exp={}
    qc.reset()
  def _pl(qc,p1,p2,q):
    return (p1+p2)*(q==1) + (p2+p1)*(q==0)
  def reset (qc):
    for p1 in ['I','X','Y','Z']:
      for p2 in qc.p2s:
        qc.exp[p1+p2]=(('X' not in (p1+p2))and('Y' not in (p1+p2) ))
  def x(qc,q):
    for p2 in qc.p2s:
      for p1 in ['Y','Z']:
        qc.exp[qc._pl(p1,p2,q)]=-qc.exp[qc._pl(p1,p2,q)]   
  def h(qc,q):
    for p2 in qc.p2s:
      temp=qc.exp[qc._pl('X',p2,q)]
      qc.exp[qc._pl('X',p2,q)]=qc.exp[qc._pl('Z',p2,q)]
      qc.exp[qc._pl('Z',p2,q)]=temp
      qc.exp[qc._pl('Y',p2,q)]=-qc.exp[qc._pl('Y',p2,q)]
  def rx(qc,theta,q):
    c=cos(theta)
    s=sin(theta)
    for p2 in qc.p2s:
      old_z=qc.exp[qc._pl('Z',p2,q)]
      old_y=qc.exp[qc._pl('Y',p2,q)]
      qc.exp[qc._pl('Z',p2,q)]=c*old_z-s*old_y
      qc.exp[qc._pl('Y',p2,q)]=c*old_y+s*old_z
  def cx(qc,c=0,t=0):
    if qc._nq==2:
      qc.h(t)
      for pair in [('XI','XZ'),('IX','ZX'),('YI','YZ'),('IY','ZY'),('XX','YY')]:
        temp=qc.exp[pair[0]]
        qc.exp[pair[0]]=qc.exp[pair[1]]
        qc.exp[pair[1]]=temp
      qc.h(t)
def execute(qc,shots=1024):
  ps={}
  def s(out):
    return (1-2*(out=='1'))
  if qc._nq==2:
    for out in ['00','01','10','11']:
      ps[out]=(1+s(out[1])*qc.exp['IZ']+s(out[0])*qc.exp['ZI']+s(out[0])*s(out[1])*qc.exp['ZZ'])/4
  elif qc._nq==1:
    for out in ['0','1']:
      ps[out]=(1+s(out)*qc.exp['Z'])/2
  c={}
  if shots==0:
    for out in ps:
      c[out]=ps[out]
  else:
    for out in ps:
      c[out]=0
    for _ in range(shots):
      cumu=0
      un=True
      r=random.random()
      for out in c:
        cumu += ps[out]
        if r<cumu and un:
          c[out] += 1
          un=False
  return c

rock=5
player=9
animal=9

seed=[random.randint(1,7) for _ in range(4)]
qc=QuantumCircuit(1)

def get_brightness(x,y,X,Y):
  qc.reset()
  qc.rx(pi**2*seed[0]*(x+X),0)
  qc.h(0)
  qc.rx(pi/2,0)
  qc.h(0)
  qc.rx(pi**2*seed[1]*(y+Y),0)
  qc.h(0)
  qc.rx(-pi/2,0)
  qc.h(0)
  colour =rock*(qc.exp['Z']>=0.5)+animal*(qc.exp['Z']<-0.95)
  return colour
  
def teleport(x,y):
  x+= random.randint(-2,2)
  y+= random.randint(-2,2)
  while get_brightness(x,y,2,2)!=0:
    x+= random.randint(-2,2)
    y+= random.randint(-2,2)
  return x,y

(x,y)=teleport(0,0)
  
caught=[]
escaped=[]
while True:
  for X in range(5):
    for Y in range(5):
      if (x+X-2,y+Y-2) in caught+escaped:
        display.set_pixel(X, Y, 0)
      else:
        display.set_pixel(X, Y, get_brightness(x,y,X,Y))
  display.set_pixel(2, 2, player)
  (dx,dy)=(0,0)
  if accelerometer.get_x()>100:
    dx+= 1
  elif accelerometer.get_x()<-100:
    dx -= 1
  elif accelerometer.get_y()>100:
    dy+= 1
  elif accelerometer.get_y()<-100:
    dy -= 1
  if get_brightness(x+dx,y+dy,2,2)!=rock:
    x+= dx
    y+= dy
  if button_a.is_pressed():
    x,y=teleport(x,y)
  if button_b.is_pressed():
    for (dx,dy) in [(0,1),(0,-1),(1,0),(-1,0)]:
      if get_brightness(x,y,2+dx,2+dy)==animal:
        caught.append( (x+dx,y+dy) )
        display.show(random.choice([Image.DUCK,Image.SNAKE]))
        sleep(500)
  if get_brightness(x,y,2,2)==animal:
    if (x,y) not in caught+escaped:
      escaped.append( (x,y) )
      display.show(Image.SAD)
    sleep(500)
  sleep(200)