import random
from math import cos,sin,pi
r2=0.70710678118 
class QuantumCircuit:
  def __init__(self,n,m=0):
    self._n=n
    self._m=m
    self.data=[]
  def __add__(self,self2):
    self3=QuantumCircuit(max(self._n,self2._n),max(self._m,self2._m))
    self3.data=self.data+self2.data
    return self3
  def initialize(self,k):
    self.data.clear() 
    self.data.append(('init',[e for e in k])) 
  def x(self,q):
    self.data.append(('x',q))
  def rx(self,theta,q):
    self.data.append(('rx',theta,q))
  def h(self,q):
    self.data.append(('h',q))
  def cx(self,s,t):
    self.data.append(('cx',s,t))
  def measure(self,q,b):
    assert b<self._m, 'Index for output bit out of range.'
    assert q<self._n, 'Index for qubit out of range.'
    self.data.append(('m',q,b))
  def rz(self,theta,q):
    self.data.append(('h',q))
    self.data.append(('rx',theta,q))
    self.data.append(('h',q))
  def ry(self,theta,q):
    self.data.append(('rx',pi/2,q))
    self.data.append(('h',q))
    self.data.append(('rx',theta,q))
    self.data.append(('h',q))
    self.data.append(('rx',-pi/2,q))
  def z(self,q):
    self.rz(pi,q)
  def y(self,q):
    self.rz(pi,q)
    self.data.append(('x',q))
def simulate(qc,shots=1024,get='counts'):
  def superpose(x,y):
    return [r2*(x[j]+y[j])for j in range(2)],[r2*(x[j]-y[j])for j in range(2)]
  def turn(x,y,theta):
    return [x[0]*cos(theta/2)+y[1]*sin(theta/2),x[1]*cos(theta/2)-y[0]*sin(theta/2)],[y[0]*cos(theta/2)+x[1]*sin(theta/2),y[1]*cos(theta/2)-x[0]*sin(theta/2)]
  k = [[0,0] for _ in range(2**qc._n)] 
  k[0] = [1.0,0.0] 
  output_map = {}
  for gate in qc.data:
    if gate[0]=='init': 
      if type(gate[1][0])==list:
        k = [e for e in gate[1]]
      else: 
        k = [[e,0] for e in gate[1]]
    elif gate[0]=='m':
      output_map[gate[2]] = gate[1]
    elif gate[0] in ['x','h','rx']: 
      j = gate[-1] 
      for i0 in range(2**j):
        for i1 in range(2**(qc._n-j-1)):
          b0=i0+2**(j+1)*i1 
          b1=b0+2**j 
          if gate[0]=='x': 
            k[b0],k[b1]=k[b1],k[b0]
          elif gate[0]=='h': 
            k[b0],k[b1]=superpose(k[b0],k[b1])
          else: 
            theta = gate[1]
            k[b0],k[b1]=turn(k[b0],k[b1],theta)
    elif gate[0]=='cx':
      [s,t] = gate[1:]
      [l,h] = sorted([s,t])
      for i0 in range(2**l):
        for i1 in range(2**(h-l-1)):
          for i2 in range(2**(qc._n-h-1)):
            b0=i0+2**(l+1)*i1+2**(h+1)*i2+2**s 
            b1=b0+2**t  
            k[b0],k[b1]=k[b1],k[b0] 
  if get=='statevector':
    return k
  else:
    m = [False for _ in range(qc._n)]
    for gate in qc.data:
      for j in range(qc._n):
        assert  not ((gate[-1]==j) and m[j]), 'Incorrect or missing measure command.'
        m[j] = (gate==('m',j,j))
    probs = [e[0]**2+e[1]**2 for e in k]
    if get in ['counts', 'memory']:
      m=[]
      for _ in range(shots):
        cumu=0
        un=True
        r=random.random()
        for j,p in enumerate(probs):
          cumu += p
          if r<cumu and un:    
            raw_out=('{0:0'+str(qc._n)+'b}').format(j)
            out_list = ['0']*qc._m
            for bit in output_map:
              out_list[qc._m-1-bit] = raw_out[qc._n-1-output_map[bit]]
            out = ''.join(out_list)
            m.append(out)
            un=False
      if get=='memory':
        return m
      else:
        counts = {}
        for out in m:
          if out in counts:
            counts[out] += 1
          else:
            counts[out] = 1
        return counts
    elif get=='expected_counts':
      return {('{0:0'+str(qc._n)+'b}').format(j):p*shots for j,p in enumerate(probs)}