
namespace Qiskit
{
    public class SimulatorBase
    {
        public virtual ComplexNumber[] Simulate(QuantumCircuit circuit)
        {

            double sum = circuit.ProbabilitySum();

            if (sum> MathHelper.Eps)
            {
                if (sum<1- MathHelper.Eps || sum > 1+ MathHelper.Eps)
                {
                    circuit.Normalize(sum);
                }

                ComplexNumber[] amplitudes = new ComplexNumber[circuit.Amplitudes.Length];

                for (int i = 0; i < amplitudes.Length; i++)
                {
                    amplitudes[i] = circuit.Amplitudes[i];
                }
                return amplitudes;
            }
            else
            {
                //Initialize the all 0 vector
                ComplexNumber[] amplitudes = new ComplexNumber[MathHelper.IntegerPower(2, circuit.NumberOfQubits)];
                amplitudes[0].Real = 1;
                return amplitudes;
            }

        }


        public virtual double[] GetProbabilities(QuantumCircuit circuit)
        {
            //Doing nothing just preparing an array
            double[] probabilities = new double[MathHelper.IntegerPower(2, circuit.NumberOfQubits)];
            return probabilities;
        }


        public virtual double[] GetProbabilities(ComplexNumber[] amplitudes)
        {
            //Calculating the probability from the amplitudes
            double[] probabilities = new double[amplitudes.Length];
            for (int i = 0; i < probabilities.Length; i++)
            {
                probabilities[i] = amplitudes[i].Real * amplitudes[i].Real + amplitudes[i].Complex * amplitudes[i].Complex;
            }

            return probabilities;
        }
    }
}