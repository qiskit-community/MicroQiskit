import random
pi = 3.14159265359
def cos(t):
    t = t % (2*pi)
    c = 1
    term = 1
    for j in range(1,16):
        term = -term * t**2/(2*j*(2*j-1))
        c += term
    return c
def sin(t):
    t = t % (2*pi)
    s = t
    term = t
    for j in range(2,16):
        term = -term * t**2/((2*j-1)*(2*j-2))
        s += term
    return s
class QuantumCircuit:
    def __init__(self,nq):
        self._nq = nq
        self.p2s = ['I','X','Y','Z']*(self._nq==2) + ['']*(self._nq==1)
        self.expectations = {}
        self.reset()
    def _pauli(self,p1,p2,q):
        if q==1:
            return p1+p2
        else:
            return p2+p1
    def reset (self):
        for p1 in ['I','X','Y','Z']:
            for p2 in self.p2s:
                self.expectations[p1+p2] = 0
        for p1 in ['I','Z']:
            for p2 in ['I','Z']*(self._nq==2) + ['']*(self._nq==1):
                self.expectations[p1+p2] = 1
    def x(self,q):
        for p2 in self.p2s:
            for p1 in ['Y','Z']:
                self.expectations[self._pauli(p1,p2,q)] = -self.expectations[self._pauli(p1,p2,q)]   
    def z(self,q):
        for p2 in self.p2s:
            for p1 in ['X','Z']:
                self.expectations[self._pauli(p1,p2,q)] = -self.expectations[self._pauli(p1,p2,q)]
    def h(self,q):
        for p2 in self.p2s:
            temp = self.expectations[self._pauli('X',p2,q)]
            self.expectations[self._pauli('X',p2,q)] = self.expectations[self._pauli('Z',p2,q)]
            self.expectations[self._pauli('Z',p2,q)] = temp
            self.expectations[self._pauli('Y',p2,q)] = -self.expectations[self._pauli('Y',p2,q)]
    def rz(self,theta,q):
        c = cos(theta)
        s = sin(theta)
        for p2 in self.p2s:
            old_x = self.expectations[self._pauli('X',p2,q)]
            old_y = self.expectations[self._pauli('Y',p2,q)]
            self.expectations[self._pauli('X',p2,q)] = c*old_x - s*old_y
            self.expectations[self._pauli('Y',p2,q)] = c*old_y + s*old_x
    def rx(self,theta,q):
        self.h(q)
        self.rz(theta,q)
        self.h(q)
    def cz(self,c=0,t=0):
        if self._nq==2:
            for pair in [('XI','XZ'),('IX','ZX'),('YI','YZ'),('IY','ZY'),('XX','YY')]:
                temp = self.expectations[pair[0]]
                self.expectations[pair[0]] = self.expectations[pair[1]]
                self.expectations[pair[1]] = temp
    def cx(self,c,t):
        self.h(t)
        self.cx(c,t)
        self.h(t)
def execute(qc,shots=1024):
    probs = {}
    if qc._nq==2:
        probs['00'] = (1+qc.expectations['IZ']+qc.expectations['ZI']+qc.expectations['ZZ'])/4
        probs['01'] = (1-qc.expectations['IZ']+qc.expectations['ZI']-qc.expectations['ZZ'])/4
        probs['10'] = (1+qc.expectations['IZ']-qc.expectations['ZI']+qc.expectations['ZZ'])/4
        probs['11'] = (1-qc.expectations['IZ']-qc.expectations['ZI']-qc.expectations['ZZ'])/4
    elif qc._nq==1:
        probs['0'] = (1+qc.expectations['Z'])/2
        probs['1'] = (1-qc.expectations['Z'])/2
    counts = {}
    if shots==0:
        for string in probs:
            counts[string] = probs[string]
    else:
        for string in probs:
            counts[string] = 0
        for shot in range(shots):
            cumu = 0
            unchosen = True
            r = random.random()
            for string in counts:
                cumu += probs[string]
                if r<cumu and unchosen:
                    counts[string] += 1
                    unchosen = False
    return counts

from microbit import *
  
qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)
  
while True:

    counts = execute(qc,shots=1)
    if counts['00']==1:
        display.show(Image.HEART)
    elif counts['01']==1:
        display.show(Image.DUCK)
    elif counts['10']==1:
        display.show(Image.HAPPY)
    else:
        display.show(Image.PACMAN)
        
    sleep(1000)
