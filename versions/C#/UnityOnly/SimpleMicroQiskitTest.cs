using Qiskit;
using Qiskit.Float;

public class SimpleMicroQiskitTest : CalculationBase {

    public ComplexNumber[] Amplitudes;


    public QuantumCircuit Circuit;



    SimulatorBase simulator = new MicroQiskitSimulator();

    public string QiskitString = "";

    public SimulatorType UsedSimulator;

    public QuantumCircuitFloat FloatCircuit;


    public float[] FloatProbabilities;

    public double[] ProbabilitieDifference;

    public void InitTest() {
        Circuit = new QuantumCircuit(Circuit.NumberOfQubits, Circuit.NumberOfOutputs);
    }



    public void StartTest() {
        if (Circuit.Amplitudes!=null && Circuit.Amplitudes.Length>0) {
            Circuit.AmplitudeLength = Circuit.Amplitudes.Length;
        }
        Amplitudes = simulator.Simulate(Circuit);
        Probabilities = simulator.GetProbabilities(Amplitudes);
        QiskitString = Circuit.GetQiskitString();

        FloatCircuit = new QuantumCircuitFloat(Circuit);


        MicroQiskitSimulatorFloat floatSimulator = new MicroQiskitSimulatorFloat();

        FloatProbabilities = floatSimulator.GetProbabilities(FloatCircuit);



        ProbabilitieDifference = new double[Probabilities.Length];

        for (int i = 0; i < Probabilities.Length; i++) {
            ProbabilitieDifference[i] = Probabilities[i] - FloatProbabilities[i];
        }
    }

    public void Normalize() {
        Circuit.Normalize();
    }

    public override void Calculate() {

        Amplitudes = simulator.Simulate(Circuit);
        Probabilities = simulator.GetProbabilities(Amplitudes);
        QubitCount = Circuit.NumberOfQubits;
        base.Calculate();
    }


    public void SetSimulator() {
        switch (UsedSimulator) {
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

    public enum SimulatorType {
        Micro,
        PythonMicro
    }
}

