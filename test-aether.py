from aether import *

shots = int(1e6)

def test_trig():
    assert( sin(pi/2)==1.0 )
    assert( cos(2*pi)==1.0 )
        
def test_x():
    qc = QuantumCircuit(1)
    qc.x(0)
    assert( execute(qc)['1']==1024 )
    qc = QuantumCircuit(2)
    qc.x(1)
    assert( execute(qc)['10']==1024 )
    qc.x(0)
    assert( execute(qc)['11']==1024 )  
    
def test_h():
    qc = QuantumCircuit(2)
    qc.h(0)
    for bit in ['00','01']:
        assert( round( execute(qc,shots=shots)[bit]/shots,1)==0.5 )
        
def test_rx():
    qc = QuantumCircuit(1)
    qc.rx(pi/4,0)
    assert( round( execute(qc,shots=shots)['0']/shots,2)==0.85 )
    assert( round( execute(qc,shots=shots)['1']/shots,2)==0.15 ) 
    qc = QuantumCircuit(2)
    qc.rx(pi/4,0)
    qc.rx(pi/8,1)
    assert( round( execute(qc,shots=shots)['00']/shots,2)==0.82 )
    assert( round( execute(qc,shots=shots)['01']/shots,2)==0.14 )
    assert( round( execute(qc,shots=shots)['10']/shots,2)==0.03 ) 
    assert( round( execute(qc,shots=shots)['11']/shots,2)==0.01 )
    
def test_cx():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    for bit in ['00','11']:
        assert( round( execute(qc,shots=shots)[bit]/shots,1)==0.5 )

test_trig()
test_x()
test_rx()
test_h()
test_cx()