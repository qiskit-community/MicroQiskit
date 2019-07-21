from microbit import *

import random
pi = 3.14159265359
def cos(t):
    return 1 - t**2/2 + t**4/24 - t**6/720 + t**8/40320 + t**10/3628800 - t**12/479001600
def sin(t):
    return t - t**3/6 + t**5/120 - t**7/5040 + t**9/362880 - t**11/39916800  + t**13/6227020800
class QuantumCircuit:
    def __init__(self,nq):
        self._nq = nq
        self.p2s = ['I','X','Y','Z']*(self._nq==2) + ['']*(self._nq==1)
        self.expectations = {}
        for p1 in ['I','X','Y','Z']:
            for p2 in self.p2s:
                self.expectations[p1+p2] = 0
        for p1 in ['I','Z']:
            for p2 in ['I','Z']*(self._nq==2) + ['']*(self._nq==1):
                self.expectations[p1+p2] = 1
    def _pauli(self,p1,p2,q):
        if q==1:
            return p1+p2
        else:
            return p2+p1
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
        self.rz(q)
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
class Job:
    def __init__(self,qc,shots):
        self.qc = qc
        self.shots = shots
    def result(self):
        return Result(self.qc,self.shots)
class Result:
    def __init__(self,qc,shots):
        self.qc = qc
        self.shots = shots
    def get_counts(self):
        probs = {}
        if self.qc._nq==2:
            probs['00'] = (1+self.qc.expectations['IZ']+self.qc.expectations['ZI']+self.qc.expectations['ZZ'])/4
            probs['01'] = (1-self.qc.expectations['IZ']+self.qc.expectations['ZI']-self.qc.expectations['ZZ'])/4
            probs['10'] = (1+self.qc.expectations['IZ']-self.qc.expectations['ZI']-self.qc.expectations['ZZ'])/4
            probs['11'] = (1-self.qc.expectations['IZ']-self.qc.expectations['ZI']+self.qc.expectations['ZZ'])/4
        elif self.qc._nq==1:
            probs['0'] = (1+self.qc.expectations['Z'])/2
            probs['1'] = (1-self.qc.expectations['Z'])/2
        counts = {}
        if self.shots==0:
            for string in probs:
                counts[string] = probs[string]
        else:
            for string in probs:
                counts[string] = 0
            for shot in range(self.shots):
                cumu = 0
                unchosen = True
                for string in counts:
                    cumu += probs[string]
                    if random.random()<cumu and unchosen:
                        counts[string] += 1
                        unchosen = False
        return counts
def execute(qc,backend,shots=1024):
    return Job(qc,shots)

while True:

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    job = execute(qc,None,shots=1)
    counts = job.result().get_counts()
    if counts['00']==1:
        display.show(Image.RABBIT)
    elif counts['01']==1:
        display.show(Image.DUCK)
    elif counts['10']==1:
        display.show(Image.TORTOISE)
    else:
        display.show(Image.BUTTERFLY)
        
    sleep(1000)