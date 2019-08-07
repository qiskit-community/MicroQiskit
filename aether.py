import random
pi=3.14159265359
def cos(T):
  T=T%(2*pi)
  c=1
  t=1
  for j in range(1,16):
    t=-t*T**2/(2*j*(2*j-1))
    c+=t
  return c
def sin(T):
  return cos(T-pi/2)
class QuantumCircuit:
  def __init__(c,n):
    c.n=n
    c.data=[]
  def x(c,q):
    c.data.append(('r',pi,q))
  def rx(c,T,q):
    c.data.append(('r',T,q))
  def h(c,q):
    c.data.append(('h',q))
  def cx(c,s,t):
    c.data.append(('cx',t))
def execute(c,shots=1024,get='counts'):
  g=0*(get=='counts')+1*(get=='memory')+2*(get=='E')
  p2s=['I','X','Y','Z']*(c.n==2)+['']*(c.n==1)
  def j(p1,p2,q):
    return (p1+p2)*(q==1)+(p2+p1)*(q==0)
  def h(q):
    for p2 in p2s:
      t=E[j('X',p2,q)]
      E[j('X',p2,q)]=E[j('Z',p2,q)]
      E[j('Z',p2,q)]=t
      E[j('Y',p2,q)]=-E[j('Y',p2,q)]
  E={}
  for p1 in['I','X','Y','Z']:
    for p2 in p2s:
      E[p1+p2]=int(('X' not in (p1+p2))and('Y' not in (p1+p2) ))
  for gate in c.data:
    if gate[0]=='r':
      T,q=gate[1],gate[2]
      C=cos(T)
      S=sin(T)
      for p2 in p2s:
        z=E[j('Z',p2,q)]
        y=E[j('Y',p2,q)]
        E[j('Z',p2,q)]=C*z-S*y
        E[j('Y',p2,q)]=C*y+S*z
    if gate[0]=='h':
      h(gate[1])
    if gate[0]=='cx':
      q=gate[1]
      h(q)
      for pair in[('XI','XZ'),('IX','ZX'),('YI','YZ'),('IY','ZY'),('XX','YY')]:
        t=E[pair[0]]
        E[pair[0]]=E[pair[1]]
        E[pair[1]]=t
      h(q)
  if g in [0,1]:
    ps={}
    def s(out):
      return(1-2*(out=='1'))
    if c.n==2:
      for out in['00','01','10','11']:
        ps[out]=(1+s(out[1])*E['IZ']+s(out[0])*E['ZI']+s(out[0])*s(out[1])*E['ZZ'])/4
    elif c.n==1:
      for out in['0','1']:
        ps[out]=(1+s(out)*E['Z'])/2
    m=[]
    c={}
    for _ in range(shots):
      cumu=0
      un=True
      r=random.random()
      for out in ps:
        cumu += ps[out]
        if r<cumu and un:
          if g==1:
            m.append(out)
          else:
            try:
              c[out]+=1
            except:
              c[out]=1
          un=False
    if g==1:
      return m
    else:
      return c
  else:
    return E