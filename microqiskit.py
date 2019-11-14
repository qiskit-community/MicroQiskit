# This is the MicroPython version of Qiskit. For the full version, see qiskit.org.
# It has many more features, and access to real quantum computers.

import random
from math import cos,sin,pi

r2=0.70710678118 # 1/sqrt(2) will come in handy

class QuantumCircuit:
  
  def __init__(self,n,m=0):
    '''Defines and initializes the attributes'''
    # The number of qubits and number of output bits must be equal in any circuit with `measure` gates.
    # This is a MicroQiskit only requirement, and so an `assert` statement is used to warn Qiskit users.
    assert (n==m or m==0), 'The number of qubits and outputs must be equal in MicroQiskit.'
    # Number of qubits `n` and number of output bits `m` are attributes of QuantumCircuit objects in MicroQiskit, but not in Qiskit.
    # For this reason, the initial _ is used.
    self._n=n
    self._m=m
    # Like Qiskit, QuantumCircuit objects in MicroQiskit have a `data` attribute, which is essentially a list of gates.
    # The contents of this in MicroQiskit are tailored to the needs of the `simulate` function.
    self.data=[]
  
  def __add__(self,self2):
    '''Allows QuantumCircuit objects to be added, as in Qiskit.'''
    self3=QuantumCircuit(max(self._n,self2._n),max(self._m,self2._m))
    self3.data=self.data+self2.data
    return self3
  
  def initialize(self,k):
    '''Initializes the qubits in a given state.'''
    self.data.clear() # Clear existing gates.
    self.data.append(('init',[e for e in k])) # Add the instruction to initialize, including the required state.
  
  def x(self,q):
    '''Applies an x gate to the given qubit.'''
    self.data.append(('x',q))
  
  def rx(self,theta,q):
    '''Applies an rx gate to the given qubit by the given angle.'''
    self.data.append(('rx',theta,q))
  
  def h(self,q):
    '''Applies an h gate to the given qubit.'''
    self.data.append(('h',q))
  
  def cx(self,s,t):
    '''Applies a cx gate to the given source and target qubits.'''
    self.data.append(('cx',s,t))
  
  def measure(self,q,b):
    '''Applies an measure gate to the given qubit and bit.'''
    assert b<self._m, 'Index for output bit out of range.'
    self.data.append(('m',q,b))
  
  def rz(self,theta,q):
    '''Applies an rz gate to the given qubit by the given angle.'''
    # This gate is constructed from `h` and `rx`.
    self.data.append(('h',q))
    self.data.append(('rx',theta,q))
    self.data.append(('h',q))
  
  def ry(self,theta,q):
    '''Applies an ry gate to the given qubit by the given angle.'''
    # This gate is constructed from `h` and `rx`.
    self.data.append(('rx',pi/2,q))
    self.data.append(('h',q))
    self.data.append(('rx',theta,q))
    self.data.append(('h',q))
    self.data.append(('rx',-pi/2,q))
  
  def z(self,q):
    # This gate is constructed from `rz`.
    '''Applies a z gate to the given qubit.'''
    self.rz(pi,q)
  
  def y(self,q):
    '''Applies an y gate to the given qubit.'''
    # This gate is constructed from `rz` and `x`.
    self.rz(pi,q)
    self.data.append(('x',q))


def simulate(qc,shots=1024,get='counts'):
  '''Simulates the given circuit `qc`, and outputs the results in the form specified by `shots` and `get`.'''
  
  def superpose(x,y):
    '''For two elements of the statevector, x and y, return (x+y)/sqrt(2) and (x-y)/sqrt(2)'''
    return [r2*(x[j]+y[j])for j in range(2)],[r2*(x[j]-y[j])for j in range(2)]
  
  def turn(x,y,theta):
    '''For two elements of the statevector, x and y, return cos(theta/2)*x - i*sin(theta/2)*y and cos(theta/2)*y - i*sin(theta/2)*x'''
    return [x[0]*cos(theta/2)+y[1]*sin(theta/2),x[1]*cos(theta/2)-y[0]*sin(theta/2)],[y[0]*cos(theta/2)+x[1]*sin(theta/2),y[1]*cos(theta/2)-x[0]*sin(theta/2)]
  
  # Initialize a 2^n element statevector. Complex numbers are expressed as a list of two real numbers.
  k = [[0,0] for _ in range(2**qc._n)] # First with zeros everywhere.
  k[0] = [1.0,0.0] # Then a single 1 to create the all |0> state.

  # Now we go through the gates and apply them to the statevector.
  # Each gate is specified by a tuple, as defined in the QuantumCircuit class
  for gate in qc.data:
    
    if gate[0]=='init': # For initializion, copy in the given statevector.
      if type(gate[1][0])==list:
        k = [e for e in gate[1]]
      else: # This allows for simple lists of real numbers to be accepted as input.
        k = [[e,0] for e in gate[1]]
    
    elif gate[0] in ['x','h','rx']: # These are the only single qubit gates recognized by the simulator.
      
      j = gate[-1] # The qubit on which these gates act is the final element of the tuple.
  
      # These gates affect elements of the statevector in pairs.
      # These pairs are the elements whose corresponding bit strings differ only on bit `j`.
      # The following loops allow us to loop over all of these pairs.
      for i0 in range(2**j):
        for i1 in range(2**(qc._n-j-1)):
          b0=i0+2**(j+1)*i1 # Index corresponding to bit string for which the `j`th digit is '0'.
          b1=b0+2**j # Index corresponding to the same bit string except that the `j`th digit is '1'.
          if gate[0]=='x': # For x, just flip the values
            k[b0],k[b1]=k[b1],k[b0]
          elif gate[0]=='h': # For x, superpose them
            k[b0],k[b1]=superpose(k[b0],k[b1])
          else: # For rx, construct the superposition required for the given angle
            theta = gate[1]
            k[b0],k[b1]=turn(k[b0],k[b1],theta)
    
    elif gate[0]=='cx':
      
      # Get the source and target qubits
      [s,t] = gate[1:]

      # Also get them sorted as highest and lowest
      [l,h] = sorted([s,t])
      
      # This gate only effects elements whose corresponding bit strings have a '1' on bit 's'.
      # Of those, it effects elements in pairs whose corresponding bit strings differ only on bit `t`.
      # The following loops allow us to loop over all of these pairs.
      for i0 in range(2**l):
        for i1 in range(2**(h-l-1)):
          for i2 in range(2**(qc._n-h-1)):
            b0=i0+2**(l+1)*i1+2**(h+1)*i2+2**s # Index corresponding to bit string for which digit `s` is `1` and digit `t` is '0'.
            b1=b0+2**t  # Index corresponding to the same bit string except that digit `t` is '1'.
            k[b0],k[b1]=k[b1],k[b0] # Flip the values.
  
  # Now for the outputs.
  if get=='statevector':
    return k # Simply return the statevector.

  else: # Output for `get='counts'` and `get='memory'`.

    # This whole block is to raise errors when the user does things regarding measurements that are allowed in Qiskit but not in MicroQiskit.
    # First we demand that all measure gates are of the form `measure(j,j)`, and that there is one for each qubit.
    for j in range(qc._n):
      assert (('m',j,j) in qc.data), 'Incorrect or missing measure command.'
    # Then we demand that no gates are applied to a qubit after its measure command.
    m = [False for _ in range(qc._n)]
    for gate in qc.data:
      for j in range(qc._n):
        assert  not ((gate[-1]==j) and m[j]), 'Incorrect or missing measure command.'
        m[j] = (gate==('m',j,j))

    # To calculate outputs, we convert the statevector into a list of probabilities.
    # Here `probs[j]` is the probability for the output bit string to be the n bit representation of j.
    probs = [e[0]**2+e[1]**2 for e in k]

    if get=='counts':
      # For simplicity and speed, the counts dictionary in MicroQiskit contains the expectation values for the counts.
      # This differs from Qiskit, in which the counts values are sampled from a random process.
      # For large values of `shots`, the results will be mostly equivalent for most common use cases.
      # An error is therefore raised if the given shots value is too low.
      # Note that this is done only for the benefit of microcontrollers.
      # Ports should contruct the counts dictionary by getting and analysing a memory output.
      # See the C++ port for an example.
      assert shots>=4**qc._n, 'Use at least shots=4**n to get well-behaved counts in MicroQiskit.'
      # For each p=probs[j], the key is the n bit representation of j, and the value is `p*shots`.
      return {('{0:0'+str(qc._n)+'b}').format(j):p*shots for j,p in enumerate(probs)}

    else: # Output for `get='memory'``.
      # For the memory output, we sample from the probability distribution contained in `ps`.
      # The `shots` samples that result are then collected in the list `m`, which is then returned.
      m=[]
      for _ in range(shots):
        cumu=0
        un=True
        r=random.random()
        for j,p in enumerate(probs):
          cumu += p
          if r<cumu and un:
            # When the `j`th element is chosen, the output is the n bit representation of j.
            out=('{0:0'+str(qc._n)+'b}').format(j)
            m.append(out)
            un=False
      return m

  # Note: Ports should also contain the possibility to get a Qiskit output, which returns a string containing a Python
  # program to create the given circuit qc. This is not needed here, since the same syntax as standard Qiskit is used.
  # See the C++ port for an example.