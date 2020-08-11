import 'package:microqiskit_cmdline/quantum_circuit.dart';
import 'package:microqiskit_cmdline/simulator.dart';

void main(List<String> arguments) {
  /*
  var ghz = QuantumCircuit(3, 3);
  ghz.h(0);
  ghz.cx(0, 1);
  ghz.cx(0, 2);
  ghz.measure(0, 0);
  ghz.measure(1, 1);
  ghz.measure(2, 2);

  var ghzStatevector = simulate(ghz, 0, 'statevector');
  print('ghzStatevector: $ghzStatevector');

  var ghzCounts = simulate(ghz);
  print('ghzCounts: $ghzCounts');

  var ghzExpected = simulate(ghz, 0, 'expected_counts');
  print('ghzExpected: $ghzExpected');
  */

  var psiMinus = QuantumCircuit(2, 2);
  psiMinus.h(0);
  psiMinus.x(1);
  psiMinus.cx(0, 1);
  psiMinus.z(1);
  psiMinus.measure(0, 0);
  psiMinus.measure(1, 1);

  var psiMinusStatevector = simulate(psiMinus, 0, 'statevector');
  print('psiMinusStatevector: $psiMinusStatevector');

  var psiMinusCounts = simulate(psiMinus);
  print('psiMinusCounts: $psiMinusCounts');

  /*
  var psiMinusExpected = simulate(psiMinus, 0, 'expected_counts');
  print('psiMinusExpected: $psiMinusExpected');
   */
}
