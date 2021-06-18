/*
Comments in this file are mostly there to point out differences with the Python version of MicroQiskit.
Access the lastest official release here: https://github.com/qiskit-community/MicroQiskit/tree/master/versions/C%2B%2B

For comments on what everything is supposed to do, see the Python version of MicroQiskit.
https://github.com/quantumjim/MicroQiskit/blob/master/microqiskit.py
https://github.com/qiskit-community/MicroQiskit

The present version of MicroQiskit in C++ has been the work of Omar Costa Hamdo and  Dr. James Wootton

In development on replit (https://repl.it/@quantum_jim/MicroQiskitC) and on github (https://github.com/omarcostahamido/MicroQiskitCpp).
*/
#ifndef MICROQISKITCPP_H
#define MICROQISKITCPP_H
#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <vector>
#include <string>
#include <complex>  
#include <ctime>
#include <map>
#define RESET   "\033[0m"
#define RED     "\033[31m"      /* Red */
#define ERROR(MESSAGE) error_handler(MESSAGE)

using namespace std;

void error_handler(const string message) 
{
  cout << RED << message << RESET << endl;
  abort();
} 

class QuantumCircuit {

  public:

    int nQubits, nBits;
    vector<vector<string>> data;
    
    QuantumCircuit (){

    }
    QuantumCircuit (int n, int m = 0){
      set_registers (n, m);
    }

    void set_registers (int n, int m = 0) {
      nQubits = n;
      nBits = m;
      if(!(nQubits==nBits || nBits==0))
      {
        ERROR("Only the cases nQubits=nBits and nBits=0 are allowed in MicroQiskit");
      }
    }

    void add (QuantumCircuit qc2) {

      nBits = max(nBits,qc2.nBits);
      nQubits = max(nQubits,qc2.nQubits);
      for (int g=0; g<qc2.data.size(); g++){ 
        data.push_back( qc2.data[g] );
      }
    }

    void initialize (vector<double> p){
      vector<string> init;
      //verify if the size of double vector is correct
      int t = pow(2, nQubits);
      if( !(p.size()==t||p.size()==t*2) ){
        ERROR("initialize: Can't initialize circuit. Please insert a vector {} with either "+to_string(t)+" or "+to_string(t*2)+" doubles");
      }
      data.clear();
      init.push_back("init");
      init.push_back(to_string(p.size()));
      for(int i=0;i<p.size();i++){
        init.push_back(to_string(p[i]));
      }
      data.push_back(init);
    }
    void x (int q) {
      vector<string> gate;
      verify_qubit_range(q,"x gate");
      gate.push_back("x");
      gate.push_back(to_string(q));
      data.push_back(gate);
    }
    void rx (double theta, int q) {
      vector<string> gate;
      verify_qubit_range(q,"rx gate");
      gate.push_back("rx");
      gate.push_back(to_string(theta));
      gate.push_back(to_string(q));
      data.push_back(gate);
    }
    void h (int q) {
      std::cout<<"hello from header"<<std::endl;
      vector<string> gate;
      verify_qubit_range(q,"h gate");
      gate.push_back("h");
      gate.push_back(to_string(q));
      data.push_back(gate);
    }
    void cx (int s, int t) { 
      vector<string> gate;
      verify_qubit_range(s,"cx gate");
      verify_qubit_range(t,"cx gate");
      gate.push_back("cx");
      gate.push_back(to_string(s));
      gate.push_back(to_string(t));
      data.push_back(gate);
    }
    //new ch gate
    void ch (int s, int t) { 
      vector<string> gate;
      verify_qubit_range(s,"ch gate");
      verify_qubit_range(t,"ch gate");
      gate.push_back("ch");
      gate.push_back(to_string(s));
      gate.push_back(to_string(t));
      data.push_back(gate);
    }
    //new crx gate
    void crx (double theta, int s, int t) { 
      vector<string> gate;
      verify_qubit_range(s,"crx gate");
      verify_qubit_range(t,"crx gate");
      gate.push_back("crx");
      gate.push_back(to_string(theta));
      gate.push_back(to_string(s));
      gate.push_back(to_string(t));
      data.push_back(gate);
    }
    void measure (int q, int b) {
      vector<string> gate;
      if(!(q==b) )
      {
        ERROR("It is only possible to add measure gates of the form measure(j,j) in MicroQiskit");
      }
      verify_qubit_range(q,"measure gate");
      verify_bit_range(b,"measure gate");

      gate.push_back("m");
      gate.push_back(to_string(b));
      gate.push_back(to_string(q));
      data.push_back(gate);
    }
    void rz (double theta, int q) {
      verify_qubit_range(q,"rz gate");
      h(q);
      rx(theta,q);
      h(q);
    }
    void ry (double theta, int q) {
      verify_qubit_range(q,"ry gate");
      rx(M_PI/2,q);
      h(q);
      rx(theta,q);
      h(q);
      rx(-M_PI/2,q);
    }
    void z ( int q) {
      verify_qubit_range(q,"z gate");
      rz(M_PI,q);
    }
    void y ( int q) {
      verify_qubit_range(q,"y gate");
      z(q);
      x(q);
    }

    bool has_measurements(){
      //this is not totally bulletproof. i.e. it doesn't care where in time you actually place the gates :/
      vector<int> mGates;
      map<int,int> mUnique;
      map<int,int>::iterator it;
      //check all gates in circuit
      for (int g=0; g<data.size(); g++){
        //collect all measure gates in mGates
        if (data[g][0]=="m"){
          //just need the qubit they are assigned to
          mGates.push_back( stoi(data[g][1]) );
        }
      }
      //a full set of measurement gates must have a measure gate on each qubit in the circuit
      //create a list of all unique measure-gated qubits
      for(int num : mGates){
        mUnique[mGates[num]]=1;
      }
      //check if we have a measure gate for each qubit
      for(int i=0; i<nQubits; i++){
        it = mUnique.find(i);
        if(it == mUnique.end()){
          return false;
        }
      }

      return true;
    }

  private:

    void verify_qubit_range(int q, string gate){
      if(!(q>=0) || !(q<nQubits) )
      {
        ERROR(gate+": Index for qubit out of range");
      }
    }

    void verify_bit_range(int b, string gate){
      if(!(b>=0) || !(b<nBits))
      {
        ERROR(gate+": Index for bit out of range");
      }
    }

};

class Simulator {
  // Contains methods required to simulate a circuit and provide the desired outputs.

  vector<vector<double>> simulate (QuantumCircuit qc) {

    vector<vector<double>> ket;

    // initializing the internal ket
    for (int j=0; j<pow(2,qc.nQubits); j++){
      vector<double> e;
      for (int k=0; k<2; k++){
        e.push_back(0.0);
      }
      ket.push_back(e); //add vector{0.0, 0.0}
    }//e.g. for 2 qubits < <0.0, 0.0> <0.0, 0.0> <0.0, 0.0> <0.0, 0.0> >
    ket[0][0] = 1.0; //change the first number on the first vector in ket. this means that by default it will be measuring 0, because that's the first bitstr.
    //e.g. < <1.0, 0.0> <0.0, 0.0> <0.0, 0.0> <0.0, 0.0> >

    //for each gate in qc.data vector (a vetor which is of the type vector<vector<string>>) there is an added vector<string>. Thus, qc.data.size() = the number of gates in qc.
    for (int g=0; g<qc.data.size(); g++){

      if ( (qc.data[g][0]=="init") ){
        // initialize
        int initsize = stoi(qc.data[g][1]);
        for(int i=0; i<initsize; i++){
          if(initsize==pow(2,qc.nQubits)){
            //if just a simple list
            ket[i][0] = stod(qc.data[g][2+i]);
            ket[i][1] = 0.0;
          } else {
            //else it must be a complete list
            ket[i/2][i%2] = stod(qc.data[g][2+i]);
          }
        }
      } else if ( (qc.data[g][0]=="x") or (qc.data[g][0]=="rx") or (qc.data[g][0]=="h") ) {

        int q;
        q = stoi( qc.data[g][qc.data[g].size()-1] );
        //retrieve the last qubit number from the gate vector (target) as an int, e.g. <"h","0"> = 0

        for (int i0=0; i0<pow(2,q); i0++){
          for (int i1=0; i1<pow(2,qc.nQubits-q-1); i1++){
            int b0,b1;
            b0 = i0 + int(pow(2,q+1)) * i1;
            b1 = b0 + int(pow(2,q));

            vector<double> e0, e1;
            e0 = ket[b0];
            e1 = ket[b1];

            if (qc.data[g][0]=="x"){
              ket[b0] = e1;
              ket[b1] = e0;
            } else if (qc.data[g][0]=="rx"){
              double theta = stof( qc.data[g][1] );
              ket[b0][0] = e0[0]*cos(theta/2)+e1[1]*sin(theta/2);
              ket[b0][1] = e0[1]*cos(theta/2)-e1[0]*sin(theta/2);
              ket[b1][0] = e1[0]*cos(theta/2)+e0[1]*sin(theta/2);
              ket[b1][1] = e1[1]*cos(theta/2)-e0[0]*sin(theta/2);
            } else if (qc.data[g][0]=="h"){
              for (int k=0; k<2; k++){
                ket[b0][k] = (e0[k] + e1[k])/sqrt(2);
                ket[b1][k] = (e0[k] - e1[k])/sqrt(2);
              }
            }

          }
        }

      } else if ( (qc.data[g][0]=="cx") or (qc.data[g][0]=="ch") or (qc.data[g][0]=="crx") ) {
        int s,t,l,h;
        s = stoi( qc.data[g][qc.data[g].size()-2] );
        t = stoi( qc.data[g][qc.data[g].size()-1] );
        if (s>t){
          h = s;
          l = t;
        } else {
          h = t;
          l = s;
        }

        for (int i0=0; i0<pow(2,l); i0++){
          for (int i1=0; i1<pow(2,h-l-1); i1++){
            for (int i2=0; i2<pow(2,qc.nQubits-h-1); i2++){
              int b0,b1;
              b0 = i0 + pow(2,l+1)*i1 + pow(2,h+1)*i2 + pow(2,s);
              b1 = b0 + pow(2,t);

              vector<double> e0, e1;
              e0 = ket[b0];
              e1 = ket[b1];

              if (qc.data[g][0]=="cx"){
                ket[b0] = e1;
                ket[b1] = e0;
              } else if (qc.data[g][0]=="ch"){
                for (int k=0; k<2; k++){
                  ket[b0][k] = (e0[k] + e1[k])/sqrt(2);
                  ket[b1][k] = (e0[k] - e1[k])/sqrt(2);
                }
              } else if (qc.data[g][0]=="crx"){
                double theta = stof( qc.data[g][1] );
                ket[b0][0] = e0[0]*cos(theta/2)+e1[1]*sin(theta/2);
                ket[b0][1] = e0[1]*cos(theta/2)-e1[0]*sin(theta/2);
                ket[b1][0] = e1[0]*cos(theta/2)+e0[1]*sin(theta/2);
                ket[b1][1] = e1[1]*cos(theta/2)-e0[0]*sin(theta/2);
              }
              
            }
          }
        }
      }

    }

    return ket;
  }

  vector<double> get_probs (QuantumCircuit qc) {

    if(!qc.has_measurements()){
      ERROR("get_probs: The circuit should have a full set of measure gates");
    }

    vector<vector<double>> ket;
    ket = simulate(qc);

    vector<double> probs;
    for (int j=0; j<ket.size(); j++){

      probs.push_back( pow(ket[j][0],2) + pow(ket[j][1],2) );

    }

    return probs;
  }

  public:

    QuantumCircuit qc;
    int shots;

    Simulator (QuantumCircuit qc_in, int shots_in = 1024) {
      srand((unsigned)time(0));//seed for rand() calculated from the epoch date
      qc = qc_in;
      shots = shots_in;
    }

    vector<complex<double>> get_statevector () {
    
      vector<vector<double>> ket;
      ket = simulate(qc);
      vector<complex<double>> complex_ket;

      for (int j=0; j<ket.size(); j++){
        complex<double> e (ket[j][0],ket[j][1]);
        complex_ket.push_back( e );
      }

      return complex_ket;
    }

    vector<string> get_memory () {

      vector<double> probs;
      probs = get_probs(qc);

      vector<string> memory;

      for (int s=0; s<shots; s++){

        double cumu = 0;
        bool un = true;
        double r = double(rand())/RAND_MAX;
        vector<char> bitstr (qc.nQubits,'0');

        for (int j=0; j<probs.size();j++){
          cumu += probs[j];//this will add up to 1  
          if ((r<=cumu) && un){
            for( int w=0; w<bitstr.size(); w++ ){
              bool result = int(pow(2,w))&j;
              bitstr[qc.nQubits-1-w]= result?'1':'0';
            }
            string out(bitstr.begin(), bitstr.end());
            memory.push_back( out );
            un = false;
          }
        }
      }

      return memory;//e.g. <"10","10","10","10","10","10","10","10","10","10">
    }

    map<string, int> get_counts () {

      map<string, int> counts;
      vector<string> memory = get_memory();
      if(memory.size()>0){
        for (int s=0; s<shots; s++){
          counts[memory[s]] += 1;//aggregate by key/bitstr
        }
      }
      
      return counts;
    }

    string get_qiskit () {
      string qiskitPy;

      if (qc.nBits==0){
        qiskitPy += "qc = QuantumCircuit("+to_string(qc.nQubits)+")\n";
      } else {
        qiskitPy += "qc = QuantumCircuit("+to_string(qc.nQubits)+","+to_string(qc.nBits)+")\n";
      }

      for (int g=0; g<qc.data.size(); g++){
          if (qc.data[g][0]=="x"){
            qiskitPy += "qc.x("+qc.data[g][1]+")\n";
          } else if (qc.data[g][0]=="rx") {
            qiskitPy += "qc.rx("+qc.data[g][1]+","+qc.data[g][2]+")\n";
          } else if (qc.data[g][0]=="h") {
            qiskitPy += "qc.h("+qc.data[g][1]+")\n";
          } else if (qc.data[g][0]=="cx") {
            qiskitPy += "qc.cx("+qc.data[g][1]+","+qc.data[g][2]+")\n";
          } else if (qc.data[g][0]=="ch") {
            qiskitPy += "qc.ch("+qc.data[g][1]+","+qc.data[g][2]+")\n";
          } else if (qc.data[g][0]=="crx") {
            qiskitPy += "qc.crx("+qc.data[g][1]+","+qc.data[g][2]+","+qc.data[g][3]+")\n";
          } else if (qc.data[g][0]=="m") {
            qiskitPy += "qc.measure("+qc.data[g][1]+","+qc.data[g][2]+")\n";
          } else if (qc.data[g][0]=="init") {
            qiskitPy += "qc.initialize({"+qc.data[g][2];

            int initsize = stoi(qc.data[g][1]);
            for(int i=0; i<initsize-1; i++){
              qiskitPy += ","+qc.data[g][3+i];
            }
            qiskitPy += "})\n";
          }
      }

      return qiskitPy;
    }

    string get_qasm () {
      string qasm;
      // initial qasm header
      qasm += "OPENQASM 2.0;\ninclude \"qelib1.inc\";\n";
      // qreg
      qasm += "qreg q["+to_string(qc.nQubits)+"];\n";
      // creg
      if (qc.nBits!=0){ // maybe don't do this and always print it
        qasm += "creg c["+to_string(qc.nBits)+"];\n"; 
      }
      // gates
      for (int g=0; g<qc.data.size(); g++){
          if (qc.data[g][0]=="x"){
            qasm += "x q["+qc.data[g][1]+"];\n";
          } else if (qc.data[g][0]=="rx") {
            qasm += "rx("+qc.data[g][1]+") q["+qc.data[g][2]+"];\n";
          } else if (qc.data[g][0]=="h") {
            qasm += "h q["+qc.data[g][1]+"];\n";
          } else if (qc.data[g][0]=="cx") {
            qasm += "cx q["+qc.data[g][1]+"],q["+qc.data[g][2]+"];\n";
          } else if (qc.data[g][0]=="ch") {
            qasm += "ch q["+qc.data[g][1]+"],q["+qc.data[g][2]+"];\n";
          } else if (qc.data[g][0]=="crx") {
            qasm += "crx("+qc.data[g][1]+") q["+qc.data[g][2]+"],q["+qc.data[g][3]+"];\n";
          } else if (qc.data[g][0]=="m") {
            qasm += "measure q["+qc.data[g][1]+"] -> c["+qc.data[g][2]+"];\n";
          }
      }

      return qasm;
    }

};
#endif
