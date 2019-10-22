# This is the MicroPython version of Qiskit. For the full version, see qiskit.org.
# It has many more features, and access to real quantum computers.
import random
from math import cos,sin,pi
r2=0.70710678118
class QuantumCircuit:
  def __init__(c,n,m=0):
    c.n=n
    c.m=m
    c.data=[('',0)]
  def __add__(c,c2):
    c3=QuantumCircuit(max(c.n,c2.n),max(c.m,c2.m))
    c3.data=c.data+c2.data
    return c3
  def initialize(c,k):
    c.data.clear()
    c.data.append(('init',[e for e in k]))
  def x(c,q):
    c.data.append(('x',q))
  def rx(c,T,q):
    c.data.append(('rx',T,q))
  def h(c,q):
    c.data.append(('h',q))
  def cx(c,s,t):
    c.data.append(('cx',s,t))
  def ccx(c,s0,s1,t):
    c.data.append(('ccx',s0,s1,t))
  def measure(c,q,b):
    assert b<c.m, 'Index for output bit out of range.'
    c.data.append(('m',q,b))
  def rz(c,T,q):
    c.data.append(('h',q))
    c.data.append(('rx',T,q))
    c.data.append(('h',q))
  def ry(c,T,q):
    c.data.append(('rx',pi/2,q))
    c.data.append(('h',q))
    c.data.append(('rx',T,q))
    c.data.append(('h',q))
    c.data.append(('rx',-pi/2,q))
  def z(c,q):
    c.rz(pi,q)
  def y(c,q):
    c.rz(pi,q)
    c.data.append(('x',q))
def simulate(c,shots=1024,get='counts'):
  def s(x,y):
    return [r2*(x[j]+y[j])for j in range(2)],[r2*(x[j]-y[j])for j in range(2)]
  def t(x,y,T):
    return [x[0]*cos(T/2)+y[1]*sin(T/2),x[1]*cos(T/2)-y[0]*sin(T/2)],[y[0]*cos(T/2)+x[1]*sin(T/2),y[1]*cos(T/2)-x[0]*sin(T/2)]
  g =(get=='memory')-(get=='statevector')
  k = [[0,0] for _ in range(2**c.n)]
  k[0] = [1.0,0.0]
  for gate in c.data:
    if gate[0]=='init':
      if type(gate[1][0])!=list:
        k = [[e,0] for e in gate[1]]
      else:
        k = [e for e in gate[1]]
    elif gate[0] in ['x','h','rx']:
      if gate[0]=='rx':
        j = gate[2]
      else:
        j = gate[1]
      for i0 in range(2**j):
        for i1 in range(2**(c.n-j-1)):
          b0=i0+2**(j+1)*i1
          b1=b0+2**j
          if gate[0]=='x':
            k[b0],k[b1]=k[b1],k[b0]
          elif gate[0]=='h':
            k[b0],k[b1]=s(k[b0],k[b1])
          else:
            k[b0],k[b1]=t(k[b0],k[b1],gate[1])
    elif gate[0]=='cx':
      [l,h] = sorted(gate[1:])
      for i0 in range(2**l):
        for i1 in range(2**(h-l-1)):
          for i2 in range(2**(c.n-h-1)):
            b0=i0+2**(l+1)*i1+2**(h+1)*i2+2**gate[1]
            b1=b0+2**gate[2]
            k[b0],k[b1]=k[b1],k[b0]
  if g==-1:
    return k
  else:
    for j in range(c.n):
      assert (('m',j,j)in c.data), 'Incorrect or missing measure command.'
    m = [False for _ in range(c.n)]
    for gate in c.data:
      for j in range(c.n):
        assert  not ((gate[-1]==j) and m[j]), 'Incorrect or missing measure command.'
        m[j] = (gate==('m',j,j))
    ps=[e[0]**2+e[1]**2 for e in k]
    if g==0:
      assert shots>=4**c.n, 'Use at least shots=4**n to get well-behaved counts in MicroQiskit.'
      return {('{0:0'+str(c.n)+'b}').format(j):p*shots for j,p in enumerate(ps)}
    else:
      m=[]
      for _ in range(shots):
        cumu=0
        un=True
        r=random.random()
        for j,p in enumerate(ps):
          cumu += p
          if r<cumu and un:
            out=('{0:0'+str(c.n)+'b}').format(j)
            m.append(out)
            un=False
      return m