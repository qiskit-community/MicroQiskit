using Qiskit;
using UnityEngine;

public class SimpleMicroQuiskitTest : CalculationBase
{

    public ComplexNumber[] amplitudes;


    public QuantumCircuit Circuit;



    SimulatorBase simulator = new MicroQuiskitSimulator();

    public string QuiskitString = "";

    public SimulatorType UsedSimulator;


    public void InitTest()
    {
        Circuit = new QuantumCircuit(Circuit.NumberOfQubits, Circuit.NumberOfOutputs);
    }
    



    public void StartTest()
    {
        amplitudes = simulator.Simulate(Circuit);
        Probabilities = simulator.GetProbabilities(amplitudes);
        QuiskitString = Circuit.GetQuiskitString();

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
                simulator = new MicroQuiskitSimulator();
                break;
            case SimulatorType.PythonMicro:
                simulator = new PythonMicroQuiskitSimulator();
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

public class PythonMicroQuiskitSimulator : SimulatorBase
{
    //You can write your own Simulator
}
