// This is the Processing version of Qiskit. For the full version, see qiskit.org.
// It has many more features, and access to real quantum computers.
import java.util.List;
import java.util.Arrays;
import java.util.Map;

class QuantumCircuit {
  int numQubits;
  int numClbits;
  List<List> data = new ArrayList();

  QuantumCircuit(int n, int m) {
    this.numQubits = n;
    this.numClbits = m;
  }

  QuantumCircuit(int n) {
    this(n, 0);
  }


  // Applies an x gate to the given qubit.
  QuantumCircuit x(int q) {
    this.data.add(Arrays.asList("x", new Integer(q)));
    return this;
  }


  // Applies an rx gate to the given qubit by the given angle.
  QuantumCircuit rx(double theta, int q) {
    this.data.add(Arrays.asList("rx", new Double(theta), new Integer(q)));
    return this;
  }

  // Applies an h gate to the given qubit.
  QuantumCircuit h(int q) {
    this.data.add(Arrays.asList("h", new Integer(q)));
    return this;
  }


  // Applies a cx gate to the given source and target qubits.
  QuantumCircuit cx(int s, int t) {
    this.data.add(Arrays.asList("cx", new Integer(s), new Integer(t)));
    return this;
  }


  // Applies an rz gate to the given qubit by the given angle.
  QuantumCircuit rz(double theta, int q) {
    // This gate is constructed from `h` and `rx`.
    this.h(q);
    this.rx(theta, q);
    this.h(q);
    return this;
  }


  // Applies an ry gate to the given qubit by the given angle.
  QuantumCircuit ry(double theta, int q) {
    // This gate is constructed from `rx` and `rz`.
    this.rx(Math.PI / 2, q);
    this.rz(theta, q);
    this.rx(-Math.PI / 2, q);
    return this;
  }


  // Applies a z gate to the given qubit.
  QuantumCircuit z(int q) {
    // This gate is constructed from `rz`.
    this.rz(Math.PI, q);
    return this;
  }


  // Applies a y gate to the given qubit.
  QuantumCircuit y(int q) {
    // This gate is constructed from `rz` and `x`.
    this.rz(Math.PI, q);
    this.x(q);
    return this;
  }


  /// Applies a measure gate to the given qubit and bit.
  QuantumCircuit measure(int q, int b) {
    if (q >= this.numQubits) {
      throw new IndexOutOfBoundsException("Index for qubit out of range.");
    }
    if (b >= this.numClbits) {
      throw new IndexOutOfBoundsException("Index for output bit out of range.");
    }
    this.data.add(Arrays.asList("m", new Integer(q), new Integer(b)));
    return this;
  }
}


class Simulator {
  double r2 = 0.70710678118;
  double noise = 0.0;

  Simulator() {
    this(0.0);
  }
  
  Simulator(double noise) {
    this.noise = noise;
  }

  List<List<Double>> superpose(List<Double> x, List<Double> y) {
    List<List<Double>> sup = new ArrayList(Arrays.asList(
      new ArrayList(Arrays.asList(
        (((Double)x.get(0).doubleValue() + ((Double)y.get(0).doubleValue())) * r2),
        (((Double)x.get(1).doubleValue() + ((Double)y.get(1).doubleValue())) * r2)
      )),
      new ArrayList(Arrays.asList(
        (((Double)x.get(0).doubleValue() - ((Double)y.get(0).doubleValue())) * r2),
        (((Double)x.get(1).doubleValue() - ((Double)y.get(1).doubleValue())) * r2)
      ))
    ));
    return sup;
  };

  List<List<Double>> turn(List<Double> x, List<Double> y, double theta) {
    List<List<Double>> trn = new ArrayList(Arrays.asList(
      new ArrayList(Arrays.asList(
        ((Double)x.get(0).doubleValue() * Math.cos(theta / 2) +
        ((Double)y.get(1).doubleValue()) * Math.sin(theta / 2)),
        ((Double)x.get(1).doubleValue() * Math.cos(theta / 2) -
        ((Double)y.get(0).doubleValue()) * Math.sin(theta / 2))
      )),
      new ArrayList(Arrays.asList(
        ((Double)y.get(0).doubleValue() * Math.cos(theta / 2) +
        ((Double)x.get(1).doubleValue()) * Math.sin(theta / 2)),
        ((Double)y.get(1).doubleValue()  * Math.cos(theta / 2) -
        ((Double)x.get(0).doubleValue()) * Math.sin(theta / 2))
      ))
    ));
    return trn;
  };


  Object simulate(QuantumCircuit qc, int shots, String get) {
    List<List> k = new ArrayList();
    for (int j = 0; j < Math.pow(2, qc.numQubits); j++) {
      k.add(Arrays.asList(0.0d, 0.0d));
    }
    k.set(0, Arrays.asList(1.0d, 0.0d));

    Map<Integer,Integer> outputMap = new HashMap();
    for (int idx = 0; idx < qc.data.size(); idx++) {
      List gate = qc.data.get(idx);
      if (gate.get(0).equals("m")) {
        outputMap.put((Integer)gate.get(2), (Integer)gate.get(1));
      }
      else if (gate.get(0).equals("x") || gate.get(0).equals("h") || gate.get(0).equals("rx")) {
        int j = ((Integer)gate.get(gate.size() - 1)).intValue();

        for (int i0 = 0; i0 < Math.pow(2, j); i0++) {
          for (int i1 = 0; i1 < Math.pow(2, qc.numQubits - j - 1); i1++) {
            int b0 = (int)(i0 + Math.pow(2, (j + 1)) * i1);
            int b1 = (int)(b0 + Math.pow(2, j));
            if (gate.get(0).equals("x")) {
              //println("b0: " + b0);
              //println("b1: " + b1);
              List temp0 = k.get(b0);
              List temp1 = k.get(b1);
              k.set(b0, temp1);
              k.set(b1, temp0);
            }
            else if (gate.get(0).equals("h")) {
              List<List<Double>> sup = this.superpose(k.get(b0), k.get(b1));
              k.set(b0, sup.get(0));
              k.set(b1, sup.get(1));
            }
            else {
              double theta = ((Double)gate.get(1)).doubleValue();
              List<List<Double>> trn = this.turn(k.get(b0), k.get(b1), theta);
              k.set(b0, trn.get(0));
              k.set(b1, trn.get(1));
            }
          }
        }
      }

      else if (gate.get(0).equals("cx")) {
        int s = ((Integer)gate.get(1)).intValue();
        int t = ((Integer)gate.get(2)).intValue();
        int l = Math.min(s, t);
        int h = Math.max(s, t);
        for (int i0 = 0; i0 < Math.pow(2, l); i0++) {
          for (int i1 = 0; i1 < Math.pow(2, (h - l - 1)); i1++) {
            for (int i2 = 0; i2 < Math.pow(2, (qc.numQubits - h - 1)); i2++) {
              int b0 = (int)(i0 + Math.pow(2, l + 1) * i1 + Math.pow(2, h + 1) * i2 + Math.pow(2, s));
              int b1 = (int)(b0 + Math.pow(2, t));
              List<Double> tmp0 = k.get(b0);
              List<Double> tmp1 = k.get(b1);
              k.set(b0, tmp1);
              k.set(b1, tmp0);
            }
          }
        }
      }
    }
    if (get.equals("statevector")) {
      return k;
    }
    else {
      List<Boolean> m = new ArrayList();
      for (int idx = 0; idx < qc.numQubits; idx++) {
        m.add(false);
      }
      for (int i = 0; i < qc.data.size(); i++) {
        List gate = qc.data.get(i);
        for (int j = 0; j < qc.numQubits; j++) {
          //int j = ((Integer)gate.get(gate.size() - 1)).intValue();
          if (((((Integer)gate.get(gate.size() - 1)).intValue() == j) && m.get(j))) {
            println("Incorrect or missing measure command.");
          }
          m.set(j, gate.get(0).equals("m") && 
            ((Integer)gate.get(1)).intValue() == j && 
            ((Integer)gate.get(2)).intValue() == j);
        }
      }

      List<Double> probs = new ArrayList();
      for (int i = 0; i < k.size(); i++) {
        probs.add((Math.pow(((Double)k.get(i).get(0)).doubleValue(), 2.0d) + 
          Math.pow(((Double)k.get(i).get(1)).doubleValue(), 2.0d)));
      }

      List<Double> uniformProbs = new ArrayList();
      for (int i = 0; i < k.size(); i++) {
        uniformProbs.add(new Double(1.0 / probs.size()));
      }
      
      if (get.equals("counts")) {
        List<String> me = new ArrayList();
        for (int idx = 0; idx < shots; idx++) {
          double cumu = 0.0;
          boolean un = true;
          double r = Math.random();
          
          // Take noise into account
          double random_noise = Math.random();
          boolean noisy = random_noise < this.noise;
            
          for (int j = 0; j < probs.size(); j++) {
            double p = 0.0;
            if (!noisy) {
              p = (Double)probs.get(j);
            }
            else {
              p = (Double)uniformProbs.get(j);
            }
            
            cumu += p;
            
            if (r < cumu && un) {
              String bitStr = Integer.toString(j, 2);
              String padStr = "" + (int)Math.pow(10, qc.numQubits - bitStr.length());
              padStr = padStr.substring(1);
              String rawOut = padStr + bitStr;
              List<String> outList = new ArrayList();
              for (int i = 0; i < qc.numClbits; i++) {
                outList.add("0");
              }
              for (Object bit : outputMap.keySet()) {
                int intQBitIdx = ((Integer)bit).intValue();
                int intCBitIdx = ((Integer)outputMap.get(bit)).intValue();
                
                outList.set(qc.numClbits - 1 - intCBitIdx,
                  Character.toString(rawOut.charAt(qc.numQubits - 1 - intQBitIdx)));
              }
              un = false;
              
              me.add(String.join("", outList));
            }
          }
        }
        Map<String,Integer> counts = new HashMap();
        for (int meIdx = 0; meIdx < me.size(); meIdx++) {
          String meas = me.get(meIdx);
          
          if (counts.containsKey(meas)) {
            counts.put(meas, ((Integer)counts.get(meas)).intValue() + 1);
          } else {
            counts.put(meas, 1);
          }
        }
        return counts;
      }
    }
    return null;

  }
}

/*
Simulator simulator = new Simulator(0.02);
// Example circuits:
QuantumCircuit psiMinus = new QuantumCircuit(2, 2);
psiMinus.h(0);
psiMinus.x(1);
psiMinus.cx(0, 1);
psiMinus.z(1);
psiMinus.measure(0, 0);
psiMinus.measure(1, 1);
Object psiMinusStatevector = simulator.simulate(psiMinus, 0, "statevector");
println("psiMinusStatevector: " + psiMinusStatevector);
println(simulator.simulate(psiMinus, 1000, "counts"));

QuantumCircuit ghz = new QuantumCircuit(3, 3);
ghz.h(0);
ghz.cx(0, 1);
ghz.cx(0, 2);
ghz.measure(0, 0);
ghz.measure(1, 1);
ghz.measure(2, 2);
Object ghzStatevector = simulator.simulate(ghz, 0, "statevector");
println("ghzStatevector: " + ghzStatevector);
println(simulator.simulate(ghz, 5, "counts"));

QuantumCircuit qc = new QuantumCircuit(3, 3);
qc.x(0);
qc.rx(Math.PI, 1);
qc.x(1);
qc.h(2);
qc.cx(0, 1);
qc.z(1);
qc.rz(Math.PI / 2, 1);
qc.ry(Math.PI / 4, 1);
qc.measure(0, 0);
qc.measure(1, 1);
qc.measure(2, 2);
println(qc.data);
println(simulator.simulate(qc, 5, "counts"));
*/
