using System;

//Needed to use the MicroQiskit simulator
using Qiskit;


public class MicroQiskitExample {

    //Simple example to generate the 2 qubit state of a bell pair
    public void GenerateBellPair() {
        QuantumCircuit circuit = new QuantumCircuit(2, 2);

        MicroQiskitSimulator simulator = new MicroQiskitSimulator();

        circuit.H(0);
        circuit.CX(0, 1);

        double[] probabilities = simulator.GetProbabilities(circuit);

        Console.WriteLine("The probability to measure 00 is: " + probabilities[0]);
        Console.WriteLine("The probability to measure 01 is: " + probabilities[1]);
        Console.WriteLine("The probability to measure 10 is: " + probabilities[2]);
        Console.WriteLine("The probability to measure 11 is: " + probabilities[3]);
    }

}
