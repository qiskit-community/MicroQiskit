from microbit import *
from aether import *
import time
  
qc = QuantumCircuit(2,2)
qc.h(0)
qc.h(1)
qc.measure(0,0)
qc.measure(1,1)
  
while True:
    
    start = time.time()
    output = execute(qc,shots=1,get='memory')[0]
    print(time.time()-start)
    if output=='00':
        display.show(Image.HEART)
    elif output=='01':
        display.show(Image.DUCK)
    elif output=='10':
        display.show(Image.HAPPY)
    else:
        display.show(Image.PACMAN)
        
    sleep(1000)
