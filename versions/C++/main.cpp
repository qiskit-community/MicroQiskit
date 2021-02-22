#include <iostream>
#include <vector>
#include <string>
#include "MicroQiskitCpp.h"

using namespace std;

int main () {

  // cout << "\n===================================================================================" << endl;
  // cout << "This is MicroQiskitCpp: an extremely minimal version of Qiskit, implemented in C++." << endl;
  // cout << "\nFor the standard version of Qiskit, see qiskit.org. To run your quantum programs\non real quantum hardware, see quantum-computing.ibm.com." << endl;
  // cout << "===================================================================================\n" << endl;


  cout << "\n**We start with a Bell pair: the standard 'Hello World' of quantum computing.**" << endl;

  // initialize a circuit with two qubits 
  QuantumCircuit qc;
  qc.set_registers(2);  
  // add the gates to create a Bell pair
  qc.h(0);
  qc.cx(0,1);

  // initialize another circuit with two qubits and two output bits
  QuantumCircuit meas;
  meas.set_registers(2,2);
  // add the measurements
  meas.measure(0,0);
  meas.measure(1,1);

  // add the measurement circuit to the end of the original circuit
  qc.add(meas);

  // simulate the circuit and get a result
  Simulator result (qc);

  // we can use the result to see what the Qiskit syntax would be
  cout << "\nThis circuit could be expressed in Qiskit as:" << endl;
  cout << result.get_qiskit() << endl;
  
  // we can use the result to see also what the QASM syntax would be
  cout << "\nThis circuit could be expressed in Qasm as:" << endl;
  cout << result.get_qasm() << endl;

  // and also to get the counts
  map<string, int> counts = result.get_counts();

  // let's print this to screen
  cout << "The counts are:" << endl;
  for(map<string, int>::iterator iter = counts.begin(); iter != counts.end(); ++iter){

    string bitstring = iter->first;
    int count = iter->second;
  
    cout << "Counts for "+bitstring+" = " << count << "\n";

  }

  cout << "\n**Now let's try single qubit rotations and a statevector output.**" << endl;

  // initialize a circuit with two qubits
  QuantumCircuit qc2;
  qc2.set_registers(2);  
  // add some single qubit gates
  qc2.rx(M_PI/4,0);
  qc2.ry(M_PI/2,1);
  qc2.rz(M_PI/8,0);

  // no measurements needed for a statevector output

  // simulate the circuit and get a result
  Simulator result2 (qc2);

   // we can use the result to see what the Qiskit syntax would be
  cout << "\nThis circuit could be expressed in Qiskit as:" << endl;
  cout << result2.get_qiskit() << endl;

  cout << "Note: It could also be expressed more efficiently in Qiskit, but MicroQiskit compiles everything down to x, rx, h and cx." << endl;

  // and also get the statevector
  vector<complex<double>> ket = result2.get_statevector();

  // let's print this to screen
  cout << "\nThe statevector is:" << endl;
  for (int j=0; j<ket.size(); j++){
    cout << "(" << real(ket[j]) << ") + (" << imag(ket[j]) << ")" <<  "*i" << endl;
  }

  cout << "\n**Finally, a three qubit GHZ with a memory output.**" << endl;

  // the circuit
  QuantumCircuit qc3;
  qc3.set_registers(3,3);  
  qc3.h(1);
  qc3.cx(1,0);
  qc3.cx(1,2);
  qc3.measure(0,0);
  qc3.measure(1,1);
  qc3.measure(2,2);

  // simulating and getting the result for 10 shots
  Simulator result3 (qc3,10);
  vector<string> memory = result3.get_memory();

  cout << "\nThis circuit could be expressed in Qiskit as:" << endl;
  cout << result3.get_qiskit() << endl;

  // print to screen
  cout << "The results are:" << endl;
  for (int j=0; j<memory.size(); j++){
    cout << "Result for sample " << j+1 << " = " << memory[j] << endl;
  }

  return 0;
}
