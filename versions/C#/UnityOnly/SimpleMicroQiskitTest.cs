using Qiskit;
using UnityEngine;

public class SimpleMicroQiskitTest : CalculationBase
{

    public ComplexNumber[] amplitudes;


    public QuantumCircuit Circuit;



    SimulatorBase simulator = new MicroQiskitSimulator();

    public string QiskitString = "";

    public SimulatorType UsedSimulator;


    public void InitTest()
    {
        Circuit = new QuantumCircuit(Circuit.NumberOfQubits, Circuit.NumberOfOutputs);
    }
    



    public void StartTest()
    {
        amplitudes = simulator.Simulate(Circuit);
        Probabilities = simulator.GetProbabilities(amplitudes);
        QiskitString = Circuit.GetQiskitString();

    }

    public void Normalize()
    {
        Circuit.Normalize();
    }

    public override void Calculate()
    {

        amplitudes = simulator.Simulate(Circuit);
        Probabilities = simulator.GetProbabilities(amplitudes);
        QubitCount = Circuit.NumberOfQubits;
        base.Calculate();
    }


    public void SetSimulator()
    {
        switch (UsedSimulator)
        {
            case SimulatorType.Micro:
                simulator = new MicroQiskitSimulator();
                break;
            case SimulatorType.PythonMicro:
                simulator = new PythonMicroQiskitSimulator();
                break;
            default:
                break;
        }
    }

    public enum SimulatorType
    {
        Micro,
        PythonMicro
    }
}

public class PythonMicroQiskitSimulator : SimulatorBase
{
    //You can write your own Simulator
}
