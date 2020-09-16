# This is the MicroPython version of Qiskit. For the full version, see qiskit.org.
# It has many more features, and access to real quantum computers.

import random
from math import cos,sin,pi

r2=0.70710678118 # 1/sqrt(2) will come in handy

class QuantumCircuit:
  
  def __init__(self,n,m=0):
    '''Defines and initializes the attributes'''
    # The number of qubits and the number of output bits are attributes of QuantumCircuit objects.
    self.num_qubits=n
    self.num_clbits=m
    # It is possible to set a name for a circuit
    self.name = ''
    # Like Qiskit, QuantumCircuit objects in MicroQiskit have a `data` attribute, which is essentially a list of gates.
    # The contents of this in MicroQiskit are tailored to the needs of the `simulate` function.
    self.data=[]
  
  def __add__(self,self2):
    '''Allows QuantumCircuit objects to be added, as in Qiskit.'''
    self3=QuantumCircuit(max(self.num_qubits,self2.num_qubits),max(self.num_clbits,self2.num_clbits))
    self3.data=self.data+self2.data
    self3.name = self.name
    return self3
  
  def initialize(self,k):
    '''Initializes the qubits in a given state.'''
    self.data[:] = [] # Clear existing gates.
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
  
  def crx(self,theta,s,t):
    '''Applies a crx gate to the given source and target qubits.'''
    self.data.append(('crx',theta,s,t))
  
  def measure(self,q,b):
    '''Applies an measure gate to the given qubit and bit.'''
    assert b<self.num_clbits, 'Index for output bit out of range.'
    assert q<self.num_qubits, 'Index for qubit out of range.'
    self.data.append(('m',q,b))
  
  def rz(self,theta,q):
    '''Applies an rz gate to the given qubit by the given angle.'''
    # This gate is constructed from `h` and `rx`.
    self.h(q)
    self.rx(theta,q)
    self.h(q)
  
  def ry(self,theta,q):
    '''Applies an ry gate to the given qubit by the given angle.'''
    # This gate is constructed from `rx` and `rz`.
    self.rx(pi/2,q)
    self.rz(theta,q)
    self.rx(-pi/2,q)
  
  def z(self,q):
    # This gate is constructed from `rz`.
    '''Applies a z gate to the given qubit.'''
    self.rz(pi,q)
  
  def y(self,q):
    '''Applies an y gate to the given qubit.'''
    # This gate is constructed from `rz` and `x`.
    self.rz(pi,q)
    self.x(q)


def simulate(qc,shots=1024,get='counts',noise_model=[]):
  '''Simulates the given circuit `qc`, and outputs the results in the form specified by `shots` and `get`.'''
  
  def superpose(x,y):
    '''For two elements of the statevector, x and y, return (x+y)/sqrt(2) and (x-y)/sqrt(2)'''
    return [r2*(x[j]+y[j])for j in range(2)],[r2*(x[j]-y[j])for j in range(2)]
  
  def turn(x,y,theta):
    '''For two elements of the statevector, x and y, return cos(theta/2)*x - i*sin(theta/2)*y and cos(theta/2)*y - i*sin(theta/2)*x'''
    theta = float(theta)
    return [x[0]*cos(theta/2)+y[1]*sin(theta/2),x[1]*cos(theta/2)-y[0]*sin(theta/2)],[y[0]*cos(theta/2)+x[1]*sin(theta/2),y[1]*cos(theta/2)-x[0]*sin(theta/2)]
  
  # Initialize a 2^n element statevector. Complex numbers are expressed as a list of two real numbers.
  k = [[0,0] for _ in range(2**qc.num_qubits)] # First with zeros everywhere.
  k[0] = [1.0,0.0] # Then a single 1 to create the all |0> state.

  # if there is a noise model, it should be a list of qc.num_qubits measurement error probabilities
  # if it is just a singe probability, turn it into such a list
  if noise_model:
    if type(noise_model)==float:
       noise_model = [noise_model]*qc.num_qubits

  # The `outputnum_clbitsap` dictionary keeps track of which qubits are read out to which output bits
  outputnum_clbitsap = {}

  # Now we go through the gates and apply them to the statevector.
  # Each gate is specified by a tuple, as defined in the QuantumCircuit class
  for gate in qc.data:
    
    if gate[0]=='init': # For initializion, copy in the given statevector.
      if type(gate[1][0])==list:
        k = [e for e in gate[1]]
      else: # This allows for simple lists of real numbers to be accepted as input.
        k = [[e,0] for e in gate[1]]
        
    elif gate[0]=='m': # For measurement, keep a record of which bit goes with which qubit.
      outputnum_clbitsap[gate[2]] = gate[1]
    
    elif gate[0] in ['x','h','rx']: # These are the only single qubit gates recognized by the simulator.
      
      j = gate[-1] # The qubit on which these gates act is the final element of the tuple.
  
      # These gates affect elements of the statevector in pairs.
      # These pairs are the elements whose corresponding bit strings differ only on bit `j`.
      # The following loops allow us to loop over all of these pairs.
      for i0 in range(2**j):
        for i1 in range(2**(qc.num_qubits-j-1)):
          b0=i0+2**(j+1)*i1 # Index corresponding to bit string for which the `j`th digit is '0'.
          b1=b0+2**j # Index corresponding to the same bit string except that the `j`th digit is '1'.
          if gate[0]=='x': # For x, just flip the values
            k[b0],k[b1]=k[b1],k[b0]
          elif gate[0]=='h': # For x, superpose them
            k[b0],k[b1]=superpose(k[b0],k[b1])
          else: # For rx, construct the superposition required for the given angle
            theta = gate[1]
            k[b0],k[b1]=turn(k[b0],k[b1],theta)
    
    elif gate[0] in ['cx','crx']: # These are the only two qubit gates recognized by the simulator.
      
      # Get the source and target qubits
      if gate[0]=='cx': 
        [s,t] = gate[1:]
      else:
        theta = gate[1]
        [s,t] = gate[2:]


      # Also get them sorted as highest and lowest
      [l,h] = sorted([s,t])
      
      # This gate only effects elements whose corresponding bit strings have a '1' on bit 's'.
      # Of those, it effects elements in pairs whose corresponding bit strings differ only on bit `t`.
      # The following loops allow us to loop over all of these pairs.
      for i0 in range(2**l):
        for i1 in range(2**(h-l-1)):
          for i2 in range(2**(qc.num_qubits-h-1)):
            b0=i0+2**(l+1)*i1+2**(h+1)*i2+2**s # Index corresponding to bit string for which digit `s` is `1` and digit `t` is '0'.
            b1=b0+2**t  # Index corresponding to the same bit string except that digit `t` is '1'.
            if gate[0]=='cx':
                k[b0],k[b1]=k[b1],k[b0] # Flip the values.
            else:
                k[b0],k[b1]=turn(k[b0],k[b1],theta) # Perform the rotation.
  
  # Now for the outputs.
    
  # For the statevector output, simply return the statevector.
  if get=='statevector':
    return k

  else:
        
    # To calculate outputs, we convert the statevector into a list of probabilities.
    # Here `probs[j]` is the probability for the output bit string to be the n bit representation of j.
    probs = [e[0]**2+e[1]**2 for e in k]
    
    # If there is a noise model, apply its effects
    if noise_model:
      for j in range(qc.num_qubits):
        p_meas = noise_model[j]
        for i0 in range(2**j):
          for i1 in range(2**(qc.num_qubits-j-1)):
            b0=i0+2**(j+1)*i1 # Index corresponding to bit string for which the `j`th digit is '0'.
            b1=b0+2**j # Index corresponding to the same bit string except that the `j`th digit is '1'.
            # change the probs to reproduce the effect of a measurement error
            p0 = probs[b0]
            p1 = probs[b1]
            probs[b0] = (1-p_meas)*p0 + p_meas*p1
            probs[b1] = (1-p_meas)*p1 + p_meas*p0
        
    # This can be output directly (as with Statevector or DensityMatrix in Qiskit
    if get=='probabilities_dict':
      # For each p=probs[j], the key is the n bit representation of j, and the value is p.
      return {('{0:0'+str(qc.num_qubits)+'b}').format(j):p for j,p in enumerate(probs)}
    # Otherwise, we need to sample
    elif get in ['counts', 'memory']:
      # When using these kinds of outputs in MicroQiskit, we demand that no gates are applied to a qubit after its measure command.
      # The following block raises an error if this is not obeyed.
      m = [False for _ in range(qc.num_qubits)]
      for gate in qc.data:
        for j in range(qc.num_qubits):
          assert  not ((gate[-1]==j) and m[j]), 'Incorrect or missing measure command.'
          m[j] = (gate==('m',j,j))
        
      # The `shots` samples that result are then collected in the list `m`.
      m=[]
      for _ in range(shots):
        cumu=0
        un=True
        r=random.random()
        for j,p in enumerate(probs):
          cumu += p
          if r<cumu and un:    
            # When the `j`th element is chosen, get the n bit representation of j.
            raw_out=('{0:0'+str(qc.num_qubits)+'b}').format(j)
            # Convert this into an m bit string, with the order specified by the measure commands
            out_list = ['0']*qc.num_clbits
            for bit in outputnum_clbitsap:
              out_list[qc.num_clbits-1-bit] = raw_out[qc.num_qubits-1-outputnum_clbitsap[bit]]
            out = ''.join(out_list)
            # Add this to the list of samples
            m.append(out)
            un=False
            
      # For the memory output, we simply return `m`
      if get=='memory':
        return m
      # For the counts output, we turn it into a counts dictionary first
      else:
        counts = {}
        for out in m:
          if out in counts:
            counts[out] += 1
          else:
            counts[out] = 1
        return counts


  # Note: Ports should also contain the possibility to get a Qiskit output, which returns a string containing a Python
  # program to create the given circuit qc. This is not needed here, since the same syntax as standard Qiskit is used.
  # See the C++ port for an example.