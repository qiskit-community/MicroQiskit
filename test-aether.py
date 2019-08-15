from aether import *

shots = int(1e6)

def test_trig():
    assert( sin(pi/2)==1.0 )
    assert( cos(2*pi)==1.0 )
        
def test_x():
    qc = QuantumCircuit(1)
    qc.x(0)
    assert( execute(qc,shots=shots,get='statevector')==[[0.0,0.0],[1.0,0.0]] )
    qc = QuantumCircuit(2)
    qc.x(1)
    assert( execute(qc,shots=shots,get='statevector')==[[0.0,0.0],[0.0,0.0],[1.0,0.0],[0.0,0.0]] )
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    assert( execute(qc,shots=shots,get='statevector')==[[0.0,0.0],[0.0,0.0],[0.0,0.0],[1.0,0.0]] ) 
    
def test_h():
    qc = QuantumCircuit(2)
    qc.h(0)
    assert( execute(qc,shots=shots,get='statevector')==[[0.70710678118, 0.0], [0.70710678118, 0.0], [0.0, 0.0], [0.0, 0.0]] )
    qc = QuantumCircuit(2)
    qc.h(1)
    assert( execute(qc,shots=shots,get='statevector')==[[0.70710678118, 0.0], [0.0, 0.0], [0.70710678118, 0.0], [0.0, 0.0]] )
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    assert( execute(qc,shots=shots,get='statevector')==[[0.49999999999074046, 0.0], [0.49999999999074046, 0.0], [0.49999999999074046, 0.0], [0.49999999999074046, 0.0]] )
        
def test_rx():
    qc = QuantumCircuit(1)
    qc.rx(pi/4,0)
    assert(execute(qc,get='statevector')==[[0.9238795325112867, 0.0], [0.0, -0.3826834323650898]])
    qc = QuantumCircuit(2)
    qc.rx(pi/4,0)
    qc.rx(pi/8,1)
    assert(execute(qc,get='statevector')==[[0.9061274463528878, 0.0], [0.0, -0.37533027751786524], [0.0, -0.18023995550173696], [-0.0746578340503426, 0.0]])
    qc.h(0)
    qc.h(1)
    assert(execute(qc,get='statevector')==[[0.4157348061435736, -0.27778511650465676], [0.4903926401925336, 0.0975451610062577], [0.4903926401925336, -0.0975451610062577], [0.4157348061435736, 0.27778511650465676]])
    
def test_cx():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    assert( execute(qc,shots=shots,get='statevector')==[[0.70710678118, 0.0], [0.0, 0.0], [0.0, 0.0], [0.70710678118, 0.0]] )
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.cx(0,1)
    qc.cx(1,0)
    qc.cx(0,1)
    assert( execute(qc,shots=shots,get='statevector')==[[0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0]] )
    

def test_memory():
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.h(1)
    qc.measure(0,0)
    qc.measure(1,1)
    m = execute(qc,shots=shots,get='memory')
    assert( len(m)==shots )
    p00 = 0
    for out in m:
      p00 +=(out=='00')/shots
    assert( round(p00,2)==0.25 )
    qc = QuantumCircuit(1,1)
    qc.h(0)
    qc.measure(0,0)
    m = execute(qc,shots=shots,get='memory')
    assert( len(m)==shots )
    p0 = 0
    for out in m:
      p0 +=(out=='0')/shots
    assert( round(p0,1)==0.5 )

def test_counts():
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.h(1)
    qc.measure(0,0)
    qc.measure(1,1)
    c = execute(qc,shots=shots,get='counts')
    for out in c:
      p = c[out]/shots
      assert( round(p,2)==0.25 )
        
def test_add():
    for n in [1,2]:
        qc = QuantumCircuit(n,n)
        meas = QuantumCircuit(n,n)
        for j in range(n):
            qc.h(j)
            meas.measure(j,j)
        c = execute(qc+meas,shots=shots,get='counts')
        for out in c:
            p = c[out]/shots
            assert( round(p,2)==round(1/2**n,2) )
    
test_trig()
test_x()
test_h()
test_rx()
test_cx()
test_memory()
test_counts()
test_add()